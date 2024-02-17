# Python: module main

## Modules
- [google.cloud.aiplatform](https://googleapis.dev/python/aiplatform/latest/index.html)
- [google.cloud.bigquery](https://googleapis.dev/python/bigquery/latest/index.html)
- [functions_framework](https://functions-framework.readthedocs.io/en/latest/)
- [google](https://googleapis.dev/python/google/latest/index.html)
- [json](https://docs.python.org/3/library/json.html)
- [os](https://docs.python.org/3/library/os.html)
- [re](https://docs.python.org/3/library/re.html)
- [requests](https://docs.python-requests.org/en/latest/)
- [uuid](https://docs.python.org/3/library/uuid.html)
- [vertexai](https://googleapis.dev/python/aiplatform/latest/index.html)
- [textract](https://textract.readthedocs.io/en/stable/)

## Functions

### `create_folder(name: str, root: str) -> Optional[Tuple[str, str]]`
Create a new folder in Google Drive with the specified name and parent folder.
Args:
- `name` (str): The name of the new folder.
- `root` (str): The ID of the parent folder where the new folder will be created.
Returns:
- `Optional[Tuple[str, str]]`: A tuple containing the ID of the created folder and a public link to the folder, or None if an error occurs.

### `delete_folders(folder_id: str) -> Optional[bool]`
Delete a folder from Google Drive based on its folder ID.
Args:
- `folder_id` (str): The ID of the folder to be deleted.
Returns:
- `Optional[bool]`: True if the folder is deleted successfully, None if an error occurs.

### `download_file(folder_id: str, file_name: str) -> Optional[str]`
Download a file from Google Drive given the folder ID and file name.
Args:
- `folder_id` (str): The ID of the Google Drive folder containing the file.
- `file_name` (str): The name of the file to be downloaded.
Returns:
- `Optional[str]`: The local file path where the file is downloaded, or None if an error occurs.

### `generate_cover_letter(resume_text: str, job_text: str) -> Optional[str]`
Generate a cover letter for a job opening based on a candidate's resume.
Args:
- `resume_text` (str): The text of the candidate's resume.
- `job_text` (str): The text of the job opening.
Returns:
- `Optional[str]`: The generated cover letter text or None if an error occurs.

### `get_credentials() -> Optional[google.oauth2.credentials.Credentials]`
Retrieve Google API credentials for the specified scopes.
Returns:
- `Optional[Credentials]`: Google API credentials, or None if an error occurs.

### `get_default_token() -> Optional[str]`
Get the default access token for Google Cloud Platform credentials.
Returns:
- `Optional[str]`: The access token if successful, None if an error occurs.

### `get_folder_contents(folder_id: str) -> Optional[List[Dict[str, str]]]`
Get the contents of a Google Drive folder given its ID.
Args:
- `folder_id` (str): The ID of the Google Drive folder.
Returns:
- `Optional[List[Dict[str, str]]]`: A list of dictionaries containing file details (id, name), or None if an error occurs.

### `get_job(job_id: str) -> Optional[Dict[str, str]]`
Retrieve job details from BigQuery based on the provided job ID.

#### Args:
- `job_id` (str): The ID of the job to retrieve.

#### Returns:
- `Optional[Dict[str, str]]`: A dictionary containing job details or None if an error occurs.

### `get_job_details(matches: Dict[str, float]) -> Optional[List[Dict[str, str]]]`
Retrieve job details from BigQuery based on a dictionary of job matches.

#### Args:
- `matches` (Dict[str, float]): A dictionary mapping job IDs to match percentages.

#### Returns:
- `Optional[List[Dict[str, str]]]`: A list of dictionaries containing job details, sorted by match percentage,
  or None if an error occurs.

### `get_matches(vector: List[float]) -> Dict[str, float]`
Get job matches based on a vector using a matching engine.

#### Args:
- `vector` (List[float]): The input vector for which matches are to be found.

#### Returns:
- `Dict[str, float]`: A dictionary mapping job IDs to match distances.

### `get_sentences(text: str) -> Optional[str]`
Tokenize the input text into sentences using a natural language processing library.

#### Args:
- `text` (str): The input text to be tokenized into sentences.

#### Returns:
- `Optional[str]`: The tokenized sentences joined into a single string, or None if an error occurs.

### `get_text_embedding(text: str) -> List[float]`
Get text embedding using a Large Language Model.

#### Args:
- `text` (str): The input text for which embedding is to be obtained.

#### Returns:
- `List[float]`: A list representing the text embedding.

### `get_token_count(content: str, model: str) -> Optional[int]`
Get the token count for the given content using a specified language model.

#### Args:
- `content` (str): The input text for which token count is to be obtained.
- `model` (str): The name of the language model (e.g., "textembedding-gecko").

#### Returns:
- `Optional[int]`: The total token count if successful, None if an error occurs.

### `get_txt_docx(path: str) -> Optional[str]`
Extract text content from a DOCX file using the python-docx library.

#### Args:
- `path` (str): The file path of the DOCX document.

#### Returns:
- `Optional[str]`: The extracted text content, or None if an error occurs.

### `get_txt_pdf(path: str) -> Optional[str]`
Extract text content from a PDF file using textract.

#### Args:
- `path` (str): The file path of the PDF document.

#### Returns:
- `Optional[str]`: The extracted text content, or None if an error occurs.

### `get_weighted_embeddings(chunk_embeddings: List[List[float]], chunk_lens: List[float]) -> List[float]`
Calculate the weighted average of embeddings based on chunk lengths.

#### Args:
- `chunk_embeddings` (List[List[float]]): List of chunk embeddings, where each inner list represents
    the embeddings for a chunk.
- `chunk_lens` (List[float]): List of chunk lengths used as weights for the weighted average.

#### Returns:
- `List[float]`: Weighted average embeddings based on chunk lengths.

### `save_cl(text: str, file_name: str, folder_id: str) -> Optional[bool]`
Save a cover letter text to a Word document, and upload it to Google Drive.

#### Args:
- `text` (str): The cover letter text to be saved.
- `file_name` (str): The desired name of the Word document (without extension).
- `folder_id` (str): The ID of the folder in which to upload the document.

#### Returns:
- `Optional[bool]`: True if the document is saved and uploaded successfully, None if an error occurs.

### `save_job(job_details: Dict[str, str], file_name: str, folder_id: str) -> Optional[bool]`
Save job details to a Word document and upload it to Google Drive.

#### Args:
- `job_details` (Dict[str, str]): A dictionary containing job details.
- `file_name` (str): The desired name of the Word document (without extension).
- `folder_id` (str): The ID of the folder in which to upload the document.

#### Returns:
- `Optional[bool]`: True if the document is saved and uploaded successfully, None if an error occurs.

### `split_input(input_string: str, max_chunk_size: int) -> List[Dict[str, Union[int, str]]]`
Split the input string into chunks based on the specified maximum chunk size.

#### Args:
- `input_string` (str): The input string to be split into chunks.
- `max_chunk_size` (int): The maximum size of each chunk.

#### Returns:
- `List[Dict[str, Union[str, int]]]`: List of chunks, where each chunk is represented as a dictionary
    with keys 'chunk_content' (str) and 'chunk_size' (int).

### `upload_file(file_name: str, folder_id: str, local_path: str) -> Optional[bool]`
Upload a file to Google Drive within a specified folder.

#### Args:
- `file_name` (str): The name of the file to be uploaded.
- `folder_id` (str): The ID of the folder in which to upload the file.
- `local_path` (str): The local path of the file to be uploaded.

#### Returns:
- `Optional[bool]`: True if the file is uploaded successfully, None if an error occurs.


### `watch_changes(folder_id: str) -> None`
Set up a watch to receive notifications about changes in a Google Drive folder.
Args:
- `folder_id` (str): The ID of the Google Drive folder to watch.
Returns:
- `None`

### `webhook(request: flask.wrappers.Request) -> <function jsonify at 0x0000026356EE3EB0>`
Handle incoming webhook requests.
Args:
- `request` (Request): The incoming HTTP request.
Returns:
- `jsonify`: JSON response based on the incoming request.

## Data
- `Dict` = `typing.Dict`
- `List` = `typing.List`
- `Optional` = `typing.Optional`
- `Tuple` = `typing.Tuple`
- `Union` = `typing.Union`