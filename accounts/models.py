from django.db import models

# Create your models here.
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class District(models.Model):
    """
    Model for geographic districts that constituents belong to.
    """
    name = models.CharField(max_length=100)
    boundary_coordinates = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    """
    Custom user manager for handling user creation with email as username.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ADMIN)
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom user model with role-based access and district association.
    """
    # Role choices
    CONSTITUENT = 'constituent'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (CONSTITUENT, _('Constituent')),
        (ADMIN, _('Administrator')),
    ]
    
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CONSTITUENT)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    profile_info = models.JSONField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email