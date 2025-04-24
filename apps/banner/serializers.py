from rest_framework import serializers
from .models import *

class BannerCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselBanner
        fields = ['id','title','banner_url','is_active']



class TitleBannerSerilizerOne(serializers.ModelSerializer):
    class Meta:
        model = TitleBannerOne
        fields = ['id','title','banner_url','is_active']


class TitleBannerSerilizerTwo(serializers.ModelSerializer):
    class Meta:
        model = TitleBannerTwo
        fields = ['id','title','banner_url','is_active']


class AllBannerSerilizer(serializers.ModelSerializer):
    class Meta:
        model = AllBanner
        fields = ['id','title','banner_url','is_active','banner_type','is_navigate']