# GCP Networking Checklist

## VPC Design

### Planning Phase

- [ ] Identify all regions where workloads will run
- [ ] Document IP address requirements (current + growth)
- [ ] Plan non-overlapping CIDR ranges for VPC peering
- [ ] Define network segmentation strategy
- [ ] Determine Shared VPC vs standalone VPC architecture
- [ ] Document connectivity requirements (on-prem, other clouds)

### VPC Configuration

- [ ] Create VPC with custom mode (not auto)
- [ ] Delete or isolate default VPC
- [ ] Verify no legacy networks exist in project
- [ ] Use clear naming conventions (`{env}-{region}-{purpose}`)
- [ ] Document VPC in architecture diagrams

### Subnet Configuration

- [ ] Create regional subnets with appropriate CIDR ranges
- [ ] Reserve secondary ranges for GKE (pods/services)
- [ ] Enable Private Google Access on all subnets
- [ ] Enable VPC Flow Logs for visibility
- [ ] Configure flow log sampling rate (cost vs visibility)
- [ ] Plan for subnet expansion (leave room)

## Firewall Rules

### Security Baseline

- [ ] Remove or restrict default `allow-*` rules
- [ ] Create deny-all default rule (lowest priority)
- [ ] Document all firewall rules with descriptions
- [ ] Use service accounts for filtering (not network tags)
- [ ] Enable firewall rule logging for security rules

### Rule Categories

- [ ] **Internal**: Allow traffic between subnets
- [ ] **Ingress**: Define allowed external access points
- [ ] **Egress**: Restrict outbound traffic where needed
- [ ] **Health checks**: Allow GCP health check ranges
- [ ] **IAP**: Allow IAP ranges for SSH/RDP (35.235.240.0/20)

### Firewall Best Practices

- [ ] Use hierarchical firewall policies for org-wide rules
- [ ] Limit 0.0.0.0/0 source ranges to essential services
- [ ] Group related rules with consistent naming
- [ ] Review firewall rules quarterly
- [ ] Test firewall rules before production deployment

## Cloud NAT

### Configuration

- [ ] Create Cloud Router in each region
- [ ] Configure Cloud NAT for private instances
- [ ] Choose NAT IP allocation strategy
  - [ ] Auto-allocate (simple, less control)
  - [ ] Manual allocation (predictable IPs)
- [ ] Configure minimum ports per VM
- [ ] Set appropriate timeouts

### Monitoring

- [ ] Enable Cloud NAT logging
- [ ] Set up alerts for port exhaustion
- [ ] Monitor NAT gateway utilization
- [ ] Review egress patterns regularly

## Load Balancing

### Architecture Decision

- [ ] Choose load balancer type based on requirements:
  - [ ] Global HTTP(S) LB - web applications
  - [ ] Regional TCP/UDP LB - non-HTTP traffic
  - [ ] Internal TCP/UDP LB - internal services
  - [ ] Internal HTTP(S) LB - internal web services

### Configuration

- [ ] Create health checks with appropriate intervals
- [ ] Configure backend services with proper timeout
- [ ] Set up SSL certificates (managed or self-managed)
- [ ] Configure URL maps for path-based routing
- [ ] Enable Cloud CDN if serving static content
- [ ] Configure session affinity if needed

### Security

- [ ] Enable Cloud Armor for DDoS protection
- [ ] Configure WAF rules for OWASP threats
- [ ] Set up rate limiting policies
- [ ] Enable access logging
- [ ] Configure SSL policies (TLS 1.2+ only)

## Security Controls

### VPC Service Controls

- [ ] Define service perimeters for sensitive projects
- [ ] Configure access levels for allowed identities
- [ ] Set up ingress/egress policies
- [ ] Test perimeter before enforcing
- [ ] Monitor VPC SC audit logs

### Private Connectivity

- [ ] Enable Private Google Access
- [ ] Configure Private Service Connect for Google APIs
- [ ] Set up VPC peering where needed
- [ ] Configure Cloud VPN or Interconnect for hybrid

### DNS Security

- [ ] Enable Cloud DNS logging for all VPC networks
- [ ] Configure DNS policies for internal resolution
- [ ] Set up private DNS zones for internal services
- [ ] Use Cloud DNS Security Extensions (DNSSEC) for public zones

## Monitoring and Logging

### Enable Logging

- [ ] VPC Flow Logs on all subnets
- [ ] Firewall rule logging on security-relevant rules
- [ ] Cloud NAT logging
- [ ] Load balancer access logs
- [ ] Cloud DNS query logging

### Alerting

- [ ] High firewall deny rates
- [ ] NAT port exhaustion warnings
- [ ] Unusual egress traffic patterns
- [ ] Load balancer error rates
- [ ] Backend health check failures

### Review Cadence

- [ ] Daily: Check security alerts
- [ ] Weekly: Review traffic patterns
- [ ] Monthly: Audit firewall rules
- [ ] Quarterly: Full networking review

## Compliance

### Documentation

- [ ] Network architecture diagrams updated
- [ ] IP address inventory maintained
- [ ] Firewall rule documentation current
- [ ] Change management records complete

### Audit

- [ ] No public IPs on sensitive workloads
- [ ] All subnets have flow logs enabled
- [ ] No overly permissive firewall rules
- [ ] VPC Service Controls enforced where required
- [ ] Private Google Access enabled everywhere

---

*GCP Networking Checklist | faion-infrastructure-engineer*
