from django_bigquery_connector.schema import DatabaseSchemaEditor as BigQueryDatabaseSchemaEditor

class DatabaseSchemaEditor(BigQueryDatabaseSchemaEditor):
    # Dummy spatial schema editor for BigQuery GIS backend
    pass