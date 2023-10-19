# Enable Google Cloud services and APIs for the created project.
resource "google_project_service" "enabled_apis" {
  # Specify the project ID for the project resource created earlier.
  project = var.project_id

  # Create an instance of the resource for each enabled API specified in input variables.
  for_each = {
    for index, api in var.enabled_apis :
    api.api_id => api
  }

  # Set the service name to enable based on input variables.
  service = each.value.api_id

  # Configure timeouts for resource creation and updates.
  timeouts {
    create = "30m"
    update = "40m"
  }

  # Disable dependent services when disabling APIs.
  disable_dependent_services = true
}