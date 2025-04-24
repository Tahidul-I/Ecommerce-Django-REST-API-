
from rest_framework import serializers
from .models import *
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['sender_type','message','timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.CharField()
    date = serializers.DateTimeField(source='latest_timestamp')
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='sender_id', read_only=True)
    sender_type = serializers.CharField(source='latest_sender_type')
    class Meta:
        model = ChatRoom
        fields = ['user_id','name', 'email','sender_type','latest_message', 'date','color_code']

class AnonymousChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.CharField()
    date = serializers.DateTimeField(source='latest_timestamp')
    name = serializers.CharField(source='anonymous_user.name', read_only=True)
    email = serializers.CharField(source='anonymous_user.email', read_only=True)
    sender_type = serializers.CharField(source='latest_sender_type')
    class Meta:
        model = AnonymousChatRoom
        fields = ['name', 'email','sender_type','latest_message', 'date','color_code']


class AnonymousChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousChatMessages
        fields = ['sender_type','message','timestamp']