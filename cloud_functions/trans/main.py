import functions_framework
import os
import requests
from google.cloud import bigquery
from google.oauth2 import service_account

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
    UNNEST(get_chunks(job_id, description, {chonk_size})) AS chunk;
    '''
    query_job = client.query(query)
    result_data = []
    try:
        results = query_job.result()  # Waits for job to complete.
        for result in results:
            result_data.append(dict(result))
        return result_data
    except Exception as e:
        if hasattr(e, 'message'):
            print('Unable to get BigQuery location results: ' + e.message)
        else:
            print('Unable to get BigQuery location results: ' + str(e))

def batch_embeddings():

    credentials = service_account.Credentials()

    # Get the access token
    access_token = credentials.get_access_token().token
    url = 'https://us-central1-aiplatform.googleapis.com/v1/projects/ml-spez-ccai/locations/us-central1/batchPredictionJobs'


    print(access_token)
    '''
    # Create the headers with the Authorization header
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }

    # Data to be sent as JSON
    data = {
        "name": "test",
        "displayName": "test",
        "model": "publishers/google/models/textembedding-gecko",
        "inputConfig": {
        "instancesFormat":"bigquery",
        "bigquerySource":{
            "inputUri" : "bq://ml-spez-ccai.test_dataset.batch_test"
        }
        },
        "outputConfig": {
        "predictionsFormat":"bigquery",
        "bigqueryDestination":{
            "outputUri": "bq://ml-spez-ccai.test_dataset.test_results"
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
    '''
@functions_framework.http
def trans(request):
    request_json = request.get_json(silent=True)
    print(request_json)
    if "mode" in request_json and request_json["mode"] == "embedding":
        #trans_job_posts()
        batch_embeddings()
    if "mode" in request_json and request_json["mode"] == "datastore":
        print("datastore")
    return 'OK'