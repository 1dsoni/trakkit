from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.urls import path, include

urlpatterns = [
    path('ht/', lambda x: JsonResponse({"success": True})),
    path('', include('apps.trade.urls')),
    path('', include('apps.portfolio.urls')),
    path('', include('apps.documentation.urls')),
]

settings.DEBUG = True
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
settings.DEBUG = False
