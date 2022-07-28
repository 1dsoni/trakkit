from django.http import JsonResponse
from django.urls import path, include

urlpatterns = [
    path('ht/', lambda x: JsonResponse({"success": True})),
    path('', include('apps.trade.urls')),
]
