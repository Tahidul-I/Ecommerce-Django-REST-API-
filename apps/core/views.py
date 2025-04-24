from django.shortcuts import render
from django.template.loader import render_to_string
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa
from ..order.models import Order
from django.utils import timezone
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ShippingCost
from ..authentication.utils import admin_user_checker
def home(request):
    
    return render(request,'home.html')

@api_view(['GET'])
def generate_invoice(request):
    order_id = request.GET.get('order_id')
    current_date = timezone.now()
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    
    html_string = render_to_string('invoice.html',{'order':order,'current_date':current_date})
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html_string.encode('UTF-8')), pdf)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    
    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice.pdf'
    return response

@api_view(['GET'])
def generate_payslip(request):
    order_id = request.GET.get('order_id')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    
    html_string = render_to_string('payslip.html',{'order':order})
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html_string.encode('UTF-8')), pdf)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    
    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=packing slip.pdf'
    return response

@api_view(['GET'])
def get_shipping_cost(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        shipping_cost = ShippingCost.objects.all().first()
        return Response({'status_code':200,'outside_dhaka':shipping_cost.outside_dhaka,'inside_dhaka':shipping_cost.inside_dhaka})
    else:
        return Response({'message':'Access denied'})

@api_view(['POST'])
def edit_shipping_cost(request):
    outside_dhaka = request.data.get('outside_dhaka')
    inside_dhaka = request.data.get('inside_dhaka')
    shipping_cost = ShippingCost.objects.all().first()
    shipping_cost.outside_dhaka = outside_dhaka
    shipping_cost.inside_dhaka = inside_dhaka
    shipping_cost.save()
    return Response({'status_code':200,'message':'Cost Updated'})

