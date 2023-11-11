import functions_framework
import os
import re
import uuid
from googleapiclient.discovery import build
import google.auth
import google.auth.transport.requests
from googleapiclient.errors import HttpError

def create_folder(folder_id):

  try:
    credentials = get_credentials()
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = {
        "name": folder_id,
        "parents" : ["1a9J_mtwKMN96jS54pqTfx9rUEutFQ6rE"],
        "mimeType": "application/vnd.google-apps.folder",
    }

    file = service.files().create(body=file_metadata, fields="id").execute()
    print(f'Folder ID: "{file.get("id")}".')
    return file.get("id")

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None

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
    if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
        request_json = request.get_json(silent=True)
        print(request_json)
        if "sessionInfo" in request_json and "session" in request_json["sessionInfo"]:
            session_id_regex = r".+\/sessions\/(.+)"
            session = request_json["sessionInfo"]["session"]
            regex_match = re.search(session_id_regex, session)
            session_id = regex_match.group(1)
        if "fulfillmentInfo" in request_json and "tag" in request_json["fulfillmentInfo"] and session_id:
            tag = request_json["fulfillmentInfo"]["tag"]
            if tag == "create_folder":
                folder_id = create_folder(session_id)

        if "test" in request_json:
            watch_changes("1a9J_mtwKMN96jS54pqTfx9rUEutFQ6rE")
    return 'OK'