from django_bq.base import DatabaseWrapper as BigQueryDatabaseWrapper

class DatabaseWrapper(BigQueryDatabaseWrapper):
    """
    GIS variant of BigQuery DatabaseWrapper.
    No spatial features are supported but allows for compatibility with django.contrib.gis.
    """

    def _set_autocommit(self, autocommit):
        # BigQuery does not support transactional control; noop.
        self.autocommit = True

    # Ensure Database is set properly
    try:
        import google.cloud.bigquery as bq
        Database = bq
    except ImportError:
        Database = None
