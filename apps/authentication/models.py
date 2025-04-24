from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
        
    def __str__(self):
        return f"{self.name} | {self.id}"

class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp =  models.CharField(max_length=6, blank=True,null=True)
    created_at = models.DateTimeField(blank=True,null=True)
    otp_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name_plural = "OTP"