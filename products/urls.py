from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("create/", views.product_create_view, name="create"),
    path("wish/", views.product_wish_view, name="wish"),
    path("basket/", views.product_basket_view, name="basket"),
]