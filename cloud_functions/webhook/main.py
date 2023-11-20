import functions_framework
import os
import re
import uuid
import json
import textract
import en_core_web_sm
import requests
from google.cloud import bigquery
from googleapiclient.discovery import build
import google.auth
import google.auth.transport.requests
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.cloud import aiplatform
from vertexai.preview.language_models import TextEmbeddingModel

def get_job_details(matches):
	job_ids = matches.keys()
	jobs_table_id = os.environ.get("JOBS_TABLE_ID")
	client = bigquery.Client()
	query = f'''
	SELECT
	job_id,
	title,
	formatted_work_type,
	description,
	max_salary,
	min_salary,
	pay_period,
	views,
	applies,
	location
	FROM
	`{jobs_table_id}`
	WHERE
	job_id IN UNNEST({job_ids})
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
			print('Unable to get BigQuery results: ' + e.message)
		else:
			print('Unable to get BigQuery results: ' + str(e))

def get_matches(vector):
	match_threshold = os.environ.get("MATCH_THRESHOLD")
	aiplatform.init(project="ml-spez-ccai", location="us-central1")
	my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name='8350381794633187328')
	response = my_index_endpoint.find_neighbors(
		deployed_index_id = "job_posting_deployed_index",
		queries = [vector],
		num_neighbors = 10
	)
	matches = {}
	if len(response[0])>0:
		for id, neighbor in enumerate(response[0]):
			if neighbor.distance>= float(match_threshold):
				matches[neighbor.id] = neighbor.distance
	return matches

def get_text_embedding(text) -> list:
    """Text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")
    embeddings = model.get_embeddings([text])
    for embedding in embeddings:
        vector = embedding.values
        print(f"Length of Embedding Vector: {len(vector)}")
    return vector

def get_token_count(content,model):
	if model == "textembedding-gecko":
		body = {
		"instances": [
			{ "content": content}
		],
		}
	else:
		body = {
		"instances": [
			{ "prompt": content}
		],
		}
	request_body = json.dumps(body)
	endpoint = f"https://us-central1-aiplatform.googleapis.com/v1beta1/projects/ml-spez-ccai/locations/us-central1/publishers/google/models/{model}:countTokens"
	access_token = get_default_token()
	auth = "Bearer " + access_token

	# Create the headers with the Authorization header
	headers = {
		'Authorization': auth,
		'Content-Type': 'application/json; charset=utf-8'
	}

	# Send the POST request with JSON data
	response = requests.post(endpoint, headers=headers, data=request_body)
	#print(response)
	if response.status_code == 200:
		response_json = response.json()
		print('Response content:', response_json)
		return int(response_json["totalTokens"])
	else:
		print(response)
		print(f'POST request failed with status code {response.status_code}')
		return None

def get_default_token():
	CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
	credentials, project_id = google.auth.default(scopes=CREDENTIAL_SCOPES)
	request = google.auth.transport.requests.Request()
	credentials.refresh(request)
	access_token = credentials.token
	print('Access token: ', access_token)
	return credentials.token

def get_sentences(text):
	text = text.replace('\n', ' ').replace('\r', '')
	nlp = en_core_web_sm.load()
	doc = nlp(text)
	return_sentences = []
	for sent in doc.sents:
		string_sentence = str(sent)
		string_sentence = re.sub("\s\s+", " ", string_sentence)
		if string_sentence != " ":
			#print("Sentence: ", string_sentence)
			return_sentences.append(string_sentence)
	print('Total number of sentences: ', len(return_sentences))
	return_text = ('\n').join(return_sentences)
	return return_text

def get_txt(path):
    try:
        text = textract.process(path)
        text = text.decode("utf8")
        return text
    except Exception as e:
        print(e.message)
        return None

def download_file(folder_id,file_name):
	try:
		credentials = get_credentials()
		service = build('drive', 'v3', credentials=credentials)
		response = service.files().list(
			q=f"'{folder_id}' in parents and trashed=false",
			fields='files(id, name)'
		).execute()

		# Print details of each file in the folder
		files = response.get('files', [])
		for file in files:
			if file["name"] == file_name:
				file_id = file["id"]
		# Download the file
		request = service.files().get_media(fileId=file_id)
		file_path = os.path.join("/tmp/", file_name)
		with open(file_path, 'wb') as file:
			downloader = MediaIoBaseDownload(file, request)
			done = False
			while done is False:
				_, done = downloader.next_chunk()

		print(f"File downloaded to: {file_path}")
		return file_path
	except HttpError as error:
		print(f"An error occurred: {error}")
		return None

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
	#print(dict(request.headers))
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
		if "pageInfo" in request_json and "formInfo" in request_json["pageInfo"] and "parameterInfo" in request_json["pageInfo"]["formInfo"]:
			page_parameters = request_json["pageInfo"]["formInfo"]["parameterInfo"]
		else:
			page_parameters = []
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
				if len(files) == 0:
					text = "I was unable to find any files."
					resume_folder_link = session_parameters["resume_folder_link"]
					html =  f'''
					<p>Please use this folder to upload a copy of your resume.</p>
					<p><a href="{resume_folder_link}" target="_blank">Upload Your Resume</a></p>
					<p>Please click the button below once done.</p>
					'''
					json_response = {
							'fulfillment_response': {
								'messages': [
									{"text": {"text": [text]}},
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
					options = []
					text = "Please click on the file name to process."
					for file in files:
						option_text = "Filename: "+file["name"]
						options.append({
							"type": "chips",
							"options": [
								{
								"text": option_text
								}
							]
						})
					json_response = {
							"page_info": {
										"form_info": {
											"parameter_info": [
												{
													"displayName": "files_displayed",
													"required": False,
													"state": "VALID",
													"value": True,
												},
											],
										},
									},
							'fulfillment_response': {
								'messages': [
									{"text": {"text": [text]}},
									{
										'payload': {
											'richContent': [options]
										}
									}
								]
							}
						}
				return json_response
			if tag == "file_confirmed":
				for parameter in page_parameters:
					if parameter["displayName"] == "files_displayed" and parameter["value"] == True:
						file_name = request_json["text"][10:]
						resume_folder_id = session_parameters["resume_folder_id"]
						file_path = download_file(resume_folder_id, file_name)
						if file_path:
							text = get_txt(file_path)
						if text:
							content = get_sentences(text)
							token_count = get_token_count(content,"textembedding-gecko")
							if token_count and token_count<3072:
								vector = get_text_embedding(text)
								matches = get_matches(vector)
								job_details = get_job_details(matches)
								options = []
								text = ''
								for job in job_details:
									match_percent = round(float(matches[job.job_id])*100, 2)
									text = f"Profile Match: {match_percent}%"
									if job.formatted_work_type:
										text = text + f"\nWork Type: {job.formatted_work_type}"
									if job.min_salary:
										text = text + f"\nMinimum Salary: {job.min_salary}"
									if job.max_salary:
										text = text + f"\nMaximum Salary: {job.max_salary}"
									if job.pay_period:
										text = text + f"\nPay Period: {job.pay_period}"

									options.append(
										{
											"type": "accordion",
											"title": job.title,
											"subtitle": job.location,
											"text": text
										}
									)
								json_response = {
									'fulfillment_response': {
										'messages': [
											{
												'payload': {
													'richContent': [options]
												}
											}
										]
									}
								}
				return json_response



	return 'OK'