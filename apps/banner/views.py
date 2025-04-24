from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
# Create your views here.
@api_view(['GET'])
def get_banner_carousel(request):
    banners = AllBanner.objects.filter(banner_type='carousel').order_by('-id')
    serializer = AllBannerSerilizer(banners,many=True)
    return Response({'status_code':200,'banners':serializer.data})

@api_view(['GET']) #For Frontend Data Fetch
def get_active_banner_carousel(request):
    banners = AllBanner.objects.filter(banner_type='carousel',is_active=True).order_by('-updated_at')
    serializer = AllBannerSerilizer(banners,many=True)
    return Response({'status_code':200,'banners':serializer.data})

@api_view(['POST'])
def save_banner(request):
    title = request.data.get('title')
    banner_url = request.data.get('banner_url')
    is_active = request.data.get('is_active')
    banner_type = request.data.get('banner_type')
    banner_obj = AllBanner(
    title = title,
    banner_url = banner_url,
    is_active = is_active,
    banner_type = banner_type
    )
    banner_obj.save()
    return Response({'status_code':200,'message':'Data Saved'})

@api_view(['POST'])
def change_banner_status(request):
    id = request.data.get('id')
    is_active = request.data.get('is_active')
    banner_obj = AllBanner.objects.get(id = id)
    if banner_obj.banner_type == "title_banner_1":
        AllBanner.objects.filter(banner_type ='title_banner_1').update(is_active = False)
    elif banner_obj.banner_type == "title_banner_2":
        AllBanner.objects.filter(banner_type ='title_banner_2').update(is_active = False)
    banner_obj.is_active = is_active
    banner_obj.save()
    return Response({'status_code':200,'message':'Title Banner Status Changed'})


@api_view(['GET'])
def get_title_banner_one(request):
    title_banners = AllBanner.objects.filter(banner_type="title_banner_1").order_by('-id')
    serializer = AllBannerSerilizer(title_banners,many=True)
    return Response({'status_code':200,'title_banners':serializer.data})

@api_view(['GET'])
def get_active_title_banner_one(request):
    title_banners = AllBanner.objects.get(banner_type="title_banner_1",is_active=True)
    serializer = AllBannerSerilizer(title_banners,many=False)
    return Response({'status_code':200,'title_banners':serializer.data})

@api_view(['GET'])
def get_title_banner_two(request):
    title_banners = AllBanner.objects.filter(banner_type="title_banner_2").order_by('-id')
    serializer = AllBannerSerilizer(title_banners,many=True)
    return Response({'status_code':200,'title_banners':serializer.data})

@api_view(['GET'])
def get_active_title_banner_two(request):
    title_banners = AllBanner.objects.get(banner_type="title_banner_2",is_active=True)
    serializer = AllBannerSerilizer(title_banners,many=False)
    return Response({'status_code':200,'title_banners':serializer.data})

@api_view(['POST'])
def delete_selected_banner(request):
    banner_ids = request.data.get('banner_ids')
    AllBanner.objects.filter(id__in = banner_ids).delete()
    return Response({'status_code':200,'message':'Deleted Successfully'})

@api_view(['POST'])
def delete_banner(request):
    id = request.data.get('id')
    AllBanner.objects.get(id=id).delete()
    return Response({'status_code':200,'message':'Banner Deleted Successfully'})