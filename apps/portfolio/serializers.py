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


class PortfolioCreateSerializer(CustomModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id',
                  'user_id',
                  'name',
                  'created_at',
                  'updated_at')


class PortfolioSerializer(CustomModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id',
                  'user_id',
                  'name',
                  'created_at',
                  'updated_at')

        extra_kwargs = {
            'ref_id': {'read_only': True},
            'user_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
