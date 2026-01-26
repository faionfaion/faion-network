# GCP Examples

Practical examples for Compute Engine, Cloud Run, IAM, and networking configurations (2025-2026).

## Compute Engine Examples

### Launch Instance with Best Practices

```bash
# Create instance with Shielded VM and OS Login
gcloud compute instances create web-server \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-balanced \
    --boot-disk-device-name=web-server \
    --shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --no-address \
    --subnet=private-subnet \
    --service-account=web-server@my-project.iam.gserviceaccount.com \
    --scopes=cloud-platform \
    --tags=web-server,allow-health-check \
    --metadata=enable-oslogin=TRUE \
    --labels=environment=production,team=platform
```

### Create Instance Template (Autoscaling Ready)

```bash
gcloud compute instance-templates create web-template \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-balanced \
    --shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --no-address \
    --network=my-vpc \
    --subnet=private-subnet \
    --region=us-central1 \
    --service-account=web-server@my-project.iam.gserviceaccount.com \
    --scopes=cloud-platform \
    --tags=web-server,allow-health-check \
    --metadata=enable-oslogin=TRUE,startup-script-url=gs://my-bucket/startup.sh \
    --labels=environment=production
```

### Regional Managed Instance Group with Autoscaling

```bash
# Create health check
gcloud compute health-checks create http web-health-check \
    --port=8080 \
    --request-path=/health \
    --check-interval=10s \
    --timeout=5s \
    --healthy-threshold=2 \
    --unhealthy-threshold=3

# Create regional MIG
gcloud compute instance-groups managed create web-mig \
    --region=us-central1 \
    --template=web-template \
    --size=3 \
    --health-check=web-health-check \
    --initial-delay=300

# Configure autoscaling
gcloud compute instance-groups managed set-autoscaling web-mig \
    --region=us-central1 \
    --min-num-replicas=2 \
    --max-num-replicas=10 \
    --target-cpu-utilization=0.6 \
    --cool-down-period=90

# Set named ports
gcloud compute instance-groups managed set-named-ports web-mig \
    --region=us-central1 \
    --named-ports=http:8080
```

### GKE Autopilot Cluster (Recommended)

```bash
# Create Autopilot cluster (fully managed)
gcloud container clusters create-auto my-cluster \
    --region=us-central1 \
    --network=my-vpc \
    --subnetwork=gke-subnet \
    --cluster-secondary-range-name=pods \
    --services-secondary-range-name=services \
    --enable-private-nodes \
    --master-ipv4-cidr=172.16.0.0/28 \
    --enable-master-authorized-networks \
    --master-authorized-networks=10.0.0.0/8 \
    --workload-pool=my-project.svc.id.goog
```

### GKE Standard Cluster (Hardened)

```bash
# Create private GKE cluster with Workload Identity
gcloud container clusters create my-cluster \
    --region=us-central1 \
    --num-nodes=1 \
    --machine-type=e2-standard-4 \
    --network=my-vpc \
    --subnetwork=gke-subnet \
    --cluster-secondary-range-name=pods \
    --services-secondary-range-name=services \
    --enable-ip-alias \
    --enable-private-nodes \
    --enable-private-endpoint \
    --master-ipv4-cidr=172.16.0.0/28 \
    --enable-master-authorized-networks \
    --master-authorized-networks=10.0.0.0/8 \
    --workload-pool=my-project.svc.id.goog \
    --enable-shielded-nodes \
    --enable-network-policy \
    --enable-dataplane-v2 \
    --release-channel=regular \
    --enable-autorepair \
    --enable-autoupgrade \
    --enable-vertical-pod-autoscaling \
    --enable-image-streaming \
    --logging=SYSTEM,WORKLOAD \
    --monitoring=SYSTEM
```

## Cloud Run Examples

### Deploy Service with Best Practices

```bash
# Deploy from container image with security settings
gcloud run deploy my-api \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-api:v1.0.0 \
    --region=us-central1 \
    --platform=managed \
    --service-account=my-api@my-project.iam.gserviceaccount.com \
    --set-secrets=DATABASE_URL=db-connection:latest,API_KEY=api-key:latest \
    --vpc-connector=my-connector \
    --vpc-egress=all-traffic \
    --cpu=1 \
    --memory=512Mi \
    --concurrency=80 \
    --min-instances=1 \
    --max-instances=10 \
    --timeout=60s \
    --cpu-throttling \
    --execution-environment=gen2 \
    --ingress=internal-and-cloud-load-balancing \
    --no-allow-unauthenticated
```

### Deploy from Source (Build Automatically)

```bash
gcloud run deploy my-app \
    --source=. \
    --region=us-central1 \
    --service-account=my-app@my-project.iam.gserviceaccount.com \
    --set-env-vars=LOG_LEVEL=info,ENV=production \
    --min-instances=1 \
    --max-instances=5 \
    --ingress=all \
    --allow-unauthenticated
```

### Cloud Run with VPC Connector

```bash
# Create VPC connector (requires Serverless VPC Access API)
gcloud compute networks vpc-access connectors create my-connector \
    --region=us-central1 \
    --network=my-vpc \
    --range=10.8.0.0/28 \
    --min-instances=2 \
    --max-instances=10

# Deploy with VPC connector
gcloud run deploy my-app \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-app:latest \
    --region=us-central1 \
    --vpc-connector=my-connector \
    --vpc-egress=all-traffic \
    --set-env-vars=DB_HOST=10.0.0.5
```

### Traffic Management (Blue-Green)

```bash
# Deploy new revision without traffic
gcloud run deploy my-app \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-app:v2.0.0 \
    --region=us-central1 \
    --tag=green \
    --no-traffic

# Test green deployment
curl https://green---my-app-abc123.run.app/health

# Gradually shift traffic
gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-tags=green=10

# Full cutover
gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-tags=green=100

# Rollback if needed
gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-latest
```

### Cloud Functions (Gen2 on Cloud Run)

```bash
# Deploy HTTP function
gcloud functions deploy my-function \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=handler \
    --trigger-http \
    --service-account=my-function@my-project.iam.gserviceaccount.com \
    --set-secrets=API_KEY=api-key:latest \
    --memory=256Mi \
    --timeout=60s \
    --min-instances=0 \
    --max-instances=100 \
    --no-allow-unauthenticated

# Deploy Pub/Sub triggered function
gcloud functions deploy process-messages \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=process \
    --trigger-topic=my-topic \
    --service-account=processor@my-project.iam.gserviceaccount.com
```

## IAM Examples

### Create Service Account with Least Privilege

```bash
# Create service account
gcloud iam service-accounts create my-app \
    --display-name="My Application Service Account" \
    --description="Service account for my-app workload"

# Grant specific roles
gcloud projects add-iam-policy-binding my-project \
    --member=serviceAccount:my-app@my-project.iam.gserviceaccount.com \
    --role=roles/storage.objectViewer \
    --condition='expression=resource.name.startsWith("projects/_/buckets/my-bucket"),title=my-bucket-only'

gcloud projects add-iam-policy-binding my-project \
    --member=serviceAccount:my-app@my-project.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor

# Grant Cloud SQL client
gcloud projects add-iam-policy-binding my-project \
    --member=serviceAccount:my-app@my-project.iam.gserviceaccount.com \
    --role=roles/cloudsql.client
```

### Workload Identity for GKE

```bash
# Create Kubernetes service account
kubectl create serviceaccount my-app -n default

# Create GCP service account
gcloud iam service-accounts create my-app-gsa \
    --display-name="GKE Workload Identity SA"

# Bind Kubernetes SA to GCP SA
gcloud iam service-accounts add-iam-policy-binding my-app-gsa@my-project.iam.gserviceaccount.com \
    --role=roles/iam.workloadIdentityUser \
    --member="serviceAccount:my-project.svc.id.goog[default/my-app]"

# Annotate Kubernetes SA
kubectl annotate serviceaccount my-app \
    iam.gke.io/gcp-service-account=my-app-gsa@my-project.iam.gserviceaccount.com

# Grant permissions to GCP SA
gcloud projects add-iam-policy-binding my-project \
    --member=serviceAccount:my-app-gsa@my-project.iam.gserviceaccount.com \
    --role=roles/storage.objectViewer
```

### Workload Identity Federation (External)

```bash
# Create workload identity pool
gcloud iam workload-identity-pools create github-pool \
    --location=global \
    --display-name="GitHub Actions Pool"

# Create OIDC provider
gcloud iam workload-identity-pools providers create-oidc github-provider \
    --location=global \
    --workload-identity-pool=github-pool \
    --display-name="GitHub OIDC" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.actor=assertion.actor"

# Create service account for GitHub Actions
gcloud iam service-accounts create github-deploy \
    --display-name="GitHub Actions Deploy"

# Allow GitHub repo to impersonate SA
gcloud iam service-accounts add-iam-policy-binding github-deploy@my-project.iam.gserviceaccount.com \
    --role=roles/iam.workloadIdentityUser \
    --member="principalSet://iam.googleapis.com/projects/123456789/locations/global/workloadIdentityPools/github-pool/attribute.repository/my-org/my-repo"
```

### Custom Role

```bash
# Create custom role with specific permissions
gcloud iam roles create myAppRole \
    --project=my-project \
    --title="My App Custom Role" \
    --description="Minimal permissions for my-app" \
    --permissions=storage.objects.get,storage.objects.list,secretmanager.versions.access \
    --stage=GA
```

## Networking Examples

### VPC with Three-Tier Subnets

```bash
# Create custom VPC
gcloud compute networks create my-vpc \
    --subnet-mode=custom \
    --bgp-routing-mode=regional

# Public subnet (for NAT, bastion if needed)
gcloud compute networks subnets create public-subnet \
    --network=my-vpc \
    --region=us-central1 \
    --range=10.0.1.0/24 \
    --enable-flow-logs \
    --logging-aggregation-interval=interval-5-sec \
    --logging-flow-sampling=0.5

# Private subnet (application workloads)
gcloud compute networks subnets create private-subnet \
    --network=my-vpc \
    --region=us-central1 \
    --range=10.0.10.0/24 \
    --enable-private-ip-google-access \
    --enable-flow-logs

# GKE subnet with secondary ranges
gcloud compute networks subnets create gke-subnet \
    --network=my-vpc \
    --region=us-central1 \
    --range=10.0.20.0/24 \
    --secondary-range=pods=10.1.0.0/16,services=10.2.0.0/20 \
    --enable-private-ip-google-access \
    --enable-flow-logs

# Database subnet
gcloud compute networks subnets create database-subnet \
    --network=my-vpc \
    --region=us-central1 \
    --range=10.0.30.0/24 \
    --enable-private-ip-google-access
```

### Firewall Rules (Least Privilege)

```bash
# Deny all ingress by default (implicit, but explicit is better)
gcloud compute firewall-rules create deny-all-ingress \
    --network=my-vpc \
    --direction=INGRESS \
    --action=DENY \
    --rules=all \
    --priority=65534

# Allow IAP for SSH (no public SSH)
gcloud compute firewall-rules create allow-iap-ssh \
    --network=my-vpc \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:22 \
    --source-ranges=35.235.240.0/20 \
    --target-tags=allow-iap-ssh \
    --priority=1000

# Allow health checks from GCP load balancers
gcloud compute firewall-rules create allow-health-check \
    --network=my-vpc \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:8080 \
    --source-ranges=130.211.0.0/22,35.191.0.0/16 \
    --target-tags=allow-health-check \
    --priority=1000

# Allow internal traffic (private subnet to database)
gcloud compute firewall-rules create allow-app-to-db \
    --network=my-vpc \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:5432 \
    --source-ranges=10.0.10.0/24 \
    --target-tags=database \
    --priority=1000
```

### Cloud NAT (Outbound Internet)

```bash
# Create Cloud Router
gcloud compute routers create my-router \
    --network=my-vpc \
    --region=us-central1

# Create Cloud NAT
gcloud compute routers nats create my-nat \
    --router=my-router \
    --region=us-central1 \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips \
    --enable-logging \
    --log-filter=ERRORS_ONLY
```

### Global HTTPS Load Balancer

```bash
# Reserve global static IP
gcloud compute addresses create web-ip \
    --global

# Create health check
gcloud compute health-checks create http web-health \
    --port=8080 \
    --request-path=/health

# Create backend service
gcloud compute backend-services create web-backend \
    --protocol=HTTP \
    --port-name=http \
    --health-checks=web-health \
    --global \
    --enable-logging \
    --logging-sample-rate=1.0

# Add MIG to backend
gcloud compute backend-services add-backend web-backend \
    --instance-group=web-mig \
    --instance-group-region=us-central1 \
    --global

# Create URL map
gcloud compute url-maps create web-map \
    --default-service=web-backend

# Create managed SSL certificate
gcloud compute ssl-certificates create web-cert \
    --domains=example.com,www.example.com \
    --global

# Create HTTPS proxy
gcloud compute target-https-proxies create web-https-proxy \
    --url-map=web-map \
    --ssl-certificates=web-cert

# Create forwarding rule
gcloud compute forwarding-rules create web-https-rule \
    --global \
    --address=web-ip \
    --target-https-proxy=web-https-proxy \
    --ports=443
```

### Cloud Armor WAF Policy

```bash
# Create security policy
gcloud compute security-policies create my-policy \
    --description="WAF policy"

# Add OWASP rules
gcloud compute security-policies rules create 1000 \
    --security-policy=my-policy \
    --expression="evaluatePreconfiguredExpr('xss-v33-stable')" \
    --action=deny-403

gcloud compute security-policies rules create 1001 \
    --security-policy=my-policy \
    --expression="evaluatePreconfiguredExpr('sqli-v33-stable')" \
    --action=deny-403

# Rate limiting
gcloud compute security-policies rules create 2000 \
    --security-policy=my-policy \
    --expression="true" \
    --action=throttle \
    --rate-limit-threshold-count=100 \
    --rate-limit-threshold-interval-sec=60 \
    --conform-action=allow \
    --exceed-action=deny-429 \
    --enforce-on-key=IP

# Apply to backend
gcloud compute backend-services update web-backend \
    --security-policy=my-policy \
    --global
```

### VPC Service Controls Perimeter

```bash
# Create access policy (org level, once)
gcloud access-context-manager policies create \
    --organization=123456789 \
    --title="my-policy"

# Create service perimeter (dry-run first!)
gcloud access-context-manager perimeters dry-run create my-perimeter \
    --policy=accessPolicies/123456789 \
    --title="Production Perimeter" \
    --resources=projects/my-project \
    --restricted-services=storage.googleapis.com,bigquery.googleapis.com \
    --vpc-allowed-services=RESTRICTED-SERVICES \
    --enable-vpc-accessible-services

# After testing, enforce
gcloud access-context-manager perimeters dry-run enforce my-perimeter \
    --policy=accessPolicies/123456789
```

## Secret Manager Examples

```bash
# Create secret
gcloud secrets create db-password \
    --replication-policy=automatic

# Add secret version
echo -n "my-secure-password" | gcloud secrets versions add db-password --data-file=-

# Access secret
gcloud secrets versions access latest --secret=db-password

# Grant access to service account
gcloud secrets add-iam-policy-binding db-password \
    --member=serviceAccount:my-app@my-project.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor
```

## Sources

- [Compute Engine Best Practices](https://cloud.google.com/compute/docs/best-practices)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [Cloud Run Best Practices](https://cloud.google.com/run/docs/best-practices)
- [VPC Best Practices](https://cloud.google.com/vpc/docs/best-practices)
- [IAM Best Practices](https://cloud.google.com/iam/docs/using-iam-securely)
- [Cloud Armor WAF Rules](https://cloud.google.com/armor/docs/waf-rules)
- [VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs/overview)

---

*GCP Examples | faion-infrastructure-engineer*
