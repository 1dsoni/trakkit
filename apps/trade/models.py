from django.db import models

from commons.db.models import MyModel


class Trade(MyModel):
    user_id = models.CharField(max_length=255)
    portfolio_id = models.CharField(max_length=255)
    trade_type = models.PositiveSmallIntegerField()  # B=1/ S=1
    security_type = models.CharField(max_length=255)
    ticker = models.CharField(max_length=255)
    volume = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=65, decimal_places=2)
    status = models.CharField(max_length=255)

    class Meta:
        db_table = "trade"

        ordering = ('-id',)

        indexes = [
            models.Index(fields=['user_id',
                                 'portfolio_id',
                                 'ticker',
                                 'trade_type',
                                 'status',
                                 'is_deleted'])
        ]
