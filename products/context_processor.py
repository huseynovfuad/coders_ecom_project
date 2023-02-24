from .models import Category


def products_extra_context(request):
    return {
        "categories": Category.objects.filter(parent__isnull=True).order_by("-created_at"),
    }