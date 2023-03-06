from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Basket
from django.db.models import Case, When, FloatField, F, Q, Count, Value, CharField, Sum
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import ProductForm

# Create your views here.

@login_required(login_url="/users/login/")
def index_view(request):
    filter_, filter_dict = Q(), {}
    products = Product.objects.annotate(
            discount_percent=Coalesce(F("discount"), 0, output_field=FloatField())
        ).annotate(
            total_price=Case(
                When(discount_percent=0, then=F("price")),
                default=F("price") - (F("price")*F("discount_percent")/100),
                output_field = FloatField()
            )
        ).annotate(
            discount_type=Case(
                When(discount__lt=5, then=Value('1')),
                When(Q(discount__gte=5)&Q(discount__lt=10), then=Value('2')),
                When(Q(discount__gte=10)&Q(discount__lt=15), then=Value('3')),
                When(Q(discount__gte=15)&Q(discount__lt=20), then=Value('4')),
                default=Value("5"),
                output_field=CharField()
            )
        ).order_by("-created_at")
    category = request.GET.getlist("category", None)
    if category:
        filter_dict["category"]="".join(f'category={cat}&' for cat in category)
        filter_.add(Q(category__parent__parent_id__in=category), Q.AND)
        # products = products.filter(
        #     category__parent__parent_id__in=category
        # )

    price = request.GET.get("price", None)
    if price:
        filter_dict["price"] = f"price={price}&"
        min_price, max_price = price.split(";")[0], price.split(";")[1]
        if min_price:
            filter_.add(Q(total_price__gte=float(min_price)), Q.AND)
            # products = products.filter(total_price__gte=float(min_price))
        if max_price:
            # products = products.filter(total_price__lt=float(max_price))
            filter_.add(Q(total_price__lt=float(max_price)), Q.AND)

    discount_list = request.GET.getlist("discount")
    if discount_list:
        filter_dict["discount"] = "".join(f'discount={d}&' for d in discount_list)
        # products = products.annotate(
        #     discount_type=Case(
        #         When(discount__lt=5, then=Value('1')),
        #         When(Q(discount__gte=5)&Q(discount__lt=10), then=Value('2')),
        #         When(Q(discount__gte=10)&Q(discount__lt=15), then=Value('3')),
        #         When(Q(discount__gte=15)&Q(discount__lt=20), then=Value('4')),
        #         default=Value("5"),
        #         output_field=CharField()
        #     )
        # ).filter(discount_type__in=discount_list)
        filter_.add(Q(discount_type__in=discount_list), Q.AND)


    products = products.filter(filter_)

    paginator = Paginator(products, 1)
    page = request.GET.get("page", 1)
    product_list = paginator.get_page(page)

    context = {
        "products": product_list,
        "paginator": paginator,
        "filter_dict": filter_dict.values()
    }
    return render(request, "products/index.html", context)


@login_required(login_url="/users/login/")
def product_create_view(request):
    context = {}
    return render(request, "products/create.html", context)



def product_wish_view(request):
    data = {}
    product = get_object_or_404(Product, id=int(request.POST.get("id")))

    if request.user in product.wishlist.all():
        product.wishlist.remove(request.user)
        data["success"] = False
    else:
        product.wishlist.add(request.user)
        data["success"] = True
    return JsonResponse(data)



def product_basket_view(request):
    data = {}
    product = get_object_or_404(Product, id=int(request.POST.get("id")))
    Basket.objects.get_or_create(
        product=product, user=request.user
    )
    return JsonResponse(data)


# def wishlist_view(request):
#     products = Product.objects.filter(
#         wishlist__in=[request.user]
#     )


from django.views import View
from django.views.generic import ListView



# class ProductCreateView(View):
#
#     def get(self, request, *args, **kwargs):
#         form = ProductForm()
#         context = {}
#         return render(request, "products/create.html", context)
#
#
#     def post(self, request, *args, **kwargs):
#         form = ProductForm(request.POST or None)
#         # do some process
#         return redirect("/")


class ProductListView(ListView):
    # model = Product
    queryset = Product.objects.order_by("-created_at")
    template_name = "products/list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        return {
            "queryset": queryset,
            "target": "coders"
        }
    def get_queryset(self):
        return Product.objects.all()

    # def get(self):



from .models import Order, OrderItem

def basket_list_view(request):
    baskets = Basket.objects.annotate(
        product_total_price=Case(
            When(product__discount__isnull=True, then=F("product__price")),
            default=F("product__price") - F("product__discount"),
            output_field=FloatField()
        )
    ).filter(user=request.user)
    basket_total_price = baskets.aggregate(
        total_price_sum=Coalesce(Sum("product_total_price"), 0, output_field=FloatField())
    )["total_price_sum"]

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user
        )
        for basket in baskets:
            qty_search = f"quantity-{basket.id}"
            if qty_search in request.POST:
                quantity = request.POST.get(qty_search)
                order_item = OrderItem.objects.create(
                    product=basket.product, quantity=float(quantity)
                )
                order.items.add(order_item)

        return redirect('/')
    context = {
        "baskets": baskets,
        "basket_total_price": basket_total_price
    }
    return render(request, "baskets/list.html", context)



def delete_item_from_basket(request):
    id = request.POST.get("id")
    Basket.objects.filter(id=int(id)).delete()
    return JsonResponse({"success": True})