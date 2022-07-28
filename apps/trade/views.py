from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter

from commons.viewsets import BaseApiViewSet
from .models import Trade
from .serializers import TradeSerializer


class TradeViewSet(BaseApiViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin):
    queryset = Trade.objects.all().select_related('portfolio')

    serializer_class = TradeSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('user_id',
                        'portfolio_id',
                        'ticker',
                        'trade_type',
                        'status')
