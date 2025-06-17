from django.urls import include, path, re_path
from django.http import JsonResponse

def api_404(request, *args):
    return JsonResponse({
        "success": False,
        "message": "Page not found", 
        "errors": ["The requested URL was not found on this server."]
    }, status=404)

urlpatterns = [
    path("api/order", include("web.apps.orders.urls")),
    re_path(r'^api/', api_404),
]

