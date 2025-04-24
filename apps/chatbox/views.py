from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.db.models import Subquery, OuterRef
from ..authentication.utils import admin_user_checker
from django.utils import timezone
def get_chat_room(user_id):
    chat_room = None
    try:
        chat_room = ChatRoom.objects.get(sender_id = user_id)
    except:
        pass
    return chat_room

def get_anonymous_chat_room(anonymous_user):
    anonymous_chat_room = None
    try:
        anonymous_chat_room = AnonymousChatRoom.objects.get(anonymous_user = anonymous_user)
    except:
        pass
    return anonymous_chat_room


@api_view(['POST'])
def send_message_to_user(request):
    user_id = request.data.get('user_id')
    chat_room = get_chat_room(user_id)
    message = request.data.get('message')
    ChatMessage(
        room=chat_room,
        message=message,
        sender_type = 'admin'
    ).save()
    return Response({'status_code':200})

@api_view(['GET'])
def get_chat_history(request):
    user_id = request.GET.get('user_id')
    chat_room = get_chat_room(user_id)
    messages = ChatMessage.objects.filter(room=chat_room).order_by('timestamp')
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def send_message_to_admin(request):
    user_id = request.data.get('user_id')
    message = request.data.get('message')
    chat_room = get_chat_room(user_id)
    if chat_room is not None:
        chat_room.update_at = timezone.now()
        chat_room.save()
        ChatMessage(
            room=chat_room,
            message=message,
            sender_type = 'user'
        ).save()
    else:
        chat_room = ChatRoom(user_id=user_id,update_at=timezone.now())
        chat_room.save()
        ChatMessage(
            room=chat_room,
            message=message,
            sender_type = 'user'
        ).save()
    return Response({'status_code':200})

@api_view(['GET'])
def get_chat_list(request):
    # Annotate the queryset with the latest message and timestamp
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        searchQuery = request.GET.get('searchQuery',None)
        SortQuery = request.GET.get('SortQuery',None)
        latest_message_subquery = ChatMessage.objects.filter(
            room=OuterRef('pk')
        ).order_by('-timestamp')

        chat_rooms = ChatRoom.objects.annotate(
            latest_message=Subquery(latest_message_subquery.values('message')[:1]),
            latest_timestamp=Subquery(latest_message_subquery.values('timestamp')[:1]),
            latest_sender_type=Subquery(latest_message_subquery.values('sender_type')[:1])
        ).filter(latest_message__isnull=False).order_by('-update_at')
        if SortQuery == 'name':
            chat_rooms = chat_rooms.filter(user__name__icontains=searchQuery)
        if SortQuery == 'email':
            chat_rooms = chat_rooms.filter(user__email__icontains=searchQuery)

        serializer = ChatRoomSerializer(chat_rooms, many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'Access Denied'})

@api_view(['POST'])
def delete_chat_room(request):
    user_id = request.data.get('user_id')
    ChatRoom.objects.get(user_id = user_id).delete()
    return Response({'status_code':200,'message':'Chat Room Deleted'})


@api_view(['POST'])
def save_anonymous_chat_data(request):
    email = request.data.get('email')
    name = request.data.get('name')
    phone = request.data.get('phone')
    existing_data = None
    try:
        existing_data = CollectAnonymousChatData.objects.get(email = email)
    except:
        pass
    if existing_data is None:
        CollectAnonymousChatData(email=email,name=name,phone=phone).save()
        return Response({'status_code':200})
    else:
        if existing_data.phone == 'None' and phone=='None':
            pass
        else:
            existing_data.phone = phone
            existing_data.save()
        return Response({'status_code':200})
    
@api_view(['POST'])
def send_anonymous_message_to_admin(request):
    email = request.data.get('email')
    message = request.data.get('message')
    anonymous_user = CollectAnonymousChatData.objects.get(email=email)
    anonymous_chat_room = get_anonymous_chat_room(anonymous_user)
    if anonymous_chat_room is not None:
        anonymous_chat_room.update_at = timezone.now()
        anonymous_chat_room.save()
        AnonymousChatMessages(
            room=anonymous_chat_room,
            message=message,
            sender_type = 'anonymous_user'
        ).save()
    else:
        anonymous_chat_room = AnonymousChatRoom(anonymous_user=anonymous_user,update_at=timezone.now())
        anonymous_chat_room.save()
        AnonymousChatMessages(
            room=anonymous_chat_room,
            message=message,
            sender_type = 'anonymous_user'
        ).save()
    return Response({'status_code':200})

@api_view(['POST'])
def send_anonymous_message_to_user(request):
    email = request.data.get('email')
    message = request.data.get('message')
    anonymous_user = CollectAnonymousChatData.objects.get(email=email)
    anonymous_chat_room = get_anonymous_chat_room(anonymous_user)
    AnonymousChatMessages(
        room=anonymous_chat_room,
        message=message,
        sender_type = 'admin'
    ).save()
    return Response({'status_code':200})


@api_view(['GET'])
def get_anonymous_chat_list(request):
    # Annotate the queryset with the latest message and timestamp
    admin_access_token = request.COOKIES.get('admin_access_token')
    admin_status = admin_user_checker(admin_access_token)
    if admin_status == True:
        searchQuery = request.GET.get('searchQuery',None)
        SortQuery = request.GET.get('SortQuery',None)
        latest_message_subquery = AnonymousChatMessages.objects.filter(
            room=OuterRef('pk')
        ).order_by('-timestamp')

        chat_rooms = AnonymousChatRoom.objects.annotate(
            latest_message=Subquery(latest_message_subquery.values('message')[:1]),
            latest_timestamp=Subquery(latest_message_subquery.values('timestamp')[:1]),
            latest_sender_type=Subquery(latest_message_subquery.values('sender_type')[:1])
        ).filter(latest_message__isnull=False).order_by('-update_at')
        if SortQuery == 'name':
            chat_rooms = chat_rooms.filter(anonymous_user__name__icontains=searchQuery)
        if SortQuery == 'email':
            chat_rooms = chat_rooms.filter(anonymous_user__email__icontains=searchQuery)

        serializer = AnonymousChatRoomSerializer(chat_rooms, many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'Access Denied'})
    
@api_view(['GET'])
def get_anonymous_user_chat_history(request):
    email = request.GET.get('email')
    anonymous_user = CollectAnonymousChatData.objects.get(email=email)
    anonymous_chat_room = get_anonymous_chat_room(anonymous_user)
    messages = AnonymousChatMessages.objects.filter(room=anonymous_chat_room).order_by('timestamp')
    serializer = AnonymousChatMessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def delete_anonymous_chat_room(request):
    email = request.data.get('email')
    anonymous_user = CollectAnonymousChatData.objects.get(email=email)
    AnonymousChatRoom.objects.get(anonymous_user=anonymous_user).delete()
    return Response({'status_code':200,'message':'Chat Room Deleted'})