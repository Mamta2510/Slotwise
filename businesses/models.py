from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Business(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="businesses",)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = models.TextField()
    timezone = models.CharField(max_length=64,default="Asia/Kolkata",)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    business = models.ForeignKey(Business,on_delete=models.PROTECT,related_name="services",)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)],)
    price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)],)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.business.name}"