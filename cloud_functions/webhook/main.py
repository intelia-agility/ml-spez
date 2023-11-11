import functions_framework
import os
import uuid
from googleapiclient.discovery import build
import google.auth
import google.auth.transport.requests

def get_credentials():
  CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform","https://www.googleapis.com/auth/drive"]
  credentials, project_id = google.auth.default(scopes=CREDENTIAL_SCOPES)
  return credentials

def watch_changes(folder_id):
    credentials = get_credentials()
    service = build('drive', 'v3', credentials=credentials)

    # Create a watch request for the folder
    watch_request = {
        'id': str(uuid.uuid4()),
        'type': 'web_hook',
        'address': 'https://us-central1-ml-spez-ccai.cloudfunctions.net/webhook',
        'payload': True
    }

    watch_response = service.files().watch(fileId=folder_id, body=watch_request).execute()

    print("Watch Request Response:", watch_response)

@functions_framework.http
def webhook(request):
    print(dict(request.headers))
    if request.headers['Content-Type'] == 'application/json':
        request_json = request.get_json(silent=True)
        print(request_json)
        if "test" in request_json:
            watch_changes("1a9J_mtwKMN96jS54pqTfx9rUEutFQ6rE")
    return 'OK'