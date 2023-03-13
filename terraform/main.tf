provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_sql_database_instance" "shortener-url" {
  name             = var.instance_name
  database_version = "POSTGRES_14"
  region           = var.region
  deletion_protection = false

  settings {
    tier = "db-custom-1-4096"

    backup_configuration {
      enabled = false
    }

    disk_autoresize = false
    disk_size        = 10

    ip_configuration {
      ipv4_enabled = true
    }
  }
}

resource "google_sql_database" "shortener" {
  name       = "shortener"
  instance   = google_sql_database_instance.shortener-url.name
  collation  = "en_US.UTF8"
  charset    = "UTF8"
}

resource "google_sql_user" "shortener-url-user" {
  name          = var.postgres_user
  password      = var.postgres_password
  instance      = google_sql_database_instance.shortener-url.name
}
