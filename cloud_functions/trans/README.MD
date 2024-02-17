# Python: module main

## Modules
- [google.cloud.aiplatform](https://googleapis.dev/python/aiplatform/latest/index.html)
- [google.cloud.bigquery](https://googleapis.dev/python/bigquery/latest/index.html)
- [functions_framework](https://functions-framework.readthedocs.io/en/latest/)
- [os](https://docs.python.org/3/library/os.html)
- [requests](https://docs.python-requests.org/en/latest/)

## Functions

### `batch_embeddings() -> None`
Perform batch embeddings by submitting a batch prediction job to AI Platform Prediction.
This function sends a POST request to submit a batch prediction job for embedding generation.
The job processes input data from a BigQuery table and stores the embeddings in another BigQuery table.

### `create_index(project_number: str) -> None`
Create an index for job postings.
Args:
- `project_number` (str): Google Cloud project number.

### `deploy_index(project_number: str, index_id: str) -> None`
Deploy an index to the Matching Engine Index Endpoint.
Args:
- `project_number` (str): Google Cloud project number.
- `index_id` (str): ID of the index to deploy.

### `export_to_gcs() -> None`
Export data from BigQuery table to Google Cloud Storage in JSON format.
This function exports the content of a BigQuery table to a specified Cloud Storage location in newline-delimited JSON format.

### `get_default_token() -> str`
Get the default access token using Google Cloud Platform credentials.
Returns:
- `str`: Access token obtained from credentials.

### `get_weighted_embeddings() -> bool`
Calculate weighted embeddings for each job and store the results in a BigQuery table.
This function defines a JavaScript UDF (User-Defined Function) to perform the weighted averaging
of chunk embeddings and then executes a BigQuery query to create a table with the calculated
weighted embeddings.
Returns:
- `bool`: True if the operation is successful, False otherwise.

### `trans(request: flask.wrappers.Request) -> str`
Handle incoming HTTP requests for various processing modes.
Args:
- `request` (Request): The incoming HTTP request.
Returns:
- `str`: Response message.

### `trans_job_posts() -> bool`
Transform job posts by chunking the description text and store the results in a BigQuery table.
This function defines a JavaScript UDF (User-Defined Function) to split the input description text
into chunks based on the specified maximum chunk size. It then executes a BigQuery query to create
a table with the transformed job posts.
Returns:
- `bool`: True if the operation is successful, False otherwise.

## Data
- `Dict` = `typing.Dict`