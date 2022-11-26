# pages/models.py

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
from django.db import models
import uuid

from products.models import (
    Product,
)


# Q&A'S ################################################################################################################
########################################################################################################################

class QandACategory(models.Model):
    """Category model for growing topic range of Q&A"""
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Q&A Category"
        verbose_name_plural = "Q&A Categories"
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name


class QandA(models.Model):
    """Models to represent growing list of Q&A potential clients may be curious about"""
    id = models.UUIDField(
        primary_key=True,
        db_index=True,  # Indexed attribute
        default=uuid.uuid4,
        editable=False
    )

    category = models.ForeignKey(
        'QandACategory',
        on_delete=models.CASCADE,
    )

    question = models.TextField(max_length=150)

    answer = models.TextField(max_length=300)

    class Meta:
        verbose_name = "Q&A"
        verbose_name_plural = "Q&A's"
        ordering = (
            'category',
        )

    def __str__(self):
        return self.question[0:25]


# HOME PAGE ############################################################################################################
########################################################################################################################
class HomePageAnnouncements(models.Model):
    """Represents image announcements displayed in the home page carousel for a more dynamic control"""
    title = models.CharField(max_length=50)  # title of the announcement card

    announcement = models.FileField(upload_to=f'announcements/')

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return self.title


class ServiceAreas(models.Model):
    """Represents a service area for dynamic display on website"""
    area = models.CharField(max_length=50)  # name of service area

    banner = models.FileField(upload_to=f'service_areas/')

    SERVICE_TYPE_CHOICES = [
        ('AC', 'All Cities'),
        ('SC', 'Select Cities'),
    ]
    service_type = models.CharField(
        max_length=2,
        choices=SERVICE_TYPE_CHOICES,
        default='SC',
    )

    class Meta:
        verbose_name = "Service Area"
        verbose_name_plural = "Service Areas"

    def __str__(self):
        return self.area


# TERMS AND CONDITIONS #################################################################################################
########################################################################################################################

class TermandConditions(models.Model):
    """Represents a section for the terms and conditions"""
    section_number = models.IntegerField()

    section_name = models.CharField(max_length=75)

    section_tc = models.TextField()

    class Meta:
        verbose_name = "Terms & Conditions"
        verbose_name_plural = "Terms & Conditions"
        ordering =[
            'section_number',
        ]

    def __str__(self):
        return f"{self.section_number} - {self.section_name}"


# CONTACT PAGE #########################################################################################################
########################################################################################################################

class OperationBlocks(models.Model):
    """Represents all possible hours of operation in a dynamic fashion"""
    day = models.CharField(max_length=15)

    start_time = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(r'\d{1,2}:\d\d [pa]m', 'Please enter a start time in the xx:xx pm/am format.'),
        ],
        blank=True,
        null=True,
    )

    end_time = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(r'\d{1,2}:\d\d [pa]m', 'Please enter an end time in the xx:xx pm/am format.'),
        ],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Operation Block"
        verbose_name_plural = "Operation Blocks"

    def hours_format_display(self):
        """Displays a schedule block in an hour format"""
        if self.start_time == None and self.end_time == None:
            return "Closed"
        else:
            return f"{self.start_time} - {self.end_time}"

    def full_format_display(self):
        """Displays a schedule block in a full format"""
        return f"{self.day.capitalize()}\t{self.hours_format_display()}"

    def __str__(self):
        return self.full_format_display()
