from rest_framework import serializers
from ..models import Product, Category, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    # total_price = serializers.ReadOnlyField(source="total_price_")
    # total_price = serializers.FloatField(read_only=True)
    total_price = serializers.SerializerMethodField()
    category = CategorySerializer()
    wishlist = UserSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


    def get_total_price(self, obj):
        return obj.price - (obj.discount or 0)



class ProductCreateSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Product
        fields = (
            "name", "category", "price", "discount", "description", "status", "company",
        )
        extra_kwargs = {
            "company": {"read_only": True}
            # "status": {"write_only": True}
        }