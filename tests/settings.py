"""
Django test settings for django-bigquery-connector tests.
"""

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'tests',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    'bigquery': {
        'ENGINE': 'django_bigquery_connector',
        'PROJECT': 'test-project',
        'CREDENTIALS': None,
        'LOCATION': 'us-central1',
    }
}