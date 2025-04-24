from django.urls import path
from . import views

urlpatterns = [
    path('v1/payment-success/',views.payment_success,name="payment_success"),
]
