from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TradeViewSet

router = SimpleRouter()

router.register('api/v1/trade', TradeViewSet, 'trade')

urlpatterns = [
    path('', include(router.urls)),
]
