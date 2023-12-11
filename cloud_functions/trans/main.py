import functions_framework
import os
import requests
from flask import Request
from flask import jsonify
from typing import Dict
from google.cloud import bigquery
import google.auth
import google.auth.transport.requests
from google.cloud import aiplatform

def create_index(project_number: str) -> None:
    """
    Create an index for job postings.

    Args:
        project_number (str): Google Cloud project number.

    Returns:
        None
    """
    endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_number}/locations/us-central1/indexes"
    request_body = {
        "display_name": "job_posting_index",
        "metadata": {
            "contentsDeltaUri": "gs://" + os.environ["DATASET_BUCKET"],
            "config": {
                "dimensions": 768,
                "approximateNeighborsCount": 10,
                "shardSize": "SHARD_SIZE_SMALL",
                "algorithm_config": {
                    "treeAhConfig": {
                        "leafNodeEmbeddingCount": 1000,
                        "leafNodesToSearchPercent": 10
                    }
                }
            }
        }
    }
    access_token = get_default_token()  # Assuming get_default_token is defined elsewhere
    auth = "Bearer " + access_token

    # Create the headers with the Authorization header
    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json; charset=utf-8'
    }

    # Send the POST request with JSON data
    response = requests.post(endpoint, headers=headers, json=request_body)

    if response.status_code == 200:
        print('POST request was successful')
        print('Response content:', response.text)
    else:
        print(f'POST request failed with status code {response.status_code}')

def deploy_index(project_number: str, index_id: str) -> None:
    """
    Deploy an index to the Matching Engine Index Endpoint.

    Args:
        project_number (str): Google Cloud project number.
        index_id (str): ID of the index to deploy.

    Returns:
        None
    """
    # Create `IndexEndpoint`
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
        display_name="job_posting_index_endpoint",
        public_endpoint_enabled=True
    )

    # Create `MatchingEngineIndex` using the provided index_id
    index_path = f'projects/{project_number}/locations/us-central1/indexes/{index_id}'
    my_index = aiplatform.MatchingEngineIndex(index_name=index_path)

    # Deploy the Index to the Index Endpoint
    DEPLOYED_INDEX_ID = "job_posting_deployed_index"
    my_index_endpoint.deploy_index(
        index=my_index,
        deployed_index_id=DEPLOYED_INDEX_ID,
        machine_type="e2-standard-2",
        min_replica_count=1,
        max_replica_count=1
    )

def get_default_token() -> str:
    """
    Get the default access token using Google Cloud Platform credentials.

    Returns:
        str: Access token obtained from credentials.
    """
    # Define the required OAuth scopes
    CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

    # Obtain default credentials with specified scopes
    credentials, project_id = google.auth.default(scopes=CREDENTIAL_SCOPES)

    # Create a request object for token refresh
    request = google.auth.transport.requests.Request()

    # Refresh the credentials to obtain a new access token
    credentials.refresh(request)

    # Access token obtained from refreshed credentials
    access_token = credentials.token

    return credentials.token

def export_to_gcs() -> None:
    """
    Export data from BigQuery table to Google Cloud Storage in JSON format.

    This function exports the content of a BigQuery table to a specified Cloud Storage location
    in newline-delimited JSON format.

    Returns:
        None
    """
    # Create a BigQuery client
    client = bigquery.Client()

    # Retrieve the Cloud Storage bucket from environment variable
    dataset_bucket = os.environ["DATASET_BUCKET"]

    # Specify the destination URI for the exported data
    destination_uri = "gs://{}/{}".format(dataset_bucket, "embeddings.json")

    # Define the dataset reference
    dataset_ref = bigquery.DatasetReference("ml-spez-ccai", "processed")

    # Define the table reference within the dataset
    table_ref = dataset_ref.table("weighted_embeddings")

    # Configure the export job
    job_config = bigquery.job.ExtractJobConfig()
    job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON

    # Initiate the extract job to export data to Cloud Storage
    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        job_config=job_config,
        # Location must match that of the source table.
        location="us-central1",
    )  # API request

    # Wait for the export job to complete
    extract_job.result()

def get_weighted_embeddings() -> bool:
    """
    Calculate weighted embeddings for each job and store the results in a BigQuery table.

    This function defines a JavaScript UDF (User-Defined Function) to perform the weighted averaging
    of chunk embeddings and then executes a BigQuery query to create a table with the calculated
    weighted embeddings.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    # Create a BigQuery client
    client = bigquery.Client()

    # Define the JavaScript UDF for weighted embeddings calculation
    js_udf = '''
    if (is_split_array.includes(false)){
        return chunk_embeddings[0];
    }
    if (chunk_embeddings.length !== chunk_lens.length) {
        return [];
    }

    var weights_sum = chunk_lens.reduce((a, b) => a + b, 0);

    var result = chunk_embeddings[0].map((_, i) =>
        chunk_embeddings.reduce((sum, arr, k) => sum + arr[i] * chunk_lens[k] / weights_sum, 0)
    );
    return result;
    '''

    # Construct the BigQuery query to create a table with weighted embeddings
    query = f'''
    CREATE TEMP FUNCTION
    weighted_embeddings(chunk_embeddings ARRAY<JSON>, chunk_lens ARRAY<INT64>, is_split_array ARRAY<BOOL>)
    RETURNS ARRAY<FLOAT64>
    LANGUAGE js AS \'''{js_udf}\''';

    CREATE OR REPLACE TABLE
    `ml-spez-ccai.processed.weighted_embeddings` AS
    SELECT
        job_id AS id,
        weighted_embeddings(ARRAY_AGG(predictions[0].embeddings.values), ARRAY_AGG(chunk_size), ARRAY_AGG(is_split)) AS embedding
    FROM
        `ml-spez-ccai.processed.embeddings`
    WHERE
        content != ""
    GROUP BY
        job_id;
    '''

    # Execute the BigQuery query
    query_job = client.query(query)

    try:
        results = query_job.result()  # Waits for job to complete.
        return True
    except Exception as e:
        if hasattr(e, 'message'):
            print('Unable to get BigQuery results: ' + e.message)
        else:
            print('Unable to get BigQuery results: ' + str(e))
        return False

def trans_job_posts() -> bool:
    """
    Transform job posts by chunking the description text and store the results in a BigQuery table.

    This function defines a JavaScript UDF (User-Defined Function) to split the input description text
    into chunks based on the specified maximum chunk size. It then executes a BigQuery query to create
    a table with the transformed job posts.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    # Create a BigQuery client
    client = bigquery.Client()

    # Get environment variables
    source_table = os.environ["SOURCE_TABLE"]
    destination_table = os.environ["DESTINATION_TABLE"]
    chunk_size = os.environ["CHUNK_SIZE"]

    # Define the JavaScript UDF for chunking
    js_udf = """
    var input = input_string;
    var maxChunkSize = max_chunk_size;
    var chunks = [];
    if(input.length > maxChunkSize) {
        while (input.length > 0) {
            // Find the last period (.) within the maximum chunk size
            var lastPeriodIndex = input.lastIndexOf('.', maxChunkSize);

            if (lastPeriodIndex <= 0 || lastPeriodIndex > maxChunkSize) {
                // If no period is found within the chunk size, split at the chunk size
                lastPeriodIndex = maxChunkSize;
            }

            // Extract the chunk
            var chunk = input.substring(0, lastPeriodIndex + 1);

            // Remove the extracted chunk from the input
            input = input.substring(lastPeriodIndex + 1);

            // Trim leading and trailing whitespace
            chunk = chunk.trim();

            // Push the chunk to the result array
            chunks.push({
                "job_id": job_id,
                "chunk_content": chunk,
                "chunk_size": chunk.length,
                "is_split": true
            });
        }
    } else {
        chunks = [{
            "job_id": job_id,
            "chunk_content": input,
            "chunk_size": input.length,
            "is_split": false
        }];
    }
    return chunks;
    """

    # Construct the BigQuery query to create a table with transformed job posts
    query = f'''
    CREATE TEMP FUNCTION get_chunks(job_id STRING, input_string STRING, max_chunk_size INT64)
    RETURNS ARRAY<STRUCT<job_id STRING, chunk_content STRING, chunk_size INT64, is_split BOOL>>
    LANGUAGE js AS \'''{js_udf}\''';

    CREATE OR REPLACE TABLE `{destination_table}` AS
    SELECT
        chunk.job_id AS job_id,
        chunk.chunk_content AS content,
        chunk.chunk_size AS chunk_size,
        chunk.is_split AS is_split
    FROM
        `{source_table}`,
        UNNEST(get_chunks(job_id, description, {chunk_size})) AS chunk
    WHERE
        description IS NOT NULL;
    '''

    # Execute the BigQuery query
    query_job = client.query(query)

    try:
        results = query_job.result()  # Waits for job to complete.
        return True
    except Exception as e:
        if hasattr(e, 'message'):
            print('Unable to get BigQuery results: ' + e.message)
        else:
            print('Unable to get BigQuery results: ' + str(e))
        return False

def batch_embeddings() -> None:
    """
    Perform batch embeddings by submitting a batch prediction job to AI Platform Prediction.

    This function sends a POST request to submit a batch prediction job for embedding generation.
    The job processes input data from a BigQuery table and stores the embeddings in another BigQuery table.

    Note: The function assumes the existence of the `get_default_token()` function.

    Returns:
        None
    """
    # Get the access token
    access_token = get_default_token()
    auth = "Bearer " + access_token

    # Define the URL for batch prediction jobs
    url = 'https://us-central1-aiplatform.googleapis.com/v1/projects/ml-spez-ccai/locations/us-central1/batchPredictionJobs'

    # Create the headers with the Authorization header
    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json; charset=utf-8'
    }

    # Define data to be sent as JSON for the batch prediction job
    data = {
        "name": "Batch-Embeddings",
        "displayName": "Batch-Embeddings",
        "model": "publishers/google/models/textembedding-gecko",
        "inputConfig": {
            "instancesFormat": "bigquery",
            "bigquerySource": {
                "inputUri": "bq://ml-spez-ccai.processed.chonks"
            }
        },
        "outputConfig": {
            "predictionsFormat": "bigquery",
            "bigqueryDestination": {
                "outputUri": "bq://ml-spez-ccai.processed.embeddings"
            }
        }
    }

    # Send the POST request with JSON data
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print('POST request was successful')
        print('Response content:', response.text)
    else:
        print(response)
        print(f'POST request failed with status code {response.status_code}')

@functions_framework.http
def trans(request: Request) -> str:
    """
    Handle incoming HTTP requests for various processing modes.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        str: Response message.
    """
    request_json: Dict[str, str] = request.get_json(silent=True)

    if "mode" in request_json:
        if request_json["mode"] == "generate_embeddings":
            split_descriptions = trans_job_posts()
            if split_descriptions:
                batch_embeddings()

        if request_json["mode"] == "export_embeddings":
            weighted_embeddings = get_weighted_embeddings()
            if weighted_embeddings:
                export_to_gcs()

        if "project_number" in request_json and request_json["mode"] == "create_index":
            project_number = request_json["project_number"]
            create_index(project_number)

        if "index_id" in request_json and "project_number" in request_json and request_json["mode"] == "deploy_index":
            index_id = request_json["index_id"]
            project_number = request_json["project_number"]
            deploy_index(project_number, index_id)

    return 'OK'