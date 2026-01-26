# Terraform State Examples

## Remote Backend Configurations

### AWS S3 Backend (Production-Ready)

```hcl
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "prod/networking/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"

    # KMS encryption (optional, for compliance)
    kms_key_id = "alias/terraform-state"

    # Cross-account access
    role_arn = "arn:aws:iam::ACCOUNT_ID:role/TerraformStateRole"

    # Prevent accidental deletion
    skip_metadata_api_check     = false
    skip_region_validation      = false
    skip_credentials_validation = false
  }
}
```

### GCS Backend (GCP)

```hcl
terraform {
  backend "gcs" {
    bucket  = "mycompany-terraform-state"
    prefix  = "prod/networking"

    # Impersonate service account (recommended)
    impersonate_service_account = "terraform@myproject.iam.gserviceaccount.com"
  }
}
```

### Azure Blob Backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "mycompanytfstate"
    container_name       = "tfstate"
    key                  = "prod/networking/terraform.tfstate"

    # Use Azure AD authentication
    use_azuread_auth = true
  }
}
```

### Terraform Cloud Backend

```hcl
terraform {
  cloud {
    organization = "mycompany"

    workspaces {
      name = "prod-networking"
    }
  }
}
```

### Terraform Cloud with Tags (Multiple Workspaces)

```hcl
terraform {
  cloud {
    organization = "mycompany"

    workspaces {
      tags = ["networking", "prod"]
    }
  }
}
```

## State Locking Infrastructure

### DynamoDB Lock Table (AWS)

```hcl
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "terraform-state-locks"
    Environment = "shared"
    ManagedBy   = "terraform"
  }

  # Prevent accidental deletion
  lifecycle {
    prevent_destroy = true
  }
}
```

### S3 Bucket for State (AWS)

```hcl
resource "aws_s3_bucket" "terraform_state" {
  bucket = "mycompany-terraform-state"

  tags = {
    Name        = "terraform-state"
    Environment = "shared"
    ManagedBy   = "terraform"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.terraform_state.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

## State Operations Examples

### List and Inspect Resources

```bash
# List all resources in state
terraform state list

# List resources matching pattern
terraform state list 'aws_instance.*'

# Show specific resource details
terraform state show aws_instance.web

# Show resource in JSON format
terraform state show -json aws_instance.web | jq
```

### Move and Rename Resources

```bash
# Rename resource (within same configuration)
terraform state mv aws_instance.web aws_instance.app_server

# Move resource to module
terraform state mv aws_instance.web module.compute.aws_instance.main

# Move resource from module to root
terraform state mv module.compute.aws_instance.main aws_instance.web

# Move entire module
terraform state mv module.old_name module.new_name
```

### Import Existing Resources

#### CLI Import (Traditional)

```bash
# Import EC2 instance
terraform import aws_instance.web i-1234567890abcdef0

# Import S3 bucket
terraform import aws_s3_bucket.data my-existing-bucket

# Import RDS instance
terraform import aws_db_instance.main my-database

# Import with module path
terraform import module.compute.aws_instance.web i-1234567890abcdef0
```

#### Import Blocks (Terraform 1.5+, Recommended)

```hcl
# In your configuration file
import {
  to = aws_instance.web
  id = "i-1234567890abcdef0"
}

import {
  to = aws_s3_bucket.data
  id = "my-existing-bucket"
}

# Then run terraform plan to preview
# terraform apply to execute imports
```

#### Generate Configuration During Import

```bash
# Generate configuration for imported resource (Terraform 1.5+)
terraform plan -generate-config-out=generated.tf
```

### Remove Resources from State

```bash
# Remove single resource (resource stays, just unmanaged)
terraform state rm aws_instance.web

# Remove multiple resources
terraform state rm aws_instance.web aws_instance.worker

# Remove entire module
terraform state rm module.compute
```

### State Backup and Recovery

```bash
# Backup state locally
terraform state pull > terraform.tfstate.backup

# Verify backup
terraform show terraform.tfstate.backup

# Push state to remote (dangerous - use carefully)
terraform state push terraform.tfstate.backup

# Force push (override lock - emergency only)
terraform state push -force terraform.tfstate.backup
```

### Replace Provider

```bash
# Replace provider (useful for registry migration)
terraform state replace-provider hashicorp/aws registry.acme.corp/acme/aws

# Auto-approve replacement
terraform state replace-provider -auto-approve hashicorp/aws registry.acme.corp/acme/aws
```

## Remote State Data Source

### Access Outputs from Another State

```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"

  config = {
    bucket = "mycompany-terraform-state"
    key    = "prod/networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use outputs from remote state
resource "aws_instance" "app" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  subnet_id     = data.terraform_remote_state.vpc.outputs.private_subnet_ids[0]

  vpc_security_group_ids = [
    data.terraform_remote_state.vpc.outputs.app_security_group_id
  ]
}
```

### Cross-Account Remote State

```hcl
data "terraform_remote_state" "shared_services" {
  backend = "s3"

  config = {
    bucket   = "shared-services-terraform-state"
    key      = "shared/terraform.tfstate"
    region   = "us-east-1"
    role_arn = "arn:aws:iam::SHARED_ACCOUNT:role/TerraformStateRead"
  }
}
```

## Moved Blocks (Terraform 1.1+)

### Refactor Without State Commands

```hcl
# When renaming a resource
moved {
  from = aws_instance.web
  to   = aws_instance.app_server
}

# When moving to a module
moved {
  from = aws_instance.web
  to   = module.compute.aws_instance.main
}

# When renaming a module
moved {
  from = module.old_compute
  to   = module.compute
}
```

## Force Replace Resource

```bash
# Modern approach (Terraform 0.15.2+)
terraform apply -replace=aws_instance.web

# Replace multiple resources
terraform apply -replace=aws_instance.web -replace=aws_instance.worker

# Deprecated approach (still works)
terraform taint aws_instance.web
terraform apply
```

## Unlock State (Emergency)

```bash
# Get lock ID from error message, then unlock
terraform force-unlock LOCK_ID

# Skip confirmation
terraform force-unlock -force LOCK_ID
```

---

*Terraform State Examples | Part of terraform-state methodology*
