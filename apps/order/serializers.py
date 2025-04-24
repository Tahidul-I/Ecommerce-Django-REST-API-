from rest_framework import serializers
from .models import *
from ..core.models import ShippingCost
class SaveBillingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['name','email','phone','country','address','order_note','city','payment_mode','discount_percentage','subscription','subscription_type','shipping_cost','order_note']

    def create(self, validated_data):
    # Create and return the Order instance
        return Order.objects.create(**validated_data)


class SaveShippingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDetails
        fields = ['country','address','city',]

    def create(self, validated_data):
        order_obj = self.context.get('order')
        shipping_obj = ShippingDetails.objects.create(order=order_obj,**validated_data)
        return shipping_obj


class OrderDetailSerializer(serializers.ModelSerializer):
    
    order_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Order
        fields = ['order_id','tracking_no','created_at','order_status','payment_mode','total_amount']

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.product.id', read_only=True)
    title = serializers.CharField(source='product.product.title', read_only=True)
    image_url = serializers.URLField(source='product.product.image_url', read_only=True)
    dimension = serializers.CharField(source='product.dimension', read_only=True)
    class Meta:
        model = OrderItems
        fields = ['product_id','title','image_url','quantity','dimension','price']


class OrderDashboardSerializer(serializers.ModelSerializer):
    billing_address = serializers.CharField(source='address', read_only=True)
    order_id = serializers.IntegerField(source='id', read_only=True)
    shipping_address = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id','name','email','billing_address','shipping_address','phone','total_amount','order_status','tracking_no','order_date']

    def get_shipping_address(self,obj):

        return obj.order_shipping_details.address
    
    def get_order_date(self, obj):
        return obj.created_at


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['name','email','address','country','city','phone','order_status','tracking_no','sub_total','discount_percentage','total_amount','shipping_cost','order_note','created_at']

class ShippingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDetails
        fields = ['country','city','address']


class AbandonCartSerializer(serializers.ModelSerializer):
    order = OrderDashboardSerializer()
    class Meta:
        model = AbandonCart
        fields = ['id','order','created_at']

class CouponCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponCode
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePickupLocations
        fields = '__all__'


class SubcribedProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='order_item.product.product.title', read_only=True)
    image_url = serializers.URLField(source='order_item.product.product.image_url', read_only=True)
    dimension = serializers.CharField(source='order_item.dimension', read_only=True)
    order_id = serializers.IntegerField(source='id', read_only=True)
    price = serializers.FloatField(source='order_item.price', read_only=True)
    order_date = serializers.DateTimeField(source='created_at', read_only=True)
    tracking_id = serializers.CharField(source='tracking_no', read_only=True)
    class Meta:
        model = Order
        fields = ['order_id','title','image_url','price','dimension','name','address','order_date','phone','tracking_id','order_status','email','subscription_type','next_due_date']
    
    def to_representation(self, instance):
       
        representation = super().to_representation(instance)
        order_item = instance.order_item.first()  # Assuming one order item per order
        if order_item:
            representation['title'] = order_item.product.product.title
            representation['image_url'] = order_item.product.product.image_url
            representation['dimension'] = order_item.dimension
            representation['price'] = order_item.price
        return representation

class ShippingCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCost
        fields = ['outside_dhaka','inside_dhaka']

