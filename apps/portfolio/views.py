from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from commons.viewsets import BaseApiViewSet
from .business.cumulative_returns import fetch_portfolio_ticker_cumulative_returns
from .business.portfolio_summary import recalculate_portfolio_ticker_summary
from .models import Portfolio
from .models import PortfolioSummary
from .serializers import PortfolioSerializer
from .serializers import PortfolioSummarySerializer


class PortfolioViewSet(BaseApiViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin):
    queryset = Portfolio.objects.all()

    lookup_field = 'id'

    serializer_class = PortfolioSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('user_id', 'name')

    @action(methods=['POST'], detail=True, url_path="recalculate-summary")
    def recalculate_summary(self, request, *args, **kwargs):
        portfolio = self.get_object()
        portfolio = recalculate_portfolio_ticker_summary(portfolio)
        return Response(self.get_serializer(portfolio).data)

    @action(methods=['GET'], detail=True, url_path="cumulative-returns")
    def fetch_cumulative_returns(self, request, *args, **kwargs):
        portfolio = self.get_object()
        return_value = fetch_portfolio_ticker_cumulative_returns(portfolio)
        return Response(
            {
                'return_value': return_value
            }
        )


class PortfolioSummaryViewSet(BaseApiViewSet,
                              mixins.ListModelMixin):
    queryset = PortfolioSummary.objects.all()

    serializer_class = PortfolioSummarySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('user_id', 'portfolio_id', 'ticker')
