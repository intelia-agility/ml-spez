# Configure the Google Cloud provider with the specified project ID.
provider "google" {
  # Set the project to the value provided in the input variable.
  project = var.project_id
}

module "enabled_apis" {
  # Set the source directory for the module.
  source = "./modules/enabled_apis"
  # Set the project to the value provided in the input variable.
  project_id = var.project_id
  # Set the enabled_apis to the value provided in the input variable.
  enabled_apis = var.enabled_apis
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
# Define a module for managing Cloud Build triggers based on input variables.
module "cloudbuild" {
  # Set the source directory for the module.
  source = "./modules/cloudbuild"

  # Create an instance of the module for each defined trigger.
  for_each = {
    for index, trigger in var.trigger_definitions :
    trigger.trigger_name => trigger
  }

  # Pass the following input variables to the module for configuration.
  project          = var.project_id              # The project where the triggers will be created.
  trigger_name     = each.value.trigger_name     # The name of the Cloud Build trigger.
  repo             = var.repo                    # The repository where the code is hosted.
  service_account  = var.service_account         # The service account to use for Cloud Build.
  build_region     = var.build_region            # The region where the builds will run.
  branch           = each.value.branch           # The branch that triggers the build.
  included_files   = each.value.included_files   # List of included files for the build.
  cloud_build_path = each.value.cloud_build_path # Path to the Cloud Build configuration.
  invert_regex     = each.value.invert_regex     # Whether to invert the regex match for the branch.
}