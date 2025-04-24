from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password,make_password
from .models import CustomUser,OTP
from ..cart.models import Cart,Wishlist
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
import random
from datetime import timedelta
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .serializers import UserSerializer
from ..authentication.utils import generate_unique_username,super_admin_user_checker
from django.db.models import Q
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.name  
        token['email'] = user.email


        return token

# @cache_control(private=True, no_cache=False, no_store=False, must_revalidate=False, max_age=259200)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Remove tokens from response body
        # Add success message
        max_age = 86400*5
        response.data['message'] = 'Login Successful'
        if 'access' in response.data:
            access_token = response.data['access']
            response.set_cookie(key='access_token', value=access_token, httponly=True, samesite='None',secure=True,max_age=max_age)  # Set access token as cookie
            return response
        else:
            return Response({'status_code':401,'message':'Invalid email or password'})

        
    
 

class CustomAccessToken(AccessToken):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove 'user' from kwargs if present
        super().__init__(*args, **kwargs)
        if user:
            total_cart_items = 0
            total_wishlist_item = 0
            try:
                total_cart_items = Cart.objects.filter(user = user).count()
            except:
                pass
            try:
                total_wishlist_item = Wishlist.objects.filter(user_id = user.id).count()
            except:
                pass

            self['total_cart_items'] = total_cart_items
            self['total_wishlist_item'] = total_wishlist_item
            self['name'] = user.name
            self['email'] = user.email



@api_view(['POST'])
def signup(request):

    values = request.data
    name = values.get('name')
    email = values.get('email')
    password = values.get('password')
    user = None
    tetra_code = random.randint(1111,9999)
    try:
        user = CustomUser.objects.get(email=email)

    except:
        pass

    if user is None:
        
        try:
            save_user = CustomUser.objects.create_user(
            name = name,
            username = generate_unique_username(name),
            email = email,
            password = password,
            is_active = False
            )

            otp_save = OTP(
                user = save_user,
                otp = tetra_code,
                created_at = timezone.now(),
                otp_verified = False
            )
            otp_save.save()
            subject="Email Verification"
            message = f"""
                        Hi {name}, here is your OTP {tetra_code} .
                        Use this code to verify your email.
                        """
            sender = settings.EMAIL_HOST_USER
            receiver = [email, ]
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            return Response({"status_code":200,"message":"Email Verification OTP Sent"})


        except :

            return Response({"status_code":422,"message":"Something went wrong"})

    else:

        return Response({"status_code":422,"message":"User with this email already exist"})
    
@api_view(['POST'])
def send_otp(request):
   
    email = request.data.get('email')
    user = None
    try:
        user = CustomUser.objects.get(email=email)
       
    except:
        pass

    if user is not None:

        try:
            user_otp = OTP.objects.get(user=user,otp_verified=False)
            otp = random.randint(1111,9999)
            user_otp.otp = otp
            user_otp.created_at = timezone.now()
            user_otp.save()

            subject="Email Verification"
            message = f"""
                        Hi {user.name}, here is your OTP {otp} .
                        Use this code to verify your email.
                        """
            sender = settings.EMAIL_HOST_USER
            receiver = [user.email, ]


            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            return Response({'status_code':200,"message":"OTP sent"})

        except:
            return Response({'status_code':422,"message":"Invalid Email"})

    else:
        
        return Response({'status_code':422,"message":"Something Went wrong.Please check if the email is correct"})


@api_view(['POST'])
def otp_verification(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    user = CustomUser.objects.get(email=email)
    user_otp = OTP.objects.get(user=user,otp_verified = False)
    current_time = timezone.now()
    time_duration = current_time - user_otp.created_at

    if time_duration <= timedelta(seconds=300):
        if otp == user_otp.otp:
            user.is_active = True
            user.save()
            user_otp.delete()
            return Response({"status_code":200,"message":"Email Verified"})
        
        else:
            return Response({"status_code":422,"message":"Invalid OTP"})
    else:
        return Response({"status_code":422,"message":"OTP Expired"})



@api_view(['POST'])
def forget_password(request):
    email = request.data.get('email')
    user = None
    try:
        user = CustomUser.objects.get(email=email,is_active=True)
    except:
        pass
    
    if user is not None:
        otp_user = OTP.objects.filter(user=user)
        otp_user.delete()
        otp = random.randint(1111,9999)
        user_otp = OTP(
            user = user,
            otp = otp,
            created_at = timezone.now(),
            otp_verified = False
        )

        user_otp.save()
        subject="Email Verification"
        message = f"""
                    Hi {user.name}, here is your OTP {user_otp.otp} .
                    Use this code to verify your email and we will let you change your password.
                    """
        sender = settings.EMAIL_HOST_USER
        receiver = [user.email, ]
        # send email
        send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
        
        return Response({"status_code":200,"message": "OTP sent"})
    
    else:
        return Response({"status_code":422,"message": "The email is not registered"})


@api_view(['POST'])
def change_password(request):
    browser_access_token = None
    try:
        browser_access_token = request.COOKIES.get('access_token')
    except:
        pass
    
    new_password = request.data.get('new_password')

    if browser_access_token is None:
        
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        access_token = CustomAccessToken(user = user)
        serialized_token = str(access_token)
        max_age = 86400*5
        response = Response({"status_code": 200, "message": "Password changed successfully"})
        response.set_cookie(key='access_token', value=serialized_token, httponly=True, secure=True, samesite='None',max_age=max_age)
        return response
    
    else:
        old_password = request.data.get('old_password')
        access_token = AccessToken(browser_access_token)
        email = access_token.payload.get("email")
        
        user = CustomUser.objects.get(email=email)
        if check_password(old_password, user.password):

            user.set_password(new_password)
            user.save()
            access_token = CustomAccessToken(user = user)
            serialized_token = str(access_token)
            response = Response({"status_code": 200, "message": "Password changed successfully"})
            max_age = 86400*5
            response.delete_cookie('access_token', path='/',samesite='None')
            response.set_cookie(key='access_token', value=serialized_token, httponly=True, secure=True, samesite='None',max_age=max_age)
            return response
        else:
            return Response({'status_code':401,'message':'Incorrect Old Password'}, status=200)
        
@api_view(['POST'])
def admin_authentication(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = None
    try:
        user = CustomUser.objects.get(email = email,is_active=True)
    except:
        pass
    if user is not None:
        if check_password(password, user.password):
            if user.is_staff == True :
                admin_access_token = CustomAccessToken(user = user)
                serialized_token = str(admin_access_token)
                response = Response({"status_code": 200, "message": "Login Successful"})
                max_age = 86400*5
                response.set_cookie(key='admin_access_token', value=serialized_token, httponly=True, secure=True, samesite='None',max_age=max_age)
                return response
            else:
                return Response({'status_code':400,'message':'Not an admin user'})
        else:
            return Response({'status_code':400,'message':'Incorrrect password'})
    
    else:
        return Response({'status_code':400,'message':'Invalid User'})


@api_view(['GET'])    
def get_user(request):
    try:
        
        browser_access_token = request.COOKIES.get('access_token')
        access_token = AccessToken(browser_access_token)
        email = access_token.payload.get("email")
        name = access_token.payload.get("name")
        user = None
        try:
            user = CustomUser.objects.get(email=email,is_active=True)
        except:
            pass
        if user is not None:
            total_cart_items = 0
            total_wishlist_item = 0
            try:
                total_cart_items = Cart.objects.filter(user = user).count()
            except:
                pass
            try:
                total_wishlist_item = Wishlist.objects.filter(user = user).count()
            except:
                pass
            return Response({'email':email,'name':name,'total_cart_items':total_cart_items,'total_wishlist_item':total_wishlist_item,'user_id':user.id}, status=200)
        else:
            return Response({'status_code':403,'error': 'Invalid User'}, status=200)

    except:
        return Response({'status_code':401,'error': 'Tokens are missing'}, status=200)
    

@api_view(['GET'])    
def get_admin_user(request):
    try:
        
        admin_access_token = request.COOKIES.get('admin_access_token')
        access_token = AccessToken(admin_access_token)
        email = access_token.payload.get("email")
        name = access_token.payload.get("name")
        user = None
        try:
            user = CustomUser.objects.get(email=email,is_active=True,is_staff = True)
        except:
            pass
        if user is not None:
            return Response({'status_code':200,'admin_email':email,'admin_name':name}, status=200)
        else:
            return Response({'status_code':403,'error': 'Invalid User'}, status=200)

    except:
        return Response({'status_code':401,'error': 'Token is missing'}, status=200)


@csrf_exempt
@api_view(['POST'])    
def logout(request):

    response = Response({
        'status':200,
        'message': 'Logout successful'
    })

    response.delete_cookie('access_token', path='/',samesite='None')

    return response

@csrf_exempt
@api_view(['POST'])    
def admin_logout(request):

    response = Response({
        'status':200,
        'message': 'Logout successful'
    })

    response.delete_cookie('admin_access_token', path='/',samesite='None')

    return response


@api_view(['GET'])
def get_all_user(request):
    try:
        admin_access_token = request.COOKIES.get('admin_access_token')
    except KeyError:
        admin_access_token = None

    if admin_access_token is not None:
        super_user_status = super_admin_user_checker(admin_access_token)
        if super_user_status:
            has_more = True
            search_key = request.GET.get('searchQuery', None)
            sort_key = request.GET.get('SortQuery', None)
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            users = CustomUser.objects.all().order_by('name')
            if search_key is None and sort_key is None:
                
                if users.count() < page*limit:
                    has_more = False
                users = users[0:page*limit]
                serializer = UserSerializer(users, many=True)
                return Response({'status_code': 200, 'user_data': serializer.data,'has_more':has_more})
            
            else:
                # Apply sorting filter
                if sort_key:
                    if sort_key == "active_user":
                        users = users.filter(is_active=True)
                    elif sort_key == "inactive_user":
                        users = users.filter(is_active=False)
                    elif sort_key == "moderator":
                        users = users.filter(is_staff=True)
                    elif sort_key == "admin":
                        users = users.filter(is_superuser=True)
                    

                # Apply search filter
                if search_key:
                    search_words = search_key.split()
                    query = Q()
                    for word in search_words:
                        query |= Q(name__icontains=word) | Q(email__icontains=word)

                    users = users.filter(query)
                

                if users.count() < page*limit:
                    has_more = False
                users = users[0:page*limit]
                serializer = UserSerializer(users, many=True)
                return Response({'status_code': 200, 'user_data': serializer.data,'has_more':has_more})

        return Response({'status_code': 400, 'message': 'Access Denied'})

    return Response({'status_code': 400, 'message': 'Access Token Missing'})




@api_view(['POST'])
def change_user_active_status(request):
    admin_access_token = None
    try:
        admin_access_token = request.COOKIES.get('admin_access_token')
    except:
        pass
    if admin_access_token is not None:
        super_user_status = super_admin_user_checker(admin_access_token)
        if super_user_status == True:
            id = request.data.get('id')
            is_active_status = request.data.get('is_active')
            user = CustomUser.objects.get(id = id)
            if user.is_superuser == True:
                return Response({'status_code':400,'message':'Unable to perform the action'})
            else:
                user.is_active = is_active_status
                user.save()
                return Response({'status_code':200,'message':'User Status Changed'})
        else:
            return Response({'status_code':400,'message':'Access Denied'})
        
@api_view(['POST'])
def change_user_staff_status(request):
    admin_access_token = None
    try:
        admin_access_token = request.COOKIES.get('admin_access_token')
    except:
        pass
    if admin_access_token is not None:
        super_user_status = super_admin_user_checker(admin_access_token)
        if super_user_status == True:
            id = request.data.get('id')
            is_active_status = request.data.get('is_active')
            user = CustomUser.objects.get(id = id)
            if user.is_superuser == True:
                return Response({'status_code':400,'message':'Unable to perform the action'})
            
            else:
                user.is_staff = is_active_status
                user.save()
                return Response({'status_code':200,'message':'User Status Changed'})
        else:
            return Response({'status_code':400,'message':'Access Denied'})

        
@api_view(['POST'])
def delete_user(request):
    admin_access_token = None
    try:
        admin_access_token = request.COOKIES.get('admin_access_token')
    except:
        pass
    if admin_access_token is not None:
        super_user_status = super_admin_user_checker(admin_access_token)
        if super_user_status == True:
            id = request.data.get('id')
            user = CustomUser.objects.get(id = id)
            if user.is_superuser == True:
                return Response({'status_code':400,'message':'Unable to perform the action'})
            else:
                user.delete()
                return Response({'status_code':200,'message':'User Deleted'})
        else:
            return Response({'status_code':400,'message':'Access Denied'})


@api_view(['POST'])
def create_user_from_dashboard(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    is_active = request.data.get('is_active')
    is_staff =  request.data.get('is_moderator')
    is_superuser = request.data.get('is_admin')
    user = None
    admin_access_token = request.COOKIES.get('admin_access_token')
    super_user_status = super_admin_user_checker(admin_access_token)
    if super_user_status == True:
        try:
            user = CustomUser.objects.get(email=email)

        except:
            pass

        if user is None:
            CustomUser.objects.create_user(
                name = name,
                email = email,
                username = generate_unique_username(name),
                password = password,
                is_active = is_active,
                is_staff = is_staff,
                is_superuser = is_superuser,
            )

            return Response({'status_code':200,'message':'User Saved'})
        else:
            return Response({'status_code':400,'message':'user with this email already exist'})
    else:
        return Response({'message':'Access Denied'})
    
@api_view(['POST'])
def google_authentication(request):
    name = request.data.get('name')
    email = request.data.get('email')
    existing_user = None
    try:
        existing_user = CustomUser.objects.get(email = email)
    except:
        pass
    if existing_user is not None:
        access_token = CustomAccessToken(user = existing_user)
        serialized_token = str(access_token)
        max_age = 86400*5
        response = Response({"status_code": 200, "message": "Login Successfull"})
        response.set_cookie(key='access_token', value=serialized_token, httponly=True, secure=True, samesite='None',max_age=max_age)
        return response
    else:
        save_user = CustomUser(
            name = name,
            username = generate_unique_username(name),
            email = email,
            password = str(random.randint(12345890,234567789056)),
            is_active = True
        )
        save_user.save()
        access_token = CustomAccessToken(user = save_user)
        serialized_token = str(access_token)
        max_age = 86400*5
        response = Response({"status_code": 200, "message": "Login Successfull"})
        response.set_cookie(key='access_token', value=serialized_token, httponly=True, secure=True, samesite='None',max_age=max_age)
        return response