# Django BigQuery Connector

A Django database backend for Google BigQuery, enabling Django ORM queries against BigQuery datasets.

## Features

- Use Django ORM to query BigQuery tables seamlessly
- Read-only operations support
- Supports most Django ORM query methods and filters
- GIS operations support (minimal)
- Django admin integration

## Installation

```bash
pip install django-bigquery-connector
```

## Configuration

Add the following to your Django settings:

```python
DATABASES = {
    'default': {
        # Your regular database for models, auth, etc.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'bigquery': {
        'ENGINE': 'django_bq',
        'PROJECT': 'your-gcp-project-id',
        'CREDENTIALS': None,  # Uses default credentials, or provide a credentials object
        'LOCATION': 'us-central1',  # Optional: BigQuery location
        'NAME': 'your-bigquery-dataset-name'
    }
}
```

## Authentication

You can provide credentials in three ways:

1. Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your service account JSON file:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
   ```

2. Pass a credentials object in the settings:
   ```python
   from google.oauth2 import service_account
   credentials = service_account.Credentials.from_service_account_file(
       '/path/to/your/service-account-file.json',
   )

   DATABASES = {
       'bigquery': {
           'ENGINE': 'django_bq',
           'PROJECT': 'your-gcp-project-id',
           'CREDENTIALS': credentials,
           'NAME': 'your-bigquery-dataset-name'
       }
   }
   ```

3. Use Application Default Credentials (ADC) by setting CREDENTIALS to None.

## Usage Examples

### Direct SQL Queries

```python
from django.db import connections

# Using the BigQuery connection
with connections['bigquery'].cursor() as cursor:
    cursor.execute("SELECT * FROM `your-project.dataset.table` LIMIT 10")
    results = cursor.fetchall()
    for row in results:
        print(row)
```

### Using Django Models

1. Define models with BigQuery tables:

```python
from django.db import models

class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        managed = False  # Important: we don't want Django to create/modify tables
        db_table = 'customers'  # Your BigQuery table name
```

2. Query using Django ORM:

```python
# Get all records
customers = Customer.objects.using('bigquery').all()

# Filter records
active_customers = Customer.objects.using('bigquery').filter(
    status='active',
    registration_date__gte='2023-01-01'
)

# Aggregate functions
from django.db.models import Count, Avg
customer_stats = Customer.objects.using('bigquery').values('country').annotate(
    count=Count('id'),
    avg_purchases=Avg('purchase_count')
)
```

## Limitations

- Read-only operations only (no INSERT, UPDATE, DELETE)
- Regular expression operations need improvements
- Some Django ORM features may not be fully supported
- Complex JOIN operations may not work as expected

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE) file for details.
