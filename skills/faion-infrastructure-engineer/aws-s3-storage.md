---
name: faion-aws-s3-storage-reference
description: AWS S3 and storage services
---

# AWS S3 & Storage

CLI reference for S3 and RDS operations.

## S3 (Simple Storage Service)

### Bucket Operations

```bash
# List/create/delete buckets
aws s3 ls
aws s3 mb s3://my-bucket-name --region eu-west-1
aws s3 rb s3://my-bucket-name --force

# List contents
aws s3 ls s3://my-bucket --recursive --human-readable
```

### Object Operations

```bash
# Upload/download/delete
aws s3 cp file.txt s3://my-bucket/file.txt
aws s3 cp s3://my-bucket/file.txt ./file.txt
aws s3 rm s3://my-bucket/file.txt

# Sync directories
aws s3 sync ./local-folder s3://my-bucket/folder
aws s3 sync s3://my-bucket/folder ./local-folder --delete
```

### Presigned URLs

```bash
# Generate presigned URL (1 hour default)
aws s3 presign s3://my-bucket/file.txt --expires-in 3600
```

### Versioning

```bash
# Enable versioning
aws s3api put-bucket-versioning \
    --bucket my-bucket \
    --versioning-configuration Status=Enabled

# List versions
aws s3api list-object-versions --bucket my-bucket
```

### Encryption

```bash
# Enable bucket encryption
aws s3api put-bucket-encryption \
    --bucket my-bucket \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "arn:aws:kms:us-east-1:123456789012:key/key-id"
            }
        }]
    }'
```

## RDS (Relational Database Service)

### Instance Management

```bash
# List instances
aws rds describe-db-instances

# Create instance
aws rds create-db-instance \
    --db-instance-identifier my-database \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.4 \
    --master-username admin \
    --master-user-password "SecurePassword123!" \
    --allocated-storage 20 \
    --storage-encrypted \
    --multi-az

# Start/stop
aws rds start-db-instance --db-instance-identifier my-database
aws rds stop-db-instance --db-instance-identifier my-database
```

### Snapshots

```bash
# Create snapshot
aws rds create-db-snapshot \
    --db-instance-identifier my-database \
    --db-snapshot-identifier my-snapshot-$(date +%Y%m%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier my-restored-database \
    --db-snapshot-identifier my-snapshot

# Copy snapshot to another region
aws rds copy-db-snapshot \
    --source-db-snapshot-identifier arn:aws:rds:us-east-1:123456789012:snapshot:my-snapshot \
    --target-db-snapshot-identifier my-snapshot-copy \
    --source-region us-east-1 \
    --region eu-west-1
```

### Aurora Clusters

```bash
# Create Aurora cluster
aws rds create-db-cluster \
    --db-cluster-identifier my-aurora-cluster \
    --engine aurora-postgresql \
    --engine-version 15.4 \
    --master-username admin \
    --master-user-password "SecurePassword123!"

# Add instance
aws rds create-db-instance \
    --db-instance-identifier my-aurora-instance \
    --db-instance-class db.r6g.large \
    --engine aurora-postgresql \
    --db-cluster-identifier my-aurora-cluster

# Failover
aws rds failover-db-cluster --db-cluster-identifier my-aurora-cluster
```

## Sources

- [S3 User Guide](https://docs.aws.amazon.com/s3/latest/userguide/)
- [S3 CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/)
- [RDS User Guide](https://docs.aws.amazon.com/rds/latest/userguide/)
- [Aurora User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/)
- [RDS CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/rds/)
