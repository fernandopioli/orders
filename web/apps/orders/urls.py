from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create', views.CreateOrderAPIView.as_view(), name='create'),
]