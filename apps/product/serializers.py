from rest_framework import serializers
from .models import *
from ..banner.models import CarouselBanner
from ..review.models import Review
from django.db.models import Avg

class ProductDataFetchSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    subcategory = serializers.CharField(source='subcategory.full_title', read_only=True)
    subcategory_id = serializers.IntegerField(source='subcategory.id', read_only=True)
    subsubcategory = serializers.CharField(source='subsubcategory.full_title', read_only=True)
    subsubcategory_id = serializers.IntegerField(source='subsubcategory.id', read_only=True)
    brand_title = serializers.SerializerMethodField()
    brand_id = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('category_id','category','subcategory_id','subcategory','subsubcategory_id','subsubcategory','id','title','brand_title','brand_id','description','image_url','old_price','new_price','is_new','is_top')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prefetch related product variations for all products in the queryset
        self.variations = ProductVariation.objects.filter(product__in=[product.id for product in self.instance]).select_related('brand')


    def get_brand_title(self, obj):
        variation = next((v for v in self.variations if v.product_id == obj.id), None)
        if variation and variation.brand:
            return variation.brand.title
        return None
    
    def get_brand_id(self, obj):
        variation = next((v for v in self.variations if v.product_id == obj.id), None)
        if variation and variation.brand:
            return variation.brand.id
        return None


class ProductVariationDataFetchSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title', read_only=True)
    brand_id = serializers.IntegerField(source='brand.id', read_only=True)
    brand_title = serializers.CharField(source='brand.title', read_only=True)
    class Meta:
        model = ProductVariation
        fields = ['id','title','dimension','old_price','new_price','stock_quantity','is_deal','is_signature','is_banner_product','brand_id','brand_title','brand_feature','is_new','is_top','full_title','sku','expires_at']

class ProductImagesDataFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        exclude = ['product','id']


class OurBestDealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurBestDeals
        exclude = ['products']


class ProductDetailsSerializer(serializers.ModelSerializer):
    product_variations = ProductVariationDataFetchSerializer(many=True, read_only=True)
    product_images = ProductImagesDataFetchSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = ('id','title','description','image_url','old_price','new_price','product_variations','product_images')



class ProductRecommendation(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields =['id','full_title']


class MeherunSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeherunSignature
        exclude = ['products']


class BannerProductsSerializer(serializers.ModelSerializer):
    banner_id = serializers.IntegerField(source='banner_obj.id', read_only=True)
    banner_url = serializers.URLField(source='banner_obj.banner_url', read_only=True)
    class Meta:
        model = BannerProducts
        fields = ['id','banner_id','title','banner_url','is_active']


class BannerRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselBanner

        fields = ['id','title']



class FeatureSectionProductVariationDataFetchSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(source='product.image_url', read_only=True)
    title = serializers.CharField(source='product.title', read_only=True)
    product_variation_id = serializers.IntegerField(source='id', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    average_rating = serializers.SerializerMethodField()
    brand_id = serializers.IntegerField(source='brand.id', read_only=True)
    brand_title = serializers.CharField(source='brand.title', read_only=True)
    class Meta:
        model = ProductVariation
        fields = ['product_id','product_variation_id','title','dimension','old_price','new_price','image_url','average_rating','brand_id','brand_title','stock_quantity']

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(product=obj.product)
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('review_star'))['review_star__avg']
            return round(average_rating, 2)  
        return 0  

class RecommendedProductSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','image_url']

class FrequentlyBroughtProductSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title',read_only=True)
    image_url = serializers.URLField(source='product.image_url',read_only=True)
    fbt_product_id = serializers.IntegerField(source='id',read_only=True)
    class Meta:
        model = ProductVariation
        fields = ['fbt_product_id','title','image_url','old_price','new_price','dimension']

class YouMayAlsoLikeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='full_title',read_only=True)
    class Meta:
        model = ProductVariation
        fields = ['id','title']

class GetYouMayAlsoLikeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title',read_only=True)
    image_url = serializers.URLField(source='product.image_url')
    class Meta:
        model = ProductVariation
        fields = ['id','title','image_url','dimension']

class YouMayAlsoLikeProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    brand_title = serializers.CharField(source='brand.title')
    title = serializers.CharField(source='product.title')
    image_url = serializers.URLField(source='product.image_url')
    product_variation_id = serializers.IntegerField(source='id',read_only = True)
    product_id = serializers.IntegerField(source='product.id',read_only = True)
    class Meta:
        model = ProductVariation
        fields = ['product_id','product_variation_id','title','old_price','new_price','dimension','image_url','average_rating','stock_quantity','brand_title']
    
    def get_average_rating(self, obj):
        reviews = Review.objects.filter(product=obj.product)
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('review_star'))['review_star__avg']
            return round(average_rating, 2)  
        return 0    


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude  = ['is_new','is_top','slug','category','subcategory','subsubcategory']


class FBTRecommendation(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    product_variation_id = serializers.IntegerField(source='id',read_only=True)
    class Meta:
        model = ProductVariation
        fields = ['product_variation_id','title']

    def get_title(self,obj):
        title = f"{obj.full_title} | Price:{obj.new_price}"
        return title
    

class SKUProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title',read_only=True)
    image_url = serializers.URLField(source='product.image_url',read_only=True)
    brand_title = serializers.CharField(source='brand.title',read_only=True)
    class Meta:
        model = ProductVariation
        fields = ['id','title','brand_title','image_url','dimension','old_price','new_price','stock_quantity','sku','expires_at']