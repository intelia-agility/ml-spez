variable "project" {
  type        = string
  description = "The CICD project id."
}
variable "trigger_name" {
  type        = string
  description = "The name of the trigger, usually the function name."
}
variable "repo" {
  type        = string
  description = "The repository connected to cloud build."
}
variable "service_account" {
  type        = string
  description = "The service account that runs the build."
}
variable "build_region" {
  type        = string
  description = "The region of the build."
}
variable "branch" {
  type        = string
  description = "The branch that is pushed to to trigger the build."
}
variable "included_files" {
  type        = string
  description = "The file path that triggers the build."
}
variable "cloud_build_path" {
  type        = string
  description = "The location of the cloudbuild.yaml file for the build."
}
variable "invert_regex" {
  type        = bool
  description = "Flag to invert the branch match regex."
}