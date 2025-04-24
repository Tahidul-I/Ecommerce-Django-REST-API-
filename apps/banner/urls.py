from django.urls import path
from . import views

urlpatterns = [
    path('v1/get-banner-carousel/',views.get_banner_carousel,name="get_banner_carousel"),
    path('v1/save-banner/',views.save_banner,name="save_banner"),
    path('v1/delete-banner/',views.delete_banner,name="delete_banner"),
    path('v1/get-active-banner-carousel/',views.get_active_banner_carousel,name="get_active_banner_carousel"),
    path('v1/change-banner-status/',views.change_banner_status,name="change_banner_status"),
    path('v1/get-title-banner-one/',views.get_title_banner_one,name="get_title_banner_one"),
    path('v1/get-active-title-banner-one/',views.get_active_title_banner_one,name="get_active_title_banner_one"),
    path('v1/get-title-banner-two/',views.get_title_banner_two,name="get_title_banner_two"),
    path('v1/get-active-title-banner-two/',views.get_active_title_banner_two,name="get_active_title_banner_two"),
    path('v1/delete-selected-banner/',views.delete_selected_banner,name="delete_selected_banner"),
]
