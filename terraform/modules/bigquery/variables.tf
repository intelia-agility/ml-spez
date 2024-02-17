variable "project_id" {
  description = "Id of the project"
  type        = string
}
variable "dataset_id" {
  description = "Id of the dataset"
  type        = string
}
variable "region" {
  description = "Region of the dataset"
  type        = string
}
variable "table_definitions" {
  description = "The table defnitions in the dataset"
  type = list(object({
    table_id = string
    time_partitioning = optional(object({
      partitioning_type  = string
      partitioning_field = string
    }))
    clustering_fields = optional(list(string))
  }))
}