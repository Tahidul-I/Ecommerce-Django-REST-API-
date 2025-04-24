from django.db import models
from ..authentication.models import CustomUser
from django.utils import timezone
import random
# Create your models here.
class ChatRoom(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_chatrooms")
    sender_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    color_code = models.CharField(max_length=7,blank=True,null=True)
    update_at = models.DateTimeField(blank=True,null=True)
    def save(self, *args, **kwargs):
        if not self.color_code:
            self.color_code = self.generate_unique_color_code()
        self.sender_id = self.user.id
        super(ChatRoom, self).save(*args, **kwargs)

    def generate_unique_color_code(self):
        existing_colors = set(ChatRoom.objects.values_list('color_code', flat=True))
        while True:
            color_code = "{:06x}".format(random.randint(0, 0xFFFFFF))
            if color_code not in existing_colors:
                return color_code

    def __str__(self):
        return f"ChatRoom for {self.user.email}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    sender_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender_type}: {self.message[:20]} at {self.timestamp}"


class CollectAnonymousChatData(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=18,blank=True,null=True)
    update_at = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Anonymous User Chat Data"

class AnonymousChatRoom(models.Model):
    anonymous_user = models.ForeignKey(CollectAnonymousChatData, on_delete=models.CASCADE,related_name="anonymous_chat")
    color_code = models.CharField(max_length=7,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.color_code:
            self.color_code = self.generate_unique_color_code()
        super(AnonymousChatRoom, self).save(*args, **kwargs)

    def generate_unique_color_code(self):
        existing_colors = set(AnonymousChatRoom.objects.values_list('color_code', flat=True))
        while True:
            color_code = "{:06x}".format(random.randint(0, 0xFFFFFF))
            if color_code not in existing_colors:
                return color_code


class AnonymousChatMessages(models.Model):
    room = models.ForeignKey(AnonymousChatRoom, on_delete=models.CASCADE,related_name="anonymous_chat")
    message = models.TextField()
    sender_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender_type}: {self.message[:20]} at {self.timestamp}"