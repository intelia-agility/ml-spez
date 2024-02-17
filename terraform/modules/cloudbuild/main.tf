# Define a Google Cloud Build Trigger resource for deploying Cloud Functions.
resource "google_cloudbuild_trigger" "cloud_functions" {
  # Set the project where this trigger will be created.
  project = var.project

  # Specify the name of the trigger, provided as an input variable.
  name = var.trigger_name

  # Set the location (region) where the trigger will be created.
  location = var.build_region

  # Add a description for the trigger, indicating its purpose.
  description = "Trigger to deploy the Cloud Function in the path ${var.included_files}"

  # Specify the filename for the Cloud Build configuration.
  filename = var.cloud_build_path

  # List of included files, typically the source code for the Cloud Function.
  included_files = [var.included_files]

  # Configure the repository event that will trigger this build.
  repository_event_config {
    # Specify the repository where the code is hosted.
    repository = var.repo

    # Configure the push event trigger settings.
    push {
      # Specify the branch that will trigger the build, provided as an input variable.
      branch = var.branch

      # Optionally, set whether to invert the regular expression match for the branch.
      invert_regex = var.invert_regex
    }
  }

  # Set the service account that Cloud Build will use for this trigger.
  service_account = "projects/${var.project}/serviceAccounts/${var.service_account}"

  # Specify whether to include build logs with the status in the trigger configuration.
  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"
}
