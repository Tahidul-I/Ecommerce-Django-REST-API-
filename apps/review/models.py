from django.db import models
from ..authentication.models import CustomUser
from ..product.models import Product
from django.utils import timezone
# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_review")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review_product")
    review_comment = models.TextField()
    review_star = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReviewImages(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="review_images")
    image_url = models.TextField()