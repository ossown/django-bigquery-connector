from unittest import mock

from django.test import SimpleTestCase

from django_bq.base import DatabaseWrapper


class TestConnection(SimpleTestCase):
    """Tests for the BigQuery database connection."""

    def test_get_connection_params(self):
        """Test that the correct connection parameters are used."""
        settings_dict = {
            'PROJECT': 'test-project',
            'CREDENTIALS': None,
            'LOCATION': 'us-central1',
        }
        
        wrapper = DatabaseWrapper(settings_dict)
        params = wrapper.get_connection_params()
        
        self.assertEqual(params['project'], 'test-project')
        self.assertIsNone(params['credentials'])
        self.assertEqual(params['location'], 'us-central1')
    
    @mock.patch('google.cloud.bigquery.Client')
    def test_get_new_connection(self, mock_client):
        """Test that a new connection is created with the correct parameters."""
        settings_dict = {
            'PROJECT': 'test-project',
            'CREDENTIALS': None,
            'LOCATION': 'us-central1',
        }
        
        wrapper = DatabaseWrapper(settings_dict)
        conn_params = wrapper.get_connection_params()
        wrapper.get_new_connection(conn_params)
        
        mock_client.assert_called_once_with(
            project='test-project',
            credentials=None,
            location='us-central1',
        )