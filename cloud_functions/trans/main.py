import functions_framework
import os
from google.cloud import bigquery
# Construct a BigQuery client object.
client = bigquery.Client()
# Triggered by a change in a storage bucket.
@functions_framework.http
def trans(request):
    request_json = request.get_json(silent=True)
    print(request_json)
    if "mode" in request_json and request_json["mode"] == "embedding":
        print("embedding")
    if "mode" in request_json and request_json["mode"] == "datastore":
        print("datastore")
    return 'OK'