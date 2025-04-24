from django.db import models
# Create your models here.
class Brand(models.Model):
    title = models.CharField(max_length=250)
    brand_logo = models.TextField()
    banner_url = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


