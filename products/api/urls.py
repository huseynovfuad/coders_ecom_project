from django.urls import path
from . import views

app_name = "products-api"

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/detail/<slug>/", views.ProductDetailView.as_view(), name="detail"),
    # path("create/", views.ProductCreateView.as_view(), name="create"),
    # path("detail/<slug>/", views.product_detail_view, name="detail"),
]