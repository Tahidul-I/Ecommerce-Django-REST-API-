from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(CollectAnonymousChatData)
admin.site.register(AnonymousChatRoom)
admin.site.register(AnonymousChatMessages)