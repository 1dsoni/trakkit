from commons.serializers import CustomModelSerializer
from .models import Trade


class TradeSerializer(CustomModelSerializer):
    class Meta:
        model = Trade
        fields = ('ref_id',
                  'user_id',
                  'portfolio_id',
                  'trade_type',
                  'security_type',
                  'ticker',
                  'volume',
                  'amount',
                  'status',
                  'created_at',
                  'updated_at')
