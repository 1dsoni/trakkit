from commons.serializers import CustomModelSerializer
from .models import Trade


class TradeCreateSerializer(CustomModelSerializer):
    class Meta:
        model = Trade
        fields = ('ref_id',
                  'user_id',
                  'portfolio',
                  'trade_type',
                  'security_type',
                  'ticker',
                  'volume',
                  'amount',
                  'status',
                  'created_at',
                  'updated_at')


class TradeSerializer(CustomModelSerializer):
    class Meta:
        model = Trade
        fields = ('ref_id',
                  'user_id',
                  'portfolio',
                  'trade_type',
                  'security_type',
                  'ticker',
                  'volume',
                  'amount',
                  'status',
                  'created_at',
                  'updated_at')

        extra_kwargs = {
            'ref_id': {'read_only': True},
            'user_id': {'read_only': True},
            'portfolio': {'read_only': True},
            'trade_type': {'read_only': True},
            'security_type': {'read_only': True},
            'ticker': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
