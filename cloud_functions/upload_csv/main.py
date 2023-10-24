import functions_framework
import os
import csv
from google.cloud import bigquery
from google.cloud import storage

# Construct a BigQuery client object.
client = bigquery.Client()

# Construct a Storage client object.
storage_client = storage.Client()

# Triggered by a change in a storage bucket.
@functions_framework.cloud_event
def upload_csv(cloud_event):
    data = cloud_event.data
    file_name = data["name"].split("/")[-1]
    uri = "gs://"+data["bucket"]+"/"+data["name"]
    bucket = storage_client.bucket(data["bucket"])
    project_id = os.environ.get("PROJECT_ID")
    dataset_id = os.environ.get("DATASET_ID")
    table_name = file_name.split(".")[0]
    csv_local = '/tmp/'+file_name
    if int(data["size"])>0 and file_name and file_name != "":
        table_id = project_id + "." + dataset_id + "."+ table_name
        blob = bucket.blob(data["name"])
        blob.download_to_filename(csv_local)
        with open(csv_local, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',')
            errors = client.insert_rows_json(table_id, csv_reader)  # Make an API request.
            if errors == []:
                print("New rows have been added.")
            else:
                print("Encountered errors while inserting rows: {}".format(errors))
    return 'OK'