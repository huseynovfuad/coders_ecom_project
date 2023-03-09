from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from ..models import Product
from .serializers import ProductSerializer, ProductCreateSerializer
from rest_framework import generics
from django.db.models import Case, When, FloatField, F

# @api_view()
# def hello_world(request):
#     products = Product.objects.all()
#
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)
#
#
#
# @api_view(["GET", "POST"])
# def product_detail_view(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     serializer = ProductSerializer(product)
#
#     if request.method == "POST":
#         print(request.data)
#     return Response(serializer.data)



class ProductListView(generics.ListCreateAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    def get_queryset(self):
        # products = Product.objects.filter(company=self.request.user.company).annotate(
        #     total_price=Case(
        #         When(discount__isnull=True, then=F("price")),
        #         default=F("price") - F("discount"),
        #         output_field=FloatField()
        #     )
        # )
        products = Product.objects.filter(company=self.request.user.company)
        return products

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSerializer
        return ProductCreateSerializer

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data, status=200)

    def perform_create(self, serializer):
        return serializer.save(company=self.request.user.company)
#
#
#
# class ProductCreateView(generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductCreateSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(company=request.user.company)
#         return Response(serializer.data, status=201)



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"