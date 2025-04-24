from django.urls import path
from . import views

urlpatterns = [
    path('v1/save-review/',views.save_review,name="save_review"),
    path('v1/get-reviews/',views.get_reviews,name="get_reviews"),
    path('v1/delete-review/',views.delete_review,name="delete_review"),
]
