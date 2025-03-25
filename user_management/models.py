from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager

# Create your models here.
class User(AbstractBaseUser):
    ROLE_CHOICE = (
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
        ('Admin', 'Admin'),
    )
    
    first_name = models.CharField(max_length=225, blank=False, null=False, default="User")
    last_name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225, unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default='Employee')
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    can_create_tasks = models.BooleanField(default=False)
    can_assign_tasks = models.BooleanField(default=False)
    can_view_all_tasks = models.BooleanField(default=False)
    
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']
    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.role == 'Admin':
            self.can_create_tasks = True
            self.can_assign_tasks = True
            self.can_view_all_tasks = True
            self.is_staff = True
        elif self.role == 'Manager':
            self.can_create_tasks = True
            self.can_assign_tasks = True
            self.can_view_all_tasks = True
        elif self.role == 'Employee':
            self.can_create_tasks = False
            self.can_assign_tasks = False
            self.can_view_all_tasks = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name}" if self.first_name else self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True