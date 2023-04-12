from django.contrib import admin

from products.models import Product

# class ProductsAdmin(admin.ModelAdmin):
#     list_display = "__all__"


admin.site.register(Product)
