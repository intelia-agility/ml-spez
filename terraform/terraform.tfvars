project_id = "ml-spez-ccai"
bigquery_datasets = [{
  dataset_id = "dialogflow_export"
  region     = "US"
  table_definitions = [{
    table_id = "interactions"
  }]
  }
]
buckets = []