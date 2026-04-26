# terraform.tfvars.example — copy to terraform.tfvars and fill in real values
# DO NOT commit terraform.tfvars with actual secrets

project_name = "myapp"
environment  = "dev"
aws_region   = "us-east-1"
vpc_cidr     = "10.0.0.0/16"
instance_type  = "t3.micro"
instance_count = 2

# Database password — set via env var: TF_VAR_db_password=...
# db_password = "change-me-in-real-tfvars"
