from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from ..product.models import ProductVariation,Product
from ..authentication.models import CustomUser
from ..authentication.utils import get_use_id,get_user
from .serilizers import *
# Create your views here.

@api_view(['POST'])
def add_to_cart(request):
    access_token = request.COOKIES.get('access_token')
    user = get_user(access_token)
    product_variation_id = int(request.data.get('product_variation_id'))
    quantity = int(request.data.get('quantity'))
    product_variation = ProductVariation.objects.get(id = product_variation_id)
    cart_product = None
    try:
        cart_product = Cart.objects.get(user = user,product_variation = product_variation)
    except:
        pass

    if cart_product is None:

        if product_variation.stock_quantity >= quantity:
            cart_data = Cart(
                user = user,
                product_variation = product_variation,
                title = product_variation.product.title,
                dimension = product_variation.dimension,
                new_price = product_variation.new_price,
                old_price = product_variation.old_price,
                image_url = product_variation.product.image_url,
                quantity = quantity
            )
            cart_data.save()
            return Response({'status_code':200,'message':'Product added to cart'})
        else:
            return Response({'status_code':203,'message':'Product out of stock.You can submit your email so that we can contact you when the product will be available'})
    
    else:

        if  cart_product.quantity + quantity <= product_variation.stock_quantity :
            cart_product.quantity = cart_product.quantity + quantity
            cart_product.save()
            return Response({'status_code':200,'message':'Product quantity Updated'})
        else:
            return Response({'status_code':202,'message':'Product out of stock'})
        



@api_view(['POST'])
def delete_cart_item(request):
    access_token = request.COOKIES.get('access_token')
    user_id = get_use_id(access_token)
    user = CustomUser.objects.get(id = user_id)
    product_variation_id = int(request.data.get('product_variation_id'))
    product_variation = ProductVariation.objects.get(id = product_variation_id)
    cart_product = Cart.objects.get(user = user,product_variation = product_variation)
    cart_product.delete()
    return Response({'status_code':200,'message':'Cart item deleted'})


@api_view(['POST'])
def update_cart(request):
    quantity = int(request.data.get('quantity'))
    product_variation_id = int(request.data.get('product_variation_id'))
    product_variation = ProductVariation.objects.get(id = product_variation_id)
    if product_variation.stock_quantity >= quantity:
        access_token = request.COOKIES.get('access_token')
        user_id = get_use_id(access_token)
        user = CustomUser.objects.get(id = user_id)
        cart_product = Cart.objects.get(user = user,product_variation = product_variation)
        cart_product.quantity = quantity
        cart_product.save()
        return Response({'status_code':200,'message':'Cart Updated'})
    else:
        return Response({'status_code':202,'message':'Poduct out of stock'})


@api_view(['GET'])
def get_cart_items(request):
    access_token = request.COOKIES.get('access_token')
    user_id = get_use_id(access_token)
    user = CustomUser.objects.get(id = user_id)
    cart_items = Cart.objects.filter(user = user)
    serilizer = CartProductSerializer(cart_items, many=True)
    return Response(serilizer.data)



@api_view(['POST'])
def add_product_to_wishlist(request):
    access_token = request.COOKIES.get('access_token')
    user_id = get_use_id(access_token)
    user = CustomUser.objects.get(id = user_id)
    product_id = request.data.get('product_id')
    product = Product.objects.get(id = product_id )
    wishlist_obj = None
    try:
        wishlist_obj = Wishlist.objects.get(user=user,product=product)
    except:
        pass
    if wishlist_obj is None:
        data = Wishlist(
            user = user,
            product = product
        )
        data.save()
        return Response({'status_code':200,'message':'Added to wishlist'})
    
    else:
        return Response({'status_code':200,'message':'Already added to wishlist'})
    

@api_view(['POST'])
def remove_wishlist_product(request):
    access_token = request.COOKIES.get('access_token')
    user_id = get_use_id(access_token)
    user = CustomUser.objects.get(id = user_id)
    product_id = request.data.get('product_id')
    product = Product.objects.get(id = product_id )
    wishlist_obj = Wishlist.objects.get(user=user,product=product)
    wishlist_obj.delete()
    return Response({'status_code':200,'message':'wishlist item removed'})

@api_view(['GET'])
def get_wishlist_products(request):
    access_token = request.COOKIES.get('access_token')
    user_id = get_use_id(access_token)
    user = CustomUser.objects.get(id = user_id)
    wishlist_objs = Wishlist.objects.filter(user=user)
    product_ids = list(wishlist_objs.values_list('product_id', flat=True))
    products = Product.objects.filter(id__in = product_ids)
    serializer = WishlistProductSeriizer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def save_local_storage_cart_data(request):
    access_token = request.COOKIES.get('access_token')
    user = get_user(access_token)
    cart_items = None
    try:
        cart_items = Cart.objects.filter(user = user)
    except:
        pass

    if len(cart_items) ==0:
        for item in request.data:
            Cart(
                user = user,
                product_variation_id = int(item['id']),
                title =  item['title'],
                dimension = item['dimension'],
                new_price = item['new_price'],
                old_price = item['old_price'],
                image_url = item['image_url'],
                quantity = item['quantity']
            ).save()            
        return Response({'status_code':200})
    else:
        return Response({'status_code':201})
    

@api_view(['POST'])
def fbt_add_to_cart(request):
    access_token = request.COOKIES.get('access_token')
    user = get_user(access_token)
    product_variation_ids = request.data.get('product_variation_ids')
    message = "Added To Cart"
    for poduct_variation_id in product_variation_ids:
        product_variation = ProductVariation.objects.get(id = poduct_variation_id)
        cart_product = None
        try:
            cart_product = Cart.objects.get(user = user,product_variation = product_variation)
        except:
            pass
        if cart_product is None:

            if product_variation.stock_quantity >= 1:
                cart_data = Cart(
                    user = user,
                    product_variation = product_variation,
                    title = product_variation.product.title,
                    dimension = product_variation.dimension,
                    new_price = product_variation.new_price,
                    old_price = product_variation.old_price,
                    image_url = product_variation.product.image_url,
                    quantity = 1
                )
                cart_data.save()
            else:
                message = "Product out of stock"
        
        else:

            if  cart_product.quantity + 1 <= product_variation.stock_quantity :
                cart_product.quantity = cart_product.quantity + 1
                cart_product.save()
                message = "Cart Updated"   
            else:
                message = "Product out of stock"

    return Response({'status_code':200,'message':message})