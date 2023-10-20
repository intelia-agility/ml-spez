variable "project_id" {
  description = "The project id"
  type        = string
}
variable "bigquery_datasets" {
  description = "The list of BigQuery datasets along with Table definitions"
  type = list(object({
    dataset_id = string
    region     = string
    table_definitions = list(object({
      table_id = string
      time_partitioning = optional(object({
        partitioning_type  = string
        partitioning_field = string
      }))
      clustering_fields = optional(list(string))
    }))
  }))
}
variable "buckets" {
  description = "The list of cloud storage buckets"
  type = list(object({
    bucket_name = string
    location    = string
  }))
}
variable "repo" {}
variable "service_account" {}
variable "build_region" {}
variable "trigger_definitions" {
  description = "The configuration of the build triggers"
  type = list(object({
    trigger_name     = string
    branch           = string
    included_files   = string
    cloud_build_path = string
    invert_regex     = bool
  }))
}