from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from apps.portfolio.business.portfolio_summary import fetch_portfolio_ticker_summary_obj
from apps.portfolio.business.portfolio_summary import update_portfolio_ticker_summary
from apps.portfolio.constants import TradeType, SecurityType, TradeStatus
from apps.portfolio.models import Portfolio
from commons.db.models import MyModel


class Trade(MyModel):
    user_id = models.CharField(max_length=255, blank=False, null=False)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT, related_name='trades')
    trade_type = models.PositiveSmallIntegerField(null=False)  # B=1/ S=1
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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.volume:
            raise ValidationError(f"volume {self.volume} is not valid")

        if not self.amount or float(str(self.amount)) <= 0:
            raise ValidationError(f"amount {self.amount} is not valid")

        if self.trade_type not in {TradeType.BUY, TradeType.SELL}:
            raise ValidationError(f"trade_type {self.trade_type} is not valid")

        if self.security_type not in {SecurityType.stock}:
            raise ValidationError(f"security_type {self.security_type} is not valid")

        if self.status not in {TradeStatus.success, TradeStatus.failed}:
            raise ValidationError(f"status {self.status} is not valid")

        with transaction.atomic():
            super().save(force_insert=force_insert,
                         force_update=force_update,
                         using=using,
                         update_fields=update_fields)
            portfolio_ticker_summary_obj = fetch_portfolio_ticker_summary_obj(
                user_id=self.user_id,
                portfolio=self.portfolio,
                ticker=self.ticker
            )
            transaction.on_commit(
                lambda: update_portfolio_ticker_summary(ticker=self.ticker,
                                                        portfolio_summary_obj=portfolio_ticker_summary_obj)
            )
