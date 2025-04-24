from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,APIView
from .serializers import *
from ..authentication.utils import admin_user_checker
from .models import *
from ..product.models import ProductVariation,Product
from ..product.serializers import FeatureSectionProductVariationDataFetchSerializer
# Create your views here.

@api_view(['POST'])
def save_brand_details(request):
    title = request.data.get('brand_title')
    logo_url = request.data.get('logo_url')
    banner_url = request.data.get('banner_url')
    Brand(title=title,brand_logo=logo_url,banner_url=banner_url).save()
    return Response({'status_code':200,'message':'Brand info saved'})

@api_view(['POST'])
def change_brand_active_status(request):
    brand_id = request.data.get('brand_id')
    status = request.data.get('status')
    brand_obj = Brand.objects.get(id = brand_id)
    brand_obj.is_active = status
    brand_obj.save()
    return Response({'status_code':200,'message':'Status Updated'})

@api_view(['GET'])
def get_brand_data(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        search_key = request.GET.get('searchQuery',None)
        has_more = True
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        brand_data = Brand.objects.all().order_by('title')
        if search_key!='':
            brand_data = brand_data.filter(title__icontains=search_key)
        if brand_data.count() < page*limit:
            has_more = False
        brand_data = brand_data[0:page*limit]
        serializer = BrandDataSerializer(brand_data, many=True)
        return Response({'brand_data':serializer.data,'has_more':has_more})
    else:
        return Response({'message':'Access Denied'})
    
@api_view(['POST'])
def update_brand_data(request):
    brand_id = request.data.get('brand_id')
    logo_url = request.data.get('logo_url')
    banner_url = request.data.get('banner_url')
    brand_title = request.data.get('brand_title')
    brand_obj = Brand.objects.get(id = brand_id)
    brand_obj.brand_logo = logo_url
    brand_obj.banner_url = banner_url
    brand_obj.title = brand_title
    brand_obj.save()
    return Response({'status_code':200,'message':'Brand data updated'})

@api_view(['GET'])
def get_brand_list(request):
    brand_data = Brand.objects.all()
    serializer = BrandListSerializer(brand_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_brand_products_for_dashboard(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        brand_id = request.GET.get('brand_id',None)
        feature_brand_id = request.GET.get('feature_id',None)
        if brand_id is not None:
            brand_products = Product.objects.filter(brand_id = brand_id).distinct()
            serializer = BrandProductSerilizer(brand_products,many=True)
            return Response(serializer.data)
        else:
            brand_products = ProductVariation.objects.filter(brand_id = feature_brand_id, brand_feature=True)
            serializer = FeatureBrandProductSerilizer(brand_products,many=True)
            return Response(serializer.data)

    else:
        return Response({'message':'Access Denied'})

@api_view(['POST'])
def delete_brand(request):
    brand_id =  request.data.get('brand_id')
    Brand.objects.get(id = brand_id).delete()
    return Response({'status_code':200,'message':'Brand Deleted'})


@api_view(['GET'])
def get_brand_products(request):
    brand_id = request.GET.get('brand_id')
    brand_products = ProductVariation.objects.filter(brand_id = brand_id,brand_feature = True)
    serializer = FeatureSectionProductVariationDataFetchSerializer(brand_products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_active_brands(request):
    brands = Brand.objects.filter(is_active = True)
    serializer = BrandSerializer(brands,many=True)
    return Response(serializer.data)