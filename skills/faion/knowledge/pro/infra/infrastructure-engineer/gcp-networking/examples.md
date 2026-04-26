# GCP Networking Examples

## Example 1: Production VPC with GKE

Multi-region VPC optimized for Kubernetes workloads.

### Architecture

```
production-vpc (global)
├── prod-us-central1 (10.0.0.0/20)
│   ├── pods: 10.4.0.0/14
│   └── services: 10.8.0.0/20
├── prod-europe-west1 (10.1.0.0/20)
│   ├── pods: 10.12.0.0/14
│   └── services: 10.16.0.0/20
└── prod-asia-east1 (10.2.0.0/20)
    ├── pods: 10.20.0.0/14
    └── services: 10.24.0.0/20
```

### Implementation

```bash
# Create VPC
gcloud compute networks create production-vpc \
    --subnet-mode=custom \
    --bgp-routing-mode=global

# US Central subnet with GKE ranges
gcloud compute networks subnets create prod-us-central1 \
    --network=production-vpc \
    --region=us-central1 \
    --range=10.0.0.0/20 \
    --secondary-range=pods=10.4.0.0/14,services=10.8.0.0/20 \
    --enable-private-ip-google-access \
    --enable-flow-logs \
    --logging-aggregation-interval=interval-5-sec \
    --logging-flow-sampling=0.5

# Europe West subnet
gcloud compute networks subnets create prod-europe-west1 \
    --network=production-vpc \
    --region=europe-west1 \
    --range=10.1.0.0/20 \
    --secondary-range=pods=10.12.0.0/14,services=10.16.0.0/20 \
    --enable-private-ip-google-access \
    --enable-flow-logs

# Asia East subnet
gcloud compute networks subnets create prod-asia-east1 \
    --network=production-vpc \
    --region=asia-east1 \
    --range=10.2.0.0/20 \
    --secondary-range=pods=10.20.0.0/14,services=10.24.0.0/20 \
    --enable-private-ip-google-access \
    --enable-flow-logs
```

---

## Example 2: Secure Firewall Configuration

Defense-in-depth firewall strategy with logging.

### Rule Hierarchy

| Priority | Rule | Purpose |
|----------|------|---------|
| 100 | allow-iap-ssh | IAP tunnel access |
| 200 | allow-health-checks | GCP health checks |
| 500 | allow-internal | Inter-subnet traffic |
| 1000 | allow-https-ingress | Public HTTPS |
| 65534 | deny-all-ingress | Default deny |

### Implementation

```bash
# Allow IAP SSH (most restrictive source)
gcloud compute firewall-rules create allow-iap-ssh \
    --network=production-vpc \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:22 \
    --source-ranges=35.235.240.0/20 \
    --target-service-accounts=bastion@project.iam.gserviceaccount.com \
    --priority=100 \
    --enable-logging \
    --description="Allow SSH via IAP to bastion hosts"

# Allow GCP health checks
gcloud compute firewall-rules create allow-health-checks \
    --network=production-vpc \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:80,tcp:443,tcp:8080 \
    --source-ranges=130.211.0.0/22,35.191.0.0/16 \
    --target-tags=lb-backend \
    --priority=200 \
    --description="Allow GCP load balancer health checks"

# Allow internal traffic
gcloud compute firewall-rules create allow-internal \
    --network=production-vpc \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp,udp,icmp \
    --source-ranges=10.0.0.0/8 \
    --priority=500 \
    --description="Allow internal RFC1918 traffic"

# Allow HTTPS ingress
gcloud compute firewall-rules create allow-https-ingress \
    --network=production-vpc \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:443 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=https-server \
    --priority=1000 \
    --enable-logging \
    --description="Allow public HTTPS traffic"

# Default deny all ingress
gcloud compute firewall-rules create deny-all-ingress \
    --network=production-vpc \
    --direction=INGRESS \
    --action=DENY \
    --rules=all \
    --source-ranges=0.0.0.0/0 \
    --priority=65534 \
    --enable-logging \
    --description="Default deny all ingress"
```

---

## Example 3: Cloud NAT for Private GKE

NAT configuration for clusters without public IPs.

### Architecture

```
Private GKE Cluster
├── Nodes: No external IPs
├── Cloud NAT: Outbound internet
└── Private Google Access: GCP APIs
```

### Implementation

```bash
# Create Cloud Router
gcloud compute routers create gke-nat-router \
    --network=production-vpc \
    --region=us-central1

# Create Cloud NAT with manual IP allocation
gcloud compute addresses create nat-ip-1 nat-ip-2 \
    --region=us-central1

gcloud compute routers nats create gke-nat \
    --router=gke-nat-router \
    --region=us-central1 \
    --nat-custom-subnet-ip-ranges=prod-us-central1 \
    --nat-external-ip-pool=nat-ip-1,nat-ip-2 \
    --min-ports-per-vm=64 \
    --max-ports-per-vm=4096 \
    --tcp-established-idle-timeout=1200s \
    --enable-logging

# Verify NAT status
gcloud compute routers get-nat-mapping-info gke-nat-router \
    --region=us-central1
```

---

## Example 4: Global HTTPS Load Balancer

Production load balancer with Cloud Armor and CDN.

### Components

```
Internet
    │
    ▼
Global Forwarding Rule (External IP)
    │
    ▼
HTTPS Proxy (SSL Certificate)
    │
    ▼
URL Map (Path routing)
    │
    ├──► /api/* → API Backend Service
    │               ├── us-central1-a MIG
    │               └── europe-west1-b MIG
    │
    └──► /* → Web Backend Service (CDN enabled)
                ├── us-central1-a MIG
                └── europe-west1-b MIG
```

### Implementation

```bash
# Reserve global IP
gcloud compute addresses create web-lb-ip --global

# Create health checks
gcloud compute health-checks create http api-health \
    --port=8080 \
    --request-path=/health \
    --check-interval=10s \
    --timeout=5s \
    --healthy-threshold=2 \
    --unhealthy-threshold=3

gcloud compute health-checks create http web-health \
    --port=80 \
    --request-path=/ \
    --check-interval=10s

# Create backend services
gcloud compute backend-services create api-backend \
    --protocol=HTTP \
    --port-name=api \
    --health-checks=api-health \
    --timeout=30s \
    --global

gcloud compute backend-services create web-backend \
    --protocol=HTTP \
    --port-name=http \
    --health-checks=web-health \
    --enable-cdn \
    --cache-mode=CACHE_ALL_STATIC \
    --default-ttl=3600 \
    --global

# Add backends (MIGs must exist)
gcloud compute backend-services add-backend api-backend \
    --instance-group=api-mig-us \
    --instance-group-zone=us-central1-a \
    --balancing-mode=UTILIZATION \
    --max-utilization=0.8 \
    --global

gcloud compute backend-services add-backend web-backend \
    --instance-group=web-mig-us \
    --instance-group-zone=us-central1-a \
    --balancing-mode=UTILIZATION \
    --max-utilization=0.8 \
    --global

# Create URL map with path rules
gcloud compute url-maps create web-url-map \
    --default-service=web-backend

gcloud compute url-maps add-path-matcher web-url-map \
    --path-matcher-name=api-matcher \
    --default-service=api-backend \
    --path-rules="/api/*=api-backend"

# Create managed SSL certificate
gcloud compute ssl-certificates create web-cert \
    --domains=example.com,www.example.com \
    --global

# Create HTTPS proxy
gcloud compute target-https-proxies create web-https-proxy \
    --url-map=web-url-map \
    --ssl-certificates=web-cert

# Create forwarding rule
gcloud compute forwarding-rules create web-https-lb \
    --global \
    --address=web-lb-ip \
    --target-https-proxy=web-https-proxy \
    --ports=443
```

### Cloud Armor Policy

```bash
# Create security policy
gcloud compute security-policies create web-security-policy \
    --description="Web application security policy"

# Add OWASP rules
gcloud compute security-policies rules create 1000 \
    --security-policy=web-security-policy \
    --expression="evaluatePreconfiguredExpr('xss-v33-stable')" \
    --action=deny-403

gcloud compute security-policies rules create 1001 \
    --security-policy=web-security-policy \
    --expression="evaluatePreconfiguredExpr('sqli-v33-stable')" \
    --action=deny-403

# Rate limiting
gcloud compute security-policies rules create 2000 \
    --security-policy=web-security-policy \
    --src-ip-ranges="*" \
    --action=throttle \
    --rate-limit-threshold-count=100 \
    --rate-limit-threshold-interval-sec=60 \
    --conform-action=allow \
    --exceed-action=deny-429

# Attach to backend
gcloud compute backend-services update web-backend \
    --security-policy=web-security-policy \
    --global
```

---

## Example 5: Shared VPC Architecture

Centralized networking for multi-project organization.

### Architecture

```
Organization
├── networking-host-project (Host Project)
│   └── shared-vpc
│       ├── prod-subnet-us (10.0.0.0/20)
│       ├── prod-subnet-eu (10.1.0.0/20)
│       └── dev-subnet-us (10.10.0.0/20)
│
├── team-a-prod (Service Project)
│   └── Uses: prod-subnet-us
│
├── team-b-prod (Service Project)
│   └── Uses: prod-subnet-eu
│
└── team-a-dev (Service Project)
    └── Uses: dev-subnet-us
```

### Implementation

```bash
# Enable Shared VPC (run as org admin)
gcloud compute shared-vpc enable networking-host-project

# Create VPC and subnets in host project
gcloud compute networks create shared-vpc \
    --project=networking-host-project \
    --subnet-mode=custom

gcloud compute networks subnets create prod-subnet-us \
    --project=networking-host-project \
    --network=shared-vpc \
    --region=us-central1 \
    --range=10.0.0.0/20 \
    --enable-private-ip-google-access

# Associate service projects
gcloud compute shared-vpc associated-projects add team-a-prod \
    --host-project=networking-host-project

gcloud compute shared-vpc associated-projects add team-b-prod \
    --host-project=networking-host-project

# Grant subnet access to service project
gcloud projects add-iam-policy-binding networking-host-project \
    --member="serviceAccount:team-a-sa@team-a-prod.iam.gserviceaccount.com" \
    --role="roles/compute.networkUser" \
    --condition="expression=resource.name.startsWith('projects/networking-host-project/regions/us-central1/subnetworks/prod-subnet-us'),title=subnet-access"
```

---

## Example 6: VPC Peering Configuration

Connect two VPCs for private communication.

### Architecture

```
production-vpc (10.0.0.0/16)
        │
        │ VPC Peering (bidirectional)
        │
shared-services-vpc (10.100.0.0/16)
    ├── DNS server
    ├── Monitoring
    └── CI/CD runners
```

### Implementation

```bash
# Create peering from production to shared-services
gcloud compute networks peerings create prod-to-shared \
    --network=production-vpc \
    --peer-project=shared-services-project \
    --peer-network=shared-services-vpc \
    --export-custom-routes \
    --import-custom-routes

# Create peering from shared-services to production
gcloud compute networks peerings create shared-to-prod \
    --network=shared-services-vpc \
    --peer-project=production-project \
    --peer-network=production-vpc \
    --export-custom-routes \
    --import-custom-routes

# Verify peering status
gcloud compute networks peerings list --network=production-vpc
```

---

*GCP Networking Examples | faion-infrastructure-engineer*
