from django_bigquery_connector.introspection import DatabaseIntrospection as BigQueryDatabaseIntrospection

class DatabaseIntrospection(BigQueryDatabaseIntrospection):
    # Dummy spatial introspection for BigQuery GIS backend
    pass