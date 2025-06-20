from django.db import models
import logging

logger = logging.getLogger("django.db.models")

class BaseBigQueryModel(models.Model):
    """
    Base model for BigQuery with custom methods.
    """
    class Meta:
        abstract = True
        managed = False  # This model is managed by BigQuery, not Django migrations

    def save(self, *args, **kwargs):
        """
        Override save method to use BigQuery.
        """
        logger.debug('entering save')
        logger.debug('checking if primary key already exists in table')

        query_params =  {field.name: getattr(self, field.name) for field in self._meta.fields}

        if not bool(self.__class__.objects.using('bigquery').filter(pk=self.pk)):
            logger.info('primary key does not exist, inserting new record')
            # If the instance does not have a primary key, insert it
            self.__class__.objects.using('bigquery').bulk_create([self])
        else:
            logger.info('primary key exists, updating existing record')
            # If the instance has a primary key, update it
            self.__class__.objects.using('bigquery').filter(pk=self.pk).update(**query_params)
