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