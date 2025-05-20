from django_bigquery_connector.creation import DatabaseCreation as BigQueryDatabaseCreation

class DatabaseCreation(BigQueryDatabaseCreation):
    # Dummy spatial creation for BigQuery GIS backend
    pass