from django.db import models
from django.contrib.auth import get_user_model
from services.mixin import DateMixin, SlugMixin
from services.uploader import Uploader
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
from services.generator import CodeGenerator
from services.slugify import slugify

# Create your models here.

User = get_user_model()



class Company(DateMixin, SlugMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    logo = models.ImageField(upload_to=Uploader.upload_logo_company)
    address = RichTextField()
    description = RichTextField()
    mobile = PhoneNumberField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def save(self, *args, **kwargs):
        self.code = CodeGenerator.create_slug_shortcode(
            size=20, model_=Company
        )
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)