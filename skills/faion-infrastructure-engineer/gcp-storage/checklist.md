# GCP Cloud Storage Checklist

## Bucket Creation

- [ ] Choose appropriate location (region/dual-region/multi-region)
- [ ] Select storage class based on access patterns
- [ ] Enable uniform bucket-level access (required for new buckets)
- [ ] Configure naming convention (globally unique, DNS-compliant)
- [ ] Set appropriate labels for cost tracking

## Security Configuration

### IAM

- [ ] Disable public access (unless explicitly required)
- [ ] Enable Public Access Prevention on bucket
- [ ] Use uniform bucket-level access (not fine-grained ACLs)
- [ ] Grant minimum required permissions (least privilege)
- [ ] Use service accounts for application access
- [ ] Review IAM policies regularly
- [ ] Separate buckets for public vs private content

### Encryption

- [ ] Evaluate encryption requirements (GMEK vs CMEK vs CSEK)
- [ ] Create Cloud KMS keyring in same location as bucket (for CMEK)
- [ ] Grant CryptoKey Encrypter/Decrypter role to service agent
- [ ] Set default encryption key on bucket
- [ ] Enable automatic key rotation
- [ ] Document key management procedures

### Network Security

- [ ] Configure VPC Service Controls for sensitive data
- [ ] Enable Private Google Access for VPC networks
- [ ] Use signed URLs for temporary access
- [ ] Implement signed policy documents for uploads
- [ ] Configure CORS policies if needed

## Lifecycle Management

- [ ] Define retention requirements
- [ ] Create lifecycle rules for storage class transitions
- [ ] Set expiration rules for temporary data
- [ ] Configure version retention policy
- [ ] Test lifecycle rules on sample data first
- [ ] Document lifecycle policies

### Recommended Transitions

| Access Frequency | Transition |
|------------------|------------|
| < 1x/month | Standard -> Nearline (30 days) |
| < 1x/quarter | Nearline -> Coldline (90 days) |
| < 1x/year | Coldline -> Archive (365 days) |

## Versioning

- [ ] Enable versioning for critical data
- [ ] Set noncurrent version expiration
- [ ] Configure noncurrent version transition policies
- [ ] Document recovery procedures

## Data Protection

- [ ] Enable Object Versioning
- [ ] Configure retention policies (if compliance required)
- [ ] Set up cross-region replication (dual/multi-region)
- [ ] Implement backup strategy
- [ ] Test restore procedures

## Monitoring & Logging

- [ ] Enable Data Access audit logs
- [ ] Configure Cloud Monitoring alerts
- [ ] Set up Storage Insights (if needed)
- [ ] Monitor usage and costs
- [ ] Create dashboards for key metrics

## Performance Optimization

- [ ] Co-locate buckets with compute resources
- [ ] Use Rapid Storage for <1ms latency needs
- [ ] Enable Anywhere Cache for regional buckets
- [ ] Configure Cloud CDN for global distribution
- [ ] Use parallel composite uploads for large files
- [ ] Implement proper retry logic

## CDN Integration

- [ ] Set up external Application Load Balancer
- [ ] Enable Cloud CDN on backend bucket
- [ ] Configure cache control headers
- [ ] Set appropriate TTLs by content type
- [ ] Use versioned URLs for cache busting
- [ ] Configure Cloud Armor for security
- [ ] Separate public CDN content from private data

### Cache Control Recommendations

| Content Type | TTL |
|--------------|-----|
| Static assets (CSS, JS) | 1 year (versioned) |
| Images | 1 week - 1 month |
| Dynamic content | 5 seconds - 1 hour |
| Real-time data | < 5 seconds |

## Cost Optimization

- [ ] Analyze access patterns
- [ ] Implement lifecycle policies
- [ ] Consider Autoclass for variable access
- [ ] Review egress costs
- [ ] Evaluate CDN vs direct access costs
- [ ] Set up billing alerts
- [ ] Use committed use discounts

## Pre-Production Review

- [ ] Security review completed
- [ ] Lifecycle rules tested
- [ ] Backup/restore tested
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Access patterns documented

## Compliance Checks

- [ ] Data residency requirements met
- [ ] Retention policies aligned with regulations
- [ ] Encryption requirements satisfied
- [ ] Audit logging enabled
- [ ] Access reviews scheduled

---

*GCP Cloud Storage Checklist v2.0*
