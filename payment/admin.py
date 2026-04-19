from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('catalog_key', 'product_id', 'product_name', 'unit_price', 'quantity', 'line_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'city', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'city')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('subtotal', 'shipping', 'total', 'created_at')
    inlines = [OrderItemInline]
