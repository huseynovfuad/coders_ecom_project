from django.contrib import admin
from .models import Company, Profile

# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "slug", "code", "mobile")
    list_display_links = ("user", "name")
    search_fields = ("name", "code")

admin.site.register(Company, CompanyAdmin)
admin.site.register(Profile)