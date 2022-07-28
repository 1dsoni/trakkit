from django.db import models

from commons.db.models import MyModel


class Portfolio(MyModel):
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = "portfolio"
        unique_together = ('user_id', 'name', 'is_deleted')
        ordering = ("-id",)


class PortfolioSummary(MyModel):
    user_id = models.CharField(max_length=255)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='summary')
    ticker = models.CharField(max_length=255)
    average_amount = models.DecimalField(null=True, max_digits=65, decimal_places=2)
    volume = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = "portfolio_summary"
        unique_together = ('user_id', 'portfolio_id', 'ticker', 'is_deleted')
        ordering = ("-id",)
