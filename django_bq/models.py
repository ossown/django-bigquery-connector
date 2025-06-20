from django.db import models

class BaseBigQueryModel(models.Model):
    """
    Base model for BigQuery with custom methods.
    """
    class Meta:
        abstract = True
        managed = False  # This model is managed by BigQuery, not Django migrations

    def update(self, **params):
        """
        Update valid fields of the model instance.
        :param params:
        :return:
        """
        valid_fields = [field.name for field in self._meta.get_fields()]
        print(f'{valid_fields=}')

        for key, value in params.items():
            if key not in valid_fields:
                raise ValueError(f"Invalid field: {key}")
        self.__class__.objects.using('bigquery').filter(pk=self.pk).update(**params)
