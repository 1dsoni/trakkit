from django.http import JsonResponse
from django.urls import path

urlpatterns = [
    path('ht/', lambda x: JsonResponse({"success": True})),
]
