# Create a Google Cloud Storage (GCS) bucket resource.
resource "google_storage_bucket" "bucket" {
  # Set the name of the GCS bucket, combining the bucket name and project ID.
  name = "${var.bucket_name}-${var.project_id}"

  # Specify the location for the GCS bucket, provided as an input variable.
  location = var.location
}