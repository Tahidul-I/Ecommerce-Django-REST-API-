from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from .models import Category,SubCategory,SubSubCategory
# Create your views here.
from ..authentication.utils import admin_user_checker
from django.db.models import Case, When, IntegerField
@api_view(['GET'])
def all_category_data(request):
    categories = Category.objects.annotate(
        special_order=Case(
            When(is_special=True, then=1),
            default=0,
            output_field=IntegerField(),
        )
    ).order_by('special_order', 'title')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def save_category_data(request):
    category_title = request.data.get('category_title')
    existing_category = None
    try:
        existing_category = Category.objects.get(query_title = category_title.lower())
    except:
        pass

    if existing_category is None:
        is_special = request.data.get('is_special')
        background_color_hex_code = request.data.get('background_color_hex_code')
        save_data = Category(
            query_title = category_title.lower(),
            title = category_title,
            is_special = is_special,
            color = background_color_hex_code
        )
        save_data.save()

        return Response({'status_code':200,'message':"Category Saved"})
    else:
        return Response({'status_code':400,'message':"Category Already Exist"})


@api_view(['POST'])
def save_subcategory_data(request):
    category_id = request.data.get('category_id')
    subcategory_name = request.data.get('subcategory_title')
    existing_category = None 
    try:
        existing_category = Category.objects.get(id = category_id)
    except:
        pass

    if existing_category is not None:
        existing_subcategory = None
        try:
            existing_subcategory = SubCategory.objects.get(query_title = subcategory_name.lower(),category_id = existing_category.id )
            
        except:
            pass
        if existing_subcategory is None:

            save_data = SubCategory(
                category = existing_category,
                query_title = subcategory_name.lower(),
                title = subcategory_name,
                full_title = f"{existing_category.title}>{subcategory_name}"
            )
            save_data.save()
            return Response({'status_code':200,'message':"SubCategory Saved"})
        else:
            return Response({'status_code':400,'message':"SubCategory Under The Same Category Already Exist"})
    
    else:
        return Response({'status_code':400,'message':"Category Does Not Exist"})
    

@api_view(['POST'])
def save_subsubcategory_data(request):
    subcategory_id = request.data.get('subcategory_id')
    subsubcategory_name = request.data.get('subsubcategory_title')
    existing_subcategory = None 
    try:
        existing_subcategory = SubCategory.objects.get(id = subcategory_id)
    except:
        pass

    if existing_subcategory is not None:
        existing_subsubcategory = None
        try:
            existing_subsubcategory = SubSubCategory.objects.get(query_title = subsubcategory_name.lower(), subcategory_id = existing_subcategory.id)
        except:
            pass

        if existing_subsubcategory is None:

            save_data = SubSubCategory(
                subcategory = existing_subcategory,
                query_title = subsubcategory_name.lower(),
                title = subsubcategory_name,
                full_title = f"{existing_subcategory.category.title}>{existing_subcategory.title}>{subsubcategory_name}"
            )
            save_data.save()
            return Response({'status_code':200,'message':"SubSubCategory Saved"})
        else:
            return Response({'status_code':400,'message':"SubSubCategory Under The Same Subcategory Already Exist"})
        
    else:
        return Response({'status_code':400,'message':"Subcategory Does Not Exist"})
    
    
@api_view(['GET'])
def get_category_data(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)

    if admin_status == True:
        categories = Category.objects.all()
        serializer = CategoryDashboardSerializer(categories,many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'Access Denied'})

@api_view(['POST'])
def delete_category_data(request):
    id = request.data.get('id')
    category = Category.objects.get(id = id)
    category.delete()
    return Response({'status_code':200,'message':'Category Deleted'})

@api_view(['POST'])
def delete_category_data_multiple(request):
    category_ids = request.data.get('category_ids')
    categories = Category.objects.filter(id__in = category_ids)
    categories.delete()
    return Response({'status_code':200,'message':'Categories Deleted'})


@api_view(['GET'])
def get_subcategory_data(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)

    if admin_status == True:
        subcategories = SubCategory.objects.all()
        serializer = SubCategoryDashboardSerializer(subcategories,many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'Access Denied'})

@api_view(['POST'])
def delete_subcategory_data(request):
    id = request.data.get('id')
    subcategory = SubCategory.objects.get(id = id)
    subcategory.delete()
    return Response({'status_code':200,'message':'SubCategory Deleted'})

@api_view(['POST'])
def delete_subcategory_data_multiple(request):
    subcategory_ids = request.data.get('subcategory_ids')
    subcategories = SubCategory.objects.filter(id__in = subcategory_ids)
    subcategories.delete()
    return Response({'status_code':200,'message':'SubCategories Deleted'})


@api_view(['GET'])
def get_subsubcategory_data(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)

    if admin_status == True:
        subsubcategories = SubSubCategory.objects.all()
        serializer = SubSubCategoryDashboardSerializer(subsubcategories,many=True)
        return Response(serializer.data)
    else:
        return Response({'messsage':'Access Denied'})


@api_view(['POST'])
def delete_subsubcategory_data(request):
    id = request.data.get('id')
    subsubcategory = SubSubCategory.objects.get(id = id)
    subsubcategory.delete()
    return Response({'status_code':200,'message':'SubSubCategory Deleted'})

@api_view(['POST'])
def delete_subsubcategory_data_multiple(request):
    subsubcategory_ids = request.data.get('subsubcategory_ids')
    subsubcategories = SubSubCategory.objects.filter(id__in = subsubcategory_ids)
    subsubcategories.delete()
    return Response({'status_code':200,'message':'SubSubCategories Deleted'})
    


