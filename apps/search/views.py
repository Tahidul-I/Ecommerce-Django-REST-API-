from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..product.models import ProductVariation
from ..product.serializers import FeatureSectionProductVariationDataFetchSerializer
from django.db.models import Q
from ..product.serializers import FeatureSectionProductVariationDataFetchSerializer
# Create your views here.
@api_view(['POST'])
def search_filter(request):
    search_keyword = request.data.get('search_keyword')
    products = ProductVariation.objects.filter(full_title__icontains=search_keyword)
    
    if not products.exists():
        # Optimize the loop to reduce the number of queries
        for i in range(len(search_keyword)):
            keyword_fragment = search_keyword[0:len(search_keyword) - i]
            products = ProductVariation.objects.filter(full_title__icontains=keyword_fragment)
            if products.exists():
                break

    serializer = FeatureSectionProductVariationDataFetchSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_product_sort_and_filter(request):
    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',500000)
    brand_ids = request.GET.get('brand_ids',None)
    sort_key = request.GET.get('SortQuery',None)
    products = ProductVariation.objects.filter(Q(new_price__gte=min_price) & Q(new_price__lte=max_price))
    if brand_ids is not None:
        products = products.filter(brand_id__in = brand_ids)
    if sort_key is not None:
        if sort_key == 'hight to low':
            products = products.order_by('-new_price')
        if sort_key == 'low to high':
            products = products.order_by('new_price')
    
    serializer = FeatureSectionProductVariationDataFetchSerializer(products, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def top_product_sort_and_filter(request):
    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',500000)
    brand_ids = request.GET.get('brand_ids',None)
    sort_key = request.GET.get('SortQuery',None)
    products = ProductVariation.objects.filter(Q(new_price__gte=min_price) & Q(new_price__lte=max_price) & Q(is_top=True))
    if brand_ids is not None:
        products = products.filter(brand_id__in = brand_ids)
    if sort_key is not None:
        if sort_key == 'heighToLow':
            products = products.order_by('-new_price')
        if sort_key == 'lowToHeigh':
            products = products.order_by('new_price')
    
    serializer = FeatureSectionProductVariationDataFetchSerializer(products, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def new_arrival_product_sort_and_filter(request):
    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',500000)
    brand_ids = request.GET.get('brand_ids',None)
    sort_key = request.GET.get('SortQuery',None)
    products = ProductVariation.objects.filter(Q(new_price__gte=min_price) & Q(new_price__lte=max_price) & Q(is_new=True))
    if brand_ids is not None:
        products = products.filter(brand_id__in = brand_ids)
    if sort_key is not None:
        if sort_key == 'hight to low':
            products = products.order_by('-new_price')
        if sort_key == 'low to high':
            products = products.order_by('new_price')
    
    serializer = FeatureSectionProductVariationDataFetchSerializer(products, many=True)
    return Response(serializer.data)