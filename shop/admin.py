from django.contrib import admin
from .models import (
    Category, Seller, Product, ProductPrice, ProductCharacteristicType,
    ProductCharacteristic, ProductReview, Order, OrderItem, Banner
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'parent']
    list_filter = ['active']
    search_fields = ['name']


class SellerAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class ProductCharacteristicTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'filter_type']


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1


class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ['author', 'created_at']
    can_delete = False


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'seller', 'price', 'limited_edition']
    list_filter = ['category', 'seller', 'limited_edition']
    search_fields = ['name', 'description']
    inlines = [ProductPriceInline, ProductCharacteristicInline, ProductReviewInline]
    fields = ['name', 'description', 'category', 'image', 'seller', 'sort_index', 'limited_edition']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'paid', 'created_at']
    list_filter = ['status', 'paid', 'created_at']
    search_fields = ['user__username', 'user__email']
    inlines = [OrderItemInline]
    fields = ['user', 'status', 'paid', 'delivery_address', 'created_at']
    readonly_fields = ['created_at']


class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type', 'active', 'order']
    list_filter = ['active', 'banner_type']
    search_fields = ['title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCharacteristicType, ProductCharacteristicTypeAdmin)
admin.site.register(ProductReview)
admin.site.register(Order, OrderAdmin)
admin.site.register(Banner, BannerAdmin)
