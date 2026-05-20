from django.contrib import admin

from .models import CartItem, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "featured")
    list_filter = ("category", "featured")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "status", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]
    search_fields = ("user__username", "email", "full_name")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "updated_at")
    search_fields = ("user__username", "product__name")
