from django.db import models
from ..authentication.models import CustomUser
from ..product.models import ProductVariation,Product
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation,on_delete=models.CASCADE)
    title = models.CharField(max_length=1500)
    dimension = models.CharField(max_length=50)
    new_price = models.FloatField()
    old_price = models.FloatField()
    image_url = models.CharField(max_length=1500)
    quantity = models.IntegerField()

    class Meta:
        verbose_name_plural = "Cart"

    def __str__(self):
        return self.user.name

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
