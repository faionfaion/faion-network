# GCP Cloud Storage Examples

## Bucket Operations

### Create Regional Bucket

```bash
# Standard regional bucket with uniform access
gcloud storage buckets create gs://my-project-data \
    --location=us-central1 \
    --storage-class=standard \
    --uniform-bucket-level-access \
    --public-access-prevention
```

### Create Multi-Regional Bucket

```bash
# Multi-regional for global access
gcloud storage buckets create gs://my-project-assets \
    --location=us \
    --storage-class=standard \
    --uniform-bucket-level-access
```

### Create Archive Bucket

```bash
# Archive bucket for compliance data
gcloud storage buckets create gs://my-project-archive \
    --location=us-central1 \
    --storage-class=archive \
    --uniform-bucket-level-access \
    --public-access-prevention
```

### Enable Versioning

```bash
gcloud storage buckets update gs://my-bucket --versioning
```

### Enable Autoclass

```bash
gcloud storage buckets update gs://my-bucket \
    --enable-autoclass \
    --autoclass-terminal-storage-class=archive
```

## Object Operations

### Upload with Metadata

```bash
gcloud storage cp local-file.json gs://my-bucket/ \
    --content-type="application/json" \
    --cache-control="max-age=3600"
```

### Sync Directory

```bash
# Sync local to bucket
gcloud storage rsync -r ./local-dir gs://my-bucket/path

# Sync and delete extra files in destination
gcloud storage rsync -r -d ./local-dir gs://my-bucket/path

# Sync from bucket to local
gcloud storage rsync -r gs://my-bucket/path ./local-dir
```

### Parallel Composite Upload (Large Files)

```bash
# Enable parallel composite uploads for files > 150MB
gcloud storage cp large-file.tar.gz gs://my-bucket/ \
    --no-clobber
```

## IAM Configuration

### Grant Service Account Access

```bash
# Object Admin (read/write/delete)
gcloud storage buckets add-iam-policy-binding gs://my-bucket \
    --member=serviceAccount:my-service@my-project.iam.gserviceaccount.com \
    --role=roles/storage.objectAdmin

# Object Viewer (read only)
gcloud storage buckets add-iam-policy-binding gs://my-bucket \
    --member=serviceAccount:my-service@my-project.iam.gserviceaccount.com \
    --role=roles/storage.objectViewer

# Object Creator (write only)
gcloud storage buckets add-iam-policy-binding gs://my-bucket \
    --member=serviceAccount:my-service@my-project.iam.gserviceaccount.com \
    --role=roles/storage.objectCreator
```

### Make Bucket Public (CDN Use Case)

```bash
# Only for public CDN content - separate from private data
gcloud storage buckets add-iam-policy-binding gs://my-public-assets \
    --member=allUsers \
    --role=roles/storage.objectViewer
```

### View IAM Policy

```bash
gcloud storage buckets get-iam-policy gs://my-bucket
```

### Remove Access

```bash
gcloud storage buckets remove-iam-policy-binding gs://my-bucket \
    --member=user:user@example.com \
    --role=roles/storage.objectAdmin
```

## CMEK Encryption

### Create KMS Keyring and Key

```bash
# Create keyring in same location as bucket
gcloud kms keyrings create my-keyring \
    --location=us-central1

# Create key
gcloud kms keys create my-storage-key \
    --keyring=my-keyring \
    --location=us-central1 \
    --purpose=encryption \
    --rotation-period=90d \
    --next-rotation-time=$(date -d "+90 days" -u +%Y-%m-%dT%H:%M:%SZ)
```

### Grant Service Agent Access to Key

```bash
# Get project number
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Grant access
gcloud kms keys add-iam-policy-binding my-storage-key \
    --keyring=my-keyring \
    --location=us-central1 \
    --member=serviceAccount:service-${PROJECT_NUMBER}@gs-project-accounts.iam.gserviceaccount.com \
    --role=roles/cloudkms.cryptoKeyEncrypterDecrypter
```

### Set Default CMEK on Bucket

```bash
gcloud storage buckets update gs://my-bucket \
    --default-encryption-key=projects/$PROJECT_ID/locations/us-central1/keyRings/my-keyring/cryptoKeys/my-storage-key
```

## Lifecycle Management

### Basic Lifecycle Configuration

```bash
cat > lifecycle.json << 'EOF'
{
  "rule": [
    {
      "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
      "condition": {"age": 30, "matchesStorageClass": ["STANDARD"]}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
      "condition": {"age": 90, "matchesStorageClass": ["NEARLINE"]}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"},
      "condition": {"age": 365, "matchesStorageClass": ["COLDLINE"]}
    }
  ]
}
EOF

gcloud storage buckets update gs://my-bucket --lifecycle-file=lifecycle.json
```

### Lifecycle with Deletion and Version Cleanup

```bash
cat > lifecycle-full.json << 'EOF'
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 730, "matchesStorageClass": ["ARCHIVE"]}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"numNewerVersions": 3, "isLive": false}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"age": 90, "isLive": false}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
      "condition": {"age": 30, "matchesStorageClass": ["STANDARD"]}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
      "condition": {"age": 365, "matchesStorageClass": ["NEARLINE"]}
    }
  ]
}
EOF

gcloud storage buckets update gs://my-bucket --lifecycle-file=lifecycle-full.json
```

### Lifecycle for Temporary Files

```bash
cat > lifecycle-temp.json << 'EOF'
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 7, "matchesPrefix": ["tmp/", "temp/"]}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"age": 1, "matchesSuffix": [".tmp", ".temp"]}
    }
  ]
}
EOF

gcloud storage buckets update gs://my-bucket --lifecycle-file=lifecycle-temp.json
```

### View Lifecycle Configuration

```bash
gcloud storage buckets describe gs://my-bucket --format="json(lifecycle)"
```

### Clear Lifecycle Rules

```bash
gcloud storage buckets update gs://my-bucket --clear-lifecycle
```

## Signed URLs

### Generate Signed URL (Read)

```bash
gcloud storage sign-url gs://my-bucket/private-file.pdf \
    --duration=1h \
    --private-key-file=service-account.json
```

### Generate Signed URL for Upload

```bash
gcloud storage sign-url gs://my-bucket/uploads/ \
    --duration=1h \
    --http-verb=PUT \
    --private-key-file=service-account.json
```

## Cloud CDN Integration

### Create Backend Bucket

```bash
# Create backend bucket for Cloud CDN
gcloud compute backend-buckets create my-cdn-backend \
    --gcs-bucket-name=my-public-assets \
    --enable-cdn \
    --cache-mode=CACHE_ALL_STATIC
```

### Create URL Map

```bash
gcloud compute url-maps create my-cdn-url-map \
    --default-backend-bucket=my-cdn-backend
```

### Create HTTPS Proxy

```bash
# Create SSL certificate first
gcloud compute ssl-certificates create my-cert \
    --domains=cdn.example.com \
    --global

# Create target HTTPS proxy
gcloud compute target-https-proxies create my-https-proxy \
    --url-map=my-cdn-url-map \
    --ssl-certificates=my-cert
```

### Create Forwarding Rule

```bash
gcloud compute forwarding-rules create my-https-rule \
    --global \
    --target-https-proxy=my-https-proxy \
    --ports=443
```

### Configure Cache Headers on Objects

```bash
# Set cache headers for static assets
gcloud storage objects update gs://my-bucket/static/** \
    --cache-control="public, max-age=31536000"

# Set cache headers for dynamic content
gcloud storage objects update gs://my-bucket/api/** \
    --cache-control="public, max-age=60"
```

### Invalidate Cache

```bash
gcloud compute url-maps invalidate-cdn-cache my-cdn-url-map \
    --path="/assets/*"
```

## Monitoring & Audit

### Enable Audit Logging

```bash
# Enable data access logs via org policy or project IAM
gcloud projects get-iam-policy $PROJECT_ID > policy.yaml

# Add audit config to policy.yaml:
# auditConfigs:
# - service: storage.googleapis.com
#   auditLogConfigs:
#   - logType: DATA_READ
#   - logType: DATA_WRITE

gcloud projects set-iam-policy $PROJECT_ID policy.yaml
```

### Query Audit Logs

```bash
gcloud logging read 'resource.type="gcs_bucket" AND protoPayload.serviceName="storage.googleapis.com"' \
    --limit=50 \
    --format=json
```

## VPC Service Controls

### Create Perimeter

```bash
# Create access policy (if not exists)
gcloud access-context-manager policies create \
    --organization=$ORG_ID \
    --title="My Access Policy"

# Create service perimeter
gcloud access-context-manager perimeters create my-perimeter \
    --policy=$POLICY_ID \
    --title="Storage Perimeter" \
    --resources="projects/$PROJECT_NUMBER" \
    --restricted-services="storage.googleapis.com" \
    --perimeter-type=regular
```

---

*GCP Cloud Storage Examples v2.0*
