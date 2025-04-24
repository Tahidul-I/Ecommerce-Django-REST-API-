from django.urls import path
from . import views

urlpatterns = [
    path('v1/all-category-data/',views.all_category_data,name="all_category_data"),
    path('v1/save-category-data/',views.save_category_data,name="save_category_data"),
    path('v1/save-subcategory-data/',views.save_subcategory_data,name="save_subcategory_data"),
    path('v1/save-subsubcategory-data/',views.save_subsubcategory_data,name="save_subsubcategory_data"),
    path('v1/get-category-data/',views.get_category_data,name="get_category_data"),
    path('v1/delete-category-data/',views.delete_category_data,name="delete_category_data"),
    path('v1/delete-category-data-multiple/',views.delete_category_data_multiple,name="delete_category_data_multiple"),
    path('v1/get-subcategory-data/',views.get_subcategory_data,name="get_subcategory_data"),
    path('v1/delete-subcategory-data/',views.delete_subcategory_data,name="delete_subcategory_data"),
    path('v1/delete-subcategory-data-multiple/',views.delete_subcategory_data_multiple,name="delete_subcategory_data_multiple"),
    path('v1/get-subsubcategory-data/',views.get_subsubcategory_data,name="get_subsubcategory_data"),
    path('v1/delete-subsubcategory-data/',views.delete_subsubcategory_data,name="delete_subsubcategory_data"),
    path('v1/delete-subsubcategory-data-multiple/',views.delete_subsubcategory_data_multiple,name="delete_subsubcategory_data_multiple"),
    
]
