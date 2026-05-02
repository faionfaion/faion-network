---
name: aws-gcp-basics
description: Pick AWS or GCP for a small SaaS, set up org/account with IAM and MFA, build a VPC, deploy a hello-world container, add a CDN, and keep costs near $30/mo.
tier: pro
group: infra-engineering
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a production-ready cloud foundation: an AWS or GCP account with root/admin/dev IAM users, a VPC with public and private subnets, a containerised hello-world service running on ECS Fargate (AWS) or Cloud Run (GCP), a CDN layer in front of it, and a cost model sitting comfortably around $30/month for a small SaaS.

## Prerequisites

- A credit card and a personal email address for account signup.
- AWS CLI v2 (`brew install awscli`) or gcloud CLI (`brew install google-cloud-sdk`) installed locally.
- Docker installed locally (`docker --version`).
- Terraform >= 1.7 installed (`brew install terraform`).
- Basic Linux shell familiarity (cd, export, cat).

## Steps

### 1. Choose AWS or GCP

Use this decision rule:

| Your situation | Pick |
|----------------|------|
| Client already pays for AWS credits or uses S3/RDS | AWS |
| You need serverless containers with zero cold-start ops work | GCP (Cloud Run) |
| You plan to use BigQuery, Vertex AI, or Firebase | GCP |
| Default / no strong signal | AWS (broader talent pool, more tutorials) |

This playbook covers both paths in parallel. Commands are labelled `[AWS]` or `[GCP]`.

### 2. Create the root account / project

**[AWS]** Go to https://aws.amazon.com/free, sign up with a new email address (e.g. `aws-root@myagency.com`). Choose a support plan of "Basic" (free). After signup, sign in to the AWS Console as root.

**[GCP]** Go to https://console.cloud.google.com, sign in with a Google account, accept the free-trial offer ($300 credit), then create a new project:

```bash
gcloud projects create myagency-saas-prod --name="MyAgency SaaS Prod"
gcloud config set project myagency-saas-prod
```

### 3. Enable root MFA

**[AWS]** In the AWS Console: click your account name → Security credentials → Multi-factor authentication → Activate MFA. Choose "Authenticator app" and scan the QR code with your phone. Store the 24-character backup codes in 1Password.

**[GCP]** GCP root = your Google account. Go to https://myaccount.google.com/security, enable 2-Step Verification with an authenticator app. Do not skip this step; your GCP billing account is tied to this Google account.

### 4. Create an admin IAM user/role

**[AWS]**

```bash
# Install AWS CLI and configure with root credentials temporarily
aws configure
# AWS Access Key ID: <root-access-key>
# AWS Secret Access Key: <root-secret-key>
# Default region: eu-central-1
# Default output format: json

# Create admin group and user
aws iam create-group --group-name admins
aws iam attach-group-policy \
  --group-name admins \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

aws iam create-user --user-name myagency-admin
aws iam add-user-to-group --user-name myagency-admin --group-name admins
aws iam create-login-profile \
  --user-name myagency-admin \
  --password "Tr0ub4dor&3-Change-Me" \
  --password-reset-required
```

Sign in as `myagency-admin`, enable MFA for it, then delete the root access key from the root session.

**[GCP]**

```bash
# Create a service account for human admin access
gcloud iam service-accounts create myagency-admin \
  --display-name="MyAgency Admin"

# Grant Owner on the project (use Organization Admin role in production)
gcloud projects add-iam-policy-binding myagency-saas-prod \
  --member="serviceAccount:myagency-admin@myagency-saas-prod.iam.gserviceaccount.com" \
  --role="roles/owner"
```

For human admins, use Google Workspace groups bound to `roles/owner` rather than personal accounts.

### 5. Create a dev IAM user

**[AWS]**

```bash
aws iam create-user --user-name myagency-dev
aws iam attach-user-policy \
  --user-name myagency-dev \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

aws iam create-access-key --user-name myagency-dev
# Save the AccessKeyId and SecretAccessKey in 1Password under "AWS Dev Key"
```

**[GCP]**

```bash
gcloud iam service-accounts create myagency-dev \
  --display-name="MyAgency Dev"

gcloud projects add-iam-policy-binding myagency-saas-prod \
  --member="serviceAccount:myagency-dev@myagency-saas-prod.iam.gserviceaccount.com" \
  --role="roles/editor"

gcloud iam service-accounts keys create ~/myagency-dev-key.json \
  --iam-account=myagency-dev@myagency-saas-prod.iam.gserviceaccount.com
```

Store `~/myagency-dev-key.json` in 1Password. Do not commit it.

### 6. Build the VPC with public and private subnets (Terraform)

Create `infra/main.tf`:

**[AWS]**

```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "myagency-vpc" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true
  tags = { Name = "myagency-public" }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-central-1a"
  tags = { Name = "myagency-private" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
```

**[GCP]**

```hcl
terraform {
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}

provider "google" {
  project = "myagency-saas-prod"
  region  = "europe-west3"
}

resource "google_compute_network" "main" {
  name                    = "myagency-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "public" {
  name          = "myagency-public"
  ip_cidr_range = "10.0.1.0/24"
  region        = "europe-west3"
  network       = google_compute_network.main.id
}

resource "google_compute_subnetwork" "private" {
  name                     = "myagency-private"
  ip_cidr_range            = "10.0.2.0/24"
  region                   = "europe-west3"
  network                  = google_compute_network.main.id
  private_ip_google_access = true
}
```

Apply:

```bash
cd infra/
terraform init
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
```

### 7. Deploy a hello-world container

**[AWS — ECS Fargate]**

Build and push the image:

```bash
# Build
docker build -t myagency-hello .
# Assumes Dockerfile: FROM nginx:alpine COPY index.html /usr/share/nginx/html/

# Create ECR repo
aws ecr create-repository --repository-name myagency-hello --region eu-central-1

# Auth and push
aws ecr get-login-password --region eu-central-1 \
  | docker login --username AWS --password-stdin \
    123456789012.dkr.ecr.eu-central-1.amazonaws.com

docker tag myagency-hello:latest \
  123456789012.dkr.ecr.eu-central-1.amazonaws.com/myagency-hello:latest

docker push 123456789012.dkr.ecr.eu-central-1.amazonaws.com/myagency-hello:latest
```

Add to `infra/main.tf` (Fargate cluster + service):

```hcl
resource "aws_ecs_cluster" "main" {
  name = "myagency"
}

resource "aws_ecs_task_definition" "hello" {
  family                   = "myagency-hello"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_exec.arn

  container_definitions = jsonencode([{
    name  = "hello"
    image = "123456789012.dkr.ecr.eu-central-1.amazonaws.com/myagency-hello:latest"
    portMappings = [{ containerPort = 80, protocol = "tcp" }]
  }])
}

resource "aws_ecs_service" "hello" {
  name            = "myagency-hello"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.hello.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.public.id]
    assign_public_ip = true
  }
}
```

(The `aws_iam_role.ecs_exec` resource granting `AmazonECSTaskExecutionRolePolicy` is omitted for brevity; add it alongside.)

**[GCP — Cloud Run]**

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Build and push via Cloud Build (no Docker daemon needed on CI)
gcloud builds submit --tag europe-west3-docker.pkg.dev/myagency-saas-prod/myagency/hello:latest .

# Deploy
gcloud run deploy myagency-hello \
  --image europe-west3-docker.pkg.dev/myagency-saas-prod/myagency/hello:latest \
  --region europe-west3 \
  --platform managed \
  --allow-unauthenticated \
  --port 80 \
  --min-instances 0 \
  --max-instances 3
```

Cloud Run returns a `*.run.app` URL immediately.

### 8. Add CDN

**[AWS — CloudFront]**

Add to `infra/main.tf`:

```hcl
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_lb.main.dns_name  # or ECS public IP for demo
    origin_id   = "myagency-alb"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled         = true
  is_ipv6_enabled = true

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "myagency-alb"
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies { forward = "none" }
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  restrictions {
    geo_restriction { restriction_type = "none" }
  }
}
```

**[GCP — Cloud CDN]**

```bash
# Reserve a global IP
gcloud compute addresses create myagency-ip --global

# Create a backend bucket (for static assets) or serverless NEG (for Cloud Run)
gcloud compute network-endpoint-groups create myagency-neg \
  --region=europe-west3 \
  --network-endpoint-type=serverless \
  --cloud-run-service=myagency-hello

gcloud compute backend-services create myagency-backend \
  --global \
  --enable-cdn

gcloud compute backend-services add-backend myagency-backend \
  --global \
  --network-endpoint-group=myagency-neg \
  --network-endpoint-group-region=europe-west3

gcloud compute url-maps create myagency-urlmap \
  --default-service myagency-backend

gcloud compute target-http-proxies create myagency-proxy \
  --url-map myagency-urlmap

gcloud compute forwarding-rules create myagency-http-rule \
  --global \
  --target-http-proxy myagency-proxy \
  --address myagency-ip \
  --ports 80
```

### 9. Estimate and cap monthly spend

**AWS cost breakdown (eu-central-1, ~$30/mo target)**

| Resource | Config | $/mo |
|----------|--------|------|
| ECS Fargate | 0.25 vCPU / 0.5 GB, 730h | ~$11 |
| NAT Gateway (if needed) | 1 AZ, 10 GB/mo data | ~$5 |
| CloudFront | 1 TB out, 10M requests | ~$9 |
| ECR storage | 1 GB | ~$0.10 |
| Misc (data transfer) | — | ~$3 |
| **Total** | | **~$28** |

Set a billing alarm:

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name billing-30usd \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 86400 \
  --threshold 30 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:billing-alerts \
  --dimensions Name=Currency,Value=USD
```

**GCP cost breakdown (europe-west3, ~$30/mo target)**

| Resource | Config | $/mo |
|----------|--------|------|
| Cloud Run | 1 vCPU / 512 MB, 1M req/mo | ~$0 (free tier) |
| Cloud CDN | 1 TB out | ~$8 |
| Artifact Registry | 1 GB image storage | ~$0.10 |
| Cloud Build | 120 free min/day | ~$0 |
| Global IP (static) | 1 address | ~$7 |
| Misc | — | ~$3 |
| **Total** | | **~$18** |

Set a GCP budget alert in the console: Billing → Budgets & alerts → Create budget → $30 threshold → notify at 50%, 90%, 100%.

## Verify

**[AWS]**

```bash
# Get the ECS task public IP from the console or:
TASK_ARN=$(aws ecs list-tasks --cluster myagency --query 'taskArns[0]' --output text)
aws ecs describe-tasks --cluster myagency --tasks "$TASK_ARN" \
  --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' \
  --output text | xargs -I{} aws ec2 describe-network-interfaces \
  --network-interface-ids {} \
  --query 'NetworkInterfaces[0].Association.PublicIp' --output text

# Then:
curl -I http://<public-ip>
# Expected: HTTP/1.1 200 OK
```

**[GCP]**

```bash
SERVICE_URL=$(gcloud run services describe myagency-hello \
  --region europe-west3 --format='value(status.url)')
curl -I "$SERVICE_URL"
# Expected: HTTP/2 200
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `aws configure` shows "Invalid client token" | Root access key created before MFA was set; key may have partial permissions | Rotate the key in IAM → Security credentials → Access keys |
| ECS task stays in PROVISIONING for >5 min | Subnet has no internet route; execution role missing ECR pull permission | Confirm `map_public_ip_on_launch = true` on the subnet and attach `AmazonECSTaskExecutionRolePolicy` to the task execution role |
| Cloud Run deploy fails: "permission denied on ECR/Artifact Registry" | Cloud Build service account lacks `roles/artifactregistry.writer` | `gcloud projects add-iam-policy-binding myagency-saas-prod --member="serviceAccount:<build-sa>@cloudbuild.gserviceaccount.com" --role=roles/artifactregistry.writer` |
| CloudFront returns 502 | Origin (ECS) security group blocks port 80 from CloudFront IPs | Add inbound rule allowing `0.0.0.0/0` on port 80, or use CloudFront managed prefix lists |
| GCP billing alert never fires | Budget alerts only notify after daily rollup | Use Pub/Sub budget notifications for near-real-time alerting |
| `terraform apply` fails: "Error acquiring the state lock" | Another apply is running or a previous run crashed | `terraform force-unlock <lock-id>` after confirming no other apply is active |

## Next

- `aws-iam-practical-patterns` — add least-privilege policies for each microservice instead of PowerUserAccess.
- `terraform-modules-structure` — refactor the single `main.tf` into reusable modules before the codebase grows.
- `aws-monitoring-observability` (AWS) or `cloud-run-monitoring` (GCP) — add CloudWatch dashboards / GCP Cloud Monitoring alerts so you know before your users do when something breaks.

## References

- [knowledge/pro/infra/infrastructure-engineer/aws-vpc-design](../../../knowledge/pro/infra/infrastructure-engineer/aws-vpc-design) — CIDR design rules and public/private subnet split pattern used in Step 6 to avoid routing conflicts as the VPC grows.
- [knowledge/pro/infra/infrastructure-engineer/aws-iam-security-foundations](../../../knowledge/pro/infra/infrastructure-engineer/aws-iam-security-foundations) — least-privilege and MFA enforcement model applied in Steps 3–5 for root, admin, and dev users.
- [knowledge/pro/infra/infrastructure-engineer/gcp-networking-vpc](../../../knowledge/pro/infra/infrastructure-engineer/gcp-networking-vpc) — GCP VPC subnet and private Google access configuration pattern applied in Step 6 for the GCP path.
- [knowledge/pro/infra/infrastructure-engineer/terraform-basics](../../../knowledge/pro/infra/infrastructure-engineer/terraform-basics) — provider lock-file conventions and plan/apply workflow applied in Steps 6–8 to keep infrastructure reproducible.
