# Configure the Google Cloud provider with the specified project ID.
provider "google" {
  # Set the project to the value provided in the input variable.
  project = var.project_id
}

# Create a module for managing BigQuery datasets and tables.
module "bigquery" {
  # Set the source directory for the module.
  source = "./modules/bigquery"

  # Create an instance of the module for each defined BigQuery dataset in input variables.
  for_each = {
    for index, dataset in var.bigquery_datasets :
    dataset.dataset_id => dataset
  }

  # Pass project ID, dataset ID, region, and table definitions to the module for configuration.
  project_id        = var.project_id
  dataset_id        = each.value.dataset_id
  region            = each.value.region
  table_definitions = each.value.table_definitions
}

# Create a module for managing Cloud Storage buckets.
module "buckets" {
  # Set the source directory for the module.
  source = "./modules/bucket"

  # Create an instance of the module for each defined bucket in input variables.
  for_each = {
    for index, bucket in var.buckets :
    bucket.bucket_name => bucket
  }

  # Pass project ID, bucket name, and location to the module for configuration.
  project_id  = var.project_id
  bucket_name = each.value.bucket_name
  location    = each.value.location
}