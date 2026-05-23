provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# Optional: Multi-region secondary provider
# provider "aws" {
#   alias  = "secondary"
#   region = var.secondary_region
# }
