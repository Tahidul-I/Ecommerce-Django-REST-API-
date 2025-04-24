from django.db import models

# Create your models here.
class AllBanner(models.Model):
    title = models.CharField(max_length = 100)
    banner_url = models.CharField(max_length = 1500)
    is_active = models.BooleanField(default=False)
    banner_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_navigate = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.title

class CarouselBanner(models.Model):
    title = models.CharField(max_length = 100)
    banner_url = models.CharField(max_length = 1500)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Carousel Banner"

    def __str__(self):
        return self.title


class TitleBannerOne(models.Model):
    title = models.CharField(max_length = 100)
    banner_url = models.CharField(max_length = 1500)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Title Banners One"

    def __str__(self):
        return self.title
    
class TitleBannerTwo(models.Model):
    title = models.CharField(max_length = 100)
    banner_url = models.CharField(max_length = 1500)
    is_active = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Title Banners Two"

    def __str__(self):
        return self.title
