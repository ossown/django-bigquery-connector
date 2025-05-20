from django_bigquery_connector.features import DatabaseFeatures as BigQueryDatabaseFeatures

class DatabaseFeatures(BigQueryDatabaseFeatures):
    gis_enabled = False
    supports_geography = False
    supports_geometry = False
    supports_spatial_ref_sys = False
    # Add more GIS-related feature flags as needed