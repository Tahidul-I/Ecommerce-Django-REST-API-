
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include("apps.authentication.urls")),
    path('',include("apps.core.urls")),
    path('api/',include("apps.category.urls")),
    path('api/',include("apps.product.urls")),
    path('api/',include("apps.banner.urls")),
    path('api/',include("apps.cart.urls")),
    path('api/',include("apps.order.urls")),
    path('api/',include("apps.payment_gateway.urls")),
    path('api/',include("apps.brand.urls")),
    path('api/',include("apps.search.urls")),
    path('api/',include("apps.review.urls")),
    path('api/',include("apps.newsletter.urls")),
    path('api/',include("apps.chatbox.urls")),
    path('api/',include("apps.analytics.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

