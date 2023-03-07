from django.urls import path
from . import views

app_name = "products-api"

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="products"),
    # path("create/", views.ProductCreateView.as_view(), name="create"),
    # path("detail/<slug>/", views.product_detail_view, name="detail"),
]