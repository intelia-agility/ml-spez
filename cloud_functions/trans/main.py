import functions_framework
import os
import requests
from google.cloud import bigquery
import google.auth
import google.auth.transport.requests
from google.cloud import aiplatform

def create_index():
    aiplatform.init(project="ml-spez-ccai", location="us-central1")
    # create Index
    my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name = "job_posting_index",
        contents_delta_uri = "gs://"+ os.environ["DATASET_BUCKET"],
        dimensions = 768,
        approximate_neighbors_count = 10,
    )

def deploy_index(index_id):
    ## create `IndexEndpoint`
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
        display_name = "job_posting_index_endpoint",
        public_endpoint_enabled = False
    )
    # deploy the Index to the Index Endpoint
    DEPLOYED_INDEX_ID = "job_posting_deployed_index"
    my_index_endpoint.deploy_index(
        index = index_id,
        deployed_index_id = DEPLOYED_INDEX_ID,
        machine_type="e2-standard-2",
        min_replica_count=0,
        max_replica_count=0
    )

def get_default_token():
  CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
  credentials, project_id = google.auth.default(scopes=CREDENTIAL_SCOPES)
  request = google.auth.transport.requests.Request()
  credentials.refresh(request)
  access_token = credentials.token
  print('Access token: ', access_token)
  return credentials.token

def export_to_gcs():
    client = bigquery.Client()
    dataset_bucket = os.environ["DATASET_BUCKET"]
    destination_uri = "gs://{}/{}".format(dataset_bucket, "embeddings.json")
    dataset_ref = bigquery.DatasetReference("ml-spez-ccai", "processed")
    table_ref = dataset_ref.table("weighted_embeddings")
    job_config = bigquery.job.ExtractJobConfig()
    job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        job_config=job_config,
        # Location must match that of the source table.
        location="us-central1",
    )  # API request
    extract_job.result()  # Waits for job to complete.


def get_weighted_embeddings():
    client = bigquery.Client()
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
    query = f'''
    CREATE TEMP FUNCTION
    weighted_embeddings(chunk_embeddings ARRAY<JSON>,chunk_lens ARRAY<INT64>,is_split_array ARRAY<BOOL>)
    RETURNS ARRAY<FLOAT64>
    LANGUAGE js AS \'''{js_udf}\''';
    CREATE OR REPLACE TABLE
    `ml-spez-ccai.processed.weighted_embeddings` AS
    SELECT
    job_id AS id,
    weighted_embeddings(ARRAY_AGG(predictions[0].embeddings.values),ARRAY_AGG(chunk_size),ARRAY_AGG(is_split)) AS embedding
    FROM
    `ml-spez-ccai.processed.embeddings`
    WHERE
    content != ""
    GROUP BY
    job_id;
    '''
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

def trans_job_posts():
    client = bigquery.Client()
    source_table = os.environ["SOURCE_TABLE"]
    destination_table = os.environ["DESTINATION_TABLE"]
    chonk_size = os.environ["CHONK_SIZE"]
    js_udf = """
    var input = input_string;
    var maxChunkSize = max_chunk_size;
    var chunks = [];
    if(input.length>maxChunkSize){
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
    }else{
    chunks =[{
        "job_id": job_id,
        "chunk_content": input,
        "chunk_size": input.length,
        "is_split": false
    }];
    }
    return chunks;

    """
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
    UNNEST(get_chunks(job_id, description, {chonk_size})) AS chunk
    WHERE
    description IS NOT NULL;
    '''
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

def batch_embeddings():

    access_token = get_default_token()
    auth = "Bearer " + access_token

    url = 'https://us-central1-aiplatform.googleapis.com/v1/projects/ml-spez-ccai/locations/us-central1/batchPredictionJobs'


    # Create the headers with the Authorization header
    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json; charset=utf-8'
    }

    # Data to be sent as JSON
    data = {
        "name": "Batch-Embeddings",
        "displayName": "Batch-Embeddings",
        "model": "publishers/google/models/textembedding-gecko",
        "inputConfig": {
        "instancesFormat":"bigquery",
        "bigquerySource":{
            "inputUri" : "bq://ml-spez-ccai.processed.chonks"
        }
        },
        "outputConfig": {
        "predictionsFormat":"bigquery",
        "bigqueryDestination":{
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
def trans(request):
    request_json = request.get_json(silent=True)
    print(request_json)
    if "mode" in request_json and request_json["mode"] == "generate_embeddings":
        split_descriptions = trans_job_posts()
        if split_descriptions:
            batch_embeddings()
    if "mode" in request_json and request_json["mode"] == "export_embeddings":
        export_to_gcs()
        '''
        weighted_embeddings = get_weighted_embeddings()
        if weighted_embeddings:
            export_to_gcs()
        '''
    if "mode" in request_json and request_json["mode"] == "create_index":
        create_index()
    if "mode" in request_json and "index_id" in request_json and request_json["mode"] == "deploy_index":
        index_id = request_json["index_id"]
        deploy_index(index_id)
    return 'OK'