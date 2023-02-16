from django.shortcuts import render
from .models import Category, Product
from django.db.models import Case, When, FloatField, F
from django.db.models.functions import Coalesce

# Create your views here.


def index_view(request):
    context = {
        "categories": Category.objects.filter(parent__isnull=True).order_by("-created_at"),
        "products": Product.objects.annotate(
            discount_percent=Coalesce(F("discount"), 0, output_field=FloatField())
        ).annotate(
            total_price=Case(
                When(discount_percent=0, then=F("price")),
                default=F("price") - (F("price")*F("discount_percent")/100),
                output_field = FloatField()
            )
        ).order_by("-created_at")
    }
    return render(request, "products/index.html", context)