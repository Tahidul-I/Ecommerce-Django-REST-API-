from django.shortcuts import render,redirect
from datetime import datetime,timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import *
from .models import *
from ..authentication.utils import get_use_id,admin_user_checker,get_user
from ..authentication.models import CustomUser
import random
from ..cart.models import Cart
from ..payment_gateway.utils import payment_gateway
from rest_framework.decorators import api_view
from django.db.models import Q
from django.db.models import Sum, F
from django.db.models import Prefetch
from ..core.models import ShippingCost
import math
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

class OrderCreateAPIView(APIView):
    def post(self, request):
        serializer = SaveBillingDetailSerializer(data=request.data.get('billing_details'))
        if serializer.is_valid():
            order = self.perform_create(serializer, request)
            user = self.get_user_from_request(request)
            product_variation_id = None
            try:
                product_variation_id = request.data.get('billing_details')['product_variation_id']
            except:
                pass
            if product_variation_id is not None:
                product_variation = ProductVariation.objects.get(id=product_variation_id)
                OrderItems(order=order,product=product_variation,quantity=1,price=product_variation.new_price,dimension=product_variation.dimension).save()
                self.update_subscription_order_totals(order,product_variation.new_price)
                shipping_detail = SaveShippingDetailSerializer(data=request.data.get('billing_details'), context = {'order':order})
                if shipping_detail.is_valid():
                    shipping_detail.save()
                indicator = 'subscription'
                payment_url = self.initiate_payment(order,indicator)
                return Response({'status_code':200,'payment_url':payment_url})

            else:
                user_cart_items = Cart.objects.filter(user=user)
                ids = user_cart_items.values_list('product_variation_id',flat=True)
                product_variations = ProductVariation.objects.filter(id__in = ids)
                product_variations.update(last_bought=datetime.now().isoformat())
                order_items = [
                OrderItems(order=order, product=item.product_variation, quantity=item.quantity,price = item.new_price,dimension=item.dimension)
                for item in user_cart_items
                ]
                OrderItems.objects.bulk_create(order_items)
                self.update_order_totals(order)
                AbandonCart(order=order).save()
                shipping_details = request.data.get('shipping_details',None)
                if shipping_details is not None:
                    shipping_detail = SaveShippingDetailSerializer(data=request.data.get('shipping_details'), context = {'order':order})
                    if shipping_detail.is_valid():
                        shipping_detail.save()
                else:
                    shipping_detail = SaveShippingDetailSerializer(data=request.data.get('billing_details'), context = {'order':order})
                    if shipping_detail.is_valid():
                        shipping_detail.save()
                if request.data.get('billing_details')['payment_mode'] == 'cash on delivery':
                    payment_url = f'https://meherunbeauty.abroadportals.com/checkout/order_complete?transaction_id={int(order.tracking_no)}'
                    return Response({'status_code':200,'payment_url':payment_url})
                    # return Response({'status_code':201,'message':order.tracking_no})
                
                if request.data.get('billing_details')['payment_mode'] == 'online':
                    indicator = 'checkout'
                    payment_url = self.initiate_payment(order,indicator)
                    return Response({'status_code':200,'payment_url':payment_url})
        return Response(serializer.errors)
    
    def perform_create(self, serializer, request):

        user = self.get_user_from_request(request)
        track_no = str(random.randint(111111,999999))

        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = str(random.randint(111111,999999))

        order = serializer.save(user=user,tracking_no = track_no)
        return order
    
    def get_user_from_request(self, request):
        access_token = request.COOKIES.get('access_token')
        user_id = get_use_id(access_token)
        return CustomUser.objects.get(id=user_id)
    
    def update_subscription_order_totals(self, order,price):
        sub_total = price
        order.sub_total = sub_total
        order.total_amount =math.floor((sub_total + order.shipping_cost) - (sub_total*order.discount_percentage/100))
        order.save()
    
    def update_order_totals(self, order):
        sub_total = order.order_item.aggregate(
            subtotal=Sum(F('quantity') * F('price'))
        )['subtotal']
        order.sub_total = sub_total
        order.total_amount = math.floor((sub_total + order.shipping_cost) - (sub_total*order.discount_percentage/100))
        order.save()
    
    def initiate_payment(self, order,indicator):
        payment_url = payment_gateway(order,indicator)
        return payment_url

@api_view(['GET'])
def get_orders(request):
    access_token = request.COOKIES.get('access_token')
    user = get_user(access_token)
    order = Order.objects.filter(user=user,subscription=False,order_abandoned=False).order_by('-created_at')
    order_serilizer = OrderDetailSerializer(order, many=True)
    total_orders = order.count()
    active_orders = order.filter(~Q(order_status ='Received') & ~Q(order_status='Canceled')).count()
    received_orders = order.filter(order_status = 'Received').count()
    canceled_orders = order.filter(order_status='Canceled').count()
    return Response({'orders':order_serilizer.data,'stats':{'total_orders':total_orders,'active_orders':active_orders,'received_orders':received_orders,'canceled_orders':canceled_orders}})

@api_view(['GET'])
def get_order_items(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id = order_id)
    shipping_detail = ShippingDetails.objects.get(order = order)
    order_items = OrderItems.objects.filter(order = order)
    order_serializer = OrderSerializer(order, many=False)
    shipping_detail_serializer = ShippingDetailSerializer(shipping_detail, many=False)
    order_items_serializer = OrderItemSerializer(order_items, many=True)
    return Response({
        'billing_details':order_serializer.data,
        'shipping_details':shipping_detail_serializer.data,
        'order_items':order_items_serializer.data,
        'total_amount':order.total_amount
    })


@api_view(['GET'])
def order_complete(request):
    access_token = None
    track_no = int(request.GET.get('track_no'))
    try:
        access_token = request.COOKIES.get('access_token')
    except:
        pass
    if access_token is not None:
        user = get_user(access_token)
        cart_items = Cart.objects.filter(user = user)
        cart_items.delete()

    order = Order.objects.get(tracking_no = track_no)
    order_items = OrderItems.objects.filter(order = order)
    serializer = OrderItemSerializer(order_items, many=True)
    order.payment_status = True
    order.order_abandoned = False
    order.save()
    try:
        AbandonCart.objects.get(order=order).delete()
    except:
        pass
    for item in order_items:
        product_variation = ProductVariation.objects.get(id = item.product.id)
        product_variation.stock_quantity = product_variation.stock_quantity - item.quantity
        product_variation.save()

    context = {
        'order': order,
        'order_items':order_items
    }
    html_content = render_to_string('order_confirmation_2.html', context)
    text_content = strip_tags(html_content)
    subject="!!! Thank you for the order !!!"
    sender = settings.EMAIL_HOST_USER
    receiver = [order.email, ]
    # send email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        sender,
        receiver,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return Response({'order_items':serializer.data})


@api_view(['GET'])
def complete_product_subscription(request):
    track_no = int(request.GET.get('track_no'))
    order = Order.objects.get(tracking_no = track_no)
    order.order_abandoned = False
    order.save()
    subscribed_product = OrderItems.objects.filter(order = order).first()
    serializer = OrderItemSerializer(subscribed_product,many=False)
    return Response({'subscription_item':serializer.data})


@api_view(['POST'])
def get_product_subscription_verification(request):
    access_token = request.COOKIES.get('access_token')
    user = get_user(access_token)
    product_variation_id = request.data.get('product_variation_id')
    product_variation = ProductVariation.objects.get(id = product_variation_id)
    has_subscription = False
    try:
        order_items = OrderItems.objects.filter(product=product_variation)
        has_subscription = order_items.filter(order__user=user,order__subscription=True).exists()
    except:
        pass
    if has_subscription == True:
        return Response({'status_code':201})
    else:
        return Response({'status_code':200})


@api_view(['POST'])
def change_order_status(request):
    order_id = request.data.get('order_id')
    order_status = request.data.get('order_status')
    order_obj = Order.objects.get(id = order_id)
    order_obj.order_status = order_status
    order_obj.save()
    return Response({'status_code':200,'message':'Order Status Changed'})

@api_view(['GET'])
def get_all_orders(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        has_more = True
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        search_key = request.GET.get('searchQuery', None)
        sort_key = request.GET.get('SortQuery', None)
        orders = Order.objects.filter(order_abandoned=False,subscription=False).order_by('-created_at')
        if start_date!='' and end_date!='':
            end_date = (datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1))
            orders = orders.filter(created_at__range=[start_date, end_date])

        if sort_key!='':
            orders = orders.filter(order_status__iexact=sort_key.capitalize()).order_by('-created_at')
        if search_key!='':
            search_words = search_key.split()
            query = Q()
            for word in search_words:
                query |= Q(name__icontains=word) | Q(phone__icontains=word) | Q(tracking_no__icontains=word)
            orders = orders.filter(query)

        if orders.count() <= page*limit:
            has_more = False
        orders = orders[0:page*limit]
        serilizer = OrderDashboardSerializer(orders,many=True)
        return Response({'orders':serilizer.data,'has_more':has_more})
    else:
         return Response({'message':'Access Denied'})

@api_view(['GET'])
def get_order_details(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id = order_id)
        shipping_detail = ShippingDetails.objects.get(order = order)
        order_items = OrderItems.objects.filter(order = order)
        order_serializer = OrderSerializer(order, many=False)
        shipping_detail_serializer = ShippingDetailSerializer(shipping_detail, many=False)
        order_items_serializer = OrderItemSerializer(order_items, many=True)
        return Response({
            'billing_details':order_serializer.data,
            'shipping_details':shipping_detail_serializer.data,
            'order_items':order_items_serializer.data,
            'total_amount':order.total_amount
        })
    
    else:
        return Response({"message":"Access Denied"})


@api_view(['POST'])
def delete_order(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        order_id = request.data.get('order_id')
        Order.objects.get(id = order_id).delete()
        return Response({'status_code':200,'message':'Order Deleted'})
    else:
        return Response({'message':'Access Denied'})
    
@api_view(['POST'])
def delete_multiple_order(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        order_ids = request.data.get('ids')
        Order.objects.filter(id__in = order_ids).delete()
        return Response({'status_code':200,'message':'Order Deleted'})
    else:
        return Response({'message':'Access Denied'})


@api_view(['GET'])
def get_all_abandon_carts(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        has_more = True
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        abandon_orders = AbandonCart.objects.all().order_by('-created_at')
        if start_date!='' and end_date!='':
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            end_date = end_date + timedelta(days=1)
            abandon_orders = abandon_orders.filter(created_at__range=[start_date, end_date])
        
        if abandon_orders.count() <= page*limit:
            has_more = False
        abandon_orders = abandon_orders[0:page*limit]
        serializer = AbandonCartSerializer(abandon_orders, many=True)
        return Response({'orders':serializer.data,'has_more':has_more})
    else:
        return Response({'message':'Access Denied'})

@api_view(['GET'])
def get_abandon_cart_details(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        abandon_cart_id = request.GET.get('abandon_cart_id')
        abandon_cart = AbandonCart.objects.get(id =abandon_cart_id )
        order = Order.objects.get(id = abandon_cart.order.id)
        shipping_detail = ShippingDetails.objects.get(order = order)
        order_items = OrderItems.objects.filter(order = order)
        order_serializer = OrderSerializer(order, many=False)
        shipping_detail_serializer = ShippingDetailSerializer(shipping_detail, many=False)
        order_items_serializer = OrderItemSerializer(order_items, many=True)
        return Response({
            'billing_details':order_serializer.data,
            'shipping_details':shipping_detail_serializer.data,
            'order_items':order_items_serializer.data,
            'total_amount':order.total_amount
        })
    else:
        return Response({'message':'Access Denied'})
    
@api_view(['POST'])
def delete_abandon_cart(request):
    abandon_cart_id = request.data.get('abandon_cart_id')
    abandon_cart = AbandonCart.objects.get(id = abandon_cart_id )
    Order.objects.get(id =abandon_cart.order.id ).delete()
    return Response({'status_code':200,'message':'Deleted Successfully'})
    
@api_view(['POST'])
def coupon_code_verify(request):
    code = request.data.get('coupon_code')
    try:
        coupon_obj = CouponCode.objects.get(code = code,is_active=True)
        return Response({'status_code':200,'discount_percentage':coupon_obj.discount_percentage})
    except:
        return Response({'status_code':201,'message':'Invalid Coupon'})
    
@api_view(['POST'])
def save_coupon_code(request):
    coupon_code = request.data.get('coupon_code')
    discount_percentage = float(request.data.get('discount_percentage'))
    try:
        CouponCode(code=coupon_code,discount_percentage=discount_percentage).save()
        return Response({'status_code':200,'message':'Coupon Saved'})
    except:
        return Response({'status_code':200,'message':'Coupon Already Exist'})
    
@api_view(['GET'])
def get_coupons(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        coupons = CouponCode.objects.all()
        serializer = CouponCodeSerializer(coupons,many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'Access Denied'})

@api_view(['POST'])
def change_coupon_active_status(request):
    coupon_id = request.data.get('coupon_id')
    status = request.data.get('status')
    coupon = CouponCode.objects.get(id = coupon_id)
    coupon.is_active = status
    coupon.save()
    return Response({'status_code':200,'message':'Status Changed'})


@api_view(['POST'])
def delete_coupon(request):
    coupon_id = request.data.get('coupon_id')
    CouponCode.objects.get(id = coupon_id).delete()
    return Response({'status_code':200,'message':'Coupon Deleted'})


@api_view(['POST'])
def delete_multiple_coupon(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        coupon_ids = request.data.get('ids')
        CouponCode.objects.filter(id__in = coupon_ids).delete()
        return Response({'status_code':200,'message':'Coupon Deleted'})
    else:
        return Response({'message':'Access Denied'})

@api_view(['POST'])
def update_coupon(request):
    coupon_id = request.data.get('coupon_id')
    coupon_code = request.data.get('coupon_code')
    discount_percentage = request.data.get('discount_percentage')
    coupon = CouponCode.objects.get(id = coupon_id)
    coupon.code = coupon_code
    coupon.discount_percentage = discount_percentage
    coupon.save()
    return Response({'status_code':200,'message':'Updated Sccessfully'})


@api_view(['POST'])
def save_store_pickup_location(request):
    address = request.data.get('address')
    branch_name = request.data.get('branch_name')
    StorePickupLocations(address=address,branch_name=branch_name).save()
    return Response({'status_code':200,'message':'Saved Successfully'})

@api_view(['POST'])
def update_store_pickup_location(request):
    store_id = int(request.data.get('id'))
    address = request.data.get('address')
    branch_name = request.data.get('branch_name')
    obj = StorePickupLocations.objects.get(id = store_id)
    obj.address = address
    obj.branch_name = branch_name
    obj.save()
    return Response({'status_code':200,'message':'Updated Successfully'})
    
@api_view(['POST'])
def delete_store_pickup_location(request):
    id = request.data.get('id')
    obj = StorePickupLocations.objects.filter(id = id)
    obj.delete()
    return Response({'status_code':200,'message':'Deleted Successfully'})

@api_view(['POST'])
def delete_multiple_store_pickup_location(request):
    ids = request.data.get('ids')
    obj = StorePickupLocations.objects.filter(id__in = ids)
    obj.delete()
    return Response({'status_code':200,'message':'Deleted Successfully'})

@api_view(['GET'])
def get_store_pickup_locations(request):
    locations = StorePickupLocations.objects.all()
    shipping_cost = ShippingCost.objects.all().first()
    location_serializer = LocationSerializer(locations, many=True)
    shipping_cost_serializer = ShippingCostSerializer(shipping_cost,many=False)
    return Response({'store_pickup_locations':location_serializer.data,'shipping_cost':shipping_cost_serializer.data})


@api_view(['GET'])
def get_product_subscriptions(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        has_more = True
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        subscribed_products = Order.objects.filter(subscription=True).prefetch_related(
            Prefetch('order_item', queryset=OrderItems.objects.select_related('product'))
        ).order_by('-created_at')

        if start_date!='' and end_date!='':
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            end_date = end_date + timedelta(days=1)
            subscribed_products = subscribed_products.filter(next_due_date__range=[start_date, end_date])
        if subscribed_products.count() <= page*limit:
            has_more = False
        
        serializer = SubcribedProductSerializer(subscribed_products[0:page*limit],many=True)
        return Response({'items':serializer.data,'has_more':has_more})
    else:
        return Response({'message':'Access Denied'})
    

@api_view(['POST'])
def update_subscription_due_date(request):
    order_id = request.data.get('order_id')
    subscription = Order.objects.get(id=order_id,subscription=True)
    subscription.update_next_due_date()

    return Response({
        'status_code':200,
        'message': 'Next due date updated successfully',
    })

@api_view(['POST'])
def delete_selected_abandoned_cart(request):
    ids = request.data.get('ids')
    AbandonCart.objects.filter(id__in = ids).delete()
    return Response({'status_code':200,'message':'Deleted Successfully'})


class AnonymousOrderCreateAPIView(APIView):
    def post(self, request):
        serializer = SaveBillingDetailSerializer(data=request.data.get('billing_details'))
        if serializer.is_valid():
            order = self.perform_create(serializer)
            cart_items = request.data.get('cart_items')
            ids = [item['id'] for item in cart_items]
            product_variations = ProductVariation.objects.filter(id__in = ids)
            product_variations.update(last_bought=datetime.now().isoformat())
            order_items = [
            OrderItems(order=order, product_id=item['id'], quantity=item['quantity'],dimension =item['dimension'],price=item['new_price'])
            for item in cart_items
            ]
            OrderItems.objects.bulk_create(order_items)
            self.update_order_totals(order)
            AbandonCart(order=order).save()
            shipping_details = request.data.get('shipping_details',None)
            if shipping_details is not None:
                shipping_detail = SaveShippingDetailSerializer(data=request.data.get('shipping_details'), context = {'order':order})
                if shipping_detail.is_valid():
                    shipping_detail.save()
            else:
                shipping_detail = SaveShippingDetailSerializer(data=request.data.get('billing_details'), context = {'order':order})
                if shipping_detail.is_valid():
                    shipping_detail.save()
            if request.data.get('billing_details')['payment_mode'] == 'cash on delivery':
                payment_url = f'https://meherunbeauty.abroadportals.com/checkout/order_complete?transaction_id={int(order.tracking_no)}'
                return Response({'status_code':200,'payment_url':payment_url})
                # return Response({'status_code':201,'message':order.tracking_no})
            
            if request.data.get('billing_details')['payment_mode'] == 'online':
                indicator = 'checkout'
                payment_url = self.initiate_payment(order,indicator)
                return Response({'status_code':200,'payment_url':payment_url})
        return Response(serializer.errors)
    
    def perform_create(self, serializer):

        track_no = str(random.randint(111111,999999))

        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = str(random.randint(111111,999999))

        order = serializer.save(tracking_no = track_no)
        return order
    
    def update_order_totals(self, order):
        sub_total = order.order_item.aggregate(
            subtotal=Sum(F('quantity') * F('price'))
        )['subtotal']
        order.sub_total = sub_total
        order.total_amount = math.floor((sub_total + order.shipping_cost) - (sub_total*order.discount_percentage/100))
        order.save()
    
    def initiate_payment(self, order,indicator):
        payment_url = payment_gateway(order,indicator)
        return payment_url

@api_view(['GET'])
def get_user_product_subscription(request):
    access_token = request.COOKIES.get('access_token')
    user = get_user(access_token)
    subscribed_products = Order.objects.filter(user=user,subscription=True).prefetch_related(
            Prefetch('order_item', queryset=OrderItems.objects.select_related('product'))
        ).order_by('-created_at')
    serializer = SubcribedProductSerializer(subscribed_products,many=True)
    return Response({'items':serializer.data})