from bigquery_backend.client import DatabaseClient as BigQueryDatabaseClient

class DatabaseClient(BigQueryDatabaseClient):
    # Dummy spatial client for BigQuery GIS backend
    pass 