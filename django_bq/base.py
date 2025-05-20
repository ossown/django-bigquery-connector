from datetime import datetime, date, time

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.utils import CursorWrapper, CursorDebugWrapper
from django.utils.asyncio import async_unsafe
from django.utils.functional import cached_property
from django.db import DatabaseError as DjangoDatabaseError

from .client import DatabaseClient
from .creation import DatabaseCreation
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor


class BigQueryCursor:
    def __init__(self, client):
        self.client = client
        self._results = None
        self.description = None

    def execute(self, query, params=None):
        if not query.strip().lower().startswith("select"):
            raise NotImplementedError("Only SELECT queries are supported in BigQuery.")

        if params:
            param_iter = iter(params)

            def replace(match):
                val = next(param_iter)
                if val is None:
                    return "NULL"
                elif isinstance(val, datetime):
                    # Format with timezone if present
                    return f"TIMESTAMP '{val.isoformat()}'"
                elif isinstance(val, date):
                    return f"DATE '{val.isoformat()}'"
                elif isinstance(val, time):
                    return f"TIME '{val.isoformat()}'"
                elif isinstance(val, str):
                    escaped = val.replace("'", "''")
                    return f"'{escaped}'"
                return str(val)

            import re
            query = re.sub(r"%s", replace, query)

        job = self.client.query(query)
        self._results = list(job)
        self.description = [(field.name,) for field in job.schema] if job.schema else []
        return self

    def fetchone(self):
        if self._results:
            return tuple(self._results.pop(0).values())
        return None

    def fetchall(self):
        if self._results:
            results = [tuple(row.values()) for row in self._results]
            self._results = []
            return results
        return []

    def fetchmany(self, size=None):
        if self._results is None:
            return []
        size = size or 1
        result = []
        for _ in range(min(size, len(self._results))):
            result.append(tuple(self._results.pop(0).values()))
        return result

    def close(self):
        self._results = None


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = "bigquery"
    display_name = "Google BigQuery"

    client_class = DatabaseClient
    creation_class = DatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations
    SchemaEditorClass = DatabaseSchemaEditor

    data_types = {
        "AutoField": "INT64",
        "BigAutoField": "INT64",
        "BinaryField": "BYTES",
        "BooleanField": "BOOL",
        "CharField": "STRING",
        "DateField": "DATE",
        "DateTimeField": "DATETIME",
        "DecimalField": "NUMERIC",
        "DurationField": "STRING",
        "FileField": "STRING",
        "FilePathField": "STRING",
        "FloatField": "FLOAT64",
        "IntegerField": "INT64",
        "BigIntegerField": "INT64",
        "IPAddressField": "STRING",
        "GenericIPAddressField": "STRING",
        "JSONField": "JSON",
        "OneToOneField": "INT64",
        "PositiveBigIntegerField": "INT64",
        "PositiveIntegerField": "INT64",
        "PositiveSmallIntegerField": "INT64",
        "SlugField": "STRING",
        "SmallAutoField": "INT64",
        "SmallIntegerField": "INT64",
        "TextField": "STRING",
        "TimeField": "TIME",
        "UUIDField": "STRING",
    }

    operators = {
        "exact": "= %s",
        "iexact": "= UPPER(%s)",
        "contains": "LIKE %s",
        "icontains": "LIKE UPPER(%s)",
        "startswith": "LIKE CONCAT(%s, '%%')",
        "istartswith": "LIKE CONCAT(UPPER(%s), '%%')",
        "endswith": "LIKE CONCAT('%%', %s)",
        "iendswith": "LIKE CONCAT('%%', UPPER(%s))",
        "regex": "REGEXP_CONTAINS(%s, %s)",
        "iregex": "REGEXP_CONTAINS(UPPER(%s), UPPER(%s))",
        "gt": "> %s",
        "gte": ">= %s",
        "lt": "< %s",
        "lte": "<= %s",
    }

    def get_connection_params(self):
        return {
            "project": self.settings_dict.get("PROJECT"),
            "credentials": self.settings_dict.get("CREDENTIALS"),
            "location": self.settings_dict.get("LOCATION"),
        }

    def get_new_connection(self, conn_params):
        from google.cloud import bigquery
        client = bigquery.Client(
            project=conn_params["project"],
            credentials=conn_params["credentials"],
            location=conn_params.get("location"),
        )
        return client

    def create_cursor(self, name=None):
        return BigQueryCursor(self.connection)

    def is_usable(self):
        try:
            self.connection.query("SELECT 1").result()
            return True
        except Exception:
            return False

    def _set_autocommit(self, autocommit):
        # No-op: BigQuery does not support transactions
        self.autocommit = True

    def make_debug_cursor(self, cursor):
        return CursorDebugWrapper(cursor, self)

    def make_cursor(self, cursor):
        return CursorWrapper(cursor, self)

    def get_database_version(self):
        return (2, 0)  # Dummy version


try:
    import google.cloud.bigquery as bq
    class DataError(Exception): pass
    class IntegrityError(Exception): pass
    class InternalError(Exception): pass
    class InterfaceError(Exception): pass
    class DatabaseError(Exception): pass
    class OperationalError(Exception): pass
    class ProgrammingError(Exception): pass
    class NotSupportedError(Exception): pass
    class Error(Exception): pass

    bq.DataError = DataError
    bq.IntegrityError = IntegrityError
    bq.InternalError = InternalError
    bq.InterfaceError = InterfaceError
    bq.DatabaseError = DatabaseError
    bq.OperationalError = OperationalError
    bq.ProgrammingError = ProgrammingError
    bq.NotSupportedError = NotSupportedError
    bq.Error = Error

    DatabaseWrapper.Database = bq
except ImportError:
    pass