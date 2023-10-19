variable "project_id" {
  description = "The id of the GCP project"
  type        = string
}
variable "enabled_apis" {
  description = "The API's to be enabled on the GCP project"
  type = list(object({
    api_name = string
    api_id   = string
  }))
}