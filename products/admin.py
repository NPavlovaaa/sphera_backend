from django.contrib import admin

from products.models import Product, Category, MakingMethod


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(MakingMethod)