# projects/admin.py
from django.contrib import admin
from .models import (
    Project,
    ProjectExhibition,
    ProjectExhibitionImage,
    ProjectExhibitionProducts,
    ProjectExhibitionTestimonials,
)


# PROJECT GALLERY ######################################################################################################
########################################################################################################################

class ProjectImageInline(admin.TabularInline):
    """InLine registration for all project images"""
    model = ProjectExhibitionImage


class ProjectProductsInline(admin.TabularInline):
    """InLine registration for the products related to the project"""
    model = ProjectExhibitionProducts


class ProjectTestimonialsInline(admin.TabularInline):
    """InLine registration for the testimonials related to the project"""
    model = ProjectExhibitionTestimonials


class ProjectExhibitionAdmin(admin.ModelAdmin):
    """Admin registration for specific project exhibition cards"""
    model = ProjectExhibition
    inlines = [
        ProjectImageInline,  # Shows project images
        ProjectProductsInline,  # Shows project products
        ProjectTestimonialsInline,  # Shows project testimonials
    ]
    list_display = [
        '__str__',
        'date_published',
    ]


admin.site.register(ProjectExhibition, ProjectExhibitionAdmin)

# PROJECT ##############################################################################################################
########################################################################################################################
class ProjectAdmin(admin.ModelAdmin):
    """Admin registration for specific project"""
    model = Project

    list_display = [
        '__str__',
        'date_last_updated',
    ]


admin.site.register(Project, ProjectAdmin)