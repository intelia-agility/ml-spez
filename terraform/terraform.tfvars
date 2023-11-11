project_id = "ml-spez-ccai"
enabled_apis = [
  {
    api_name = "Dialogflow API"
    api_id   = "dialogflow.googleapis.com"
    }, {
    api_name = "Vertex AI API"
    api_id   = "aiplatform.googleapis.com"
    }, {
    api_name = "Cloud Functions API"
    api_id   = "cloudfunctions.googleapis.com"
    }, {
    api_name = "Cloud Run API"
    api_id   = "run.googleapis.com"
    }, {
    api_name = "Eventarc API"
    api_id   = "eventarc.googleapis.com"
    }
]
bigquery_datasets = [{
  dataset_id = "dialogflow_export"
  region     = "US"
  table_definitions = [{
    table_id = "interactions"
  }]
  }, {
  dataset_id = "processed"
  region     = "us-central1"
  table_definitions = []
  }, {
  dataset_id = "linkedin_kaggle"
  region     = "us-central1"
  table_definitions = [{
    table_id = "job_postings"
    },
    {
      table_id = "job_skills"
    },
    {
      table_id = "job_industries"
    },
    {
      table_id = "benefits"
    },
    {
      table_id = "companies"
    },
    {
      table_id = "company_industries"
    },
    {
      table_id = "company_specialities"
    },
    {
      table_id = "employee_counts"
  }]
}]
buckets = [{
  bucket_name = "csv-landing"
  location    = "us-central1"
}, {
  bucket_name = "job-embeddings"
  location    = "us-central1"
}]
service_account = "ml-spez@ml-spez-ccai.iam.gserviceaccount.com"
repo            = "projects/ml-spez-ccai/locations/australia-southeast1/connections/ml_spez_repo_connection/repositories/intelia-agility-ml-spez"
build_region    = "australia-southeast1"
trigger_definitions = [{
  trigger_name     = "Upload-CSV"
  branch           = ".*"
  included_files   = "cloud_functions/upload_csv/**"
  cloud_build_path = "cloud_functions/upload_csv/cloudbuild.yaml"
  invert_regex     = false
}, {
  trigger_name     = "Trans"
  branch           = ".*"
  included_files   = "cloud_functions/trans/**"
  cloud_build_path = "cloud_functions/trans/cloudbuild.yaml"
  invert_regex     = false
}, {
  trigger_name     = "Webhook"
  branch           = ".*"
  included_files   = "cloud_functions/webhook/**"
  cloud_build_path = "cloud_functions/webhook/cloudbuild.yaml"
  invert_regex     = false
}]