from django.urls import path
from . import views
urlpatterns = [
    path('v1/save-brand-details/',views.save_brand_details,name='save_brand_details'),
    path('v1/change-brand-active-status/',views.change_brand_active_status,name='change_brand_active_status'),
    path('v1/get-brand-data/',views.get_brand_data,name='get_brand_data'),
    path('v1/update-brand-data/',views.update_brand_data,name='update_brand_data'),
    path('v1/get-brand-list/',views.get_brand_list,name='get_brand_list'),
    path('v1/delete-brand/',views.delete_brand,name='delete_brand'),
    path('v1/get-brand-products-for-dashboard/',views.get_brand_products_for_dashboard,name='get_brand_products_for_dashboard'),
    path('v1/get-active-brands/',views.get_active_brands,name='get_active_brands'),
    path('v1/get-brand-products/',views.get_brand_products,name='get_brand_products'),
]
