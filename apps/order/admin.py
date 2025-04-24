from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(ShippingDetails)
admin.site.register(AbandonCart)
admin.site.register(CouponCode)
admin.site.register(StorePickupLocations)