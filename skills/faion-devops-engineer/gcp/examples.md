# GCP CLI Examples

Comprehensive gcloud CLI command reference for Google Cloud Platform operations.

---

## Configuration

### Authentication

```bash
# Interactive login (opens browser)
gcloud auth login

# Service account authentication
gcloud auth activate-service-account --key-file=service-account.json

# Application default credentials (local development)
gcloud auth application-default login

# List authenticated accounts
gcloud auth list

# Revoke credentials
gcloud auth revoke [ACCOUNT]

# Print access token (for API calls)
gcloud auth print-access-token
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

### Named Configurations

```bash
# Create named configuration
gcloud config configurations create production

# Activate configuration
gcloud config configurations activate production

# Set properties in current config
gcloud config set compute/zone us-central1-a
gcloud config set compute/region us-central1

# View all configurations
gcloud config configurations list

# View current config
gcloud config list
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

---

## GKE (Google Kubernetes Engine)

### Cluster Management

```bash
# Create Autopilot cluster (recommended)
gcloud container clusters create-auto my-autopilot-cluster \
    --region=us-central1

# Create Standard cluster
gcloud container clusters create my-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --machine-type=e2-standard-4 \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=10

# Create private cluster
gcloud container clusters create my-private-cluster \
    --zone=us-central1-a \
    --enable-private-nodes \
    --enable-private-endpoint \
    --master-ipv4-cidr=172.16.0.0/28

# Get cluster credentials (configure kubectl)
gcloud container clusters get-credentials my-cluster \
    --zone=us-central1-a

# List clusters
gcloud container clusters list

# Describe cluster
gcloud container clusters describe my-cluster --zone=us-central1-a

# Delete cluster
gcloud container clusters delete my-cluster --zone=us-central1-a
```

### Node Pools

```bash
# Create node pool
gcloud container node-pools create my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --machine-type=n2-standard-8

# Create Spot node pool
gcloud container node-pools create spot-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --spot \
    --num-nodes=5 \
    --enable-autoscaling \
    --min-nodes=0 \
    --max-nodes=20

# Create GPU node pool
gcloud container node-pools create gpu-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --num-nodes=1

# Enable autoscaling on existing pool
gcloud container node-pools update my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=20

# List node pools
gcloud container node-pools list --cluster=my-cluster --zone=us-central1-a

# Delete node pool
gcloud container node-pools delete my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a
```

### Workload Identity

```bash
# Enable Workload Identity on cluster
gcloud container clusters update my-cluster \
    --zone=us-central1-a \
    --workload-pool=my-project.svc.id.goog

# Create GCP service account
gcloud iam service-accounts create my-gsa

# Grant IAM roles to GSA
gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:my-gsa@my-project.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer"

# Bind KSA to GSA
gcloud iam service-accounts add-iam-policy-binding my-gsa@my-project.iam.gserviceaccount.com \
    --role="roles/iam.workloadIdentityUser" \
    --member="serviceAccount:my-project.svc.id.goog[my-namespace/my-ksa]"
```

### Cluster Upgrades

```bash
# Get available versions
gcloud container get-server-config --zone=us-central1-a

# Upgrade control plane
gcloud container clusters upgrade my-cluster \
    --zone=us-central1-a \
    --master \
    --cluster-version=1.28

# Upgrade node pool
gcloud container clusters upgrade my-cluster \
    --zone=us-central1-a \
    --node-pool=default-pool
```

---

## Cloud Run

### Service Deployment

```bash
# Deploy from source (builds automatically)
gcloud run deploy my-service \
    --source=. \
    --region=us-central1 \
    --allow-unauthenticated

# Deploy from container image
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated

# Deploy with environment variables
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --set-env-vars=DATABASE_URL=xxx,API_KEY=yyy

# Deploy with secrets
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --set-secrets=API_KEY=my-secret:latest

# Deploy with resource limits
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --memory=2Gi \
    --cpu=2 \
    --concurrency=100 \
    --max-instances=10 \
    --min-instances=1

# Deploy with VPC connector
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --vpc-connector=my-connector \
    --vpc-egress=all-traffic
```

### Service Management

```bash
# List services
gcloud run services list

# Describe service
gcloud run services describe my-service --region=us-central1

# Get service URL
gcloud run services describe my-service \
    --region=us-central1 \
    --format='value(status.url)'

# Update service
gcloud run services update my-service \
    --region=us-central1 \
    --memory=4Gi

# Delete service
gcloud run services delete my-service --region=us-central1
```

### Traffic Management

```bash
# Deploy new revision without traffic
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:v2 \
    --region=us-central1 \
    --tag=green \
    --no-traffic

# Split traffic (canary deployment)
gcloud run services update-traffic my-service \
    --region=us-central1 \
    --to-tags=green=10,latest=90

# Route all traffic to latest
gcloud run services update-traffic my-service \
    --region=us-central1 \
    --to-latest

# Rollback to previous revision
gcloud run services update-traffic my-service \
    --region=us-central1 \
    --to-revisions=my-service-00001=100
```

---

## IAM

### Service Accounts

```bash
# Create service account
gcloud iam service-accounts create my-service-account \
    --display-name="My Service Account"

# List service accounts
gcloud iam service-accounts list

# Create key (avoid if possible - use Workload Identity)
gcloud iam service-accounts keys create key.json \
    --iam-account=my-sa@my-project.iam.gserviceaccount.com

# List keys
gcloud iam service-accounts keys list \
    --iam-account=my-sa@my-project.iam.gserviceaccount.com

# Delete key
gcloud iam service-accounts keys delete KEY_ID \
    --iam-account=my-sa@my-project.iam.gserviceaccount.com

# Disable service account
gcloud iam service-accounts disable my-sa@my-project.iam.gserviceaccount.com

# Delete service account
gcloud iam service-accounts delete my-sa@my-project.iam.gserviceaccount.com
```

### IAM Bindings

```bash
# View project IAM policy
gcloud projects get-iam-policy my-project

# Add user binding
gcloud projects add-iam-policy-binding my-project \
    --member=user:user@example.com \
    --role=roles/viewer

# Add service account binding
gcloud projects add-iam-policy-binding my-project \
    --member=serviceAccount:my-sa@my-project.iam.gserviceaccount.com \
    --role=roles/storage.admin

# Add binding with condition
gcloud projects add-iam-policy-binding my-project \
    --member=user:user@example.com \
    --role=roles/storage.objectViewer \
    --condition='expression=request.time < timestamp("2025-12-31T00:00:00Z"),title=temporary-access'

# Remove binding
gcloud projects remove-iam-policy-binding my-project \
    --member=user:user@example.com \
    --role=roles/viewer

# Grant Cloud Run invoker
gcloud run services add-iam-policy-binding my-service \
    --region=us-central1 \
    --member=allUsers \
    --role=roles/run.invoker
```

### Workload Identity Federation

```bash
# Create workload identity pool
gcloud iam workload-identity-pools create my-pool \
    --location="global" \
    --display-name="My Pool"

# Create OIDC provider (GitHub Actions)
gcloud iam workload-identity-pools providers create-oidc github-provider \
    --location="global" \
    --workload-identity-pool="my-pool" \
    --display-name="GitHub Actions" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository"

# Grant service account impersonation
gcloud iam service-accounts add-iam-policy-binding my-sa@my-project.iam.gserviceaccount.com \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/my-pool/attribute.repository/my-org/my-repo"

# List pools
gcloud iam workload-identity-pools list --location="global"

# List providers
gcloud iam workload-identity-pools providers list \
    --location="global" \
    --workload-identity-pool="my-pool"
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

---

## VPC Networking

### VPC and Subnets

```bash
# Create VPC network
gcloud compute networks create my-vpc \
    --subnet-mode=custom

# Create subnet
gcloud compute networks subnets create my-subnet \
    --network=my-vpc \
    --region=us-central1 \
    --range=10.0.0.0/24

# Create subnet with secondary ranges (for GKE)
gcloud compute networks subnets create my-gke-subnet \
    --network=my-vpc \
    --region=us-central1 \
    --range=10.0.0.0/24 \
    --secondary-range=pods=10.1.0.0/16,services=10.2.0.0/20

# Enable Private Google Access
gcloud compute networks subnets update my-subnet \
    --region=us-central1 \
    --enable-private-ip-google-access

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
# Allow SSH
gcloud compute firewall-rules create allow-ssh \
    --network=my-vpc \
    --allow=tcp:22 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=ssh-enabled

# Allow HTTP/HTTPS
gcloud compute firewall-rules create allow-http \
    --network=my-vpc \
    --allow=tcp:80,tcp:443 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server

# Allow internal traffic
gcloud compute firewall-rules create allow-internal \
    --network=my-vpc \
    --allow=tcp,udp,icmp \
    --source-ranges=10.0.0.0/8

# Deny all ingress (apply first)
gcloud compute firewall-rules create deny-all-ingress \
    --network=my-vpc \
    --direction=INGRESS \
    --action=DENY \
    --rules=all \
    --priority=65534

# List firewall rules
gcloud compute firewall-rules list

# Delete firewall rule
gcloud compute firewall-rules delete allow-ssh
```

### Cloud NAT

```bash
# Create router
gcloud compute routers create my-router \
    --network=my-vpc \
    --region=us-central1

# Create Cloud NAT
gcloud compute routers nats create my-nat \
    --router=my-router \
    --region=us-central1 \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips

# List NAT configurations
gcloud compute routers nats list --router=my-router --region=us-central1
```

### VPC Connector (for Cloud Run/Functions)

```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create my-connector \
    --region=us-central1 \
    --network=my-vpc \
    --range=10.8.0.0/28

# List connectors
gcloud compute networks vpc-access connectors list --region=us-central1

# Delete connector
gcloud compute networks vpc-access connectors delete my-connector --region=us-central1
```

### Private Service Connect

```bash
# Create PSC endpoint for Google APIs
gcloud compute addresses create psc-endpoint-ip \
    --global \
    --purpose=PRIVATE_SERVICE_CONNECT \
    --addresses=10.0.100.1 \
    --network=my-vpc

gcloud compute forwarding-rules create psc-endpoint \
    --global \
    --network=my-vpc \
    --address=psc-endpoint-ip \
    --target-google-apis-bundle=all-apis
```

---

## Cloud Storage

### Bucket Operations

```bash
# Create bucket
gcloud storage buckets create gs://my-bucket \
    --location=us-central1 \
    --uniform-bucket-level-access

# Create bucket with lifecycle
gcloud storage buckets create gs://my-archive-bucket \
    --location=us \
    --storage-class=archive

# Enable versioning
gcloud storage buckets update gs://my-bucket --versioning

# List buckets
gcloud storage buckets list

# Delete bucket with contents
gcloud storage rm -r gs://my-bucket
```

### Object Operations

```bash
# Copy files
gcloud storage cp local-file.txt gs://my-bucket/
gcloud storage cp gs://my-bucket/file.txt ./local/
gcloud storage cp -r ./local-dir gs://my-bucket/

# Sync directories
gcloud storage rsync -r ./local-dir gs://my-bucket/path
gcloud storage rsync -r -d ./local-dir gs://my-bucket/  # -d deletes extra

# List objects
gcloud storage ls gs://my-bucket
gcloud storage ls gs://my-bucket/** --recursive

# Delete objects
gcloud storage rm gs://my-bucket/file.txt
gcloud storage rm -r gs://my-bucket/path/
```

---

## Secret Manager

```bash
# Create secret
gcloud secrets create my-secret

# Add secret version
echo -n "my-secret-value" | gcloud secrets versions add my-secret --data-file=-

# Add from file
gcloud secrets versions add my-secret --data-file=secret.txt

# Access secret
gcloud secrets versions access latest --secret=my-secret

# List secrets
gcloud secrets list

# Grant access
gcloud secrets add-iam-policy-binding my-secret \
    --member=serviceAccount:my-sa@my-project.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor

# Delete secret
gcloud secrets delete my-secret
```

---

## Cloud SQL

### Instance Management

```bash
# Create PostgreSQL instance
gcloud sql instances create my-postgres \
    --database-version=POSTGRES_15 \
    --tier=db-custom-2-7680 \
    --region=us-central1 \
    --root-password=secretpassword \
    --storage-size=100GB \
    --storage-auto-increase

# Create with private IP only
gcloud sql instances create my-postgres \
    --database-version=POSTGRES_15 \
    --tier=db-custom-2-7680 \
    --region=us-central1 \
    --network=my-vpc \
    --no-assign-ip

# List instances
gcloud sql instances list

# Stop instance (save costs)
gcloud sql instances patch my-postgres --activation-policy=NEVER

# Start instance
gcloud sql instances patch my-postgres --activation-policy=ALWAYS

# Delete instance
gcloud sql instances delete my-postgres
```

### Database and Users

```bash
# Create database
gcloud sql databases create mydb --instance=my-postgres

# Create user
gcloud sql users create myuser \
    --instance=my-postgres \
    --password=userpassword

# Connect directly
gcloud sql connect my-postgres --user=postgres
```

---

## Monitoring and Logging

### Logging

```bash
# Read logs
gcloud logging read "resource.type=gce_instance" --limit=50

# Read with filter
gcloud logging read 'severity>=ERROR AND resource.type="cloud_run_revision"' \
    --limit=100

# Stream logs (tail)
gcloud logging tail "resource.type=cloud_run_revision"

# Write log entry
gcloud logging write my-log "Test log message" --severity=INFO
```

### Recommender (Cost Optimization)

```bash
# Find idle resources
gcloud recommender recommendations list \
    --project=my-project \
    --location=us-central1-a \
    --recommender=google.compute.instance.IdleResourceRecommender

# IAM recommendations
gcloud recommender recommendations list \
    --project=my-project \
    --location=global \
    --recommender=google.iam.policy.Recommender
```

---

## Output Formatting

```bash
# JSON output
gcloud compute instances list --format=json

# YAML output
gcloud compute instances list --format=yaml

# Custom table
gcloud compute instances list \
    --format="table(name,zone,machineType,status)"

# Value only
gcloud compute instances describe my-instance \
    --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# Filtering
gcloud compute instances list --filter="status=RUNNING"
gcloud compute instances list --filter="labels.env=production"
```

---

## Troubleshooting

```bash
# Enable verbose output
gcloud compute instances list --verbosity=debug

# Log HTTP requests
gcloud compute instances list --log-http

# Check current configuration
gcloud info

# Enable API
gcloud services enable compute.googleapis.com

# Check quotas
gcloud compute project-info describe --format="yaml(quotas)"
gcloud compute regions describe us-central1 --format="yaml(quotas)"
```

---

*GCP CLI Examples v2.0 | Updated: 2026-01*
