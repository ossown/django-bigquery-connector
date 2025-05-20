from django_bigquery_connector.client import DatabaseClient as BigQueryDatabaseClient

class DatabaseClient(BigQueryDatabaseClient):
    # Dummy spatial client for BigQuery GIS backend
    pass