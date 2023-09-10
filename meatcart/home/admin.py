from django.contrib import admin
from . models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'product_image', 'product_description', 'product_price_per_kg', 'product_available_stock')

admin.site.register(Categories)
admin.site.register(Product, ProductAdmin)
admin.site.register(Wishitem)