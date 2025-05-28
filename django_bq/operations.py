from django.db.backends.base.operations import BaseDatabaseOperations
from django.conf import settings
from django.utils.encoding import force_str
from datetime import datetime, date, timedelta
import django.apps


class DatabaseOperations(BaseDatabaseOperations):
    explain_prefix = "EXPLAIN"
    cast_char_field_without_max_length = "STRING"
    compiler_module = "django.db.models.sql.compiler"

    def __init__(self, connection):
        super().__init__(connection)
        self.dataset = self.connection.settings_dict.get('NAME')

    def quote_name(self, name):
        table_name_mapping = {m._meta.db_table: f'{self.dataset}.{m._meta.db_table}' for m in django.apps.apps.get_models()}
        if '.' not in name and self.dataset:
            name = table_name_mapping.get(name, name)
        return f"`{name}`"

    def date_extract_sql(self, lookup_type, sql, params):
        return f"EXTRACT({lookup_type.upper()} FROM {sql})", params

    def datetime_extract_sql(self, lookup_type, sql, params, tzname):
        return f"EXTRACT({lookup_type.upper()} FROM {sql})", params

    def time_extract_sql(self, lookup_type, sql, params):
        return self.date_extract_sql(lookup_type, sql, params)

    def date_trunc_sql(self, lookup_type, sql, params, tzname=None):
        return f"DATE_TRUNC({sql}, {lookup_type.upper()})", params

    def datetime_trunc_sql(self, lookup_type, sql, params, tzname=None):
        return f"TIMESTAMP_TRUNC({sql}, {lookup_type.upper()})", params

    def time_trunc_sql(self, lookup_type, sql, params, tzname=None):
        return f"TIME_TRUNC({sql}, {lookup_type.upper()})", params

    def datetime_cast_date_sql(self, sql, params, tzname):
        return f"DATE({sql})", params

    def datetime_cast_time_sql(self, sql, params, tzname):
        return f"TIME({sql})", params

    def deferrable_sql(self):
        return ""

    def distinct_sql(self, fields, params):
        if fields:
            raise NotImplementedError("DISTINCT ON fields not supported by BigQuery")
        return ["DISTINCT"], []

    def unification_cast_sql(self, output_field):
        return "%s"

    def fetch_returned_insert_columns(self, cursor, returning_params):
        return cursor.fetchone()

    def field_cast_sql(self, db_type, internal_type):
        return "%s"

    def force_no_ordering(self):
        return []

    def limit_offset_sql(self, low_mark, high_mark):
        limit, offset = self._get_limit_offset_params(low_mark, high_mark)
        return " ".join(
            sql for sql in (
                f"LIMIT {limit}" if limit else None,
                f"OFFSET {offset}" if offset else None,
            ) if sql
        )

    def last_executed_query(self, cursor, sql, params):
        from django.utils.encoding import force_str
        def to_string(s):
            return force_str(s, strings_only=True, errors="replace")
        if isinstance(params, (list, tuple)):
            u_params = tuple(to_string(val) for val in params)
        elif params is None:
            u_params = ()
        else:
            u_params = {to_string(k): to_string(v) for k, v in params.items()}
        return "QUERY = %r - PARAMS = %r" % (sql, u_params)

    def no_limit_value(self):
        return None

    def pk_default_value(self):
        return "NULL"

    def adapt_datefield_value(self, value):
        return f'{value.isoformat()}' if value else None

    def adapt_datetimefield_value(self, value):
        return f'{value.isoformat()}' if value else None

    def adapt_timefield_value(self, value):
        return f'{value.isoformat()}' if value else None

    def adapt_decimalfield_value(self, value, max_digits=None, decimal_places=None):
        return str(value)

    def adapt_ipaddressfield_value(self, value):
        return value or None

    def year_lookup_bounds_for_date_field(self, value, iso_year=False):
        if iso_year:
            first = date.fromisocalendar(value, 1, 1)
            second = date.fromisocalendar(value + 1, 1, 1) - timedelta(days=1)
        else:
            first = date(value, 1, 1)
            second = date(value, 12, 31)
        return [str(first), str(second)]

    def year_lookup_bounds_for_datetime_field(self, value, iso_year=False):
        if iso_year:
            first = datetime.fromisocalendar(value, 1, 1)
            second = datetime.fromisocalendar(value + 1, 1, 1) - timedelta(microseconds=1)
        else:
            first = datetime(value, 1, 1)
            second = datetime(value, 12, 31, 23, 59, 59, 999999)
        return [str(first), str(second)]

    def get_db_converters(self, expression):
        return []

    def combine_expression(self, connector, sub_expressions):
        return f" {connector} ".join(sub_expressions)

    def lookup_cast(self, lookup_type, internal_type=None):
        if lookup_type in ("iexact", "icontains", "istartswith", "iendswith"):
            return "UPPER(%s)"
        return "%s"

    def pattern_ops(self):
        return {
            "contains": "ILIKE CONCAT('%%', %s, '%%')",
            "icontains": "ILIKE CONCAT('%%', %s, '%%')",
            "startswith": "ILIKE CONCAT(%s, '%%')",
            "istartswith": "ILIKE CONCAT(%s, '%%')",
            "endswith": "ILIKE CONCAT('%%', %s)",
            "iendswith": "ILIKE CONCAT('%%', %s)",
        }

    def prep_for_like_query(self, x):
        return str(x).replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")

    def regex_lookup(self, lookup_type):
        if lookup_type == "regex":
            return "REGEXP_CONTAINS(%s, %s)"
        elif lookup_type == "iregex":
            return "REGEXP_CONTAINS(LOWER(%s), LOWER(%s))"
        raise NotImplementedError(f"Unsupported regex type: {lookup_type}")

    def explain_query_prefix(self, format=None, **options):
        return self.explain_prefix
