from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('generate-invoice/',views.generate_invoice,name="generate_invoice"),
    path('generate-payslip/',views.generate_payslip,name="generate_payslip"),
    path('api/v1/get-shipping-cost/',views.get_shipping_cost,name="get_shipping_cost"),
    path('api/v1/edit-shipping-cost/',views.edit_shipping_cost,name="edit_shipping_cost"),
]
