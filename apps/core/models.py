from django.db import models

# Create your models here.
class ShippingCost(models.Model):
    outside_dhaka = models.FloatField()
    inside_dhaka = models.FloatField()