from rest_framework import serializers
from ..models import Product



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("wishlist", )



class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name", "category", "price", "discount", "description", "status"
        )