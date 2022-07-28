from commons.serializers import CustomModelSerializer
from .models import Portfolio
from .models import PortfolioSummary


class PortfolioSummarySerializer(CustomModelSerializer):
    class Meta:
        model = PortfolioSummary
        fields = ('ticker',
                  'average_amount',
                  'volume',
                  'updated_at')


class PortfolioSerializer(CustomModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('ref_id',
                  'user_id',
                  'name',
                  'created_at',
                  'updated_at')
