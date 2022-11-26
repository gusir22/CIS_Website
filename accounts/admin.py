# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    AdministrationMore,
    StaffMore,
    SalesMore,
    ConstructionMore,
    CustomerMore,
)


# BASE USER ADMIN ######################################################################################################
########################################################################################################################
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    """Admin registration for Custom User models"""
    list_display = [
        '__str__',
        'username',
        'type',
    ]

    fieldsets = (
        (
            "Account Info",
            {"fields": (
                "username",
                "password",
                "type",
            )
            }
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                )
            }
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            }
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            }
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)


# ADMINISTRATION TYPE ADMIN ############################################################################################
########################################################################################################################
class AdministrationAdmin(admin.ModelAdmin):
    """Admin registration for Administration More details"""
    list_display = [
        'user',
    ]


admin.site.register(AdministrationMore, AdministrationAdmin)


# STAFF TYPE ADMIN #####################################################################################################
########################################################################################################################
class StaffAdmin(admin.ModelAdmin):
    """Admin registration for Staff More details"""
    list_display = [
        'user',
        'get_staff_type',
    ]

    def get_staff_type(self, obj):
        """Extracts Staff Type for User"""
        return obj.get_staff_type_display()
    # Define Admin Column Name
    get_staff_type.short_description = "Staff Type"


admin.site.register(StaffMore, StaffAdmin)


# SALES TYPE ADMIN #####################################################################################################
########################################################################################################################
class SalesAdmin(admin.ModelAdmin):
    """Admin registration for Sales More details"""
    list_display = [
        'user',
        'get_sales_type',
    ]

    def get_sales_type(self, obj):
        """Extracts Sales Type for User"""
        return obj.get_sales_type_display()
    # Define Admin Column Name
    get_sales_type.short_description = "Sales Type"


admin.site.register(SalesMore, SalesAdmin)


# CONSTRUCTION TYPE ADMIN ##############################################################################################
########################################################################################################################
class ConstructionAdmin(admin.ModelAdmin):
    """Admin registration for Construction More details"""
    list_display = [
        'user',
        'get_construction_type',
    ]

    def get_construction_type(self, obj):
        """Extracts Construction Type for User"""
        return obj.get_construction_type_display()
    # Define Admin Column Name
    get_construction_type.short_description = "Construction Type"


admin.site.register(ConstructionMore, ConstructionAdmin)


# CUSTOMER TYPE ADMIN ##################################################################################################
########################################################################################################################
class CustomerAdmin(admin.ModelAdmin):
    """Admin registration for Customer More details"""
    list_display = [
        'user',
    ]


admin.site.register(CustomerMore, CustomerAdmin)
