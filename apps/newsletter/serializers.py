from rest_framework import serializers
from .models import *

class EmailForOutOfStockProductsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product_variation.product.title',read_only = True)
    dimension = serializers.CharField(source='product_variation.dimension',read_only = True)
    price = serializers.CharField(source='product_variation.new_price',read_only = True)
    image_url = serializers.URLField(source='product_variation.product.image_url',read_only = True)
    product_variation_id = serializers.IntegerField(source='product_variation.id',read_only = True)
    class Meta:
        model = EmailForOutOfStockProducts
        fields = ['product_variation_id','title','dimension','price','image_url']

class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = '__all__'

class ProductRequestEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailForOutOfStockProducts
        fields = ['id','email','status']

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id','name','email','phone','message','is_replied','created_at','replied_text']