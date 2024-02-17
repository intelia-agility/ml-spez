import functions_framework
import os
from google.cloud import bigquery
# Construct a BigQuery client object.
client = bigquery.Client()
# Triggered by a change in a storage bucket.
@functions_framework.cloud_event
def upload_csv(cloud_event: dict) -> str:
    """
    Upload CSV file to BigQuery table.

    Args:
        cloud_event (dict): Cloud event data.

    Returns:
        str: Status of the upload process.
    """
    data = cloud_event.data
    file_name = data["name"].split("/")[-1]
    uri = "gs://" + data["bucket"] + "/" + data["name"]
    project_id = os.environ.get("PROJECT_ID")
    dataset_id = os.environ.get("DATASET_ID")
    table_name = file_name.split(".")[0]

    if int(data["size"]) > 0 and file_name and file_name != "":
        table_id = f"{project_id}.{dataset_id}.{table_name}"
        job_config = bigquery.LoadJobConfig(
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
            allow_jagged_rows=True,
            allow_quoted_newlines=True
        )
        client = bigquery.Client()
        load_job = client.load_table_from_uri(
            uri, table_id, job_config=job_config
        )  # Make an API request.
        load_job.result()  # Waits for the job to complete.
        destination_table = client.get_table(table_id)  # Make an API request.
        print("Total {} rows in table".format(destination_table.num_rows))
        return 'OK'
    else:
        return 'File size is zero or file name is empty.'