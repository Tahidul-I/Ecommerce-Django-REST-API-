from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from ..authentication.utils import admin_user_checker
from ..banner.models import AllBanner
from ..review.models import Review
from django.db.models import Avg
from django.db.models import Q, OuterRef, Subquery, Min
from django.utils import timezone
from datetime import timedelta

@api_view(['POST'])
def save_category_product_data(request):

    product_data = request.data
    category_id = int(product_data['category_id'])
    title = product_data['title']
    description = product_data['description']
    image_url = product_data['image_url']
    old_price = float(product_data['old_price'])
    new_price = float(product_data['new_price'])
    brand_id = product_data['brand_id']
    product_object = Product(
        category_id = category_id,
        brand_id = brand_id,
        title = title,
        description = description,
        image_url = image_url,
        old_price = old_price,
        new_price = new_price
    )

    product_object.save()

    for variation in product_data['product_variation']:
        product_variation_object = ProductVariation(
            product = product_object,
            brand_id = brand_id,
            dimension = variation['dimension'],
            old_price = float(variation['old_price']),
            new_price = float(variation['new_price']),
            is_deal = variation['is_deal'],
            is_signature = variation['is_signature'],
            is_banner_product = variation['is_banner_product'],
            is_new = variation['is_new'],
            is_top = variation['is_top'],
            stock_quantity = variation['stock_quantity'],
            brand_feature = variation['brand_feature'],
            expires_at = variation['expires_at'],
        )
        product_variation_object.save()

    for image_url in product_data['product_images']:
        image_url_object = ProductImages(
            product = product_object,
            image_url = image_url
        )

        image_url_object.save()
    
    return Response({'status_code':200,'message':'Product Data Saved'})




@api_view(['POST'])
def save_subcategory_product_data(request):

    product_data = request.data
    subcategory_id = int(product_data['category_id'])
    subcategory = SubCategory.objects.get(id = subcategory_id)
    title = product_data['title']
    description = product_data['description']
    image_url = product_data['image_url']
    old_price = float(product_data['old_price'])
    new_price = float(product_data['new_price'])
    brand_id = int(product_data['brand_id'])
    product_object = Product(
        category = subcategory.category,
        subcategory_id = subcategory_id,
        brand_id = brand_id,
        title = title,
        description = description,
        image_url = image_url,
        old_price = old_price,
        new_price = new_price
    )

    product_object.save()

    for variation in product_data['product_variation']:
        product_variation_object = ProductVariation(
            product = product_object,
            brand_id = brand_id,
            dimension = variation['dimension'],
            old_price = float(variation['old_price']),
            new_price = float(variation['new_price']),
            is_deal = variation['is_deal'],
            is_signature = variation['is_signature'],
            is_banner_product = variation['is_banner_product'],
            is_new = variation['is_new'],
            is_top = variation['is_top'],
            stock_quantity = variation['stock_quantity'],
            brand_feature = variation['brand_feature'],
            expires_at = variation['expires_at'],
        )
        product_variation_object.save()

    for image_url in product_data['product_images']:
        image_url_object = ProductImages(
            product = product_object,
            image_url = image_url
        )

        image_url_object.save()
    
    return Response({'status_code':200,'message':'Product Data Saved'})


@api_view(['POST'])
def save_subsubcategory_product_data(request):

    product_data = request.data
    subsubcategory_id = int(product_data['category_id'])
    subsubcategory = SubSubCategory.objects.get(id = subsubcategory_id)
    title = product_data['title']
    description = product_data['description']
    image_url = product_data['image_url']
    old_price = float(product_data['old_price'])
    new_price = float(product_data['new_price'])
    brand_id = int(product_data['brand_id'])
    product_object = Product(
        category = subsubcategory.subcategory.category,
        subcategory = subsubcategory.subcategory,
        subsubcategory_id = subsubcategory_id,
        brand_id = brand_id,
        title = title,
        description = description,
        image_url = image_url,
        old_price = old_price,
        new_price = new_price
    )

    product_object.save()

    for variation in product_data['product_variation']:
        product_variation_object = ProductVariation(
            product = product_object,
            brand_id = brand_id,
            dimension = variation['dimension'],
            old_price = float(variation['old_price']),
            new_price = float(variation['new_price']),
            is_deal = variation['is_deal'],
            is_signature = variation['is_signature'],
            is_banner_product = variation['is_banner_product'],
            is_new = variation['is_new'],
            is_top = variation['is_top'],
            stock_quantity = variation['stock_quantity'],
            brand_feature = variation['brand_feature'],
            expires_at = variation['expires_at'],
        )
        product_variation_object.save()

    for image_url in product_data['product_images']:
        image_url_object = ProductImages(
            product = product_object,
            image_url = image_url
        )

        image_url_object.save()
    
    return Response({'status_code':200,'message':'Product Data Saved'})



@api_view(['GET']) #For Forntend Data Fetch
def get_our_best_deals(request):
    best_deals = OurBestDeals.objects.filter(is_active = True)
    serializer = OurBestDealsSerializer(best_deals,many=True)
    return Response(serializer.data)

@api_view(['GET']) 
def get_our_best_deals_dashboard(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        best_deals = OurBestDeals.objects.all()
        serializer = OurBestDealsSerializer(best_deals,many=True)
        return Response(serializer.data)
    else:
        return Response({'status_code':400,'message':'Access Denied'})



@api_view(['GET']) #For Frontend Data Fetch
def get_our_best_deal_products(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    has_more = True
    deal = None
    best_deal_id = int(request.GET.get('best_deal_id'))
    try:
        deal = OurBestDeals.objects.get(id = best_deal_id)
    except OurBestDeals.DoesNotExist:
        return Response({"error": "OurBestDeals not found"})

    products = deal.products.all()
    if products.count() < page*limit:
        has_more = False
    products = products[0:page*limit]
    serializer = FeatureSectionProductVariationDataFetchSerializer(products, many=True)
    
    return Response({'best_deal_products':serializer.data,'has_more':has_more})


@api_view(['GET'])
def get_our_best_deal_products_dashboard(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        deal = None
        best_deal_id = int(request.GET.get('best_deal_id'))
        try:
            deal = OurBestDeals.objects.get(id = best_deal_id)
        except OurBestDeals.DoesNotExist:
            return Response({"error": "OurBestDeals not found"})

        products = deal.products.all()
        serializer = ProductVariationDataFetchSerializer(products, many=True)

        return Response(serializer.data)
    else:
        return Response({'status_code':200,'message':'Access Denied'})


@api_view(['POST'])
def save_our_best_deals_products(request):
    deal_id = request.data.get('id',None)
    title = request.data.get('title')
    product_variation_ids = request.data.get('product_variation_ids')
    banner_url = request.data.get('banner_url')
    
    # Validate input
    if not title or not product_variation_ids:
        return Response({'status_code': 400, 'message': 'Title and product variation IDs are required'})

    # Retrieve product variations
    product_variations = ProductVariation.objects.filter(id__in=product_variation_ids)
    print(product_variations.count())

    if deal_id is not None:
        # Try to retrieve the existing OurBestDeals object
        try:
            deal = OurBestDeals.objects.get(id=deal_id)
            # Update title and banner URL if provided
            if banner_url is not None:
                deal.banner_url = banner_url
            
            deal.title = title       
            deal.save()
            deal.products.set(product_variations)
            return Response({'status_code': 200, 'message': 'Updated Successfully'})
        except:
            return Response({'status_code': 404, 'message': 'OurBestDeals object not found'})
    else:
        # Create a new OurBestDeals object
        deal = OurBestDeals.objects.create(title=title, banner_url=banner_url)
        deal.products.set(product_variations)
        return Response({'status_code': 200, 'message': 'Uploaded Successfully'})

    # Set the product variations
    

    


@api_view(['GET'])
def get_best_deal_product_recommendations(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)

    if admin_status == True: 
        product_varitions = ProductVariation.objects.filter(is_deal = True)
        serializer = ProductRecommendation(product_varitions,many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'Access Denied'})

@api_view(['GET']) #For Frontend Data Fetch
def get_product_details(request):
    #Get The product
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id = product_id)
    #GEt average product reviews
    reviews =  Review.objects.filter(product_id=product_id)
    average_rating =reviews.aggregate(average_rating=Avg('review_star'))['average_rating']
    if average_rating is None:
        average_rating = 0
    #Get Product Images
    product_images = ProductImages.objects.filter(product = product)
    #Get Product Recommendations
    recommended_product_obj = RecommendedProduct.objects.filter(main_product = product )
    recommended_product_ids = list(recommended_product_obj.values_list('recommended_product_id', flat=True))
    recommended_products = Product.objects.filter(id__in = recommended_product_ids)
    #Get Frequently Brought Tofetehr Product
    fbt_product_obj = FrequentlyBroughtTogether.objects.get(main_product = product)
    fbt_product = ProductVariation.objects.get(id = fbt_product_obj.frequently_brought_product.id)
    #Get Product Variations
    product_variations = ProductVariation.objects.filter(product = product)
    #Get You May Also Like Products
    you_may_also_like_product_ids = list(YouMayAlsoLike.objects.all().values_list('product_id', flat=True))
    you_may_also_like_products = ProductVariation.objects.filter(id__in = you_may_also_like_product_ids)
    # Serilize All The Data
    product_serilizer = ProductInfoSerializer(product, many=False)
    product_variation_serializer = ProductVariationDataFetchSerializer(product_variations, many=True)
    recommended_product_serializer = RecommendedProductSerilizer(recommended_products, many=True)
    product_image_serializer = ProductImagesDataFetchSerializer(product_images, many=True)
    fbt_product_serializer = FrequentlyBroughtProductSerilizer(fbt_product,context={'product':product},many=False)
    you_may_also_like_product_serializer = YouMayAlsoLikeProductSerializer(you_may_also_like_products, many=True)
    return Response({'status_code':200,
                     'product_info':product_serilizer.data,
                     'product_variations':product_variation_serializer.data,
                     'product_recommendations':recommended_product_serializer.data,
                     'product_images':product_image_serializer.data,
                     'fbt_product':fbt_product_serializer.data,
                     'average_rating':average_rating,
                     'total_reviews': reviews.count(),
                     'you_may_like_products':you_may_also_like_product_serializer.data
                     })




@api_view(['POST']) #For Frontend Data Fetch
def get_all_product_variations_from_product_variation_id(request):
    product_variation_id  = request.data.get('product_variation_id')
    product_variation = ProductVariation.objects.get(id = product_variation_id)
    product = Product.objects.get(id = product_variation.product.id)
    serializer = ProductDetailsSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['GET'])  #For Forntend Data Fetch
def get_new_arrival_products(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    has_more = True
    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',500000)
    brand_ids = request.GET.get('brand_ids',None)
    sort_key = request.GET.get('SortQuery',None)
    products = ProductVariation.objects.filter(Q(new_price__gte=min_price) & Q(new_price__lte=max_price) & Q(is_new=True))
    if brand_ids is not None:
        try:
            brand_ids = list(map(int, brand_ids.split(',')))
            products = products.filter(brand_id__in = brand_ids)
        except:
            pass
    if sort_key is not None:
        if sort_key == 'HighToLow':
            products = products.order_by('-new_price')
        if sort_key == 'LowToHigh':
            products = products.order_by('new_price')
    if products.count() < page*limit:
        has_more = False
    
    products = products[0:page*limit]
    serializer = FeatureSectionProductVariationDataFetchSerializer(products,many=True)
    return Response({'new_arrival_products':serializer.data,'has_more':has_more})


@api_view(['GET']) #For Forntend Data Fetch
def get_top_products(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    has_more = True
    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',500000)
    brand_ids = request.GET.get('brand_ids',None)
    sort_key = request.GET.get('SortQuery',None)
    products = ProductVariation.objects.filter(Q(new_price__gte=min_price) & Q(new_price__lte=max_price) & Q(is_top=True))
    if brand_ids is not None:
        try:
            brand_ids = list(map(int, brand_ids.split(',')))
            products = products.filter(brand_id__in = brand_ids)
        except:
            pass
    if sort_key is not None:
        if sort_key == 'HighToLow':
            products = products.order_by('-new_price')
        if sort_key == 'LowToHigh':
            products = products.order_by('new_price')
    
    if products.count() < page*limit:
        has_more = False
    products = products[0:page*limit]
    serializer = FeatureSectionProductVariationDataFetchSerializer(products,many=True)
    return Response({"top_products":serializer.data,'has_more':has_more})

@api_view(['GET'])
def get_meherun_signature_dashboard(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        signature_objects = MeherunSignature.objects.all()
        serializer = MeherunSignatureSerializer(signature_objects,many=True)
        return Response(serializer.data)
    else:
        return Response({'status_code':200,'message':'Access Denied'})


@api_view(['GET']) #For Forntend Data Fetch
def get_meherun_signature(request):
    signature_objects = MeherunSignature.objects.filter(is_active = True)
    serializer = MeherunSignatureSerializer(signature_objects,many=True)
    return Response(serializer.data)

@api_view(['GET']) #For Forntend Data Fetch
def get_meherun_signature_products(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    has_more = True
    signature_products = None
    signature_obj_id = int(request.GET.get('signature_obj_id'))
    try:
        signature_products = MeherunSignature.objects.get(id = signature_obj_id)
    except MeherunSignature.DoesNotExist:
        return Response({"error": "MeherunSignature not found"})

    products = signature_products.products.all()
    if products.count() < page*limit:
        has_more = False

    products = products[0:page*limit]
    serializer = FeatureSectionProductVariationDataFetchSerializer(products, many=True)
    return Response({'signature_products':serializer.data,'has_more':has_more})


@api_view(['POST'])
def save_meherun_signature_products(request):
    signature_id = request.data.get('id',None)
    title = request.data.get('title')
    product_variation_ids = request.data.get('product_variation_ids')
    banner_url = request.data.get('banner_url',None)
    
    # Validate input
    if not title or not product_variation_ids:
        return Response({'status_code': 400, 'message': 'Title and product variation IDs are required'})

    # Retrieve product variations
    product_variations = ProductVariation.objects.filter(id__in=product_variation_ids)

    if signature_id is not None:
        # Try to retrieve the existing MeherunSignature object
        try:
            signature_object = MeherunSignature.objects.get(id=signature_id)
            if banner_url:
                signature_object.banner_url = banner_url 
            # Update title and banner URL if provided
            signature_object.title = title
            signature_object.save()
            signature_object.products.set(product_variations)
            return Response({'status_code': 200, 'message': 'Updated Successfully'})
        except:
            return Response({'status_code': 404, 'message': 'MeherunSignature object not found'})
    else:
        # Create a new MeherunSignature object
        signature_object = MeherunSignature.objects.create(title=title, banner_url=banner_url)
        signature_object.products.set(product_variations)
        return Response({'status_code': 200, 'message': 'Uploaded Successfully'})

@api_view(['GET'])
def get_meherun_signature_product_recommendations(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)

    if admin_status == True:
        product_varitions = ProductVariation.objects.filter(is_signature = True)
        serializer = ProductRecommendation(product_varitions,many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'Access Denied'})


@api_view(['POST'])
def save_banner_product(request):
    banner_carousel_id = request.data.get('banner_carousel_id',None)
    product_variation_ids = request.data.get('product_variation_ids')
    banner_product_object = None
    try:
        banner_product_object = BannerProducts.objects.get(banner_obj_id = banner_carousel_id)
    except:
        pass
    if banner_product_object is None:
        banner_object = AllBanner.objects.get(id = banner_carousel_id)
        banner_object.is_navigate = True
        banner_object.save()
        banner_product_object = BannerProducts.objects.create(title=banner_object.title,banner_obj = banner_object)
        product_variations = ProductVariation.objects.filter(id__in = product_variation_ids)
        banner_product_object.products.set(product_variations)
        return Response({'status_code':200,'message':'Uploaded Successfully'})
    else:
        return Response({'status_code':400,'message':'Duplicate Error For Carousel Banner'})

@api_view(['POST'])
def update_banner_product(request):
    product_related_banner_id = request.data.get('product_related_banner_id')
    banner_carousel_id = request.data.get('banner_carousel_id')
    banner_carousel_object = AllBanner.objects.get(id = banner_carousel_id)
    product_variation_ids = request.data.get('product_variation_ids')
    product_variations = ProductVariation.objects.filter(id__in = product_variation_ids)
    product_banner_obj  = BannerProducts.objects.get(id = product_related_banner_id)
    product_banner_obj.title = banner_carousel_object.title
    product_banner_obj.banner_obj = banner_carousel_object
    product_banner_obj.save()
    product_banner_obj.products.set(product_variations)
    return Response({'status_code':200,'message':'Updated Succcessfully'})

@api_view(['GET'])
def get_banner_products_dashboard(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        banner_products = None
        banner_id = request.GET.get('banner_id')
        try:
            banner_products = BannerProducts.objects.get(banner_obj_id = banner_id)
        except MeherunSignature.DoesNotExist:
            return Response({"error": "Banner Products not found"})

        products = banner_products.products.all()
        serializer = ProductVariationDataFetchSerializer(products, many=True)
        banner_carousel_obj = AllBanner.objects.get(id = banner_id)
        return Response({'banner_obj':{'banner_id':banner_carousel_obj.id,'title':banner_carousel_obj.title},'products':serializer.data})
    else:
        return Response({'message':'Access Denied'})


@api_view(['GET'])
def get_banner_main_objects(request):
    banner_carousel_main_objects = BannerProducts.objects.all()
    serializer = BannerProductsSerializer(banner_carousel_main_objects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_banner_recommendation(request):
    banners = AllBanner.objects.filter(is_active = True)
    serializer = BannerRecommendationSerializer(banners,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_banner_carousel_product_recommendations(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)

    if admin_status == True:
        product_varitions = ProductVariation.objects.filter(is_banner_product = True)
        serializer = ProductRecommendation(product_varitions,many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'Access Denied'})

    
@api_view(['GET'])
def get_all_products(request):
    products = Product.objects.all()
    serializer = ProductDataFetchSerializer(products,many=True)
    return Response({'status_code':200,'products':serializer.data})



@api_view(['POST'])
def update_product(request):
    product_id = request.data.get('product_id')
    brand_id = request.data.get('brand_id')
    product = Product.objects.get(id = product_id)
    category_id = request.data.get('category_id',None)
    subcategory_id = request.data.get('subcategory_id',None)
    subsubcategory_id = request.data.get('subsubcategory_id',None)
    title = request.data.get('title')
    new_price = request.data.get('new_price')
    old_price = request.data.get('old_price')
    description = request.data.get('description')
    image_url = request.data.get('image_url')

    product_variations = ProductVariation.objects.filter(product = product)
    for item in product_variations:
        item.brand_id = brand_id
        item.save()
    if category_id is not None:
        product_obj = Product(
            id = product.id,
            category_id = category_id,
            brand_id = brand_id,
            title = title,
            description = description,
            new_price = new_price,
            old_price = old_price,
            image_url = image_url
        )
        product_obj.save()
        return Response({'status_code':200,'message':'Updated Successfully'})
    if subcategory_id is not None:
        subcategory = SubCategory.objects.get(id = subcategory_id)
        product_obj = Product(
            id = product.id,
            category = subcategory.category,
            subcategory_id = subcategory_id,
            brand_id = brand_id,
            title = title,
            description = description,
            new_price = new_price,
            old_price = old_price,
            image_url = image_url
        )
        product_obj.save()
        return Response({'status_code':200,'message':'Updated Successfully'})
    
    if subsubcategory_id is not None:
        subsubcategory = SubSubCategory.objects.get(id = subsubcategory_id)
        product_obj = Product(
            id = product.id,
            category = subsubcategory.subcategory.category,
            subcategory = subsubcategory.subcategory,
            subsubcategory_id = subsubcategory_id,
            brand_id = brand_id,
            title = title,
            description = description,
            new_price = new_price,
            old_price = old_price,
            image_url = image_url
        )
        product_obj.save()
        return Response({'status_code':200,'message':'Updated Successfully'})



@api_view(['POST'])
def update_product_variation(request):
    product_id = request.data.get('product_id')
    product = Product.objects.get(id=product_id)
    delete_selected_variation_ids = request.data.get('delete_selected_variation_ids',[])
    product_variation_data = request.data.get('product_variation')

    for variation in product_variation_data:
        variation_id = variation.get('id',None)

        if variation_id is not None:
            # Update existing ProductVariation
            variation_obj = ProductVariation.objects.get(id=variation_id)
        else:
            # Create a new ProductVariation
            variation_obj = ProductVariation(product=product, brand=product.brand)

        # Set or update fields
        variation_obj.dimension = variation['dimension']
        variation_obj.old_price = float(variation['old_price'])
        variation_obj.new_price = float(variation['new_price'])
        variation_obj.is_deal = variation['is_deal']
        variation_obj.is_signature = variation['is_signature']
        variation_obj.is_banner_product = variation['is_banner_product']
        variation_obj.is_new = variation['is_new']
        variation_obj.is_top = variation['is_top']
        variation_obj.stock_quantity = variation['stock_quantity']
        variation_obj.brand_feature = variation['brand_feature']
        variation_obj.expires_at = variation['expires_at']

        # Save the object
        variation_obj.save()
    ProductVariation.objects.filter(id__in = delete_selected_variation_ids).delete()

    return Response({"status_code":200,'message': "Product variations updated successfully"})


@api_view(['GET'])
def get_product_variation_for_dashboard(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        product_id = request.GET.get('product_id')
        product_variations = ProductVariation.objects.filter(product_id = product_id)
        serilaizer = ProductVariationDataFetchSerializer(product_variations,many=True)
        return Response({'product_id':int(product_id),'product_variations':serilaizer.data})

@api_view(['GET'])
def get_product_images_for_dashboard(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        product_id = request.GET.get('product_id')
        product_images = ProductImages.objects.filter(product_id = product_id)
        serilaizer = ProductImagesDataFetchSerializer(product_images,many=True)
        return Response({'product_id':int(product_id),'product_images':serilaizer.data})


@api_view(['POST'])
def update_product_images(request):
    product_id = request.data.get('product_id')
    product = Product.objects.get(id = int(product_id))
    sent_product_images = request.data.get('product_images')
    product_images = ProductImages.objects.filter(product_id = product_id)
    product_images.delete()
    for image in sent_product_images:
        image_obj = ProductImages(
            product = product,
            image_url = image
        )
        image_obj.save()
    
    return Response({'status_code':200,'message':'Updated Successfully'})

@api_view(['GET'])
def get_products(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        has_more = True 
        sort_key = request.GET.get('SortQuery',None)
        search_key = request.GET.get('searchQuery',None)
        products = Product.objects.all().order_by('title')
        if sort_key == 'brand':
            products = products.filter(brand__title__icontains = search_key)
        if sort_key == 'title':
            products = products.filter(title__icontains = search_key)
        if sort_key == 'category':
            products = products.filter(category__title__icontains = search_key)
        
        if products.count() < page*limit:
            has_more = False
        products = products[0:page*limit]
        serializer = ProductDataFetchSerializer(products,many=True)
        return Response({'status_code':200,'products':serializer.data,'has_more':has_more})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['POST'])
def delete_product(request):
    id = request.data.get('id')
    product = Product.objects.get(id = id)
    product.delete()
    return Response({'status_code':200,'message':'Product deleted'})

@api_view(['POST'])
def delete_multiple_product(request):
    product_ids = request.data.get('product_ids')
    products = Product.objects.filter(id__in = product_ids)
    products.delete()
    return Response({'status_code':200,'message':'Products deleted'})

@api_view(['POST'])
def delete_product_variation(request):
    id = request.data.get('id')
    product = ProductVariation.objects.get(id = id)
    product.delete()
    return Response({'status_code':200,'message':'Product variation deleted'})


@api_view(['POST'])
def delete_multiple_product_variation(request):
    product_variation_ids = request.data.get('product_variation_ids')
    product_variations = ProductVariation.objects.filter(id__in = product_variation_ids)
    product_variations.delete()
    return Response({'status_code':200,'message':'Product Variations deleted'})


@api_view(['POST'])
def change_best_deals_active_status(request):
    id = request.data.get('best_deal_id')
    active_status = request.data.get('is_active')
    best_deal_object = OurBestDeals.objects.get(id = id)
    best_deal_object.is_active = active_status
    best_deal_object.save()
    return Response({'status_code':200,'message':'Status Updated'})


@api_view(['POST'])
def change_meherun_signature_active_status(request):
    id = request.data.get('signature_id')
    active_status = request.data.get('is_active')
    signature_object = MeherunSignature.objects.get(id = id)
    signature_object.is_active = active_status
    signature_object.save()
    return Response({'status_code':200,'message':'Status Updated'})


@api_view(['POST'])
def change_banner_product_active_status(request):
    id = request.data.get('banner_product_object_id')
    active_status = request.data.get('is_active')
    banner_product_object = BannerProducts.objects.get(id = id)
    banner_product_object.is_active = active_status
    banner_product_object.save()
    return Response({'status_code':200,'message':'Status Updated'})


@api_view(['POST'])
def delete_best_deals_product(request):
    best_deal_id = request.data.get('id')
    best_deal_object = OurBestDeals.objects.get(id = best_deal_id)
    best_deal_object.delete()
    return Response({'status_code':200,'message':'Deleted'})

@api_view(['POST'])
def delete_meherun_signature_product(request):
    signature_id = request.data.get('id')
    signature_object = MeherunSignature.objects.get(id = signature_id)
    signature_object.delete()
    return Response({'status_code':200,'message':'Deleted'})

@api_view(['POST'])
def delete_banner_product(request):
    banner_id = request.data.get('id')
    banner_object = BannerProducts.objects.get(id = banner_id)
    banner = AllBanner.objects.get(id = banner_object.banner_obj_id)
    banner.is_navigate = False
    banner.save()
    banner_object.delete()
    return Response({'status_code':200,'message':'Deleted'})

@api_view(['POST'])
def save_recommended_product(request):
    main_product_id = request.data.get('main_product_id')
    recommended_product_ids = request.data.get('recommended_product_ids')
    recommended_product_objects_count = None
    try:
        recommended_product_objects_count = RecommendedProduct.objects.filter(main_product_id = main_product_id).count()
    except:
        pass
    if recommended_product_objects_count == 0:
        for product_id in recommended_product_ids:
            data = RecommendedProduct(
                main_product_id = main_product_id,
                recommended_product_id = product_id
            )
            data.save()

        return Response({'status_code':200,'message':'Product recommendations added'})
    else:
        return Response({'status_code':400,'message':'Process Failed. You May Edit'})


@api_view(['POST'])
def update_recommended_product(request):
    main_product_id = request.data.get('main_product_id')
    recommended_product_ids = request.data.get('recommended_product_ids')
    existing_recommended_products = RecommendedProduct.objects.filter(main_product_id = main_product_id)
    existing_recommended_products.delete()
    for product_id in recommended_product_ids:
        data = RecommendedProduct(
            main_product_id = main_product_id,
            recommended_product_id = product_id
        )
        data.save()

    return Response({'status_code':200,'message':'Product recommendations updated'})

@api_view(['GET'])
def get_recommendations_for_recommended_product_dashboard(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        product_id = request.GET.get('product_id',None)
        if product_id is not None:
            recommended_products = Product.objects.exclude(id = product_id).order_by('title')
            serializer = RecommendedProductSerilizer(recommended_products,many=True)
            return Response(serializer.data)
        else:
            return Response({'status_code':400,'message':'Request Parameter Missing'})
    
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['GET'])
def get_added_recommended_products(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        product_id = request.GET.get('product_id')
        recommended_products = RecommendedProduct.objects.filter(main_product_id = product_id)
        recommended_product_ids = list(recommended_products.values_list('recommended_product_id', flat=True))
        added_recommended_products = Product.objects.filter(id__in = recommended_product_ids)
        serilizer = RecommendedProductSerilizer(added_recommended_products,many=True)
        return Response({'product_id':int(product_id),'products':serilizer.data})
    else:
        return Response({'status_code':200,'message':'Access Denied}'})
    
@api_view(['POST'])
def save_frequently_brought_product(request):
    main_product_id = request.data.get('main_product_id')
    frequently_brought_product_id = request.data.get('frequently_brought_product_id')
    frequently_brought_product_obj = None
    try:
        frequently_brought_product_obj = FrequentlyBroughtTogether.objects.get(main_product_id = main_product_id)
    except:
        pass
    if frequently_brought_product_obj is None:
        data = FrequentlyBroughtTogether(
            main_product_id = main_product_id,
            frequently_brought_product_id = int(frequently_brought_product_id)
        )
        data.save()
        return Response({'status_code':200,'message':'Frequently Brought Together Product Added'})
    else:
        return Response({'status_code':400,'message':'Can Not Add Multiple Product'})
    

@api_view(['POST'])
def update_frequently_brought_product(request):
    main_product_id = request.data.get('main_product_id')
    frequently_brought_product_id = request.data.get('frequently_brought_product_id')
    frequently_brought_product_obj = None
    try:
        frequently_brought_product_obj = FrequentlyBroughtTogether.objects.get(main_product_id = main_product_id)
    except:
        pass
    if frequently_brought_product_obj is not None:
        frequently_brought_product_obj.frequently_brought_product_id = int(frequently_brought_product_id)
        frequently_brought_product_obj.save()
        return Response({'status_code':200,'message':'Updated Successfully'})
    else:
        return Response({'status_code':400,'message':'Edit not possbile'})
    
@api_view(['GET'])
def get_frequently_brought_product_for_dashboard(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        fbt_product = None
        main_product_id = request.GET.get('product_id')
        try:
            fbt_product = FrequentlyBroughtTogether.objects.get(main_product_id = int(main_product_id))
        except:
            pass
        if fbt_product is not None:
            product = ProductVariation.objects.get(id = fbt_product.frequently_brought_product.id)
            return Response({'status_code':200,'main_product_id':int(main_product_id),'fbt_product_id':product.id,'title':product.product.title,'image_url':product.product.image_url,'price':product.new_price,'dimension':product.dimension})
        else:
            return Response({'status_code':400,'message':'Not Found. Add Product First'})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['GET'])
def get_product_recommendation_for_fbt(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id = product_id)
        variation_ids = list(product.product_variations.values_list('id', flat=True))
        product_variations = ProductVariation.objects.exclude(id__in = variation_ids).order_by('full_title')
        serializer = FBTRecommendation(product_variations, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_product_recommendation_for_you_may_also_like(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        existing_products = YouMayAlsoLike.objects.all()
        existing_product_ids = list(existing_products.values_list('product_id', flat=True))
        products = ProductVariation.objects.exclude(id__in = existing_product_ids).order_by('product__title')
        serializer = YouMayAlsoLikeSerializer(products,many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'Access Denied'})
    

@api_view(['POST'])
def save_you_may_also_like_products(request):
    product_ids = request.data.get('product_ids')
    for id in product_ids:
        existing_product = None
        try:
            existing_product = YouMayAlsoLike.objects.get(product_id = id)
        except:
            pass
        if existing_product is None:
            data = YouMayAlsoLike(product_id = id)
            data.save()
        else:
            pass
    return Response({'status_code':200,'message':'Uploaded'})


@api_view(['POST'])
def delete_you_may_also_like_product(request):
    product_id = int(request.data.get('product_id'))
    you_may_also_like_product = YouMayAlsoLike.objects.get(product_id = product_id)
    you_may_also_like_product.delete()
    return Response({'status_code':200,'message':'Removed Successfully'})
    
@api_view(['GET'])
def get_you_may_also_like_product(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        has_more = True
        existing_products = YouMayAlsoLike.objects.all()
        existing_product_ids = list(existing_products.values_list('product_id', flat=True))
        products = ProductVariation.objects.filter(id__in = existing_product_ids).order_by('product__title')
        serializer = GetYouMayAlsoLikeSerializer(products,many=True)
        if products.count() < page*limit:
            has_more = False

        products = products[0:page*limit]
        return Response({'products':serializer.data,'has_more':has_more})
    else:
        return Response({'message':'Access Denied'})
    


@api_view(['GET'])
def get_category_products(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    has_more = True
    category_id = request.GET.get('category_id')
    min_price_subquery = ProductVariation.objects.filter(
                product=OuterRef('product')
            ).values('product').annotate(
                min_price=Min('new_price')
            ).values('min_price')

    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',500000)
    brand_ids = request.GET.get('brand_ids',None)
    sort_key = request.GET.get('SortQuery',None)
    lowest_priced_variations = ProductVariation.objects.filter(
        Q(new_price__gte=min_price) & Q(new_price__lte=max_price) & Q(product__category_id=category_id),
                new_price=Subquery(min_price_subquery)
            ).select_related('product')
    if brand_ids is not None:
        try:
            brand_ids = list(map(int, brand_ids.split(',')))
            lowest_priced_variations = lowest_priced_variations.filter(brand_id__in = brand_ids)
        except:
            pass
    if sort_key is not None:
        if sort_key == 'HighToLow':
            lowest_priced_variations = lowest_priced_variations.order_by('-new_price')
        if sort_key == 'LowToHigh':
            lowest_priced_variations = lowest_priced_variations.order_by('new_price')
    if lowest_priced_variations.count() < page*limit:
        has_more = False
    lowest_priced_variations = lowest_priced_variations[0:page*limit]
    serializer = FeatureSectionProductVariationDataFetchSerializer(lowest_priced_variations, many=True)
    return Response({'category_products':serializer.data,'has_more':has_more})

@api_view(['GET'])
def get_subcategory_products(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    has_more = True
    subcategory_id = request.GET.get('category_id')
    min_price_subquery = ProductVariation.objects.filter(
                product=OuterRef('product')
            ).values('product').annotate(
                min_price=Min('new_price')
            ).values('min_price')

    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',500000)
    brand_ids = request.GET.get('brand_ids',None)
    sort_key = request.GET.get('SortQuery',None)
    lowest_priced_variations = ProductVariation.objects.filter(
        Q(new_price__gte=min_price) & Q(new_price__lte=max_price) & Q(product__subcategory_id=subcategory_id),
                new_price=Subquery(min_price_subquery)
            ).select_related('product')
    if brand_ids is not None:
        try:
            brand_ids = list(map(int, brand_ids.split(',')))
            lowest_priced_variations = lowest_priced_variations.filter(brand_id__in = brand_ids)
        except:
            pass
    if sort_key is not None:
        if sort_key == 'HighToLow':
            lowest_priced_variations = lowest_priced_variations.order_by('-new_price')
        if sort_key == 'LowToHigh':
            lowest_priced_variations = lowest_priced_variations.order_by('new_price')

    if lowest_priced_variations.count() < page*limit:
        has_more = False

    lowest_priced_variations = lowest_priced_variations[0:page*limit]
    serializer = FeatureSectionProductVariationDataFetchSerializer(lowest_priced_variations, many=True)
    return Response({'category_products':serializer.data,'has_more':has_more})

@api_view(['GET'])
def get_subsubcategory_products(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    has_more = True
    subsubcategory_id = request.GET.get('category_id')
    min_price_subquery = ProductVariation.objects.filter(
                product=OuterRef('product')
            ).values('product').annotate(
                min_price=Min('new_price')
            ).values('min_price')

    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',500000)
    brand_ids = request.GET.get('brand_ids',None)
    sort_key = request.GET.get('SortQuery',None)
    lowest_priced_variations = ProductVariation.objects.filter(
        Q(new_price__gte=min_price) & Q(new_price__lte=max_price) & Q(product__subsubcategory_id=subsubcategory_id),
                new_price=Subquery(min_price_subquery)
            ).select_related('product')
    if brand_ids is not None:
        try:
            brand_ids = list(map(int, brand_ids.split(',')))
            lowest_priced_variations = lowest_priced_variations.filter(brand_id__in = brand_ids)
        except:
            pass
    if sort_key is not None:
        if sort_key == 'HighToLow':
            lowest_priced_variations = lowest_priced_variations.order_by('-new_price')
        if sort_key == 'LowToHigh':
            lowest_priced_variations = lowest_priced_variations.order_by('new_price')

    if lowest_priced_variations.count() < page*limit:
        has_more = False
    lowest_priced_variations = lowest_priced_variations[0:page*limit]
    serializer = FeatureSectionProductVariationDataFetchSerializer(lowest_priced_variations, many=True)
    return Response({'category_products':serializer.data,'has_more':has_more})


@api_view(['POST'])
def delete_selected_product(request):
    product_ids = request.data.get('product_ids')
    Product.objects.filter(id__in = product_ids).delete()
    return Response({'status_code':200,'message':'Dleeted Successfully'})

@api_view(['POST'])
def delete_selected_you_may_also_like_product(request):
    product_ids = request.data.get('product_ids')
    YouMayAlsoLike.objects.filter(product_id__in = product_ids).delete()
    return Response({'status_code':200,'message':'Removed Successfully'})

@api_view(['POST'])
def delete_selected_best_deals(request):
    best_deal_ids = request.data.get('best_deal_ids')
    OurBestDeals.objects.filter(id__in = best_deal_ids).delete()
    return Response({'status_code':200,'message':'Removed Successfully'})

@api_view(['POST'])
def delete_selected_meherun_signature(request):
    signature_ids = request.data.get('signature_ids')
    MeherunSignature.objects.filter(id__in = signature_ids).delete()
    return Response({'status_code':200,'message':'Removed Successfully'})

@api_view(['POST'])
def delete_selected_banner_products(request):
    product_banner_ids = request.data.get('product_banner_ids') 
    product_banner_objs = BannerProducts.objects.filter(id__in = product_banner_ids)
    banner_ids = product_banner_objs.values_list('banner_obj_id')
    banner_objs = AllBanner.objects.filter(id__in = banner_ids)
    banner_objs.update(is_navigate = False)
    product_banner_objs.delete()
    return Response({'status_code':200,'message':'Removed Successfully'})

@api_view(['GET'])
def get_banner_products(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    has_more = True
    banner_products = None
    banner_id = request.GET.get('banner_id')
    try:
        banner_products = BannerProducts.objects.get(banner_obj_id = banner_id)
    except MeherunSignature.DoesNotExist:
        return Response({"error": "Banner Products not found"})

    products = banner_products.products.all()
    if products.count()< page*limit:
        has_more = False
    products = products[0:page*limit]
    serializer = FeatureSectionProductVariationDataFetchSerializer(products, many=True)
    return Response({'banner_products':serializer.data,'has_more':has_more})

@api_view(['GET'])
def product_sku(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        product_variations = ProductVariation.objects.all().select_related('product').order_by('product__title')
        sort_key = request.GET.get('SortQuery',None)
        search_key = request.GET.get('searchQuery',None)
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        has_more = True
        if sort_key == 'sku':
            product_variations = product_variations.filter(sku__icontains = search_key)
        if sort_key == 'title':
            product_variations = product_variations.filter(product__title__icontains = search_key)
        if sort_key == 'dimension':
            product_variations = product_variations.filter(dimension__icontains = search_key)
        if sort_key == 'brand':
            product_variations = product_variations.filter(brand__title__icontains = search_key)
        
        if product_variations.count() <=page*limit:
            has_more = False
        
        product_variations = product_variations[0:page*limit]
        serializer = SKUProductSerializer(product_variations,many=True)
        return Response({'products':serializer.data,'has_more':has_more})

@api_view(['GET'])
def expired_products(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        sort_key = request.GET.get('SortQuery',None)
        search_key = request.GET.get('searchQuery',None)
        expired_products = ProductVariation.objects.filter(expires_at__lt=timezone.now().date())
        if sort_key == 'sku':
            expired_products = expired_products.filter(sku__icontains = search_key)
        if sort_key == 'title':
            expired_products = expired_products.filter(product__title__icontains = search_key)
        if sort_key == 'dimension':
            expired_products = expired_products.filter(dimension__icontains = search_key)
        if sort_key == 'brand':
            expired_products = expired_products.filter(brand__title__icontains = search_key)
        serializer = SKUProductSerializer(expired_products, many=True)
        return Response(serializer.data)
    else:
        return Response({'Access Denied'})
    
@api_view(['GET'])
def about_to_expire_products(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        today = timezone.now().date()  # Get today's date
        future_date = today + timedelta(days=1)  # Calculate the date 2 months from today
        sort_key = request.GET.get('SortQuery',None)
        search_key = request.GET.get('searchQuery',None)
        # Filter products where expires_at is between today and the future date
        about_to_expire = ProductVariation.objects.filter(expires_at__gte=today, expires_at__lte=future_date)
        if sort_key == 'sku':
            about_to_expire = about_to_expire.filter(sku__icontains = search_key)
        if sort_key == 'title':
            about_to_expire = about_to_expire.filter(product__title__icontains = search_key)
        if sort_key == 'dimension':
            about_to_expire = about_to_expire.filter(dimension__icontains = search_key)
        if sort_key == 'brand':
            about_to_expire = about_to_expire.filter(brand__title__icontains = search_key)

        serializer = SKUProductSerializer(about_to_expire, many=True)
        return Response(serializer.data)
    else:
        return Response({'Access Denied'})