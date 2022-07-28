from rest_framework import mixins

from commons.viewsets import BaseApiViewSet
from .models import Trade
from .serializers import TradeSerializer


class TradeViewSet(BaseApiViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
