project_id = "ml-spez-ccai"
bigquery_datasets = [{
  dataset_id = "dialogflow_export"
  region     = "US"
  table_definitions = [{
    table_id = "interactions"
  }]
  }
]
buckets = [{
  bucket_name = "csv-landing"
  location    = "US"
}]
service_account = "ml-spez@ml-spez-ccai.iam.gserviceaccount.com"
repo            = "projects/ml-spez-ccai/locations/australia-southeast1/connections/ml_spez_repo_connection/repositories/intelia-agility-ml-spez"
build_region    = "australia-southeast1"
trigger_definitions = [{
  trigger_name     = "Upload-CSV"
  branch           = "^main$"
  included_files   = "cloud_functions/upload_csv**"
  cloud_build_path = "cloud_functions/upload_csv/cloudbuild.yaml"
  invert_regex     = false
}]