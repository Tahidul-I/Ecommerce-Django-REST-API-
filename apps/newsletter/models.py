from django.db import models
from ..product.models import ProductVariation
# Create your models here.
class NewsLetter(models.Model):
    email = models.EmailField()

class EmailForOutOfStockProducts(models.Model):

    EMAIL_STATUS = [
    ('Pending', 'Pending'),
    ('Sent', 'Sent'),
    ]
    product_variation = models.ForeignKey(ProductVariation,on_delete=models.CASCADE,related_name="email_for_products")
    email = models.EmailField()
    status = models.CharField(max_length=250,default="Pending",choices = EMAIL_STATUS,verbose_name="Status")

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100,blank=True,null=True)
    message = models.TextField()
    is_replied = models.BooleanField(default = False)
    replied_text = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(blank=True,null=True)
    replied_at = models.DateTimeField(blank=True,null=True)
