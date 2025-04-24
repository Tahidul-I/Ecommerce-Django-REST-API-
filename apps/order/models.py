from django.db import models
from ..authentication.models import CustomUser
from ..product.models import ProductVariation
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class Order(models.Model):

    ORDER_STATUS = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Received', 'Received'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    ]

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100,verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=14,verbose_name="Contact Number")
    country = models.CharField(max_length=100,verbose_name="Country Name")
    city = models.CharField(max_length=100,verbose_name="City")
    address =models.TextField(verbose_name="Address")
    order_note = models.TextField(verbose_name="Order Note",blank=True,null=True)
    sub_total = models.FloatField(blank=True,null=True)
    discount_percentage = models.FloatField(default=0)
    shipping_cost = models.FloatField(default=0)
    total_amount = models.FloatField(verbose_name="Total Payment",blank=True,null=True)
    payment_mode = models.CharField(max_length=250)
    tracking_no = models.CharField(max_length=250,verbose_name = "Tracking ID")
    order_status = models.CharField(max_length=250,default="Pending",choices = ORDER_STATUS,verbose_name="Order Status")
    payment_status = models.BooleanField(default=False,verbose_name="Payment Status")
    order_abandoned =  models.BooleanField(default=True,verbose_name="Cart Abandonment")
    subscription_type = models.CharField(max_length=100,blank=True,null=True)
    subscription = models.BooleanField(default=False,verbose_name="Subscribed")
    created_at = models.DateTimeField(auto_now_add = True,verbose_name="Creating Date")
    updated_at = models.DateTimeField(auto_now = True,verbose_name= "Updating Date")
    next_due_date = models.DateField(auto_now_add=True)
    def update_next_due_date(self):
        if self.subscription_type == "Weekly":
            self.next_due_date += timedelta(weeks=1)
        elif self.subscription_type == "Monthly":
            self.next_due_date += timedelta(days=30)  # Simplified month calculation
        elif self.subscription_type == "Every 2 Months":
            self.next_due_date += timedelta(days=60)
        elif self.subscription_type == "Every 3 Months":
            self.next_due_date += timedelta(days=90)
        elif self.subscription_type == "Every 4 Months":
            self.next_due_date += timedelta(days=120)
        self.save()
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    product = models.ForeignKey(ProductVariation,on_delete=models.CASCADE,related_name="ordered_product")
    quantity = models.IntegerField()
    price = models.FloatField()
    dimension = models.CharField(max_length = 100)
    def __str__(self):
        return f"{self.order.id}-{self.order.tracking_no}"
    
    
class ShippingDetails(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name="order_shipping_details")
    country = models.CharField(max_length=100,verbose_name="Country Name")
    city = models.CharField(max_length=100,verbose_name="City")
    address =models.TextField(verbose_name="Address")

    def __str__(self):
        return f"Order ID - {self.order.tracking_no}"
    

class CouponCode(models.Model):
    code = models.CharField(max_length=100,unique=True)
    discount_percentage = models.FloatField()
    is_active = models.BooleanField(default=False)
    
class AbandonCart(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name="abandon_order")
    created_at =  models.DateTimeField(auto_now_add=True,verbose_name="Creating Date")
    updated_at =  models.DateTimeField(auto_now=True,verbose_name="Update Date")


class StorePickupLocations(models.Model):
    branch_name = models.CharField(max_length=100)
    address = models.TextField()

    