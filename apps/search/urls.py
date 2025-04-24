from django.urls import path
from . import views
urlpatterns = [
    path('v1/search-filter/',views.search_filter,name="search_filter"),
    path('v1/search-product-sort-and-filter/',views.search_product_sort_and_filter,name="search_product_sort_and_filter"),
    path('v1/top-product-sort-and-filter/',views.top_product_sort_and_filter,name="top_product_sort_and_filter"),
    path('v1/new-arrival-product-sort-and-filter/',views.new_arrival_product_sort_and_filter,name="new_arrival_product_sort_and_filter"),
]
