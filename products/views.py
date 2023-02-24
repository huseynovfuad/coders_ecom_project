
from django.shortcuts import render
from .models import Category, Product
from django.db.models import Case, When, FloatField, F, Q, Count, Value, CharField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator

# Create your views here.


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
        print(filter_dict)
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
        "categories": Category.objects.filter(parent__isnull=True).order_by("-created_at"),
        "products": product_list,
        "paginator": paginator,
        "filter_dict": filter_dict.values()
    }
    return render(request, "products/index.html", context)