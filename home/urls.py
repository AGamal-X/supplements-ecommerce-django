from django.urls import include, path
from . import views
urlpatterns = [
path('', views.index, name='home'),
path('<str:product_id>/', views.home_detail, name='home_detail'),
]