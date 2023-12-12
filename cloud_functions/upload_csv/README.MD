# Python: module main

## Modules
- [google.cloud.bigquery](https://googleapis.dev/python/bigquery/latest/index.html)
- [functions_framework](https://functions-framework.readthedocs.io/en/latest/)
- [os](https://docs.python.org/3/library/os.html)

## Functions

### `upload_csv(cloud_event: dict) -> str`
Upload CSV file to BigQuery table.
Args:
- `cloud_event` (dict): Cloud event data.
Returns:
- `str`: Status of the upload process.

## Data
- `client` = `<google.cloud.bigquery.client.Client object>`