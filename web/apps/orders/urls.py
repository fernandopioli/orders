from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.OrderAPIView.as_view(), name='order'),
]