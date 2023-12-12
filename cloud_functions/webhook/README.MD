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

... (similarly, descriptions for other functions)

## Data
- `Dict` = `typing.Dict`
- `List` = `typing.List`
- `Optional` = `typing.Optional`
- `Tuple` = `typing.Tuple`
- `Union` = `typing.Union`