from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter

from commons.viewsets import BaseApiViewSet
from .models import Portfolio
from .serializers import PortfolioSerializer


class PortfolioViewSet(BaseApiViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('user_id', 'name')
