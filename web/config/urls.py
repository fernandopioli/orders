from django.urls import path, include

urlpatterns = [
    path('api/order', include('web.apps.orders.urls')),
]