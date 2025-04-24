from django.urls import path
from . import views

urlpatterns = [
    path('v1/update-cart/',views.update_cart,name="update_cart"),
    path('v1/delete-cart-item/',views.delete_cart_item,name="delete_cart_item"),
    path('v1/add-to-cart/',views.add_to_cart,name="add_to_cart"),
    path('v1/get-cart-items/',views.get_cart_items,name="get_cart_items"),
    path('v1/add-product-to-wishlist/',views.add_product_to_wishlist,name="add_product_to_wishlist"),
    path('v1/remove-wishlist-product/',views.remove_wishlist_product,name="remove_wishlist_product"),
    path('v1/get-wishlist-products/',views.get_wishlist_products,name="get_wishlist_products"),
    path('v1/save-local-storage-cart-data/',views.save_local_storage_cart_data,name="save_local_storage_cart_data"),
    path('v1/fbt-add-to-cart/',views.fbt_add_to_cart,name="fbt_add_to_cart"),
]
