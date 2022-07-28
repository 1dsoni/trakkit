from commons.serializers import CustomModelSerializer
from .models import Portfolio


class PortfolioSerializer(CustomModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('ref_id',
                  'user_id',
                  'name',
                  'created_at',
                  'updated_at')
