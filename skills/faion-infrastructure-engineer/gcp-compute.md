---
name: faion-gcp-compute-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# GCP Compute Engine

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-agent

## Instance Management

```bash
# List instances
gcloud compute instances list

# List instances in specific zone
gcloud compute instances list --zones=us-central1-a

# Create instance
gcloud compute instances create my-instance \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-balanced \
    --tags=http-server,https-server

# Create instance with startup script
gcloud compute instances create my-instance \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --metadata-from-file=startup-script=startup.sh

# Create preemptible/spot instance
gcloud compute instances create my-spot \
    --zone=us-central1-a \
    --provisioning-model=SPOT \
    --instance-termination-action=STOP

# Start/stop/delete instances
gcloud compute instances start my-instance --zone=us-central1-a
gcloud compute instances stop my-instance --zone=us-central1-a
gcloud compute instances delete my-instance --zone=us-central1-a

# SSH into instance
gcloud compute ssh my-instance --zone=us-central1-a

# SSH with specific user
gcloud compute ssh user@my-instance --zone=us-central1-a

# Copy files to/from instance
gcloud compute scp local-file.txt my-instance:/remote/path --zone=us-central1-a
gcloud compute scp my-instance:/remote/file.txt ./local/ --zone=us-central1-a

# Describe instance
gcloud compute instances describe my-instance --zone=us-central1-a
```

## Machine Types

```bash
# List machine types
gcloud compute machine-types list --zones=us-central1-a

# Filter by CPU/memory
gcloud compute machine-types list \
    --filter="guestCpus>=4 AND memoryMb>=16384" \
    --zones=us-central1-a

# Common machine types
# e2-micro, e2-small, e2-medium (cost-effective)
# n2-standard-2, n2-standard-4, n2-standard-8 (balanced)
# n2-highmem-2, n2-highmem-4 (memory optimized)
# n2-highcpu-2, n2-highcpu-4 (compute optimized)
# c2-standard-4, c2-standard-8 (compute intensive)
```

## Images and Snapshots

```bash
# List images
gcloud compute images list

# List images from specific project
gcloud compute images list --project=ubuntu-os-cloud

# Create image from disk
gcloud compute images create my-image \
    --source-disk=my-disk \
    --source-disk-zone=us-central1-a

# Create image from snapshot
gcloud compute images create my-image \
    --source-snapshot=my-snapshot

# Delete image
gcloud compute images delete my-image

# Create snapshot
gcloud compute disks snapshot my-disk \
    --zone=us-central1-a \
    --snapshot-names=my-snapshot

# List snapshots
gcloud compute snapshots list

# Delete snapshot
gcloud compute snapshots delete my-snapshot
```

## Disks

```bash
# List disks
gcloud compute disks list

# Create disk
gcloud compute disks create my-disk \
    --zone=us-central1-a \
    --size=100GB \
    --type=pd-balanced

# Attach disk to instance
gcloud compute instances attach-disk my-instance \
    --disk=my-disk \
    --zone=us-central1-a

# Detach disk
gcloud compute instances detach-disk my-instance \
    --disk=my-disk \
    --zone=us-central1-a

# Resize disk
gcloud compute disks resize my-disk \
    --zone=us-central1-a \
    --size=200GB

# Delete disk
gcloud compute disks delete my-disk --zone=us-central1-a
```

## Instance Groups and Templates

```bash
# Create instance template
gcloud compute instance-templates create my-template \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB

# Create managed instance group
gcloud compute instance-groups managed create my-group \
    --zone=us-central1-a \
    --template=my-template \
    --size=3

# Set autoscaling
gcloud compute instance-groups managed set-autoscaling my-group \
    --zone=us-central1-a \
    --min-num-replicas=2 \
    --max-num-replicas=10 \
    --target-cpu-utilization=0.6

# Update instance group (rolling update)
gcloud compute instance-groups managed rolling-action start-update my-group \
    --zone=us-central1-a \
    --version=template=my-template-v2 \
    --max-unavailable=1

# List instance groups
gcloud compute instance-groups managed list
```

## GKE (Google Kubernetes Engine)

### Cluster Management

```bash
# Create cluster
gcloud container clusters create my-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --machine-type=e2-standard-4 \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=10

# Create Autopilot cluster (managed)
gcloud container clusters create-auto my-autopilot-cluster \
    --region=us-central1

# List clusters
gcloud container clusters list

# Get cluster credentials (configure kubectl)
gcloud container clusters get-credentials my-cluster \
    --zone=us-central1-a

# Describe cluster
gcloud container clusters describe my-cluster --zone=us-central1-a

# Resize cluster
gcloud container clusters resize my-cluster \
    --zone=us-central1-a \
    --num-nodes=5

# Delete cluster
gcloud container clusters delete my-cluster --zone=us-central1-a
```

### Node Pools

```bash
# List node pools
gcloud container node-pools list --cluster=my-cluster --zone=us-central1-a

# Create node pool
gcloud container node-pools create my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --machine-type=n2-standard-8

# Create preemptible node pool
gcloud container node-pools create spot-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --spot \
    --num-nodes=5

# Enable autoscaling on node pool
gcloud container node-pools update my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=20

# Delete node pool
gcloud container node-pools delete my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a
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

*GCP Compute Engine Skill v1.0*
*Layer 3 Technical Skill*
*Used by: faion-devops-agent*

## Sources

- [Compute Engine Documentation](https://cloud.google.com/compute/docs)
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [Compute Engine Machine Types](https://cloud.google.com/compute/docs/machine-types)
- [GKE Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview)
- [Managed Instance Groups](https://cloud.google.com/compute/docs/instance-groups)
