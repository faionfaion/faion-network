# AWS Networking LLM Prompts

> AI assistant prompts for VPC architecture and networking tasks.

## VPC Design

### Design Multi-AZ VPC

```
Design a production-ready VPC architecture for [APPLICATION_TYPE] with:

Requirements:
- Region: [REGION]
- Expected workloads: [WORKLOAD_DESCRIPTION]
- Compliance requirements: [COMPLIANCE e.g., HIPAA, PCI-DSS, SOC2]
- Connectivity needs: [ON_PREM/OTHER_VPCs/INTERNET]

Provide:
1. CIDR allocation plan (with room for growth)
2. Subnet design (public, private, data tiers)
3. Routing architecture
4. NAT Gateway strategy (HA vs cost optimization)
5. VPC endpoint recommendations
6. Security group baseline

Output as Terraform or CloudFormation (specify preference).
```

### Subnet Sizing Calculator

```
Calculate subnet sizing for:

VPC CIDR: [e.g., 10.0.0.0/16]
Availability Zones: [NUMBER]
Tiers needed: [public, private, data, etc.]
Expected resources per tier:
- Public: [ALB, NAT, bastion count]
- Private: [EC2, ECS tasks, Lambda ENIs]
- Data: [RDS, ElastiCache nodes]

Growth factor: [e.g., 2x over 3 years]

Provide:
1. Recommended CIDR blocks per subnet
2. Available IP count per subnet
3. Reserved IPs (AWS uses 5 per subnet)
4. Warnings if sizing is insufficient
```

## Security Groups

### Security Group Audit

```
Audit these security group rules for security issues:

[PASTE SECURITY GROUP RULES OR JSON]

Check for:
1. Overly permissive inbound rules (0.0.0.0/0)
2. Missing egress restrictions
3. Unused port ranges
4. Missing descriptions
5. Circular dependencies
6. Best practice violations

Provide:
1. Risk assessment (Critical/High/Medium/Low)
2. Specific recommendations with replacement rules
3. AWS CLI commands to fix issues
```

### Generate Security Group Rules

```
Generate security group rules for this architecture:

Application: [APPLICATION_TYPE]
Components:
- [COMPONENT_1]: [PORTS, PROTOCOLS]
- [COMPONENT_2]: [PORTS, PROTOCOLS]
- [COMPONENT_3]: [PORTS, PROTOCOLS]

Traffic flows:
- Internet -> [COMPONENT]
- [COMPONENT] -> [COMPONENT]
- [COMPONENT] -> AWS Services: [LIST]

Requirements:
- Zero trust (no 0.0.0.0/0 except where absolutely necessary)
- Reference security groups, not CIDRs where possible
- Include descriptions for all rules

Output as:
- [ ] Terraform
- [ ] CloudFormation
- [ ] AWS CLI commands
```

## Transit Gateway

### Transit Gateway Design

```
Design Transit Gateway architecture for:

VPCs to connect:
- [VPC_1]: [CIDR, purpose, region]
- [VPC_2]: [CIDR, purpose, region]
- [VPC_3]: [CIDR, purpose, region]

On-premises connectivity: [YES/NO, if yes: Direct Connect/VPN]
Isolation requirements: [Which VPCs should NOT communicate]
Shared services: [VPCs that all others need access to]

Provide:
1. TGW route table design
2. Attachment configuration
3. Route propagation vs static routes
4. Blackhole routes for isolation
5. Terraform module or CloudFormation template
```

### Migrate from VPC Peering to Transit Gateway

```
Plan migration from VPC peering to Transit Gateway:

Current peering connections:
[LIST EXISTING PEERING CONNECTIONS WITH CIDRs]

Requirements:
- Zero downtime migration
- Rollback capability
- Minimal application changes

Provide:
1. Step-by-step migration plan
2. Pre-migration checklist
3. Route table changes needed
4. Testing procedures
5. Rollback procedures
```

## VPC Endpoints

### VPC Endpoint Strategy

```
Recommend VPC endpoints for this workload:

Application services:
- [SERVICE_1]: uses [AWS_SERVICES]
- [SERVICE_2]: uses [AWS_SERVICES]

Current NAT Gateway cost: [MONTHLY_COST]
Security requirements: [DATA_SHOULD_NOT_TRAVERSE_INTERNET: yes/no]

Provide:
1. Required gateway endpoints (free)
2. Recommended interface endpoints
3. Estimated cost savings
4. Endpoint policy recommendations
5. Terraform/CloudFormation for implementation
```

## Troubleshooting

### Connectivity Troubleshooting

```
Help troubleshoot connectivity issue:

Source: [RESOURCE_TYPE, subnet, security group]
Destination: [RESOURCE_TYPE, subnet/IP, port]
Error: [TIMEOUT/CONNECTION_REFUSED/etc.]

Already checked:
- [ ] Security group rules
- [ ] NACL rules
- [ ] Route tables
- [ ] VPC peering/TGW routes

Provide:
1. Systematic troubleshooting steps
2. AWS CLI commands to diagnose
3. Common causes for this scenario
4. Reachability Analyzer setup if needed
```

### Flow Log Analysis

```
Analyze these VPC flow log entries:

[PASTE FLOW LOG ENTRIES]

Questions:
1. Identify rejected traffic patterns
2. Find potential security issues
3. Identify misconfigured security groups
4. Suggest CloudWatch Insights queries for ongoing monitoring
```

## Cost Optimization

### NAT Gateway Cost Reduction

```
Analyze NAT Gateway costs and suggest optimizations:

Current setup:
- NAT Gateways: [COUNT, per AZ or shared]
- Monthly data processed: [GB]
- Monthly cost: [USD]

Workloads using NAT:
- [WORKLOAD_1]: [TRAFFIC_TYPE, destination]
- [WORKLOAD_2]: [TRAFFIC_TYPE, destination]

Provide:
1. VPC endpoints that would reduce traffic
2. Architecture changes to reduce cross-AZ traffic
3. NAT instance alternative analysis (when appropriate)
4. Estimated savings per recommendation
```

### Multi-Account Networking Cost

```
Optimize networking costs across accounts:

Accounts:
- [ACCOUNT_1]: [VPCs, workloads]
- [ACCOUNT_2]: [VPCs, workloads]
- [ACCOUNT_3]: [VPCs, workloads]

Current connectivity: [PEERING/TGW/both]
Data transfer patterns: [DESCRIBE]

Provide:
1. Architecture recommendations
2. TGW vs peering cost comparison
3. Centralized egress strategy
4. Shared VPC endpoints via RAM
```

## Migration

### On-Premises to AWS Connectivity

```
Design hybrid connectivity for:

On-premises:
- Location: [CITY/REGION]
- Current bandwidth needs: [Mbps]
- Growth projection: [%/year]
- Latency requirements: [ms]

AWS:
- Region: [PRIMARY_REGION]
- DR region: [if applicable]
- VPCs to connect: [COUNT, CIDRs]

Requirements:
- Redundancy level: [SINGLE/DUAL]
- Budget: [MONTHLY]
- Encryption: [REQUIRED/PREFERRED]

Provide:
1. Direct Connect vs VPN recommendation
2. Architecture diagram description
3. Transit Gateway configuration
4. BGP routing design
5. Failover strategy
6. Implementation timeline
```

## Compliance

### Network Security Assessment

```
Assess network security for [COMPLIANCE_FRAMEWORK]:

Current architecture:
[DESCRIBE VPC ARCHITECTURE]

Compliance framework: [HIPAA/PCI-DSS/SOC2/FedRAMP]

Provide:
1. Gap analysis against framework requirements
2. Required network controls
3. Flow log and monitoring requirements
4. Network segmentation recommendations
5. Documentation requirements
6. Remediation priorities
```

## Code Review

### Review Terraform Networking Code

```
Review this Terraform networking configuration:

[PASTE TERRAFORM CODE]

Check for:
1. Security best practices
2. High availability issues
3. Cost optimization opportunities
4. Tagging consistency
5. Missing resources
6. Hardcoded values that should be variables

Provide specific line-by-line feedback and corrected code.
```

### Review CloudFormation Networking Template

```
Review this CloudFormation networking template:

[PASTE CLOUDFORMATION YAML/JSON]

Check for:
1. Security best practices
2. Missing DependsOn relationships
3. Proper use of Conditions
4. Output exports for cross-stack references
5. Parameter constraints
6. Missing deletion policies

Provide corrected template with explanations.
```

---

*Prompts Version: 2025.01*
