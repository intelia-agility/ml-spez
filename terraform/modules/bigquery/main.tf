# Create a BigQuery dataset in the specified project.
resource "google_bigquery_dataset" "project_dataset" {
  # Specify the dataset ID, provided as an input variable.
  dataset_id = var.dataset_id

  # Add a description for the dataset.
  description = "This is the dataset for the various tables"

  # Set the location for the dataset, provided as an input variable.
  location = var.region

  # Set the project where the dataset will be created, provided as an input variable.
  project = var.project_id
}

# Create BigQuery tables within the dataset.
resource "google_bigquery_table" "dataset_tables" {
  # Add a description for the tables.
  description = "This creates the tables specified in the dataset"

  # Specify the dataset ID from the previously created dataset resource.
  dataset_id = google_bigquery_dataset.project_dataset.dataset_id

  # Create an instance of the resource for each table definition in input variables.
  for_each = {
    for index, table_definition in var.table_definitions :
    table_definition.table_id => table_definition
  }

  # Set the table ID for each table based on input variables.
  table_id = each.value.table_id

  # Configure dynamic time partitioning if specified.
  dynamic "time_partitioning" {
    for_each = try(length(each.value.time_partitioning), 0) > 0 ? [1] : []
    content {
      type  = each.value.time_partitioning.partitioning_type
      field = each.value.time_partitioning.partitioning_field
    }
  }

  # Specify clustering fields for the table, if any.
  clustering = each.value.clustering_fields

  # Define the schema for the table using a JSON file.
  schema = file("${path.module}/schemas/${each.value.table_id}.json")

  # Disable deletion protection for the table.
  deletion_protection = false
}