import functions_framework
import os
from google.cloud import bigquery

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
    LANGUAGE js AS {js_udf};
    CREATE OR REPLACE TABLE `{destination_table}` AS
    SELECT
    chunk.job_id AS job_id,
    chunk.chunk_content AS content,
    chunk.chunk_size AS chunk_size,
    chunk.is_split AS is_split
    FROM
    `{source_table}`,
    UNNEST(get_chunks(job_id, description, {chonk_size})) AS chunk
    LIMIT 10;
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

@functions_framework.http
def trans(request):
    request_json = request.get_json(silent=True)
    print(request_json)
    if "mode" in request_json and request_json["mode"] == "embedding":
        trans_job_posts()
    if "mode" in request_json and request_json["mode"] == "datastore":
        print("datastore")
    return 'OK'