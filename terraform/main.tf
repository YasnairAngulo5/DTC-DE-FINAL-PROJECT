terraform {
    required_version = ">=1.3.7"
  backend "local" {} # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  //credentials = file("<NAME>.json")
  project = var.project
  region  = var.region
  //zone    = "us-central1-c"
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "dtc-wb-bucket" {
  name          = "${local.data_lake_bucket}" # If you want Concatenating DL bucket & Project name for unique naming
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type      = "Delete"
    }
    condition {
      age       = 30 //days
    }
    
  }

  force_destroy = true

}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}

# Resources Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "resources" {
  name          = "${local.resources_bucket}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type      = "Delete"
    }
    condition {
      age       = 30 //days
    }
    
  }

  force_destroy = true

}

# Upload a text file as an object
# to the storage bucket

resource "google_storage_bucket_object" "storage-resources" {
 name         = "indicators.csv"
 source       = "./resources/indicators.csv"
 content_type = "text/plain"
 bucket       = google_storage_bucket.resources.id
}


# Dataset production
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "production" {
  dataset_id = "production"
  project    = var.project
  location   = var.region
}

# Dataset staging
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "staging" {
  dataset_id = "staging"
  project    = var.project
  location   = var.region
}

# Dataset dbt_sandbox
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "development" {
  dataset_id = "development"
  project    = var.project
  location   = var.region
}


