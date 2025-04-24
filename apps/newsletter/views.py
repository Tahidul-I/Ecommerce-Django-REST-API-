from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from ..authentication.utils import admin_user_checker
from .serializers import *
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ..product.models import ProductVariation
from django.utils import timezone
from django.conf import settings
# Create your views here.
@api_view(['POST'])
def news_letter_subscription(request):
    email = request.data.get('email')
    existing_data = None
    try:
        existing_data = NewsLetter.objects.get(email = email)
    except:
        pass

    if existing_data is None:
        NewsLetter(email = email).save()
        return Response({'status_code':200,'message':'Thanks for your subscription'})
    else:
        return Response({'status_code':202,'message':'You have already subscribed'})


@api_view(['POST'])
def email_for_product_arrival(request):
    product_variation_id = request.data.get('product_variation_id')
    email = request.data.get('email')
    existing_data = None
    try:
        existing_data = EmailForOutOfStockProducts.objects.get(product_variation_id = product_variation_id,email = email )
    except:
        pass

    if existing_data is None:
        EmailForOutOfStockProducts(product_variation_id = product_variation_id, email = email).save()
        return Response({'status_code':200,'message':'Email received. We will contact you as soon as the product arrives'})
    else:
        return Response({'status_code':202,'message':'We have already received your email for this product'})



@api_view(['GET'])
def get_all_product_arrival_request(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        has_more = True
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        distinct_products = EmailForOutOfStockProducts.objects.distinct('product_variation__product__title').order_by('product_variation__product__title')
        search_key = request.GET.get('searchQuery', None)
        if search_key is None:
            if distinct_products.count() < page*limit:
                has_more = False
            
            distinct_products = distinct_products[0:page*limit]
            serializer = EmailForOutOfStockProductsSerializer(distinct_products, many=True)
            return Response({'products':serializer.data,'has_more':has_more})
        else:
            distinct_products = distinct_products.filter(product_variation__product__title__icontains = search_key)
            if distinct_products.count() < page*limit:
                has_more = False
            distinct_products = distinct_products[0:page*limit]
            serializer = EmailForOutOfStockProductsSerializer(distinct_products, many=True)
            return Response({'products':serializer.data,'has_more':has_more})
    else:
        return Response({'message':'Access Denied'})

@api_view(['GET'])
def get_product_arrival_request_emails(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        has_more = True
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        search_key = request.GET.get('searchQuery', None)
        sort_key = request.GET.get('SortQuery', None)
        product_variation_id = int(request.GET.get('product_variation_id'))
        emails = EmailForOutOfStockProducts.objects.filter(product_variation_id = product_variation_id).values('id','email','status').order_by('email')
        if search_key is None and sort_key is None:
            if emails.count()< page*limit:
                has_more = False
            emails = emails[0:page*limit]
            serializer = ProductRequestEmailSerializer(emails, many=True)
            return Response({'emails':serializer.data,'has_more':has_more})
        else:
            if sort_key.lower() == 'pending':
                emails = emails.filter(status = 'Pending')
            if sort_key.lower() == 'sent':
                emails = emails.filter(status = 'Sent')
            if search_key is not None:
                emails = emails.filter(email__icontains = search_key)
            if emails.count()< page*limit:
                has_more = False
            emails = emails[0:page*limit]
            serializer = ProductRequestEmailSerializer(emails, many=True)
            return Response({'emails':serializer.data,'has_more':has_more})
    else:
        return Response({'message':'Access Denied'})


@api_view(['GET'])
def get_all_news_letter_email(request):
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        has_more = True
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        search_key = request.GET.get('searchQuery', None)
        all_emails = NewsLetter.objects.all().order_by('email')
        if search_key is None:
            if all_emails.count() < page*limit:
                has_more = False
            all_emails = all_emails[0:page*limit]
            serializer = NewsLetterSerializer(all_emails, many=True)
            return Response({'emails':serializer.data,'has_more':has_more})
        else:
            all_emails = all_emails.filter(email__icontains = search_key)
            if all_emails.count() < page*limit:
                has_more = False
            all_emails = all_emails[0:page*limit]
            serializer = NewsLetterSerializer(all_emails, many=True)
            return Response({'emails':serializer.data,'has_more':has_more})
    else:
        return Response({'message':'Access Denied'})


@api_view(['POST'])
def delete_news_letter_email(request):
    news_letter_obj_id = request.data.get('id')
    NewsLetter.objects.get(id = news_letter_obj_id).delete()
    return Response({'status_code':200,'message':'Deleted Successfully'})


@api_view(['POST'])
def contact_us(request):
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')
    phone = request.data.get('phone','Blank')
    ContactUs(name=name,email=email,message=message,phone=phone,created_at=timezone.now()).save()
    return Response({'status_code':200,'message':'Thanks for reaching out to us. We will reply you very soon'})

@api_view(['POST'])
def delete_selected_news_letter_email(request):
    ids = request.data.get('ids')
    NewsLetter.objects.filter(id__in = ids).delete()
    return Response({'status_code':200,'message':'Deleted Successfully'})


@api_view(['POST'])
def send_product_arrival_request_emails(request):
    product_variation_id = request.data.get('product_variation_id')
    product_variation = ProductVariation.objects.select_related('product').get(id=product_variation_id)
    emails = request.data.get('emails')
    queryset = EmailForOutOfStockProducts.objects.filter(email__in = emails)
    context = {
        'product': product_variation.product,
    }
    subject = '!!! Your Requested Product Has Arrived !!!'
    from_email = 'towhidulislamnishat@gmail.com'
    html_content = render_to_string('subscription_email.html', context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, bcc=emails)
    email.attach_alternative(html_content, "text/html")
    email.send()
    queryset.update(status="Sent")
    return Response({'status_code':200,'message':'Email Sent'})

@api_view(['POST'])
def delete_selected_product_request_emails(request):
    ids = request.data.get('ids')
    EmailForOutOfStockProducts.objects.filter(id__in = ids).delete()
    return Response({'status_code':200,'message':'Deleted Successfully'})

@api_view(['GET'])
def get_all_contact_us_messages(request):
    id = request.GET.get('id',None)
    if id is not None:
        objects = ContactUs.objects.get(id=id)
        serializer = ContactUsSerializer(objects,many=False)
    else:
        objects = ContactUs.objects.all().order_by('-created_at')
        serializer = ContactUsSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def reply_contact_us_message_through_email(request):
    id = request.data.get('id')
    replied_message = request.data.get('replied_message')
    obj = ContactUs.objects.get(id = id)
    obj.is_replied = True
    obj.replied_text = replied_message
    obj.replied_at = timezone.now()
    obj.save()
    context = {
        'message': replied_message,
        'name':obj.name
    }
    html_content = render_to_string('contact_us.html', context)
    text_content = strip_tags(html_content)
    subject="!!! Thanks for contacting us !!!"
    sender = settings.EMAIL_HOST_USER
    receiver = [obj.email, ]
    # send email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        sender,
        receiver,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return Response({'status_code':200,'message':'Email Sent'})


@api_view(['POST'])
def delete_contact_us(request):
    id = request.data.get('ids')
    ContactUs.objects.filter(id__in=id).delete()
    return Response({'status_code':200,'message':'Deleted Successfully'})