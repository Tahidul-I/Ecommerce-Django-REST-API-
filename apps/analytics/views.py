from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum, F,Count
from ..order.models import OrderItems,Order
from ..product.models import ProductVariation
from django.utils import timezone
from datetime import timedelta
import pandas as pd
from django.db.models import Q
@api_view(['GET'])
def top_selling_products(request):
    # Aggregate total quantities sold per product variation and rename the field
    top_products = (OrderItems.objects
                    .values(sku=F('product__sku'))  # Renaming the field
                    .annotate(total_sold=Sum('quantity'))
                    .order_by('-total_sold')[:15])  # Limit to top 15 products

    # Prepare data for charting
    product_sku = [item['sku'] for item in top_products]
    quantities_sold = [item['total_sold'] for item in top_products]

    return Response({'product_sku':product_sku,'quantities_sold':quantities_sold})


@api_view(['GET'])
def monthly_product_revenue(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=45)  # Last 60 days for comparison

    # Query orders from the last 60 days
    orders = Order.objects.filter(created_at__date__gte=start_date,order_abandoned=False,subscription=False,order_status="Received")

    # Aggregate revenue by day
    data = orders.values('created_at__date').annotate(total_revenue=Sum('total_amount')).order_by('created_at__date')
    try:
        # Convert to a DataFrame for easier manipulation
        df = pd.DataFrame(list(data))

        # Fill missing dates with 0 revenue
        all_dates = pd.date_range(start=start_date, end=today)
        df = df.set_index('created_at__date').reindex(all_dates).fillna(0)
        df.index.name = 'Date'

        # Separate lists for dates and revenues
        dates = df.index.strftime('%Y-%m-%d').tolist()  # Convert index to string format for JSON
        revenues = df['total_revenue'].tolist()

        return Response({'dates': dates, 'revenues': revenues})
    except:
        return Response({'dates': [], 'revenues': []})

@api_view(['GET'])
def get_category_sales_data(request):
    orders =  Order.objects.filter(order_abandoned=False,order_status="Received")
    order_items = OrderItems.objects.filter(order__in=orders)
    category_sales = order_items.values('product__product__category__title') \
    .annotate(total_sales=Sum(F('price') * F('quantity'))) \
    .order_by('-total_sales')
    overall_sales = category_sales.aggregate(total=Sum('total_sales'))['total']
    # Convert to lists for labels and data
    categories = [item['product__product__category__title'] for item in category_sales]
    total_sales = [item['total_sales'] for item in category_sales]
    total_sales_percentage = [round((value * 100 / overall_sales), 2) for value in total_sales]

    return Response({'categories': categories, 'total_sales': total_sales,'total_sales_percentage':total_sales_percentage})

@api_view(['GET'])
def get_order_summary(request):
    total_orders = Order.objects.filter(order_abandoned=False,subscription=False)
    active_orders = total_orders.exclude(Q(order_status="Pending") | Q(order_status="Received") | Q(order_status="Canceled"))
    received_orders = total_orders.filter(order_status="Received")
    canceled_orders = total_orders.filter(order_status="Canceled")
    return Response({'total_orders':total_orders.count(),'active_orders':active_orders.count(),'received_orders':received_orders.count(),'canceled_orders':canceled_orders.count()})

@api_view(['GET'])
def get_dead_stock_products(request):
    six_months_ago = timezone.now() - timedelta(minutes=5)
    dead_stock = ProductVariation.objects.filter(last_bought__lt=six_months_ago).values('sku','stock_quantity').order_by('stock_quantity')
    product_sku = [item['sku'] for item in dead_stock]
    quantity = [item['stock_quantity'] for item in dead_stock]
    return Response({'product_sku':product_sku,'quantity':quantity})

@api_view(['GET'])
def get_subscribed_product_info(request):
    subscribed_products = OrderItems.objects.filter(order__subscription = True).select_related('order').values(sku=F('product__sku')).annotate(total=Count('product')).order_by('-total')
    quantity = [item['total'] for item in subscribed_products]
    sku = [item['sku'] for item in subscribed_products]
    return Response({'sku':sku,'quantity':quantity})

@api_view(['GET'])
def get_low_level_stocks(request):
    low_level_stocks = ProductVariation.objects.filter(stock_quantity__lte = 10).values('stock_quantity','sku').order_by('-stock_quantity')
    quantity = [item['stock_quantity'] for item in low_level_stocks]
    sku = [item['sku'] for item in low_level_stocks]
    return Response({'sku':sku,'quantity':quantity})