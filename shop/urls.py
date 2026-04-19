from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shop'),
    path('search-suggestions/', views.search_suggestions, name='shop_search_suggestions'),
    path('<str:product_id>/', views.shop_detail, name='shop_detail'),
]
