from django_bigquery_connector.operations import DatabaseOperations as BigQueryDatabaseOperations

class DatabaseOperations(BigQueryDatabaseOperations):
    """
    Dummy GIS operations class for BigQuery.
    No real spatial support is implemented.
    """

    def geo_db_type(self, f):
        raise NotImplementedError("BigQuery does not support spatial data types.")

    def get_geometry_converter(self, geom_class):
        raise NotImplementedError("BigQuery does not support geometry conversion.")

    def convert_geometry(self, value, geom_class):
        raise NotImplementedError("BigQuery does not support geometry conversion.")