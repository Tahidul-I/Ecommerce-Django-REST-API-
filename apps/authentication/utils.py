from rest_framework_simplejwt.tokens import AccessToken
from .models import CustomUser


def admin_user_checker(admin_access_token):
    
    access_token = AccessToken(admin_access_token)
    email = access_token.payload.get("email")
    user = None
    try:
        user = CustomUser.objects.get(email=email,is_active=True,is_staff = True)
    except:
        pass
    if user is not None:
        return True
    else:
        return False
    
def super_admin_user_checker(admin_access_token):
    access_token = AccessToken(admin_access_token)
    email = access_token.payload.get("email")
    user = None
    try:
        user = CustomUser.objects.get(email=email,is_active=True,is_superuser = True)
    except:
        pass
    if user is not None:
        return True
    else:
        return False
    

def generate_unique_username(name):
    base_username = name.lower().replace(' ', '_')
    username = base_username
    counter = 1

    while CustomUser.objects.filter(username=username).exists():
        username = f"{base_username}_{counter}"
        counter += 1

    return username

def get_use_id(user_access_token):
    access_token = AccessToken(user_access_token)
    email = access_token.payload.get("email")
    user = CustomUser.objects.get(email = email)
    return user.id

def get_user(user_access_token):
    access_token = AccessToken(user_access_token)
    email = access_token.payload.get("email")
    user = CustomUser.objects.get(email = email)
    return user