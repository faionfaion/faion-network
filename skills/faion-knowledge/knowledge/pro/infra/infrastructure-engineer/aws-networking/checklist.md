# AWS Networking Checklist

> Pre-deployment and audit checklist for VPC infrastructure.

## VPC Design

### IP Address Planning

- [ ] CIDR block sized for growth (minimum /16 for production)
- [ ] No overlapping CIDRs with other VPCs or on-prem networks
- [ ] IPAM configured for multi-account environments
- [ ] Secondary CIDR blocks planned if needed
- [ ] Reserved ranges documented for future expansion

### Subnet Architecture

- [ ] Minimum 3 AZs for high availability
- [ ] Public subnets sized appropriately (/24 minimum)
- [ ] Private subnets sized for workload growth
- [ ] Data subnets isolated from application tier
- [ ] Subnet naming convention established (env-tier-az)

### Routing

- [ ] Main route table has no public routes
- [ ] Public subnets have Internet Gateway route
- [ ] Private subnets route through NAT Gateway
- [ ] NAT Gateway deployed in each AZ (for HA)
- [ ] VPC endpoint routes added to private route tables

## Security Controls

### Security Groups

- [ ] No `0.0.0.0/0` inbound rules (except ALB on 443)
- [ ] Outbound restricted to necessary destinations
- [ ] Source references other SGs where possible (not CIDRs)
- [ ] Descriptions added to all rules
- [ ] Naming convention: `{env}-{app}-{tier}-sg`
- [ ] Monthly audit scheduled via AWS Config

### Network ACLs

- [ ] Default NACL allows all (use SGs as primary)
- [ ] Custom NACLs only for additional guardrails
- [ ] Ephemeral port ranges configured (1024-65535)
- [ ] Rule numbers allow for future insertions (100, 200, 300...)
- [ ] Deny rules documented with justification

### VPC Flow Logs

- [ ] Flow logs enabled on all VPCs
- [ ] Log destination: CloudWatch Logs or S3
- [ ] Retention policy configured (30-90 days)
- [ ] IAM role for flow logs created
- [ ] Reject-only logs for security analysis

## Connectivity

### VPC Peering

- [ ] Peering connections use specific routes (not full CIDR)
- [ ] DNS resolution enabled across peers
- [ ] Security groups reference peer VPC SGs
- [ ] No transitive peering assumptions

### Transit Gateway

- [ ] TGW route tables segmented by environment
- [ ] Attachment per VPC/VPN/Direct Connect
- [ ] Route propagation configured appropriately
- [ ] Default route table associations reviewed
- [ ] Cross-account sharing via RAM if needed
- [ ] Blackhole routes for deprecated networks

### VPC Endpoints

- [ ] Gateway endpoints for S3 and DynamoDB (free)
- [ ] Interface endpoints for critical services:
  - [ ] Secrets Manager
  - [ ] SSM (Systems Manager)
  - [ ] ECR (dkr and api)
  - [ ] CloudWatch Logs
  - [ ] STS
- [ ] Endpoint policies restrict access
- [ ] Private DNS enabled for interface endpoints

## DNS

### Route 53 Private Hosted Zones

- [ ] PHZ associated with all relevant VPCs
- [ ] Split-horizon DNS configured if needed
- [ ] Resolver rules for on-prem DNS forwarding
- [ ] DNSSEC enabled where supported

### DNS Resolution

- [ ] `enableDnsSupport: true`
- [ ] `enableDnsHostnames: true`
- [ ] Custom DHCP options if using on-prem DNS

## Monitoring & Security

### Observability

- [ ] VPC Flow Logs analyzed in CloudWatch Insights
- [ ] Network Access Analyzer configured
- [ ] Reachability Analyzer for troubleshooting
- [ ] CloudWatch alarms for NAT Gateway metrics
- [ ] Traffic Mirroring for packet inspection (if needed)

### Threat Detection

- [ ] GuardDuty enabled in all regions
- [ ] VPC Flow Log analysis in GuardDuty
- [ ] Network Firewall for egress inspection (production)
- [ ] WAF on ALB/CloudFront for web traffic
- [ ] Lambda auto-remediation for common threats

### Compliance

- [ ] VPC Block Public Access enabled
- [ ] AWS Config rules for networking:
  - [ ] `vpc-sg-open-only-to-authorized-ports`
  - [ ] `vpc-flow-logs-enabled`
  - [ ] `vpc-default-security-group-closed`
- [ ] Regular audit of unused security groups
- [ ] Regular audit of unused ENIs

## High Availability

### NAT Gateway

- [ ] NAT Gateway per AZ (not shared)
- [ ] CloudWatch alarms for ErrorPortAllocation
- [ ] Sufficient Elastic IP allocation

### Load Balancing

- [ ] ALB spans all AZs
- [ ] Cross-zone load balancing enabled
- [ ] Health checks configured correctly
- [ ] SSL/TLS termination with ACM certificates

### Failover

- [ ] Multi-AZ database deployments
- [ ] Auto Scaling groups span all AZs
- [ ] DNS failover configured if needed

## Cost Optimization

- [ ] NAT Gateway data processing monitored
- [ ] VPC endpoints reduce NAT costs for AWS traffic
- [ ] Unused Elastic IPs released
- [ ] Data transfer between AZs minimized
- [ ] Transit Gateway attachments reviewed for necessity

## Documentation

- [ ] Network diagram updated
- [ ] CIDR allocation documented
- [ ] Security group rules documented
- [ ] Runbooks for common operations
- [ ] Incident response procedures for network issues

---

*Checklist Version: 2025.01*
