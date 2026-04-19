from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from core import views as core_views

urlpatterns = [
    path('cart/add/<str:catalog_key>/<str:product_id>/', core_views.add_product_to_cart, name='add_to_cart'),
    path('cart/update/', core_views.cart_update, name='cart_update'),
    path('', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('home/', include('home.urls')),
    path('payment/', include('payment.urls')),
    path('shop/', include('shop.urls')),
    path('shoppingcart/', include('shoppingcart.urls')),
    path('cart/', include('shoppingcart.urls')),
    path('', include('accounts.urls')),
    path('contact/', include('Contact.urls')),
    path('contact', RedirectView.as_view(url='/contact/', permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
