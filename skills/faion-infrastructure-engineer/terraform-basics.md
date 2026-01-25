# Terraform Basics

Technical reference for Terraform fundamentals: HCL syntax, providers, resources, and core concepts.

---

## HCL Syntax

### Basic Blocks

```hcl
# Provider configuration
provider "aws" {
  region  = "us-east-1"
  profile = "default"
}

# Resource definition
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name        = "web-server"
    Environment = "production"
  }
}

# Data source (read-only)
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# Variable definition
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"

  validation {
    condition     = can(regex("^t[23]\\.", var.instance_type))
    error_message = "Instance type must be t2 or t3 family."
  }
}

# Output value
output "instance_ip" {
  description = "Public IP of the instance"
  value       = aws_instance.web.public_ip
  sensitive   = false
}

# Local values
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
```

### Expressions

```hcl
# String interpolation
name = "web-${var.environment}"

# Conditional
instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"

# For expression (list)
instance_ids = [for i in aws_instance.web : i.id]

# For expression (map)
instance_map = {for i in aws_instance.web : i.tags.Name => i.id}

# Dynamic blocks
dynamic "ingress" {
  for_each = var.ingress_rules
  content {
    from_port   = ingress.value.from_port
    to_port     = ingress.value.to_port
    protocol    = ingress.value.protocol
    cidr_blocks = ingress.value.cidr_blocks
  }
}

# Splat expression
all_ips = aws_instance.web[*].public_ip

# Type constraints
variable "ports" {
  type = list(object({
    port     = number
    protocol = string
  }))
}
```

### Built-in Functions

```hcl
# String functions
upper(var.name)                    # UPPERCASE
lower(var.name)                    # lowercase
replace(var.text, "old", "new")    # Replace substring
split(",", var.list_string)        # Split to list
join("-", var.list)                # Join list
format("%s-%s", var.a, var.b)      # Format string
trimspace(var.text)                # Trim whitespace

# Collection functions
length(var.list)                   # List/map length
element(var.list, 0)               # Get element by index
lookup(var.map, "key", "default")  # Map lookup with default
merge(var.map1, var.map2)          # Merge maps
concat(var.list1, var.list2)       # Concatenate lists
flatten([var.list1, var.list2])    # Flatten nested lists
distinct(var.list)                 # Remove duplicates
contains(var.list, "value")        # Check membership
keys(var.map)                      # Get map keys
values(var.map)                    # Get map values

# Filesystem functions
file("${path.module}/script.sh")   # Read file content
fileexists("${path.module}/x.txt") # Check file exists
templatefile("tpl.tftpl", {x = 1}) # Template rendering
basename("/path/to/file.txt")      # Get filename
dirname("/path/to/file.txt")       # Get directory

# Numeric functions
max(1, 2, 3)                       # Maximum value
min(1, 2, 3)                       # Minimum value
ceil(1.5)                          # Round up
floor(1.5)                         # Round down
abs(-5)                            # Absolute value

# Encoding functions
base64encode(var.text)             # Base64 encode
base64decode(var.encoded)          # Base64 decode
jsonencode(var.object)             # JSON encode
jsondecode(var.json_string)        # JSON decode
yamlencode(var.object)             # YAML encode
yamldecode(var.yaml_string)        # YAML decode

# Hash functions
md5(var.text)                      # MD5 hash
sha256(var.text)                   # SHA256 hash
uuid()                             # Generate UUID

# Date/time functions
timestamp()                        # Current UTC timestamp
formatdate("YYYY-MM-DD", timestamp())
```

---

## Providers

### AWS Provider

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile

  default_tags {
    tags = {
      ManagedBy = "terraform"
      Project   = var.project_name
    }
  }

  # Assume role
  assume_role {
    role_arn     = "arn:aws:iam::ACCOUNT_ID:role/TerraformRole"
    session_name = "terraform-session"
  }
}

# Multi-region setup
provider "aws" {
  alias  = "us_west"
  region = "us-west-2"
}

resource "aws_instance" "west" {
  provider = aws.us_west
  # ...
}
```

### Google Cloud Provider

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
  zone    = var.gcp_zone

  # Service account credentials
  credentials = file(var.gcp_credentials_file)
}

# Google Beta provider (for beta features)
provider "google-beta" {
  project = var.gcp_project
  region  = var.gcp_region
}
```

### Azure Provider

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }

  subscription_id = var.azure_subscription_id
  tenant_id       = var.azure_tenant_id
}
```

### Multi-Cloud Setup

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
```

---

## Resources

### Common Resource Patterns

```hcl
# Count - create multiple identical resources
resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  tags = {
    Name = "web-${count.index + 1}"
  }
}

# for_each - create resources from map/set
resource "aws_iam_user" "users" {
  for_each = toset(var.user_names)
  name     = each.value
}

# Depends on - explicit dependencies
resource "aws_instance" "app" {
  # ...
  depends_on = [aws_db_instance.database]
}

# Lifecycle rules
resource "aws_instance" "web" {
  # ...
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
    ignore_changes        = [tags]

    precondition {
      condition     = var.environment != ""
      error_message = "Environment must be set."
    }

    postcondition {
      condition     = self.public_ip != ""
      error_message = "Instance must have public IP."
    }
  }
}

# Provisioners (use sparingly)
resource "aws_instance" "web" {
  # ...

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
      host        = self.public_ip
    }
  }

  provisioner "local-exec" {
    command = "echo ${self.public_ip} >> inventory.txt"
  }
}
```

### Data Sources

```hcl
# AWS AMI lookup
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# AWS availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# AWS caller identity
data "aws_caller_identity" "current" {}

# AWS region
data "aws_region" "current" {}

# External data source
data "external" "example" {
  program = ["python3", "${path.module}/scripts/get_data.py"]

  query = {
    id = var.resource_id
  }
}

# HTTP data source
data "http" "example" {
  url = "https://api.example.com/data"

  request_headers = {
    Accept = "application/json"
  }
}

# Template file
data "template_file" "init" {
  template = file("${path.module}/templates/init.tftpl")

  vars = {
    server_name = var.server_name
    port        = var.port
  }
}
```

---

## Commands Quick Reference

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize working directory |
| `terraform plan` | Preview changes |
| `terraform apply` | Apply changes |
| `terraform destroy` | Destroy infrastructure |
| `terraform fmt` | Format configuration |
| `terraform validate` | Validate configuration |
| `terraform output` | Show outputs |
| `terraform console` | Interactive console |
| `terraform graph` | Generate dependency graph |
| `terraform providers` | Show required providers |
| `terraform version` | Show version |

---

## Best Practices

### Code Organization

```hcl
# versions.tf - Provider version constraints
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# providers.tf - Provider configuration
provider "aws" {
  region = var.aws_region
}

# variables.tf - Input variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# main.tf - Main resources
resource "aws_vpc" "main" {
  # ...
}

# outputs.tf - Output values
output "vpc_id" {
  value = aws_vpc.main.id
}

# locals.tf - Local values
locals {
  common_tags = {
    Project = var.project_name
  }
}

# data.tf - Data sources
data "aws_availability_zones" "available" {}
```

### Naming Conventions

```hcl
# Resource naming: {project}-{environment}-{resource}-{index}
resource "aws_instance" "myapp_prod_web_1" {
  tags = {
    Name = "myapp-prod-web-1"
  }
}

# Variable naming: snake_case
variable "instance_type" {}
variable "vpc_cidr_block" {}

# Output naming: descriptive snake_case
output "web_server_public_ip" {}
output "database_endpoint" {}

# Local naming: descriptive snake_case
locals {
  common_tags = {}
}
```

### Security Best Practices

```hcl
# Never store secrets in code
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# Use data sources for secrets
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "myapp/db/password"
}

# Enable encryption
resource "aws_s3_bucket" "data" {
  bucket = "my-secure-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.bucket_key.arn
    }
  }
}

# Restrict network access
resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks  # Not 0.0.0.0/0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

*Terraform Basics Reference*
*Part of faion-devops-engineer skill*

## Sources

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Language](https://www.terraform.io/language)
- [Terraform CLI](https://www.terraform.io/cli)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
