from django.urls import path

from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('v1/auth/signup/', views.signup, name='signup'),
    path('v1/auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/admin-authentication/', views.admin_authentication, name='admin_authentication'),
    path('v1/auth/logout/', views.logout, name='logout'),
    path('v1/auth/admin-logout/', views.admin_logout, name='admin_logout'),
    path('v1/auth/get-user/', views.get_user, name='get_user'),
    path('v1/auth/get-admin-user/', views.get_admin_user, name='get_admin_user'),
    path('v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/send-otp/', views.send_otp, name='send_otp'), 
    path('v1/auth/otp-verification/', views.otp_verification, name='otp_verification'), 
    path('v1/auth/forget-password/', views.forget_password, name='forget_password'),
    path('v1/auth/change-password/', views.change_password, name='change_password'),
    path('v1/get-all-user/', views.get_all_user, name='get_all_user'),
    path('v1/change-user-active-status/', views.change_user_active_status, name='change_user_active_status'),
    path('v1/change-user-staff-status/', views.change_user_staff_status, name='change_user_staff_status'),
    path('v1/delete-user/', views.delete_user, name='delete_user'),
    path('v1/create-user/', views.create_user_from_dashboard, name='create_user_from_dashboard'),
    path('v1/google-authentication/', views.google_authentication, name='google_authentication'),
]

