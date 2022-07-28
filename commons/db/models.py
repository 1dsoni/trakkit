import uuid

from django.db import models


class CustomManager(models.Manager):

    def get_queryset(self):
        return super(CustomManager, self).get_queryset().filter(is_deleted=0)


def random_ref_id():
    return str(uuid.uuid4())


class MyModel(models.Model):
    ref_id = models.CharField(max_length=64,
                              unique=True,
                              default=random_ref_id)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.IntegerField(default=0)

    objects = CustomManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self._meta.db_table}, id={self.pk}'
