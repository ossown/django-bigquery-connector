from unittest import mock
from django.test import SimpleTestCase

from django_bq.operations import DatabaseOperations


class TestDatabaseOperations(SimpleTestCase):
    """Tests for the BigQuery database operations."""

    def setUp(self):
        self.connection = mock.MagicMock()
        self.ops = DatabaseOperations(self.connection)
    
    def test_date_extract_sql(self):
        """Test that date extraction SQL is correctly generated."""
        sql, params = self.ops.date_extract_sql('year', 'field', [])
        self.assertEqual(sql, "EXTRACT(YEAR FROM field)")
        self.assertEqual(params, [])
    
    def test_datetime_extract_sql(self):
        """Test that datetime extraction SQL is correctly generated."""
        sql, params = self.ops.datetime_extract_sql('year', 'field', [], None)
        self.assertEqual(sql, "EXTRACT(YEAR FROM field)")
        self.assertEqual(params, [])
    
    def test_time_extract_sql(self):
        """Test that time extraction SQL is correctly generated."""
        sql, params = self.ops.time_extract_sql('hour', 'field', [])
        self.assertEqual(sql, "EXTRACT(HOUR FROM field)")
        self.assertEqual(params, [])