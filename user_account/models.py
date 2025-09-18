from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.forms import ValidationError
import uuid
# Create your models here.
class CustomManager(BaseUserManager):

    def create_user(self,email,password=None,**extra_kwargs):
        if not email or not password :
            raise ValueError('Invalid credentials')
        email = self.normalize_email(email=email)
        user = self.model(email=email,**extra_kwargs)
        user.set_password(password)
        user.save()
        return user 
    def create_superuser(self,email,password,**extra_kwargs):
        extra_kwargs.setdefault('is_active',True)
        extra_kwargs.setdefault('is_staff',True)
        extra_kwargs.setdefault('is_superuser',True)
        
        if extra_kwargs.get('is_active') is not True:
            raise ValidationError('Super user must have is_active true')
        if extra_kwargs.get('is_staff') is not True:
            raise ValidationError('Superuser must have is_staff true')
        if extra_kwargs.get('is_superuser') is not True:
            raise ValidationError('Superuser must have is_superuser true')
        
        return self.create_user(email,password,**extra_kwargs)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    first_name       = models.CharField(max_length=50)
    last_name        = models.CharField(max_length=50)
    email            = models.EmailField(unique=True)
    phone_number     = models.CharField(max_length=15, unique=True)
    address_line_1   = models.CharField(max_length=255)
    address_line_2   = models.CharField(max_length=255, blank=True)
    city             = models.CharField(max_length=50)
    state            = models.CharField(max_length=50)
    country          = models.CharField(max_length=50)
    date_joined      = models.DateTimeField(auto_now_add=True)
    is_active        = models.BooleanField(default=False)
    is_staff         = models.BooleanField(default=False)
    is_superuser     = models.BooleanField(default=False)

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

        
        


