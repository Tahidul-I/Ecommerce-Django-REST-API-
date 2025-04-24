from django.urls import path
from . import views

urlpatterns = [
    path('v1/top-selling-products/',views.top_selling_products,name="top_selling_products"),
    path('v1/monthly-product-revenue/',views.monthly_product_revenue,name="monthly_product_revenue"),
    path('v1/get-category-sales-data/',views.get_category_sales_data,name="get_category_sales_data"),
    path('v1/get-order-summary/',views.get_order_summary,name="get_order_summary"),
    path('v1/get-dead-stock-products/',views.get_dead_stock_products,name="get_dead_stock_products"),
    path('v1/get-subscribed-product-info/',views.get_subscribed_product_info,name="get_subscribed_product_info"),
    path('v1/get-low-level-stocks/',views.get_low_level_stocks,name="get_low_level_stocks"),
]
