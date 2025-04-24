from django.urls import path
from . import views
urlpatterns = [
    path('v1/send-message-to-admin/',views.send_message_to_admin,name="send_message_to_admin"),
    path('v1/send-message-to-user/',views.send_message_to_user,name="send_message_to_user"),
    path('v1/get-chat-history/',views.get_chat_history,name="get_chat_history"),
    path('v1/get-chat-list/',views.get_chat_list,name="get_chat_list"),
    path('v1/delete-chat-room/',views.delete_chat_room,name="delete_chat_room"),
    path('v1/save-anonymous-chat-data/',views.save_anonymous_chat_data,name="save_anonymous_chat_data"),
    path('v1/send-anonymous-message-to-admin/',views.send_anonymous_message_to_admin,name="send_anonymous_message_to_admin"),
    path('v1/send-anonymous-message-to-user/',views.send_anonymous_message_to_user,name="send_anonymous_message_to_user"),
    path('v1/get-anonymous-chat-list/',views.get_anonymous_chat_list,name="get_anonymous_chat_list"),
    path('v1/get-anonymous-user-chat-history/',views.get_anonymous_user_chat_history,name="get_anonymous_user_chat_history"),
    path('v1/delete-anonymous-chat-room/',views.delete_anonymous_chat_room,name="delete_anonymous_chat_room"),
]
