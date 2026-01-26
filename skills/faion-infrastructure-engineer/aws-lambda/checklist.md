# AWS Lambda Checklist

Pre-deployment and operational checklists for Lambda functions.

## Function Design Checklist

### Code Structure

- [ ] Handler contains only business logic
- [ ] SDK clients initialized outside handler
- [ ] Database connections initialized outside handler
- [ ] Static assets cached in /tmp
- [ ] No blocking operations in INIT phase
- [ ] Idempotent processing implemented
- [ ] Graceful error handling with proper status codes

### Performance

- [ ] Memory sized appropriately (use Power Tuning)
- [ ] Timeout set with buffer (not at limit)
- [ ] Connection pooling configured
- [ ] Unnecessary dependencies removed
- [ ] Code minified/bundled (Node.js)
- [ ] Native dependencies compiled for Lambda (Amazon Linux 2)

### Cold Start Optimization

- [ ] SnapStart enabled (Java/Python/.NET)
- [ ] Provisioned Concurrency evaluated (if strict latency required)
- [ ] ARM64/Graviton2 considered for I/O workloads
- [ ] Initialization code optimized
- [ ] Lazy loading implemented for rarely-used modules

## Security Checklist

### IAM

- [ ] Execution role follows least privilege
- [ ] No wildcard (*) permissions in production
- [ ] Resource-based policies configured for cross-account
- [ ] Function URL authentication configured (if used)
- [ ] VPC execution role has ENI permissions (if VPC)

### Secrets Management

- [ ] Sensitive data in Secrets Manager or Parameter Store
- [ ] Environment variables encrypted with KMS
- [ ] No hardcoded credentials in code
- [ ] Secrets rotated regularly

### Network

- [ ] VPC used only when necessary
- [ ] VPC endpoints configured for AWS services
- [ ] Security groups follow least privilege
- [ ] Private subnets used for sensitive workloads

## Deployment Checklist

### Pre-Deployment

- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Code reviewed
- [ ] Dependencies audited for vulnerabilities
- [ ] Package size within limits (50MB compressed)

### Deployment Configuration

- [ ] Alias configured for environment (dev/staging/prod)
- [ ] Version published
- [ ] Deployment strategy defined (all-at-once/canary/linear)
- [ ] Rollback alarms configured
- [ ] Dead-letter queue configured

### Post-Deployment

- [ ] Smoke tests executed
- [ ] Metrics baseline established
- [ ] Alerts configured
- [ ] Documentation updated

## Layers Checklist

### Layer Creation

- [ ] Correct directory structure (python/, nodejs/, lib/)
- [ ] Compatible runtimes specified
- [ ] Layer version documented
- [ ] Dependencies pinned to specific versions
- [ ] Size optimized (remove unnecessary files)

### Layer Management

- [ ] Version control in place
- [ ] Update automation configured
- [ ] Testing workflow for new versions
- [ ] Rollback procedure documented
- [ ] Usage audit scheduled

## Event Source Checklist

### SQS

- [ ] Batch size configured appropriately
- [ ] Batching window set (if needed)
- [ ] ReportBatchItemFailures enabled
- [ ] DLQ configured
- [ ] Visibility timeout > function timeout
- [ ] Event filtering configured (if needed)

### Kinesis/DynamoDB Streams

- [ ] Starting position defined (LATEST/TRIM_HORIZON)
- [ ] Batch size configured
- [ ] Parallelization factor set (if needed)
- [ ] BisectBatchOnFunctionError enabled
- [ ] MaximumRetryAttempts configured
- [ ] MaximumRecordAgeInSeconds configured
- [ ] On-failure destination configured

### API Gateway

- [ ] Timeout configured (< 29s limit)
- [ ] Authorization configured
- [ ] Request validation enabled
- [ ] Response mapping configured
- [ ] CORS configured (if needed)
- [ ] Throttling configured

## Monitoring Checklist

### CloudWatch Metrics

- [ ] Duration alarm configured
- [ ] Error rate alarm configured
- [ ] Throttle alarm configured
- [ ] Concurrent executions monitored
- [ ] Iterator age monitored (streams)
- [ ] Dead-letter queue depth monitored

### Logging

- [ ] Structured logging (JSON) implemented
- [ ] Log level configurable via environment variable
- [ ] Request ID included in all logs
- [ ] Sensitive data excluded from logs
- [ ] Log retention configured
- [ ] Log insights queries prepared

### Tracing

- [ ] X-Ray enabled
- [ ] Custom segments for key operations
- [ ] Downstream calls traced
- [ ] Performance baselines established

## Cost Optimization Checklist

- [ ] Memory right-sized (Power Tuning)
- [ ] ARM64 architecture evaluated
- [ ] Provisioned Concurrency justified (if used)
- [ ] Reserved Concurrency set to prevent runaway
- [ ] Unnecessary invocations eliminated (event filtering)
- [ ] Log retention optimized
- [ ] Compute Optimizer recommendations reviewed

## Operational Readiness

### Documentation

- [ ] Architecture diagram updated
- [ ] API documentation complete
- [ ] Runbook created
- [ ] Troubleshooting guide available

### Disaster Recovery

- [ ] Multi-region deployment (if required)
- [ ] Backup strategy for state
- [ ] Recovery time objective (RTO) defined
- [ ] Recovery point objective (RPO) defined

### Maintenance

- [ ] Runtime deprecation tracked
- [ ] Dependency update schedule
- [ ] Security patch process
- [ ] Performance review schedule

---

*AWS Lambda Checklist | Use with [README.md](README.md)*
