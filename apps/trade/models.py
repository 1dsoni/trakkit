from django.db import models, transaction

from apps.portfolio.business.portfolio_summary import update_portfolio_ticker_summary, \
    fetch_portfolio_ticker_summary_obj
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
