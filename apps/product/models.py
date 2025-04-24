from django.db import models
from django.utils.text import slugify
from ..category.models import Category,SubCategory,SubSubCategory
from ..banner.models import AllBanner,CarouselBanner
from ..brand.models import Brand
import uuid
from django.utils import timezone
# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(Category, related_name="category_products", on_delete=models.CASCADE,blank=True,null=True)
    subcategory = models.ForeignKey(SubCategory, related_name="subcategory_products", on_delete=models.CASCADE,blank=True,null=True)
    subsubcategory = models.ForeignKey(SubSubCategory, related_name="subsubcategory_products", on_delete=models.CASCADE,blank=True,null=True)
    brand =  models.ForeignKey(Brand,blank=True,null=True,on_delete=models.SET_NULL,related_name="brand_products")
    title = models.CharField(max_length=500)
    description = models.TextField()
    image_url = models.CharField(max_length=1500,default="None")
    old_price = models.FloatField()
    new_price = models.FloatField()
    is_new = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True,null=True,max_length=500)
    
    class Meta:
        verbose_name_plural = "Product"

    def save(self, *args, **kwargs):
    
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
          

class ProductVariation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_variations")
    brand =  models.ForeignKey(Brand,null=True,on_delete=models.SET_NULL,related_name="brand_product_variations")
    dimension = models.CharField(max_length=500)
    old_price = models.FloatField()
    new_price = models.FloatField()
    is_deal =  models.BooleanField(default=False)
    is_signature = models.BooleanField(default=False)
    is_banner_product = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    brand_feature = models.BooleanField(default=False)
    stock_quantity = models.IntegerField()
    full_title = models.CharField(max_length = 1200, blank=True, null=True,db_index=True)
    sku = models.CharField(max_length=20,blank=True, editable=False)
    last_bought = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField(blank=True,null=True)
    def save(self, *args, **kwargs):
        self.update_full_title()
        if not self.sku:
            self.sku = self.generate_unique_sku()

        super().save(*args, **kwargs)

    def generate_unique_sku(self):
        return str(uuid.uuid4().hex[:10].upper())
    
    def __str__(self):
        return f"{self.product.title} | {self.dimension} |SKU:{self.sku}"

    class Meta:
        verbose_name_plural = "Product Variation"


    
    def update_full_title(self):
        self.full_title = self.__str__()
    


class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_images")
    image_url = models.CharField(max_length=1200,default=None)
    
    class Meta:
        verbose_name_plural = "Product Images"



    
class OurBestDeals(models.Model):
    title = models.CharField(max_length = 150)
    banner_url = models.CharField(max_length=1500)
    products = models.ManyToManyField(ProductVariation, related_name='top_deals')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Our Best Deals"

    def __str__(self):
        return self.title


class MeherunSignature(models.Model):

    title = models.CharField(max_length = 150)
    banner_url = models.CharField(max_length=1500)
    products = models.ManyToManyField(ProductVariation, related_name='signature')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Meherun's Signature"


    def __str__(self):
        return self.title


class BannerProducts(models.Model):
    title = models.CharField(max_length=100)
    banner_obj = models.OneToOneField(AllBanner,related_name="banner",on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductVariation, related_name='banner_products')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Banner Related Products"


    def __str__(self):
        return self.banner_obj.title
    


class FrequentlyBroughtTogether(models.Model):
    main_product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="fbt_main")
    frequently_brought_product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name="Fbt_product")
    
    def __str__(self):
        return f"{self.main_product.title}(main) > {self.frequently_brought_product.product.title}|{self.frequently_brought_product.dimension}|(FBT)"
    
    class Meta:
        verbose_name_plural = "Frequently Brought Together"

class RecommendedProduct(models.Model):
    main_product =  models.ForeignKey(Product,on_delete=models.CASCADE,related_name="main_for_recommended_product")
    recommended_product_id = models.IntegerField()

class YouMayAlsoLike(models.Model):
    product = models.ForeignKey(ProductVariation,on_delete=models.CASCADE,related_name = "you_may_also_like_products",blank=True,null=True)
    def __str__(self):

        return f"{self.product.product.title} | {self.product.dimension} | {self.product.new_price}"
    
