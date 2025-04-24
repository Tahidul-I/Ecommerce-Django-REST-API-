from rest_framework import serializers
from .models import Category, SubCategory, SubSubCategory

class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ('id','title', 'slug')

class SubCategorySerializer(serializers.ModelSerializer):
    related_subsubcategory = SubSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id','title', 'slug', 'related_subsubcategory')

class CategorySerializer(serializers.ModelSerializer):
    related_subcategory = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id','title', 'slug', 'related_subcategory','is_special','color')


class CategoryDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title','is_special','color')

class SubCategoryDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id','full_title')

class SubSubCategoryDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ('id','full_title')