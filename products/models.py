# products/models.py
from django.db import models
from django.urls import reverse

import uuid


class ProductCategory(models.Model):
    """Describes the product category for all category types of options in the growing product line"""
    id = models.UUIDField(
        primary_key=True,
        db_index=True,  # Indexed attribute
        default=uuid.uuid4,
        editable=False
    )

    name_singular = models.CharField(max_length=50)

    name_plural = models.CharField(max_length=50)

    description = models.TextField(blank=True, null=True)

    tags = models.TextField(blank=True, null=True)  # Used for search views

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        ordering = (
            'name_plural',
        )

    def __str__(self):
        return self.name_plural


class ProductStyle(models.Model):
    """Product Style model for growing selection of product lines"""
    id = models.UUIDField(
        primary_key=True,
        db_index=True,  # Indexed attribute
        default=uuid.uuid4,
        editable=False
    )

    category = models.ForeignKey(
        'ProductCategory',
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=25)

    tags = models.TextField(blank=True, null=True)  # Used for search views

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"
        ordering = (
            'category',
            'name',
        )

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product models to represent growing list of products offered"""
    id = models.UUIDField(
        primary_key=True,
        db_index=True,  # Indexed attribute
        default=uuid.uuid4,
        editable=False
    )

    style = models.ForeignKey(
        'ProductStyle',
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=50)

    description = models.TextField()  # Used in the public pages to explain the product to potential clients

    # Used in the public pages to explain benefits/disadvantages of the product to potential clients
    pros_description = models.TextField(blank=True, null=True)
    cons_description = models.TextField(blank=True, null=True)

    # Used in the public and private pages to display the products price/unit
    # Recommended to use display_product_price function to format price listing
    price_range = models.CharField(max_length=20, blank=True, null=True)
    price_unit = models.CharField(max_length=20, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)  # Used for private company view for product notes

    tags = models.TextField(blank=True, null=True)  # Used for search views

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = (
            'style',
            'name',
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('fence_detail_public', args=[str(self.pk)])

    def category_name(self):
        """Provides the category name in plural format"""
        return self.style.category.name_plural

    def category_name_singular(self):
        """Provides the category name in singular format"""
        return self.style.category.name_singular

    def display_formal_product_name(self):
        """Provides a formal name for the product"""
        return f"{self.style} {self.name} {self.category_name_singular()}"

    def display_product_price(self):
        """Displays a formatted product price; if no define price range, returns a message"""
        if self.price_range and self.price_unit:
            return f'${self.price_range}/{self.price_unit}'
        else:
            return 'Pricing per request'

    def get_all_product_related_tags(self):
        """Returns the value of all the tags related to this product. Product, Style, and Category tags"""
        return self.tags + self.style.tags + self.style.category.tags



class ProductImage(models.Model):
    """Allows for multiple images for the Product item"""
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)

    images = models.FileField(upload_to='products/')

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return self.product.name
