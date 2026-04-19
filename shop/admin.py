from django.contrib import admin

from core.product_admin import RichProductAdmin
from .models import Product


@admin.register(Product)
class ProductAdmin(RichProductAdmin):
    list_display = ('id', 'name', 'category', 'price', 'image_tag')
    list_filter = ('category',)
