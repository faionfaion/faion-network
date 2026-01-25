---
name: faion-gcp-networking-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# GCP Networking, IAM & Operations

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-agent

## Configuration

### gcloud CLI Installation

```bash
# Install gcloud CLI (Linux)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Install via apt (Debian/Ubuntu)
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt update && sudo apt install google-cloud-cli

# Verify installation
gcloud version
```

### Authentication

```bash
# Interactive login (opens browser)
gcloud auth login

# Service account authentication
gcloud auth activate-service-account --key-file=service-account.json

# Application default credentials (for local development)
gcloud auth application-default login

# List authenticated accounts
gcloud auth list

# Revoke credentials
gcloud auth revoke [ACCOUNT]
```

### Project Configuration

```bash
# Set default project
gcloud config set project my-project-id

# Get current project
gcloud config get-value project

# List projects
gcloud projects list

# Create project
gcloud projects create my-new-project --name="My Project"

# Delete project
gcloud projects delete my-project-id
```

### Configuration Management

```bash
# View all configurations
gcloud config configurations list

# Create named configuration
gcloud config configurations create production

# Activate configuration
gcloud config configurations activate production

# Set properties in current config
gcloud config set compute/zone us-central1-a
gcloud config set compute/region us-central1

# View current config
gcloud config list

# Set multiple properties
gcloud config set core/project my-project
gcloud config set compute/zone us-central1-a
gcloud config set compute/region us-central1
```

### Environment Variables

```bash
# Project
export CLOUDSDK_CORE_PROJECT="my-project-id"

# Region/Zone
export CLOUDSDK_COMPUTE_REGION="us-central1"
export CLOUDSDK_COMPUTE_ZONE="us-central1-a"

# Credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Disable prompts (CI/CD)
export CLOUDSDK_CORE_DISABLE_PROMPTS=1
```

## VPC Networking

### Networks

```bash
# Create VPC network
gcloud compute networks create my-vpc \
    --subnet-mode=custom

# Create subnet
gcloud compute networks subnets create my-subnet \
    --network=my-vpc \
    --region=us-central1 \
    --range=10.0.0.0/24

# List networks
gcloud compute networks list

# List subnets
gcloud compute networks subnets list

# Delete subnet
gcloud compute networks subnets delete my-subnet --region=us-central1

# Delete network
gcloud compute networks delete my-vpc
```

### Firewall Rules

```bash
# Create firewall rule (allow SSH)
gcloud compute firewall-rules create allow-ssh \
    --network=my-vpc \
    --allow=tcp:22 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=ssh-enabled

# Create firewall rule (allow HTTP/HTTPS)
gcloud compute firewall-rules create allow-http \
    --network=my-vpc \
    --allow=tcp:80,tcp:443 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server

# Create firewall rule (internal)
gcloud compute firewall-rules create allow-internal \
    --network=my-vpc \
    --allow=tcp,udp,icmp \
    --source-ranges=10.0.0.0/8

# List firewall rules
gcloud compute firewall-rules list

# Delete firewall rule
gcloud compute firewall-rules delete allow-ssh
```

### Static IPs and NAT

```bash
# Reserve static IP
gcloud compute addresses create my-static-ip \
    --region=us-central1

# List addresses
gcloud compute addresses list

# Create Cloud NAT
gcloud compute routers create my-router \
    --network=my-vpc \
    --region=us-central1

gcloud compute routers nats create my-nat \
    --router=my-router \
    --region=us-central1 \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips
```

### Load Balancing

```bash
# Create health check
gcloud compute health-checks create http my-health-check \
    --port=80

# Create backend service
gcloud compute backend-services create my-backend \
    --protocol=HTTP \
    --health-checks=my-health-check \
    --global

# Add instance group to backend
gcloud compute backend-services add-backend my-backend \
    --instance-group=my-instance-group \
    --instance-group-zone=us-central1-a \
    --global

# Create URL map
gcloud compute url-maps create my-url-map \
    --default-service=my-backend

# Create target proxy
gcloud compute target-http-proxies create my-proxy \
    --url-map=my-url-map

# Create forwarding rule
gcloud compute forwarding-rules create my-lb \
    --global \
    --target-http-proxy=my-proxy \
    --ports=80
```

## IAM (Identity and Access Management)

### Service Accounts

```bash
# Create service account
gcloud iam service-accounts create my-service-account \
    --display-name="My Service Account"

# List service accounts
gcloud iam service-accounts list

# Create key for service account
gcloud iam service-accounts keys create key.json \
    --iam-account=my-service-account@my-project.iam.gserviceaccount.com

# List keys
gcloud iam service-accounts keys list \
    --iam-account=my-service-account@my-project.iam.gserviceaccount.com

# Delete key
gcloud iam service-accounts keys delete KEY_ID \
    --iam-account=my-service-account@my-project.iam.gserviceaccount.com

# Delete service account
gcloud iam service-accounts delete my-service-account@my-project.iam.gserviceaccount.com
```

### IAM Bindings

```bash
# View project IAM policy
gcloud projects get-iam-policy my-project

# Add IAM binding
gcloud projects add-iam-policy-binding my-project \
    --member=user:user@example.com \
    --role=roles/viewer

# Add service account binding
gcloud projects add-iam-policy-binding my-project \
    --member=serviceAccount:my-sa@my-project.iam.gserviceaccount.com \
    --role=roles/storage.admin

# Remove IAM binding
gcloud projects remove-iam-policy-binding my-project \
    --member=user:user@example.com \
    --role=roles/viewer

# Grant Cloud Run invoker
gcloud run services add-iam-policy-binding my-service \
    --region=us-central1 \
    --member=allUsers \
    --role=roles/run.invoker
```

### Custom Roles

```bash
# Create custom role
gcloud iam roles create myCustomRole \
    --project=my-project \
    --title="My Custom Role" \
    --description="Custom role for specific access" \
    --permissions=storage.buckets.list,storage.objects.get

# List custom roles
gcloud iam roles list --project=my-project

# Update custom role
gcloud iam roles update myCustomRole \
    --project=my-project \
    --add-permissions=storage.objects.create

# Delete custom role
gcloud iam roles delete myCustomRole --project=my-project
```

## Secret Manager

### Secret Operations

```bash
# Create secret
gcloud secrets create my-secret

# Add secret version
echo -n "my-secret-value" | gcloud secrets versions add my-secret --data-file=-

# Add secret from file
gcloud secrets versions add my-secret --data-file=secret.txt

# List secrets
gcloud secrets list

# Access secret (get value)
gcloud secrets versions access latest --secret=my-secret

# Access specific version
gcloud secrets versions access 1 --secret=my-secret

# List versions
gcloud secrets versions list my-secret

# Disable version
gcloud secrets versions disable 1 --secret=my-secret

# Delete secret
gcloud secrets delete my-secret
```

### IAM for Secrets

```bash
# Grant access to secret
gcloud secrets add-iam-policy-binding my-secret \
    --member=serviceAccount:my-sa@my-project.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor

# View IAM policy
gcloud secrets get-iam-policy my-secret
```

## Cloud Logging and Monitoring

### Logging

```bash
# Read logs
gcloud logging read "resource.type=gce_instance" --limit=50

# Read logs with filter
gcloud logging read 'severity>=ERROR AND resource.type="cloud_run_revision"' \
    --limit=100

# Read logs for specific resource
gcloud logging read 'resource.labels.function_name="my-function"' \
    --limit=50

# Stream logs (tail)
gcloud logging tail "resource.type=cloud_run_revision"

# Write log entry
gcloud logging write my-log "Test log message" --severity=INFO
```

### Metrics

```bash
# List metric descriptors
gcloud monitoring metrics list

# Get time series data
gcloud monitoring metrics read \
    'compute.googleapis.com/instance/cpu/utilization' \
    --start-time="2024-01-01T00:00:00Z" \
    --end-time="2024-01-02T00:00:00Z"
```

### Alerting

```bash
# Create notification channel
gcloud alpha monitoring channels create \
    --display-name="Email Channel" \
    --type=email \
    --channel-labels=email_address=alerts@example.com

# List notification channels
gcloud alpha monitoring channels list

# Create alert policy (via JSON)
gcloud alpha monitoring policies create --policy-from-file=alert-policy.json
```

## Pub/Sub

### Topics

```bash
# Create topic
gcloud pubsub topics create my-topic

# List topics
gcloud pubsub topics list

# Delete topic
gcloud pubsub topics delete my-topic

# Publish message
gcloud pubsub topics publish my-topic --message="Hello World"

# Publish with attributes
gcloud pubsub topics publish my-topic \
    --message="Hello" \
    --attribute=key1=value1,key2=value2
```

### Subscriptions

```bash
# Create pull subscription
gcloud pubsub subscriptions create my-sub --topic=my-topic

# Create push subscription
gcloud pubsub subscriptions create my-push-sub \
    --topic=my-topic \
    --push-endpoint=https://example.com/webhook

# List subscriptions
gcloud pubsub subscriptions list

# Pull messages
gcloud pubsub subscriptions pull my-sub --limit=10 --auto-ack

# Delete subscription
gcloud pubsub subscriptions delete my-sub
```

## Artifact Registry

### Repository Management

```bash
# Create Docker repository
gcloud artifacts repositories create my-repo \
    --repository-format=docker \
    --location=us-central1

# List repositories
gcloud artifacts repositories list

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Push image
docker tag my-image us-central1-docker.pkg.dev/my-project/my-repo/my-image:v1
docker push us-central1-docker.pkg.dev/my-project/my-repo/my-image:v1

# List images
gcloud artifacts docker images list us-central1-docker.pkg.dev/my-project/my-repo

# Delete image
gcloud artifacts docker images delete \
    us-central1-docker.pkg.dev/my-project/my-repo/my-image:v1
```

## Output Formatting

### Format Options

```bash
# JSON output
gcloud compute instances list --format=json

# YAML output
gcloud compute instances list --format=yaml

# Table output
gcloud compute instances list --format=table

# Custom format
gcloud compute instances list \
    --format="table(name,zone,machineType,status)"

# Value only
gcloud compute instances describe my-instance \
    --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# CSV output
gcloud compute instances list \
    --format="csv(name,zone,machineType)"
```

### Filtering

```bash
# Filter by field
gcloud compute instances list --filter="status=RUNNING"

# Multiple filters
gcloud compute instances list \
    --filter="status=RUNNING AND machineType:n2-*"

# Filter by label
gcloud compute instances list --filter="labels.env=production"

# Filter by creation time
gcloud compute instances list \
    --filter="creationTimestamp>'2024-01-01'"
```

## Troubleshooting

### Debug Mode

```bash
# Enable verbose output
gcloud compute instances list --verbosity=debug

# Log HTTP requests
gcloud compute instances list --log-http

# Check current configuration
gcloud info

# Check authentication
gcloud auth list
gcloud config list account
```

### Common Errors

```bash
# Permission denied - check IAM roles
gcloud projects get-iam-policy my-project

# API not enabled
gcloud services enable compute.googleapis.com
gcloud services enable run.googleapis.com

# Quota exceeded
gcloud compute project-info describe --format="yaml(quotas)"
gcloud compute regions describe us-central1 --format="yaml(quotas)"

# Network errors
gcloud compute firewall-rules list
gcloud compute routes list
```

---

*GCP Networking, IAM & Operations Skill v1.0*
*Layer 3 Technical Skill*
*Used by: faion-devops-agent*

## Sources

- [VPC Documentation](https://cloud.google.com/vpc/docs)
- [Cloud Load Balancing](https://cloud.google.com/load-balancing/docs)
- [Cloud CDN](https://cloud.google.com/cdn/docs)
- [Cloud Armor](https://cloud.google.com/armor/docs)
- [VPC Networking Best Practices](https://cloud.google.com/vpc/docs/best-practices)
