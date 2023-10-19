terraform {
  backend "gcs" {
    bucket = "ml-spez-ccai-tf-state"
    prefix = "env/main"
  }
}