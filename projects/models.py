# projects/models.py
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid

from products.models import (
    Product,
)

# Create your models here.
class Project(models.Model):
    """Represents a construction project root model."""
    id = models.UUIDField(
        primary_key=True,
        db_index=True,  # Indexed attribute
        default=uuid.uuid4,
        editable=False
    )

    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_last_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)

    PROJECT_TYPES = [
        ('COMMERCIAL', 'Commercial'),
        ('RESIDENTIAL', 'Residential'),
        ('GOVERNMENT', 'Government'),
    ]

    type = models.CharField(
        max_length=12,
        choices=PROJECT_TYPES,
        default="RESIDENTIAL",
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name


# PROJECT GALLERY MODELS ###############################################################################################
########################################################################################################################
class ProjectExhibition(models.Model):
    """Represents a single card for the Project Gallery page to display a completed project with optional client
    testimonials"""

    id = models.UUIDField(
        primary_key=True,
        db_index=True,  # Indexed attribute
        default=uuid.uuid4,
        editable=False
    )

    date_published = models.DateTimeField(auto_now_add=True, auto_now=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    tags = models.TextField(blank=True, null=True)  # Used for search views

    class Meta:
        verbose_name = "Project Exhibition"
        verbose_name_plural = "Project Exhibitions"

    def __str__(self):
        return f"{self.project.name} Gallery Exhibition"


class ProjectExhibitionImage(models.Model):
    """Allows for multiple images for the Project Exhibition cards"""
    project = models.ForeignKey(ProjectExhibition, on_delete=models.CASCADE)

    images = models.FileField(upload_to='project_gallery/')

    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def __str__(self):
        return f"{self.project.project.name} Gallery Image"

class ProjectExhibitionProducts(models.Model):
    """Allows for multiple products for the Project Exhibition cards"""
    project = models.ForeignKey(ProjectExhibition, default=None, on_delete=models.CASCADE)

    products = models.ForeignKey(Product, on_delete=models.CASCADE,)

    class Meta:
        verbose_name = "Project Product"
        verbose_name_plural = "Project Products"

    def __str__(self):
        return f"{self.project.project.name} Products"


class ProjectExhibitionTestimonials(models.Model):
    """Allows for multiple products for the Project Exhibition cards"""
    project = models.ForeignKey(ProjectExhibition, default=None, on_delete=models.CASCADE)

    hide_testimonial = models.BooleanField(default=False)

    author = models.CharField(max_length=50)

    testimonial = models.TextField(max_length=350)

    # 5 star system
    star_rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = "Project Testimonial"
        verbose_name_plural = "Project Testimonials"

    def __str__(self):
        return f"{self.author} in {self.project.project.name}"

    def star_rating_range(self):
        return "i"*self.star_rating