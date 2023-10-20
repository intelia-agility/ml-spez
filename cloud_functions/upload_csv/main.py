import functions_framework
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def upload_csv(cloud_event):
    data = cloud_event.data
    print(data)
    '''
    file_paths = data["name"].split("/")
    if int(data["size"])>0 and len(file_paths)>1:
        table_name = file_paths[-2]
        table_id = "ap-exec-dashboard-poc.looker_dashboards."+table_name
        print("Table id is {}".format(table_id))
        uri = "gs://"+data["bucket"]+"/"+data["name"]
        job_config = bigquery.LoadJobConfig(
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
            max_bad_records=100
            )
        load_job = client.load_table_from_uri(
            uri, table_id, job_config=job_config
        )  # Make an API request.

        load_job.result()  # Waits for the job to complete.

        destination_table = client.get_table(table_id)  # Make an API request.
        print("Total {} rows in table".format(destination_table.num_rows))
    else:
        print("No table name present")
    print("Function execution finished.")
    '''