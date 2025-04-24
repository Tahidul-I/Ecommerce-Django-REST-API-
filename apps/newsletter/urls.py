from django.urls import path
from . import views
urlpatterns = [
    path('v1/news-letter-subscription/',views.news_letter_subscription,name="news_letter_subscription"),
    path('v1/email-for-product-arrival/',views.email_for_product_arrival,name="email_for_product_arrival"),
    path('v1/get-all-news-letter-email/',views.get_all_news_letter_email,name="get_all_news_letter_email"),
    path('v1/delete-news-letter-email/',views.delete_news_letter_email,name="delete_news_letter_email"),
    path('v1/contact-us/',views.contact_us,name="contact_us"),
    path('v1/delete-selected-news-letter-email/',views.delete_selected_news_letter_email,name="delete_selected_news_letter_email"),
    path('v1/get-all-product-arrival-request/',views.get_all_product_arrival_request,name="get_all_product_arrival_request"),
    path('v1/get-product-arrival-request-emails/',views.get_product_arrival_request_emails,name="get_product_arrival_request_emails"),
    path('v1/send-product-arrival-request-emails/',views.send_product_arrival_request_emails,name="send_product_arrival_request_emails"),
    path('v1/delete-selected-product-request-emails/',views.delete_selected_product_request_emails,name="delete_selected_product_request_emails"),
    path('v1/get-all-contact-us-messages/',views.get_all_contact_us_messages, name="get_all_contact_us_messages"),
    path('v1/reply-contact-us-message-through-email/',views.reply_contact_us_message_through_email, name="reply_contact_us_message_through_email"),
    path('v1/delete-contact-us/',views.delete_contact_us, name="delete_contact_us"),
]
