from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PortfolioViewSet

router = SimpleRouter()

router.register('api/v1/portfolio', PortfolioViewSet, 'portfolio')

urlpatterns = [
    path('', include(router.urls)),
]
