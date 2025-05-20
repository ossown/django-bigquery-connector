from bigquery_backend.introspection import DatabaseIntrospection as BigQueryDatabaseIntrospection

class DatabaseIntrospection(BigQueryDatabaseIntrospection):
    # Dummy spatial introspection for BigQuery GIS backend
    pass 