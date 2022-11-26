# products/admin.py
from django.contrib import admin
from .models import (
    ProductCategory,
    ProductStyle,
    Product,
    ProductImage,
)


admin.site.register(ProductCategory)


class ProductImageInline(admin.TabularInline):
    """Admin registration for product image list to show under the product admin views"""
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    """Admin registration for specific products"""
    inlines = [
        ProductImageInline,  # Shows product image list from the product admin view
    ]
    list_display = [
        '__str__',
        'style',
        'category_name',
    ]


admin.site.register(Product, ProductAdmin)


class ProductStyleAdmin(admin.ModelAdmin):
    """Admin registration for Product Styles"""

    list_display = [
        '__str__',
        'category'
    ]


admin.site.register(ProductStyle, ProductStyleAdmin)
