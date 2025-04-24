from rest_framework import serializers
from .models import Cart
from ..product.models import Product
from ..review.models import Review
from django.db.models import Avg
class CartProductSerializer(serializers.ModelSerializer):
    product_variation_id = serializers.IntegerField(source='product_variation.id',read_only=True)
    product_id = serializers.IntegerField(source='product_variation.product.id',read_only=True)
    stock_quantity = serializers.IntegerField(source='product_variation.stock_quantity',read_only=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['product_id','product_variation_id','title','old_price','new_price','dimension','image_url','quantity','stock_quantity','average_rating']

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(product=obj.product_variation.product)
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('review_star'))['review_star__avg']
            return round(average_rating, 2) 
        return 0 


class WishlistProductSeriizer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','title','new_price','image_url','average_rating','total_reviews']

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(product=obj)
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('review_star'))['review_star__avg']
            return round(average_rating, 2)  
        return 0  

    def get_total_reviews(self, obj):
        reviews = Review.objects.filter(product=obj)
        return reviews.count()

