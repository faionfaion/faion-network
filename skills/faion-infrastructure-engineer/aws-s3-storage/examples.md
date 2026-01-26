# AWS S3 Examples

## Bucket Operations

### Create and Configure Bucket

```bash
# Create bucket
aws s3 mb s3://my-app-data-prod --region eu-west-1

# List buckets
aws s3 ls

# List bucket contents
aws s3 ls s3://my-app-data-prod --recursive --human-readable

# Delete bucket (must be empty)
aws s3 rb s3://my-app-data-prod

# Force delete bucket with contents
aws s3 rb s3://my-app-data-prod --force
```

### Object Operations

```bash
# Upload file
aws s3 cp file.txt s3://my-bucket/file.txt

# Upload with encryption
aws s3 cp file.txt s3://my-bucket/file.txt \
    --sse aws:kms \
    --sse-kms-key-id alias/my-key

# Download file
aws s3 cp s3://my-bucket/file.txt ./file.txt

# Sync directories
aws s3 sync ./local-folder s3://my-bucket/folder

# Sync with delete (mirror)
aws s3 sync s3://my-bucket/folder ./local-folder --delete

# Delete object
aws s3 rm s3://my-bucket/file.txt

# Delete prefix recursively
aws s3 rm s3://my-bucket/logs/ --recursive
```

### Presigned URLs

```bash
# Generate presigned URL (1 hour)
aws s3 presign s3://my-bucket/file.txt --expires-in 3600

# Presigned URL for upload (PUT)
aws s3 presign s3://my-bucket/uploads/new-file.txt \
    --expires-in 600 \
    --region eu-west-1
```

## Bucket Policies

### Enforce HTTPS Only

```bash
aws s3api put-bucket-policy --bucket my-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonHTTPS",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}'
```

### Enforce Encryption on Upload

```bash
aws s3api put-bucket-policy --bucket my-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUnencryptedUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": ["aws:kms", "AES256"]
        }
      }
    }
  ]
}'
```

### Cross-Account Access

```bash
aws s3api put-bucket-policy --bucket my-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CrossAccountAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:root"
      },
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}'
```

## Encryption

### Enable Default Encryption (SSE-S3)

```bash
aws s3api put-bucket-encryption \
    --bucket my-bucket \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            },
            "BucketKeyEnabled": false
        }]
    }'
```

### Enable Default Encryption (SSE-KMS with Bucket Keys)

```bash
aws s3api put-bucket-encryption \
    --bucket my-bucket \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "arn:aws:kms:eu-west-1:123456789012:key/12345678-1234-1234-1234-123456789012"
            },
            "BucketKeyEnabled": true
        }]
    }'
```

### Check Bucket Encryption

```bash
aws s3api get-bucket-encryption --bucket my-bucket
```

## Versioning

### Enable Versioning

```bash
aws s3api put-bucket-versioning \
    --bucket my-bucket \
    --versioning-configuration Status=Enabled
```

### Enable MFA Delete

```bash
aws s3api put-bucket-versioning \
    --bucket my-bucket \
    --versioning-configuration Status=Enabled,MFADelete=Enabled \
    --mfa "arn:aws:iam::123456789012:mfa/user 123456"
```

### List Object Versions

```bash
aws s3api list-object-versions --bucket my-bucket

# List versions for specific prefix
aws s3api list-object-versions \
    --bucket my-bucket \
    --prefix "data/" \
    --max-items 100
```

### Delete Specific Version

```bash
aws s3api delete-object \
    --bucket my-bucket \
    --key file.txt \
    --version-id "abc123"
```

### Restore Previous Version

```bash
# Copy previous version as current
aws s3api copy-object \
    --bucket my-bucket \
    --copy-source "my-bucket/file.txt?versionId=abc123" \
    --key file.txt
```

## Lifecycle Policies

### Create Lifecycle Policy

```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket my-bucket \
    --lifecycle-configuration '{
        "Rules": [
            {
                "ID": "TransitionToIA",
                "Status": "Enabled",
                "Filter": {
                    "Prefix": "data/"
                },
                "Transitions": [
                    {
                        "Days": 30,
                        "StorageClass": "STANDARD_IA"
                    },
                    {
                        "Days": 90,
                        "StorageClass": "GLACIER"
                    }
                ]
            },
            {
                "ID": "ExpireLogs",
                "Status": "Enabled",
                "Filter": {
                    "Prefix": "logs/"
                },
                "Expiration": {
                    "Days": 90
                }
            },
            {
                "ID": "CleanupOldVersions",
                "Status": "Enabled",
                "Filter": {},
                "NoncurrentVersionTransitions": [
                    {
                        "NoncurrentDays": 30,
                        "StorageClass": "GLACIER"
                    }
                ],
                "NoncurrentVersionExpiration": {
                    "NoncurrentDays": 365
                }
            },
            {
                "ID": "AbortIncompleteUploads",
                "Status": "Enabled",
                "Filter": {},
                "AbortIncompleteMultipartUpload": {
                    "DaysAfterInitiation": 7
                }
            },
            {
                "ID": "CleanupDeleteMarkers",
                "Status": "Enabled",
                "Filter": {},
                "Expiration": {
                    "ExpiredObjectDeleteMarker": true
                }
            }
        ]
    }'
```

### Get Lifecycle Configuration

```bash
aws s3api get-bucket-lifecycle-configuration --bucket my-bucket
```

### Delete Lifecycle Configuration

```bash
aws s3api delete-bucket-lifecycle --bucket my-bucket
```

## Replication

### Create Replication IAM Role

```bash
# Create role
aws iam create-role \
    --role-name S3ReplicationRole \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "s3.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }'

# Attach policy
aws iam put-role-policy \
    --role-name S3ReplicationRole \
    --policy-name S3ReplicationPolicy \
    --policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetReplicationConfiguration",
                    "s3:ListBucket"
                ],
                "Resource": "arn:aws:s3:::source-bucket"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObjectVersionForReplication",
                    "s3:GetObjectVersionAcl",
                    "s3:GetObjectVersionTagging"
                ],
                "Resource": "arn:aws:s3:::source-bucket/*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ReplicateObject",
                    "s3:ReplicateDelete",
                    "s3:ReplicateTags"
                ],
                "Resource": "arn:aws:s3:::destination-bucket/*"
            }
        ]
    }'
```

### Configure Cross-Region Replication

```bash
aws s3api put-bucket-replication \
    --bucket source-bucket \
    --replication-configuration '{
        "Role": "arn:aws:iam::123456789012:role/S3ReplicationRole",
        "Rules": [
            {
                "ID": "ReplicateAll",
                "Status": "Enabled",
                "Priority": 1,
                "Filter": {},
                "Destination": {
                    "Bucket": "arn:aws:s3:::destination-bucket",
                    "StorageClass": "STANDARD_IA",
                    "ReplicationTime": {
                        "Status": "Enabled",
                        "Time": {
                            "Minutes": 15
                        }
                    },
                    "Metrics": {
                        "Status": "Enabled",
                        "EventThreshold": {
                            "Minutes": 15
                        }
                    }
                },
                "DeleteMarkerReplication": {
                    "Status": "Enabled"
                }
            }
        ]
    }'
```

### Check Replication Status

```bash
aws s3api get-bucket-replication --bucket source-bucket

# Check object replication status
aws s3api head-object \
    --bucket source-bucket \
    --key file.txt \
    --query 'ReplicationStatus'
```

## Block Public Access

### Block at Account Level

```bash
aws s3control put-public-access-block \
    --account-id 123456789012 \
    --public-access-block-configuration '{
        "BlockPublicAcls": true,
        "IgnorePublicAcls": true,
        "BlockPublicPolicy": true,
        "RestrictPublicBuckets": true
    }'
```

### Block at Bucket Level

```bash
aws s3api put-public-access-block \
    --bucket my-bucket \
    --public-access-block-configuration '{
        "BlockPublicAcls": true,
        "IgnorePublicAcls": true,
        "BlockPublicPolicy": true,
        "RestrictPublicBuckets": true
    }'
```

## Access Logging

### Enable Server Access Logging

```bash
# Create logging bucket
aws s3 mb s3://my-bucket-logs --region eu-west-1

# Grant S3 log delivery permissions
aws s3api put-bucket-acl \
    --bucket my-bucket-logs \
    --grant-write URI=http://acs.amazonaws.com/groups/s3/LogDelivery \
    --grant-read-acp URI=http://acs.amazonaws.com/groups/s3/LogDelivery

# Enable logging
aws s3api put-bucket-logging \
    --bucket my-bucket \
    --bucket-logging-status '{
        "LoggingEnabled": {
            "TargetBucket": "my-bucket-logs",
            "TargetPrefix": "my-bucket/"
        }
    }'
```

## S3 Inventory

### Configure Inventory

```bash
aws s3api put-bucket-inventory-configuration \
    --bucket my-bucket \
    --id "WeeklyInventory" \
    --inventory-configuration '{
        "Destination": {
            "S3BucketDestination": {
                "Bucket": "arn:aws:s3:::inventory-bucket",
                "Format": "CSV",
                "Prefix": "inventory"
            }
        },
        "IsEnabled": true,
        "Id": "WeeklyInventory",
        "IncludedObjectVersions": "All",
        "OptionalFields": [
            "Size",
            "LastModifiedDate",
            "StorageClass",
            "ETag",
            "ReplicationStatus",
            "EncryptionStatus"
        ],
        "Schedule": {
            "Frequency": "Weekly"
        }
    }'
```

---

*AWS S3 Examples | faion-infrastructure-engineer*
