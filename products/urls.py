from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("api-products/", views.product_list_from_api_view, name="api-products"),
    path("create/", views.product_create_view, name="create"),
    path("wish/", views.product_wish_view, name="wish"),
    path("basket/", views.product_basket_view, name="basket"),

    # path("create2/", views.ProductCreateView.as_view(), name="create2"),
    path("list/", views.ProductListView.as_view(), name="list"),
    path("basket/list/", views.basket_list_view, name="basket-list"),
    path("delete/item/", views.delete_item_from_basket, name="delete-item"),
]