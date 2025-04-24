from rest_framework import serializers
from .models import *
from ..product.models import Product,ProductVariation
class BrandDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BrandListSerializer(serializers.ModelSerializer):
    brand_id = serializers.IntegerField(source = 'id',read_only=True)
    class Meta:
        model = Brand
        fields = ['brand_id','title']

class BrandProductSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','image_url']

class FeatureBrandProductSerilizer(serializers.ModelSerializer):
    title = serializers.CharField(source = 'product.title',read_only=True)
    image_url = serializers.CharField(source = 'product.image_url',read_only=True)
    class Meta:
        model = ProductVariation
        fields = ['id','title','image_url','dimension']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id','banner_url']