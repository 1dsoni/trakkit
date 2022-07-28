from django.db import models

from commons.db.models import MyModel


class Portfolio(MyModel):
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = "portfolio"

        ordering = ("-id",)

        unique_together = ('user_id',
                           'name',
                           'is_deleted')
