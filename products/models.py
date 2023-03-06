from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from services.mixin import DateMixin, SlugMixin
from services.slugify import slugify
from services.generator import CodeGenerator
from services.uploader import Uploader
from accounts.models import Company
from ckeditor.fields import RichTextField
from services.choices import PRODUCT_STATUS
from django.db.models import Q
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Category(DateMixin, SlugMixin, MPTTModel):
    name = models.CharField(max_length=300)
    icon = models.ImageField(upload_to=Uploader.upload_logo_category, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.code = CodeGenerator.create_slug_shortcode(
            size=20, model_=Category
        )
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


    @property
    def product_count(self):
        return Product.objects.filter(
            Q(category_id=self.id)|Q(category__parent_id=self.id)|
            Q(category__parent__parent_id=self.id)
        ).count()



class Product(DateMixin, SlugMixin):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    description = RichTextField()
    status = models.CharField(max_length=200, choices=PRODUCT_STATUS)
    wishlist = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Product"
        verbose_name_plural = "Products"


    def save(self, *args, **kwargs):
        self.code = CodeGenerator.create_slug_shortcode(
            size=20, model_=Product
        )
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)



class ProductImage(DateMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Uploader.upload_image_product)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"



class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} --> {self.product.name}"




class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, blank=True)
