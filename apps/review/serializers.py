from rest_framework import serializers
from .models import *

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImages
        fields = ['image_url']


class ReviewSerializer(serializers.ModelSerializer):
    review_images = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.name')
    review_id = serializers.IntegerField(source='id')
    class Meta:
        model = Review
        fields = ['review_id','username','review_star','review_comment','updated_at','review_images']
    
    def get_review_images(self, obj):
        return obj.review_images.values_list('image_url', flat=True)
