import functions_framework
import os
import re
import uuid
from googleapiclient.discovery import build
import google.auth
import google.auth.transport.requests
from googleapiclient.errors import HttpError

def get_folder_contents(folder_id):

  try:
    credentials = get_credentials()
    service = build('drive', 'v3', credentials=credentials)
    response = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields='files(id, name)'
    ).execute()

    # Print details of each file in the folder
    files = response.get('files', [])
    return files

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None


def create_folder(name, root):

  try:
    credentials = get_credentials()
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = {
        "name": name,
        "parents" : [root],
        "mimeType": "application/vnd.google-apps.folder",
    }

    file = service.files().create(body=file_metadata, fields="id").execute()
    folder_id = file.get("id")
    permission = {
        'type': 'anyone',
        'role': 'writer'
    }
    permission_result = service.permissions().create(
        fileId=folder_id,
        body=permission,
        fields='id'
    ).execute()

    public_link = f'https://drive.google.com/drive/folders/{folder_id}?usp=sharing'
    return folder_id, public_link

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
    root_folder_id = os.environ.get("ROOT_FOLDER_ID")
    if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
        request_json = request.get_json(silent=True)
        print(request_json)
        if "sessionInfo" in request_json and "session" in request_json["sessionInfo"]:
            session_info = request_json["sessionInfo"]
            if "parameters" in session_info:
                session_parameters = session_info["parameters"]
            else:
               session_parameters = {}
            session_id_regex = r".+\/sessions\/(.+)"
            session = request_json["sessionInfo"]["session"]
            regex_match = re.search(session_id_regex, session)
            session_id = regex_match.group(1)
        if "fulfillmentInfo" in request_json and "tag" in request_json["fulfillmentInfo"] and session_id:
            tag = request_json["fulfillmentInfo"]["tag"]
            if tag == "create_folder":
                if "folders_created" not in session_parameters:
                    session_folder_id, session_folder_link = create_folder(session_id, root_folder_id)
                    resume_folder_id, resume_folder_link = create_folder("Resumes", session_folder_id)
                    cl_folder_id, cl_folder_link = create_folder("Cover Letters", session_folder_id)
                    matches_folder_id, matches_folder_link = create_folder("Matching Jobs", session_folder_id)
                    #watch_changes(folder_id)
                    html =  f'''
                    <p>Please use this folder to upload a copy of your resume.</p>
                    <p><a href="{resume_folder_link}" target="_blank">Upload Your Resume</a></p>
                    <p>Please click the button below once done.</p>
                    '''
                    json_response = {
                        "sessionInfo": {
                            "parameters": {
                                "folders_created": True,
                                "session_folder_id": session_folder_id,
                                "session_folder_link": session_folder_link,
                                "resume_folder_id": resume_folder_id,
                                "resume_folder_link": resume_folder_link,
                                "cl_folder_id": cl_folder_id,
                                "cl_folder_link": cl_folder_link,
                                "matches_folder_id": matches_folder_id,
                                "matches_folder_link": matches_folder_link
                            },
                        },
                        'fulfillment_response': {
                            'messages': [
                                {
                                    'payload': {
                                        'richContent': [
                                            [
                                                {
                                                    "type": "html",
                                                    "html": html
                                                },
                                                {
                                                    "type": "chips",
                                                    "options": [
                                                    {
                                                        "text": "I have uploaded the file"
                                                    }
                                                ]
                                                }
                                            ]
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                else:
                    resume_folder_link = session_parameters["resume_folder_link"]
                    html =  f'''
                    <p>Please use this folder to upload a copy of your resume.</p>
                    <p><a href="{resume_folder_link}" target="_blank">Upload Your Resume</a></p>
                    <p>Please click the button below once done.</p>
                    '''
                    json_response = {
                        'fulfillment_response': {
                            'messages': [
                                {
                                    'payload': {
                                        'richContent': [
                                            [
                                                {
                                                    "type": "html",
                                                    "html": html
                                                },
                                                {
                                                    "type": "chips",
                                                    "options": [
                                                    {
                                                        "text": "I have uploaded the file"
                                                    }
                                                ]
                                                }
                                            ]
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                return json_response
            if tag == "file_uploaded":
                resume_folder_id = session_parameters["resume_folder_id"]
                files = get_folder_contents(resume_folder_id)
                options = []
                if len(files) == 0:
                    text = "I was unable to find any files. Please upload a file to the shared folder to continue."
                else:
                    text = "Please click on the file name to process."
                    for file in files:
                       options.append({"text": file["name"]})

                json_response = {
                        'fulfillment_response': {
                            'messages': [
                                {"text": {"text": [text]}},
                                {
                                    'payload': {
                                        'richContent': [
                                            [
                                                {
                                                    "type": "chips",
                                                    "options": options
                                                }
                                            ]
                                        ]
                                    }
                                }
                            ]
                        }
                    }


    return 'OK'