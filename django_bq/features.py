from django.db.backends.base.features import BaseDatabaseFeatures

class DatabaseFeatures(BaseDatabaseFeatures):
    supports_transactions = False
    can_return_columns_from_insert = False
    # Add more feature flags as needed for BigQuery