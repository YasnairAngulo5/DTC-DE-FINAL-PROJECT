locals {
  data_lake_bucket = "dtc-wb-data-lake"
  resources_bucket = "dtc-resources-bucket"
}

variable "project" {
  description = "Your GCP Project ID"  //dtc-de-project-382603
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}


variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "bank_data"
}

variable "TABLE_NAME" {
  description   = "BigQuery Table"
  type          = string
  default       = "world_bank"

}