# AWS Networking Examples

> CLI commands and code examples for VPC, subnets, security groups, and Transit Gateway.

## VPC Operations

### Create VPC

```bash
# Create VPC with DNS support
aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=production-vpc},{Key=Environment,Value=production}]'

# Enable DNS hostnames
aws ec2 modify-vpc-attribute \
    --vpc-id vpc-0123456789abcdef0 \
    --enable-dns-hostnames '{"Value": true}'

# Enable DNS support
aws ec2 modify-vpc-attribute \
    --vpc-id vpc-0123456789abcdef0 \
    --enable-dns-support '{"Value": true}'
```

### Describe VPCs

```bash
# List all VPCs
aws ec2 describe-vpcs --output table

# Get specific VPC details
aws ec2 describe-vpcs \
    --vpc-ids vpc-0123456789abcdef0 \
    --query 'Vpcs[0].[VpcId,CidrBlock,State,Tags[?Key==`Name`].Value|[0]]' \
    --output table

# Find VPC by name
aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=production-vpc" \
    --query 'Vpcs[0].VpcId' \
    --output text
```

### Secondary CIDR Blocks

```bash
# Add secondary CIDR
aws ec2 associate-vpc-cidr-block \
    --vpc-id vpc-0123456789abcdef0 \
    --cidr-block 10.1.0.0/16

# Remove secondary CIDR
aws ec2 disassociate-vpc-cidr-block \
    --association-id vpc-cidr-assoc-0123456789abcdef0
```

## Subnet Operations

### Create Subnets

```bash
# Create public subnet
aws ec2 create-subnet \
    --vpc-id vpc-0123456789abcdef0 \
    --cidr-block 10.0.0.0/24 \
    --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=production-public-a},{Key=Tier,Value=public}]'

# Create private subnet
aws ec2 create-subnet \
    --vpc-id vpc-0123456789abcdef0 \
    --cidr-block 10.0.16.0/24 \
    --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=production-private-a},{Key=Tier,Value=private}]'

# Create data subnet
aws ec2 create-subnet \
    --vpc-id vpc-0123456789abcdef0 \
    --cidr-block 10.0.32.0/24 \
    --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=production-data-a},{Key=Tier,Value=data}]'
```

### Enable Auto-Assign Public IP

```bash
# For public subnets only
aws ec2 modify-subnet-attribute \
    --subnet-id subnet-0123456789abcdef0 \
    --map-public-ip-on-launch
```

### List Subnets

```bash
# List all subnets in VPC
aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=vpc-0123456789abcdef0" \
    --query 'Subnets[*].[SubnetId,CidrBlock,AvailabilityZone,Tags[?Key==`Name`].Value|[0]]' \
    --output table

# Get available IPs in subnet
aws ec2 describe-subnets \
    --subnet-ids subnet-0123456789abcdef0 \
    --query 'Subnets[0].AvailableIpAddressCount'
```

## Internet Gateway

```bash
# Create Internet Gateway
aws ec2 create-internet-gateway \
    --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=production-igw}]'

# Attach to VPC
aws ec2 attach-internet-gateway \
    --internet-gateway-id igw-0123456789abcdef0 \
    --vpc-id vpc-0123456789abcdef0

# Detach from VPC
aws ec2 detach-internet-gateway \
    --internet-gateway-id igw-0123456789abcdef0 \
    --vpc-id vpc-0123456789abcdef0
```

## NAT Gateway

```bash
# Allocate Elastic IP
aws ec2 allocate-address --domain vpc

# Create NAT Gateway
aws ec2 create-nat-gateway \
    --subnet-id subnet-0123456789abcdef0 \
    --allocation-id eipalloc-0123456789abcdef0 \
    --tag-specifications 'ResourceType=natgateway,Tags=[{Key=Name,Value=production-nat-a}]'

# Wait for NAT Gateway
aws ec2 wait nat-gateway-available \
    --nat-gateway-ids nat-0123456789abcdef0

# Delete NAT Gateway
aws ec2 delete-nat-gateway --nat-gateway-id nat-0123456789abcdef0
```

## Route Tables

### Create and Configure

```bash
# Create route table
aws ec2 create-route-table \
    --vpc-id vpc-0123456789abcdef0 \
    --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=production-private-rt}]'

# Add route to Internet Gateway (public)
aws ec2 create-route \
    --route-table-id rtb-0123456789abcdef0 \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id igw-0123456789abcdef0

# Add route to NAT Gateway (private)
aws ec2 create-route \
    --route-table-id rtb-0123456789abcdef1 \
    --destination-cidr-block 0.0.0.0/0 \
    --nat-gateway-id nat-0123456789abcdef0

# Associate subnet with route table
aws ec2 associate-route-table \
    --route-table-id rtb-0123456789abcdef0 \
    --subnet-id subnet-0123456789abcdef0
```

### View Routes

```bash
# List routes in table
aws ec2 describe-route-tables \
    --route-table-ids rtb-0123456789abcdef0 \
    --query 'RouteTables[0].Routes[*].[DestinationCidrBlock,GatewayId,NatGatewayId,State]' \
    --output table
```

## Security Groups

### Create Security Group

```bash
# Create security group
aws ec2 create-security-group \
    --group-name production-web-sg \
    --description "Security group for web servers" \
    --vpc-id vpc-0123456789abcdef0 \
    --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=production-web-sg}]'
```

### Add Inbound Rules

```bash
# Allow HTTPS from anywhere (ALB only)
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0 \
    --tag-specifications 'ResourceType=security-group-rule,Tags=[{Key=Description,Value=HTTPS from internet}]'

# Allow from another security group
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 8080 \
    --source-group sg-0123456789abcdef1

# Allow from specific CIDR (internal)
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 22 \
    --cidr 10.0.0.0/8
```

### Add Outbound Rules

```bash
# Allow HTTPS outbound
aws ec2 authorize-security-group-egress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Allow PostgreSQL to RDS security group
aws ec2 authorize-security-group-egress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 5432 \
    --source-group sg-0123456789abcdef2
```

### Revoke Rules

```bash
# Revoke inbound rule
aws ec2 revoke-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# Revoke all egress (then add specific rules)
aws ec2 revoke-security-group-egress \
    --group-id sg-0123456789abcdef0 \
    --protocol all \
    --port all \
    --cidr 0.0.0.0/0
```

### Audit Security Groups

```bash
# Find security groups with 0.0.0.0/0 inbound
aws ec2 describe-security-groups \
    --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' \
    --output table

# Find unused security groups
aws ec2 describe-network-interfaces \
    --query 'NetworkInterfaces[*].Groups[*].GroupId' \
    --output text | tr '\t' '\n' | sort -u > /tmp/used-sgs.txt

aws ec2 describe-security-groups \
    --query 'SecurityGroups[*].GroupId' \
    --output text | tr '\t' '\n' | sort -u > /tmp/all-sgs.txt

comm -23 /tmp/all-sgs.txt /tmp/used-sgs.txt
```

## Network ACLs

```bash
# Create NACL
aws ec2 create-network-acl \
    --vpc-id vpc-0123456789abcdef0 \
    --tag-specifications 'ResourceType=network-acl,Tags=[{Key=Name,Value=production-private-nacl}]'

# Add inbound rule (allow HTTPS)
aws ec2 create-network-acl-entry \
    --network-acl-id acl-0123456789abcdef0 \
    --rule-number 100 \
    --protocol tcp \
    --port-range From=443,To=443 \
    --cidr-block 0.0.0.0/0 \
    --rule-action allow \
    --ingress

# Add outbound rule (ephemeral ports)
aws ec2 create-network-acl-entry \
    --network-acl-id acl-0123456789abcdef0 \
    --rule-number 100 \
    --protocol tcp \
    --port-range From=1024,To=65535 \
    --cidr-block 0.0.0.0/0 \
    --rule-action allow \
    --egress

# Associate with subnet
aws ec2 replace-network-acl-association \
    --association-id aclassoc-0123456789abcdef0 \
    --network-acl-id acl-0123456789abcdef0
```

## VPC Endpoints

### Gateway Endpoints (S3, DynamoDB)

```bash
# Create S3 gateway endpoint
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-0123456789abcdef0 \
    --service-name com.amazonaws.us-east-1.s3 \
    --route-table-ids rtb-0123456789abcdef0 rtb-0123456789abcdef1 \
    --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=production-s3-endpoint}]'

# Create DynamoDB gateway endpoint
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-0123456789abcdef0 \
    --service-name com.amazonaws.us-east-1.dynamodb \
    --route-table-ids rtb-0123456789abcdef0 rtb-0123456789abcdef1
```

### Interface Endpoints

```bash
# Create Secrets Manager interface endpoint
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-0123456789abcdef0 \
    --vpc-endpoint-type Interface \
    --service-name com.amazonaws.us-east-1.secretsmanager \
    --subnet-ids subnet-0123456789abcdef0 subnet-0123456789abcdef1 \
    --security-group-ids sg-0123456789abcdef0 \
    --private-dns-enabled \
    --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=production-secretsmanager-endpoint}]'

# Create SSM endpoints (need 3 for Session Manager)
for service in ssm ssmmessages ec2messages; do
    aws ec2 create-vpc-endpoint \
        --vpc-id vpc-0123456789abcdef0 \
        --vpc-endpoint-type Interface \
        --service-name com.amazonaws.us-east-1.$service \
        --subnet-ids subnet-0123456789abcdef0 \
        --security-group-ids sg-0123456789abcdef0 \
        --private-dns-enabled
done
```

## Transit Gateway

### Create Transit Gateway

```bash
# Create Transit Gateway
aws ec2 create-transit-gateway \
    --description "Production Transit Gateway" \
    --options AutoAcceptSharedAttachments=enable,DefaultRouteTableAssociation=disable,DefaultRouteTablePropagation=disable,DnsSupport=enable,VpnEcmpSupport=enable \
    --tag-specifications 'ResourceType=transit-gateway,Tags=[{Key=Name,Value=production-tgw}]'

# Wait for TGW to be available
aws ec2 describe-transit-gateways \
    --transit-gateway-ids tgw-0123456789abcdef0 \
    --query 'TransitGateways[0].State'
```

### Attach VPCs

```bash
# Attach VPC to Transit Gateway
aws ec2 create-transit-gateway-vpc-attachment \
    --transit-gateway-id tgw-0123456789abcdef0 \
    --vpc-id vpc-0123456789abcdef0 \
    --subnet-ids subnet-0123456789abcdef0 subnet-0123456789abcdef1 \
    --tag-specifications 'ResourceType=transit-gateway-attachment,Tags=[{Key=Name,Value=production-vpc-attachment}]'

# List attachments
aws ec2 describe-transit-gateway-attachments \
    --filters "Name=transit-gateway-id,Values=tgw-0123456789abcdef0" \
    --query 'TransitGatewayAttachments[*].[TransitGatewayAttachmentId,ResourceType,State,Tags[?Key==`Name`].Value|[0]]' \
    --output table
```

### Transit Gateway Route Tables

```bash
# Create route table
aws ec2 create-transit-gateway-route-table \
    --transit-gateway-id tgw-0123456789abcdef0 \
    --tag-specifications 'ResourceType=transit-gateway-route-table,Tags=[{Key=Name,Value=production-rt}]'

# Associate attachment with route table
aws ec2 associate-transit-gateway-route-table \
    --transit-gateway-route-table-id tgw-rtb-0123456789abcdef0 \
    --transit-gateway-attachment-id tgw-attach-0123456789abcdef0

# Enable route propagation
aws ec2 enable-transit-gateway-route-table-propagation \
    --transit-gateway-route-table-id tgw-rtb-0123456789abcdef0 \
    --transit-gateway-attachment-id tgw-attach-0123456789abcdef0

# Add static route
aws ec2 create-transit-gateway-route \
    --transit-gateway-route-table-id tgw-rtb-0123456789abcdef0 \
    --destination-cidr-block 10.0.0.0/8 \
    --transit-gateway-attachment-id tgw-attach-0123456789abcdef0

# Add blackhole route
aws ec2 create-transit-gateway-route \
    --transit-gateway-route-table-id tgw-rtb-0123456789abcdef0 \
    --destination-cidr-block 192.168.0.0/16 \
    --blackhole
```

### View Transit Gateway Routes

```bash
# Search routes
aws ec2 search-transit-gateway-routes \
    --transit-gateway-route-table-id tgw-rtb-0123456789abcdef0 \
    --filters "Name=type,Values=static,propagated" \
    --query 'Routes[*].[DestinationCidrBlock,Type,State,TransitGatewayAttachments[0].TransitGatewayAttachmentId]' \
    --output table
```

## VPC Flow Logs

```bash
# Create CloudWatch log group
aws logs create-log-group --log-group-name /vpc/flow-logs/production

# Create IAM role for flow logs (see templates.md)

# Enable flow logs on VPC
aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-ids vpc-0123456789abcdef0 \
    --traffic-type ALL \
    --log-destination-type cloud-watch-logs \
    --log-group-name /vpc/flow-logs/production \
    --deliver-logs-permission-arn arn:aws:iam::123456789012:role/flow-logs-role \
    --tag-specifications 'ResourceType=vpc-flow-log,Tags=[{Key=Name,Value=production-vpc-flow-logs}]'

# Enable flow logs to S3
aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-ids vpc-0123456789abcdef0 \
    --traffic-type REJECT \
    --log-destination-type s3 \
    --log-destination arn:aws:s3:::my-flow-logs-bucket/production/

# Query flow logs in CloudWatch Insights
# Top 10 rejected connections
aws logs start-query \
    --log-group-name /vpc/flow-logs/production \
    --start-time $(date -d '1 hour ago' +%s) \
    --end-time $(date +%s) \
    --query-string 'filter action = "REJECT" | stats count(*) as rejections by srcAddr, dstPort | sort rejections desc | limit 10'
```

## VPC Peering

```bash
# Create peering connection
aws ec2 create-vpc-peering-connection \
    --vpc-id vpc-0123456789abcdef0 \
    --peer-vpc-id vpc-0123456789abcdef1 \
    --tag-specifications 'ResourceType=vpc-peering-connection,Tags=[{Key=Name,Value=prod-to-staging}]'

# Accept peering (if same account)
aws ec2 accept-vpc-peering-connection \
    --vpc-peering-connection-id pcx-0123456789abcdef0

# Add route to peer VPC
aws ec2 create-route \
    --route-table-id rtb-0123456789abcdef0 \
    --destination-cidr-block 10.1.0.0/16 \
    --vpc-peering-connection-id pcx-0123456789abcdef0

# Enable DNS resolution for peering
aws ec2 modify-vpc-peering-connection-options \
    --vpc-peering-connection-id pcx-0123456789abcdef0 \
    --requester-peering-connection-options AllowDnsResolutionFromRemoteVpc=true \
    --accepter-peering-connection-options AllowDnsResolutionFromRemoteVpc=true
```

## Troubleshooting

```bash
# Check VPC route tables
aws ec2 describe-route-tables \
    --filters "Name=vpc-id,Values=vpc-0123456789abcdef0" \
    --query 'RouteTables[*].[RouteTableId,Tags[?Key==`Name`].Value|[0],Associations[*].SubnetId]' \
    --output table

# Check security group rules for instance
aws ec2 describe-instances \
    --instance-ids i-0123456789abcdef0 \
    --query 'Reservations[0].Instances[0].SecurityGroups[*].GroupId' \
    --output text | xargs -n1 aws ec2 describe-security-groups --group-ids

# Reachability Analyzer
aws ec2 create-network-insights-path \
    --source i-0123456789abcdef0 \
    --destination i-0123456789abcdef1 \
    --protocol TCP \
    --destination-port 443

aws ec2 start-network-insights-analysis \
    --network-insights-path-id nip-0123456789abcdef0

# Network Access Analyzer
aws ec2 create-network-insights-access-scope \
    --match-paths '[{"Source":{"ResourceStatement":{"ResourceTypes":["AWS::EC2::InternetGateway"]}}}]'
```

---

*Examples Version: 2025.01*
