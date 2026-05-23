terraform {
  backend "gcs" {
    bucket = "COMPANY-terraform-state"
    prefix = "ENV/COMPONENT"
    # Recommended: impersonate a service account
    # impersonate_service_account = "terraform@PROJECT.iam.gserviceaccount.com"
  }
}
