# accounts/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid


# BASE USER ############################################################################################################
########################################################################################################################
class CustomUser(AbstractUser):
    """Represents the base for all user types"""

    id = models.UUIDField(
        primary_key=True,
        db_index=True,  # Indexed attribute
        default=uuid.uuid4,
        editable=False
    )

    class Types(models.TextChoices):
        ADMINISTRATION = "ADMINISTRATION", "Administration"
        STAFF = "STAFF", "Staff"
        SALES = "SALES", "Sales"
        CONSTRUCTION = "CONSTRUCTION", "Construction"
        CUSTOMER = "CUSTOMER", "Customer"

    type = models.CharField('Type', max_length=20,
                            choices=Types.choices, default=Types.CUSTOMER)

    phone_number = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        verbose_name = "Base User"
        verbose_name_plural = "All Users"
        ordering = (
            'last_name',
            'first_name',
        )

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


# ADMINISTRATION TYPE ##################################################################################################
########################################################################################################################
class AdministrationManager(BaseUserManager):
    """Ensures we only get Administration users when executing queries on this user type by extending the
    BaseUserManager model"""

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.ADMINISTRATION)


class AdministrationMore(models.Model):
    """Add Administration attributes here"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Flag used for privacy of personnel not available to public
    available_to_public = models.BooleanField(default=False)

    # Profile picture
    photo = models.ImageField(upload_to='personnel/', blank=True, null=True)

    class Meta:
        verbose_name = "Administration Member"
        verbose_name_plural = "Administration Team"


class AdministrationUser(CustomUser):
    """Represents Users that are part of the administration"""
    base_type = CustomUser.Types.ADMINISTRATION
    objects = AdministrationManager()

    @property
    def more(self):
        """Attaches Administration user to its custom attributes"""
        return self.administrationmore

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        """Ensures that if base user does not exist, Administration user will still be created accordingly"""
        if not self.pk:
            self.type = CustomUser.Types.ADMINISTRATION


# STAFF TYPE ###########################################################################################################
########################################################################################################################
class StaffManager(BaseUserManager):
    """Ensures we only get Staff users when executing queries on this user type by extending the
    BaseUserManager model"""
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.STAFF)


class StaffMore(models.Model):
    """Add Staff attributes here"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Profile picture
    photo = models.ImageField(upload_to='personnel/', blank=True, null=True)

    # Staff types
    STAFF_TYPES = [
        ('OF', 'Office Manager'),
        ('PE', 'Permit Expediter'),
        ('RE', 'Receptionist'),
    ]

    staff_type = models.CharField(
        max_length=25,
        choices=STAFF_TYPES,
        default='PE'
    )

    # Flag used for privacy of personnel not available to public
    available_to_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Staff Member"
        verbose_name_plural = "Office Staff"


class StaffUser(CustomUser):
    """Represents Users that are part of the office staff"""
    base_type = CustomUser.Types.STAFF
    objects = StaffManager()

    @property
    def more(self):
        """Attaches Staff user to its custom attributes"""
        return self.staffmore

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        """Ensures that if base user does not exist, Staff user will still be created accordingly"""
        if not self.pk:
            self.type = CustomUser.Types.STAFF


# SALES TYPE ###########################################################################################################
########################################################################################################################
class SalesManager(BaseUserManager):
    """Ensures we only get Sales users when executing queries on this user type by extending the
    BaseUserManager model"""

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.SALES)


class SalesMore(models.Model):
    """Add Sales attributes here"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Profile picture
    photo = models.ImageField(upload_to='personnel/', blank=True, null=True)

    # Sales types
    SALES_TYPES = [
        ('SM', 'Sales Manager'),
        ('SA', 'Sales Associate'),
        ('SP', 'Sales Apprentice'),
    ]

    sales_type = models.CharField(
        max_length=25,
        choices=SALES_TYPES,
        default='SP'
    )

    # Flag used for privacy of personnel not available to public
    available_to_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Sales Member"
        verbose_name_plural = "Sales Team"


class SalesUser(CustomUser):
    """Represents Users that are part of the sales team"""
    base_type = CustomUser.Types.SALES
    objects = SalesManager()

    @property
    def more(self):
        """Attaches Sales user to its custom attributes"""
        return self.salesmore

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        """Ensures that if base user does not exist, Sales user will still be created accordingly"""
        if not self.pk:
            self.type = CustomUser.Types.SALES


# CONSTRUCTION TYPE ####################################################################################################
########################################################################################################################
class ConstructionManager(BaseUserManager):
    """Ensures we only get Construction users when executing queries on this user type by extending the
    BaseUserManager model"""
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.CONSTRUCTION)


class ConstructionMore(models.Model):
    """Add Construction attributes here"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Profile picture
    photo = models.ImageField(upload_to='personnel/', blank=True, null=True)

    # Construction types
    CONSTRUCTION_TYPES = [
        ('PM', 'Project Manager'),
        ('CL', 'Crew Leader'),
        ('CM', 'Crew Member'),
    ]

    construction_type = models.CharField(
        max_length=25,
        choices=CONSTRUCTION_TYPES,
        default='CM'
    )

    # Flag used for privacy of personnel not available to public
    available_to_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Construction Member"
        verbose_name_plural = "Construction Crew"


class ConstructionUser(CustomUser):
    """Represents Users that are part of the construction crew"""
    base_type = CustomUser.Types.CONSTRUCTION
    objects = ConstructionManager()

    @property
    def more(self):
        """Attaches Construction user to its custom attributes"""
        return self.constructionmore

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        """Ensures that if base user does not exist, Construction user will still be created accordingly"""
        if not self.pk:
            self.type = CustomUser.Types.CONSTRUCTION


# CUSTOMER TYPE ########################################################################################################
########################################################################################################################
class CustomerManager(BaseUserManager):
    """Ensures we only get Customer users when executing queries on this user type by extending the
    BaseUserManager model"""
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.CUSTOMER)


class CustomerMore(models.Model):
    """Add Customer attributes here"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class CustomerUser(CustomUser):
    """Represents users that are customers"""
    base_type = CustomUser.Types.CUSTOMER
    objects = CustomerManager()

    @property
    def more(self):
        """Attaches Customer user to its custom attributes"""
        return self.staffmore

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        """Ensures that if base user does not exist, Customer user will still be created accordingly"""
        if not self.pk:
            self.type = CustomUser.Types.CUSTOMER
