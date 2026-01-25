---
name: faion-gcp-storage-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# GCP Storage & Databases

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-agent

## Cloud Storage

### Bucket Operations

```bash
# List buckets
gcloud storage buckets list

# Create bucket
gcloud storage buckets create gs://my-bucket \
    --location=us-central1 \
    --uniform-bucket-level-access

# Create bucket with specific storage class
gcloud storage buckets create gs://my-archive-bucket \
    --location=us \
    --storage-class=archive

# Describe bucket
gcloud storage buckets describe gs://my-bucket

# Update bucket (enable versioning)
gcloud storage buckets update gs://my-bucket --versioning

# Delete bucket (must be empty)
gcloud storage buckets delete gs://my-bucket

# Delete bucket with all contents
gcloud storage rm -r gs://my-bucket
```

### Object Operations

```bash
# List objects
gcloud storage ls gs://my-bucket
gcloud storage ls gs://my-bucket/** --recursive

# Copy files
gcloud storage cp local-file.txt gs://my-bucket/
gcloud storage cp gs://my-bucket/file.txt ./local/
gcloud storage cp -r ./local-dir gs://my-bucket/

# Sync directories
gcloud storage rsync -r ./local-dir gs://my-bucket/path
gcloud storage rsync -r gs://my-bucket/path ./local-dir
gcloud storage rsync -r -d ./local-dir gs://my-bucket/  # -d deletes extra files

# Move/rename objects
gcloud storage mv gs://my-bucket/old-name.txt gs://my-bucket/new-name.txt

# Delete objects
gcloud storage rm gs://my-bucket/file.txt
gcloud storage rm -r gs://my-bucket/path/

# Get object metadata
gcloud storage objects describe gs://my-bucket/file.txt

# Set object metadata
gcloud storage objects update gs://my-bucket/file.txt \
    --content-type="application/json"
```

### Access Control

```bash
# Make bucket public
gcloud storage buckets add-iam-policy-binding gs://my-bucket \
    --member=allUsers \
    --role=roles/storage.objectViewer

# Grant user access
gcloud storage buckets add-iam-policy-binding gs://my-bucket \
    --member=user:user@example.com \
    --role=roles/storage.objectAdmin

# Remove access
gcloud storage buckets remove-iam-policy-binding gs://my-bucket \
    --member=user:user@example.com \
    --role=roles/storage.objectAdmin

# View IAM policy
gcloud storage buckets get-iam-policy gs://my-bucket

# Generate signed URL (requires service account)
gcloud storage sign-url gs://my-bucket/file.txt \
    --duration=1h \
    --private-key-file=service-account.json
```

### Lifecycle Management

```bash
# Set lifecycle policy
cat > lifecycle.json << 'EOF'
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 365}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
      "condition": {"age": 30}
    }
  ]
}
EOF
gcloud storage buckets update gs://my-bucket --lifecycle-file=lifecycle.json

# View lifecycle policy
gcloud storage buckets describe gs://my-bucket --format="json(lifecycle)"

# Remove lifecycle policy
gcloud storage buckets update gs://my-bucket --clear-lifecycle
```

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

# Create MySQL instance
gcloud sql instances create my-mysql \
    --database-version=MYSQL_8_0 \
    --tier=db-n1-standard-2 \
    --region=us-central1 \
    --root-password=secretpassword

# List instances
gcloud sql instances list

# Describe instance
gcloud sql instances describe my-postgres

# Start/stop instance
gcloud sql instances patch my-postgres --activation-policy=NEVER  # Stop
gcloud sql instances patch my-postgres --activation-policy=ALWAYS # Start

# Delete instance
gcloud sql instances delete my-postgres
```

### Database Operations

```bash
# Create database
gcloud sql databases create mydb --instance=my-postgres

# List databases
gcloud sql databases list --instance=my-postgres

# Delete database
gcloud sql databases delete mydb --instance=my-postgres

# Create user
gcloud sql users create myuser \
    --instance=my-postgres \
    --password=userpassword

# List users
gcloud sql users list --instance=my-postgres

# Change password
gcloud sql users set-password myuser \
    --instance=my-postgres \
    --password=newpassword

# Delete user
gcloud sql users delete myuser --instance=my-postgres
```

### Connections

```bash
# Connect via Cloud SQL Proxy
cloud-sql-proxy --port 5432 my-project:us-central1:my-postgres

# Direct connection (public IP)
gcloud sql connect my-postgres --user=postgres

# Export database
gcloud sql export sql my-postgres gs://my-bucket/backup.sql \
    --database=mydb

# Import database
gcloud sql import sql my-postgres gs://my-bucket/backup.sql \
    --database=mydb
```

## BigQuery

### Dataset Operations

```bash
# Create dataset
bq mk --dataset my_project:my_dataset

# With location
bq mk --dataset --location=US my_project:my_dataset

# List datasets
bq ls

# Describe dataset
bq show my_dataset

# Delete dataset
bq rm -r -f my_dataset  # -r removes tables, -f force
```

### Table Operations

```bash
# Create table with schema
bq mk --table my_dataset.my_table name:STRING,age:INTEGER,email:STRING

# Create table from schema file
bq mk --table my_dataset.my_table schema.json

# List tables
bq ls my_dataset

# Describe table
bq show my_dataset.my_table

# Delete table
bq rm -f my_dataset.my_table
```

### Query Operations

```bash
# Run query
bq query --use_legacy_sql=false 'SELECT * FROM my_dataset.my_table LIMIT 10'

# Save query results to table
bq query --use_legacy_sql=false \
    --destination_table=my_dataset.results \
    'SELECT * FROM my_dataset.my_table WHERE age > 30'

# Export to Cloud Storage
bq extract --destination_format=CSV \
    my_dataset.my_table \
    gs://my-bucket/export/*.csv
```

### Data Loading

```bash
# Load from CSV
bq load --source_format=CSV \
    my_dataset.my_table \
    gs://my-bucket/data.csv \
    name:STRING,age:INTEGER,email:STRING

# Load from JSON
bq load --source_format=NEWLINE_DELIMITED_JSON \
    my_dataset.my_table \
    gs://my-bucket/data.json \
    schema.json

# Load with autodetect schema
bq load --autodetect \
    --source_format=CSV \
    my_dataset.my_table \
    gs://my-bucket/data.csv
```

---

*GCP Storage & Databases Skill v1.0*
*Layer 3 Technical Skill*
*Used by: faion-devops-agent*

## Sources

- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Cloud Spanner Documentation](https://cloud.google.com/spanner/docs)
- [Filestore Documentation](https://cloud.google.com/filestore/docs)
- [Storage Best Practices](https://cloud.google.com/storage/docs/best-practices)
