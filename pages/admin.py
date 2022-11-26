# pages/admin.py
from django.contrib import admin
from .models import (
    QandA,
    QandACategory,
    HomePageAnnouncements,
    ServiceAreas,
    AboutUsText,
    TermandConditions,
    OperationBlocks,
)

from products.models import (
    Product,
)


# Q&A'S ################################################################################################################
########################################################################################################################

class QandAAdmin(admin.ModelAdmin):
    model = QandA
    list_display = [
        '__str__',
        'category',
    ]


admin.site.register(QandA, QandAAdmin)


# Simple QandACategory registry
admin.site.register(QandACategory)


# HOME PAGE ############################################################################################################
########################################################################################################################

class AnnouncementAdmin(admin.ModelAdmin):
    model = HomePageAnnouncements
    list_display = [
        '__str__',
    ]


admin.site.register(HomePageAnnouncements, AnnouncementAdmin)


class ServiceAreaAdmin(admin.ModelAdmin):
    model = ServiceAreas
    list_display = [
        '__str__',
        'service_type',
    ]


admin.site.register(ServiceAreas, ServiceAreaAdmin)


class AboutUsTextAdmin(admin.ModelAdmin):
    model = AboutUsText
    list_display = [
        '__str__',
    ]


admin.site.register(AboutUsText, AboutUsTextAdmin)


# TERMS AND CONDITIONS #################################################################################################
########################################################################################################################

class TermsandConditionsAdmin(admin.ModelAdmin):
    model = TermandConditions
    list_display = [
        '__str__',
    ]


admin.site.register(TermandConditions, TermsandConditionsAdmin)


# CONTACT PAGE #########################################################################################################
########################################################################################################################

class OperationBlockAdmin(admin.ModelAdmin):
    model = OperationBlocks
    list_display = [
        '__str__',
    ]


admin.site.register(OperationBlocks, OperationBlockAdmin)
