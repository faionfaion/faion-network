# GCP Compute Engine Examples

Practical gcloud CLI commands and patterns for VMs, instance groups, autoscaling, and Spot VMs.

## VM Management

### Create Standard VM

```bash
# Basic VM
gcloud compute instances create my-instance \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2404-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-balanced \
    --tags=http-server,https-server

# VM with startup script
gcloud compute instances create my-instance \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --metadata-from-file=startup-script=startup.sh

# VM with service account
gcloud compute instances create my-instance \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --service-account=my-sa@project.iam.gserviceaccount.com \
    --scopes=cloud-platform
```

### Create Spot VM

```bash
# Spot VM with STOP action
gcloud compute instances create my-spot-vm \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --provisioning-model=SPOT \
    --instance-termination-action=STOP \
    --image-family=ubuntu-2404-lts \
    --image-project=ubuntu-os-cloud

# Spot VM with DELETE action (for ephemeral workloads)
gcloud compute instances create batch-worker \
    --zone=us-central1-a \
    --machine-type=n2-standard-4 \
    --provisioning-model=SPOT \
    --instance-termination-action=DELETE \
    --metadata-from-file=startup-script=batch-startup.sh
```

### Create Preemptible VM (Legacy)

```bash
# Preemptible VM (max 24 hours, use Spot instead)
gcloud compute instances create my-preemptible \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --preemptible
```

### VM Operations

```bash
# List instances
gcloud compute instances list

# List in specific zone
gcloud compute instances list --zones=us-central1-a

# Describe instance
gcloud compute instances describe my-instance --zone=us-central1-a

# Start/stop/delete
gcloud compute instances start my-instance --zone=us-central1-a
gcloud compute instances stop my-instance --zone=us-central1-a
gcloud compute instances delete my-instance --zone=us-central1-a

# SSH into instance
gcloud compute ssh my-instance --zone=us-central1-a

# SSH with specific user
gcloud compute ssh user@my-instance --zone=us-central1-a

# Copy files
gcloud compute scp local-file.txt my-instance:/remote/path --zone=us-central1-a
gcloud compute scp my-instance:/remote/file.txt ./local/ --zone=us-central1-a
```

---

## Machine Types

### List and Filter Machine Types

```bash
# List all machine types in zone
gcloud compute machine-types list --zones=us-central1-a

# Filter by CPU/memory
gcloud compute machine-types list \
    --filter="guestCpus>=4 AND memoryMb>=16384" \
    --zones=us-central1-a

# List machine type families
gcloud compute machine-types list \
    --filter="name~^e2-" \
    --zones=us-central1-a
```

### Common Machine Types

| Type | vCPUs | Memory | Use Case |
|------|-------|--------|----------|
| e2-micro | 0.25-2 | 1 GB | Free tier, tiny workloads |
| e2-small | 0.5-2 | 2 GB | Dev/test |
| e2-medium | 1-2 | 4 GB | Small apps |
| n2-standard-2 | 2 | 8 GB | General workloads |
| n2-standard-4 | 4 | 16 GB | Medium workloads |
| n2-standard-8 | 8 | 32 GB | Large workloads |
| n2-highmem-4 | 4 | 32 GB | Memory-intensive |
| n2-highcpu-4 | 4 | 4 GB | CPU-intensive |
| c2-standard-4 | 4 | 16 GB | Compute-optimized |

---

## Images and Snapshots

### Images

```bash
# List images
gcloud compute images list

# List from specific project
gcloud compute images list --project=ubuntu-os-cloud

# Create image from disk
gcloud compute images create my-image \
    --source-disk=my-disk \
    --source-disk-zone=us-central1-a \
    --family=my-image-family

# Create image from snapshot
gcloud compute images create my-image \
    --source-snapshot=my-snapshot

# Delete image
gcloud compute images delete my-image
```

### Snapshots

```bash
# Create snapshot
gcloud compute disks snapshot my-disk \
    --zone=us-central1-a \
    --snapshot-names=my-snapshot

# List snapshots
gcloud compute snapshots list

# Create scheduled snapshot policy
gcloud compute resource-policies create snapshot-schedule my-schedule \
    --region=us-central1 \
    --max-retention-days=14 \
    --on-source-disk-delete=keep-auto-snapshots \
    --hourly-schedule=4 \
    --start-time=00:00

# Attach policy to disk
gcloud compute disks add-resource-policies my-disk \
    --zone=us-central1-a \
    --resource-policies=my-schedule

# Delete snapshot
gcloud compute snapshots delete my-snapshot
```

---

## Disks

### Disk Operations

```bash
# List disks
gcloud compute disks list

# Create disk
gcloud compute disks create my-disk \
    --zone=us-central1-a \
    --size=100GB \
    --type=pd-balanced

# Create SSD disk
gcloud compute disks create my-ssd-disk \
    --zone=us-central1-a \
    --size=100GB \
    --type=pd-ssd

# Attach disk to instance
gcloud compute instances attach-disk my-instance \
    --disk=my-disk \
    --zone=us-central1-a

# Detach disk
gcloud compute instances detach-disk my-instance \
    --disk=my-disk \
    --zone=us-central1-a

# Resize disk (online, no downtime)
gcloud compute disks resize my-disk \
    --zone=us-central1-a \
    --size=200GB

# Delete disk
gcloud compute disks delete my-disk --zone=us-central1-a
```

---

## Instance Templates

### Create Templates

```bash
# Basic template
gcloud compute instance-templates create my-template \
    --machine-type=e2-medium \
    --image-family=ubuntu-2404-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-balanced \
    --tags=http-server

# Template with startup script
gcloud compute instance-templates create my-template-v2 \
    --machine-type=e2-medium \
    --image-family=ubuntu-2404-lts \
    --image-project=ubuntu-os-cloud \
    --metadata-from-file=startup-script=startup.sh \
    --service-account=my-sa@project.iam.gserviceaccount.com \
    --scopes=cloud-platform

# Spot VM template
gcloud compute instance-templates create spot-template \
    --machine-type=n2-standard-4 \
    --provisioning-model=SPOT \
    --instance-termination-action=STOP \
    --image-family=ubuntu-2404-lts \
    --image-project=ubuntu-os-cloud \
    --metadata-from-file=shutdown-script=save-state.sh

# List templates
gcloud compute instance-templates list

# Describe template
gcloud compute instance-templates describe my-template

# Delete template
gcloud compute instance-templates delete my-template
```

---

## Managed Instance Groups (MIGs)

### Zonal MIG

```bash
# Create zonal MIG
gcloud compute instance-groups managed create my-mig \
    --zone=us-central1-a \
    --template=my-template \
    --size=3

# Create with named ports (for load balancing)
gcloud compute instance-groups managed create my-mig \
    --zone=us-central1-a \
    --template=my-template \
    --size=3 \
    --named-ports=http:8080,https:8443
```

### Regional MIG (Recommended for Production)

```bash
# Create regional MIG (multi-zone)
gcloud compute instance-groups managed create my-regional-mig \
    --region=us-central1 \
    --template=my-template \
    --size=3 \
    --zones=us-central1-a,us-central1-b,us-central1-c

# Regional MIG with target distribution
gcloud compute instance-groups managed create my-regional-mig \
    --region=us-central1 \
    --template=my-template \
    --size=6 \
    --target-distribution-shape=EVEN
```

### MIG Operations

```bash
# List MIGs
gcloud compute instance-groups managed list

# Describe MIG
gcloud compute instance-groups managed describe my-mig --zone=us-central1-a

# Resize MIG
gcloud compute instance-groups managed resize my-mig \
    --zone=us-central1-a \
    --size=5

# List managed instances
gcloud compute instance-groups managed list-instances my-mig \
    --zone=us-central1-a
```

### Rolling Updates

```bash
# Start rolling update with new template
gcloud compute instance-groups managed rolling-action start-update my-mig \
    --zone=us-central1-a \
    --version=template=my-template-v2 \
    --max-unavailable=1 \
    --max-surge=1

# Canary deployment (partial update)
gcloud compute instance-groups managed rolling-action start-update my-mig \
    --zone=us-central1-a \
    --version=template=my-template-v1 \
    --canary-version=template=my-template-v2,target-size=20%

# Replace all instances
gcloud compute instance-groups managed rolling-action replace my-mig \
    --zone=us-central1-a \
    --max-unavailable=1

# Restart all instances
gcloud compute instance-groups managed rolling-action restart my-mig \
    --zone=us-central1-a
```

### Autohealing

```bash
# Create HTTP health check
gcloud compute health-checks create http my-health-check \
    --port=8080 \
    --request-path=/health \
    --check-interval=10s \
    --timeout=5s \
    --healthy-threshold=2 \
    --unhealthy-threshold=3

# Set autohealing on MIG
gcloud compute instance-groups managed update my-mig \
    --zone=us-central1-a \
    --health-check=my-health-check \
    --initial-delay=300
```

---

## Autoscaling

### Basic Autoscaling

```bash
# CPU-based autoscaling
gcloud compute instance-groups managed set-autoscaling my-mig \
    --zone=us-central1-a \
    --min-num-replicas=2 \
    --max-num-replicas=10 \
    --target-cpu-utilization=0.6 \
    --cool-down-period=60

# Load balancing capacity autoscaling
gcloud compute instance-groups managed set-autoscaling my-mig \
    --zone=us-central1-a \
    --min-num-replicas=2 \
    --max-num-replicas=20 \
    --target-load-balancing-utilization=0.8
```

### Custom Metrics Autoscaling

```bash
# Custom Cloud Monitoring metric
gcloud compute instance-groups managed set-autoscaling my-mig \
    --zone=us-central1-a \
    --min-num-replicas=2 \
    --max-num-replicas=10 \
    --update-stackdriver-metric=custom.googleapis.com/queue_depth \
    --stackdriver-metric-single-instance-assignment=10
```

### Schedule-Based Autoscaling

```bash
# Create scaling schedule
gcloud compute instance-groups managed update-autoscaling my-mig \
    --zone=us-central1-a \
    --set-schedule=business-hours \
    --schedule-cron="0 9 * * MON-FRI" \
    --schedule-min-required-replicas=10 \
    --schedule-duration-sec=32400 \
    --schedule-time-zone="America/New_York"
```

### Predictive Autoscaling

```bash
# Enable predictive autoscaling
gcloud compute instance-groups managed update-autoscaling my-mig \
    --zone=us-central1-a \
    --cpu-utilization-predictive-method=OPTIMIZE_AVAILABILITY

# Forecast only (no action)
gcloud compute instance-groups managed update-autoscaling my-mig \
    --zone=us-central1-a \
    --cpu-utilization-predictive-method=FORECAST_ONLY
```

### Scale-in Controls

```bash
# Limit scale-in rate
gcloud compute instance-groups managed update-autoscaling my-mig \
    --zone=us-central1-a \
    --scale-in-control-max-scaled-in-replicas=10 \
    --scale-in-control-time-window-sec=1200
```

### Autoscaling Operations

```bash
# Describe autoscaler
gcloud compute instance-groups managed describe my-mig \
    --zone=us-central1-a

# Stop autoscaling
gcloud compute instance-groups managed stop-autoscaling my-mig \
    --zone=us-central1-a
```

---

## GKE Node Pools with Spot VMs

### Create Spot Node Pool

```bash
# Create cluster with standard nodes
gcloud container clusters create my-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --machine-type=e2-standard-4

# Add Spot node pool
gcloud container node-pools create spot-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --spot \
    --num-nodes=5 \
    --machine-type=n2-standard-4 \
    --enable-autoscaling \
    --min-nodes=0 \
    --max-nodes=20

# Add taint to Spot node pool
gcloud container node-pools create spot-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --spot \
    --num-nodes=5 \
    --node-taints=cloud.google.com/gke-spot=true:NoSchedule
```

### Node Pool Autoscaling

```bash
# Enable autoscaling on existing pool
gcloud container node-pools update my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=20
```

---

## Shutdown Scripts for Spot VMs

### Example Shutdown Script

```bash
#!/bin/bash
# shutdown-script.sh - Must complete within 30 seconds

# Save application state
/opt/app/save-state.sh

# Drain connections gracefully
systemctl stop nginx

# Upload checkpoint to GCS
gsutil cp /var/lib/app/checkpoint.dat gs://my-bucket/checkpoints/$(hostname)/

# Log shutdown
curl -X POST "http://metadata.google.internal/computeMetadata/v1/instance/guest-attributes/shutdown-complete" \
    -H "Metadata-Flavor: Google" \
    -d "true"
```

### Attach Shutdown Script to Template

```bash
gcloud compute instance-templates create spot-template \
    --machine-type=n2-standard-4 \
    --provisioning-model=SPOT \
    --instance-termination-action=STOP \
    --image-family=ubuntu-2404-lts \
    --image-project=ubuntu-os-cloud \
    --metadata-from-file=shutdown-script=shutdown-script.sh
```

---

*Examples v2.0 | GCP Compute Engine*
