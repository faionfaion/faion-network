# AWS Examples

Practical examples for EC2, IAM, and networking configurations.

## EC2 Examples

### Launch Instance with Best Practices

```bash
# Launch instance with IMDSv2 required
aws ec2 run-instances \
    --image-id ami-0123456789abcdef0 \
    --instance-type t3.medium \
    --key-name my-key-pair \
    --security-group-ids sg-web-tier \
    --subnet-id subnet-private-1a \
    --iam-instance-profile Name=ec2-ssm-role \
    --metadata-options "HttpTokens=required,HttpPutResponseHopLimit=2,HttpEndpoint=enabled" \
    --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":50,"VolumeType":"gp3","Encrypted":true}}]' \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=web-server},{Key=Environment,Value=production}]' \
    --disable-api-termination
```

### Create Launch Template

```bash
aws ec2 create-launch-template \
    --launch-template-name web-server-template \
    --version-description "v1 - initial" \
    --launch-template-data '{
        "ImageId": "ami-0123456789abcdef0",
        "InstanceType": "t3.medium",
        "KeyName": "my-key-pair",
        "SecurityGroupIds": ["sg-web-tier"],
        "MetadataOptions": {
            "HttpTokens": "required",
            "HttpPutResponseHopLimit": 2,
            "HttpEndpoint": "enabled"
        },
        "BlockDeviceMappings": [{
            "DeviceName": "/dev/xvda",
            "Ebs": {
                "VolumeSize": 50,
                "VolumeType": "gp3",
                "Encrypted": true,
                "DeleteOnTermination": true
            }
        }],
        "TagSpecifications": [{
            "ResourceType": "instance",
            "Tags": [
                {"Key": "Name", "Value": "web-server"},
                {"Key": "ManagedBy", "Value": "launch-template"}
            ]
        }],
        "IamInstanceProfile": {"Name": "ec2-ssm-role"}
    }'
```

### Auto Scaling Group

```bash
# Create Auto Scaling Group
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name web-asg \
    --launch-template LaunchTemplateName=web-server-template,Version='$Latest' \
    --min-size 2 \
    --max-size 10 \
    --desired-capacity 3 \
    --vpc-zone-identifier "subnet-1a,subnet-1b,subnet-1c" \
    --target-group-arns "arn:aws:elasticloadbalancing:region:account:targetgroup/web-tg/1234567890123456" \
    --health-check-type ELB \
    --health-check-grace-period 300 \
    --tags "Key=Environment,Value=production,PropagateAtLaunch=true"

# Create scaling policy (target tracking)
aws autoscaling put-scaling-policy \
    --auto-scaling-group-name web-asg \
    --policy-name cpu-target-tracking \
    --policy-type TargetTrackingScaling \
    --target-tracking-configuration '{
        "TargetValue": 70.0,
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "ASGAverageCPUUtilization"
        }
    }'
```

### Security Groups (Role-Based)

```bash
# Web tier security group
aws ec2 create-security-group \
    --group-name web-tier-sg \
    --description "Web tier - public facing" \
    --vpc-id vpc-0123456789abcdef0

aws ec2 authorize-security-group-ingress \
    --group-id sg-web-tier \
    --ip-permissions '[
        {"IpProtocol": "tcp", "FromPort": 443, "ToPort": 443, "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "HTTPS from anywhere"}]},
        {"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80, "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "HTTP for redirect"}]}
    ]'

# App tier security group
aws ec2 create-security-group \
    --group-name app-tier-sg \
    --description "App tier - internal only" \
    --vpc-id vpc-0123456789abcdef0

aws ec2 authorize-security-group-ingress \
    --group-id sg-app-tier \
    --ip-permissions '[
        {"IpProtocol": "tcp", "FromPort": 8080, "ToPort": 8080, "UserIdGroupPairs": [{"GroupId": "sg-web-tier", "Description": "From web tier"}]}
    ]'

# Database tier security group
aws ec2 create-security-group \
    --group-name db-tier-sg \
    --description "Database tier - restricted" \
    --vpc-id vpc-0123456789abcdef0

aws ec2 authorize-security-group-ingress \
    --group-id sg-db-tier \
    --ip-permissions '[
        {"IpProtocol": "tcp", "FromPort": 5432, "ToPort": 5432, "UserIdGroupPairs": [{"GroupId": "sg-app-tier", "Description": "PostgreSQL from app tier"}]}
    ]'
```

## IAM Examples

### Least Privilege Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3ReadSpecificBucket",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-app-bucket",
                "arn:aws:s3:::my-app-bucket/*"
            ]
        },
        {
            "Sid": "SecretsManagerReadSpecific",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:myapp/prod/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceTag/Environment": "production"
                }
            }
        },
        {
            "Sid": "KMSDecryptSpecificKey",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"
            ]
        }
    ]
}
```

### EC2 Instance Role (SSM Access)

```bash
# Create trust policy
cat > trust-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

# Create role
aws iam create-role \
    --role-name ec2-ssm-role \
    --assume-role-policy-document file://trust-policy.json

# Attach SSM managed policy
aws iam attach-role-policy \
    --role-name ec2-ssm-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore

# Create instance profile
aws iam create-instance-profile --instance-profile-name ec2-ssm-role
aws iam add-role-to-instance-profile \
    --instance-profile-name ec2-ssm-role \
    --role-name ec2-ssm-role
```

### Cross-Account Role

```bash
# Create role in target account
cat > cross-account-trust.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::SOURCE_ACCOUNT_ID:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "Bool": {"aws:MultiFactorAuthPresent": "true"},
                "StringEquals": {"sts:ExternalId": "unique-external-id"}
            }
        }
    ]
}
EOF

aws iam create-role \
    --role-name CrossAccountReadOnly \
    --assume-role-policy-document file://cross-account-trust.json

# Assume role from source account
aws sts assume-role \
    --role-arn arn:aws:iam::TARGET_ACCOUNT:role/CrossAccountReadOnly \
    --role-session-name my-session \
    --external-id unique-external-id
```

### Permission Boundary

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowedServices",
            "Effect": "Allow",
            "Action": [
                "ec2:*",
                "s3:*",
                "rds:*",
                "lambda:*",
                "logs:*",
                "cloudwatch:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "DenyIAMChanges",
            "Effect": "Deny",
            "Action": [
                "iam:CreateUser",
                "iam:DeleteUser",
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:AttachRolePolicy",
                "iam:DetachRolePolicy",
                "iam:PutRolePermissionsBoundary",
                "iam:DeleteRolePermissionsBoundary"
            ],
            "Resource": "*"
        },
        {
            "Sid": "DenyOrganizations",
            "Effect": "Deny",
            "Action": "organizations:*",
            "Resource": "*"
        }
    ]
}
```

## Networking Examples

### VPC with Three-Tier Subnets

```bash
# Create VPC
aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=production-vpc}]'

# Enable DNS
aws ec2 modify-vpc-attribute --vpc-id vpc-xxx --enable-dns-hostnames '{"Value": true}'
aws ec2 modify-vpc-attribute --vpc-id vpc-xxx --enable-dns-support '{"Value": true}'

# Create Internet Gateway
aws ec2 create-internet-gateway \
    --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=production-igw}]'
aws ec2 attach-internet-gateway --vpc-id vpc-xxx --internet-gateway-id igw-xxx

# Create subnets (3 AZs x 3 tiers = 9 subnets)
# Public subnets
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24 --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=public-1a},{Key=Tier,Value=public}]'
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.2.0/24 --availability-zone us-east-1b \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=public-1b},{Key=Tier,Value=public}]'
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.3.0/24 --availability-zone us-east-1c \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=public-1c},{Key=Tier,Value=public}]'

# Private subnets (application)
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.11.0/24 --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=private-1a},{Key=Tier,Value=private}]'
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.12.0/24 --availability-zone us-east-1b \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=private-1b},{Key=Tier,Value=private}]'
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.13.0/24 --availability-zone us-east-1c \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=private-1c},{Key=Tier,Value=private}]'

# Database subnets
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.21.0/24 --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=database-1a},{Key=Tier,Value=database}]'
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.22.0/24 --availability-zone us-east-1b \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=database-1b},{Key=Tier,Value=database}]'
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.23.0/24 --availability-zone us-east-1c \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=database-1c},{Key=Tier,Value=database}]'
```

### NAT Gateway (Per-AZ for Production)

```bash
# Allocate Elastic IPs
aws ec2 allocate-address --domain vpc --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Name,Value=nat-1a}]'
aws ec2 allocate-address --domain vpc --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Name,Value=nat-1b}]'
aws ec2 allocate-address --domain vpc --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Name,Value=nat-1c}]'

# Create NAT Gateways
aws ec2 create-nat-gateway \
    --subnet-id subnet-public-1a \
    --allocation-id eipalloc-1a \
    --tag-specifications 'ResourceType=natgateway,Tags=[{Key=Name,Value=nat-1a}]'
aws ec2 create-nat-gateway \
    --subnet-id subnet-public-1b \
    --allocation-id eipalloc-1b \
    --tag-specifications 'ResourceType=natgateway,Tags=[{Key=Name,Value=nat-1b}]'
aws ec2 create-nat-gateway \
    --subnet-id subnet-public-1c \
    --allocation-id eipalloc-1c \
    --tag-specifications 'ResourceType=natgateway,Tags=[{Key=Name,Value=nat-1c}]'
```

### VPC Endpoints

```bash
# Gateway endpoint for S3 (free)
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-xxx \
    --service-name com.amazonaws.us-east-1.s3 \
    --route-table-ids rtb-private \
    --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=s3-endpoint}]'

# Interface endpoint for Secrets Manager
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-xxx \
    --vpc-endpoint-type Interface \
    --service-name com.amazonaws.us-east-1.secretsmanager \
    --subnet-ids subnet-private-1a subnet-private-1b subnet-private-1c \
    --security-group-ids sg-endpoints \
    --private-dns-enabled \
    --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=secretsmanager-endpoint}]'

# Interface endpoint for ECR
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-xxx \
    --vpc-endpoint-type Interface \
    --service-name com.amazonaws.us-east-1.ecr.api \
    --subnet-ids subnet-private-1a subnet-private-1b subnet-private-1c \
    --security-group-ids sg-endpoints \
    --private-dns-enabled
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-xxx \
    --vpc-endpoint-type Interface \
    --service-name com.amazonaws.us-east-1.ecr.dkr \
    --subnet-ids subnet-private-1a subnet-private-1b subnet-private-1c \
    --security-group-ids sg-endpoints \
    --private-dns-enabled
```

### Transit Gateway

```bash
# Create Transit Gateway
aws ec2 create-transit-gateway \
    --description "Central transit gateway" \
    --options "AmazonSideAsn=64512,AutoAcceptSharedAttachments=enable,DefaultRouteTableAssociation=enable,DefaultRouteTablePropagation=enable,VpnEcmpSupport=enable,DnsSupport=enable" \
    --tag-specifications 'ResourceType=transit-gateway,Tags=[{Key=Name,Value=central-tgw}]'

# Attach VPCs
aws ec2 create-transit-gateway-vpc-attachment \
    --transit-gateway-id tgw-xxx \
    --vpc-id vpc-production \
    --subnet-ids subnet-tgw-1a subnet-tgw-1b subnet-tgw-1c \
    --tag-specifications 'ResourceType=transit-gateway-attachment,Tags=[{Key=Name,Value=production-attachment}]'

aws ec2 create-transit-gateway-vpc-attachment \
    --transit-gateway-id tgw-xxx \
    --vpc-id vpc-shared-services \
    --subnet-ids subnet-tgw-shared-1a subnet-tgw-shared-1b \
    --tag-specifications 'ResourceType=transit-gateway-attachment,Tags=[{Key=Name,Value=shared-services-attachment}]'
```

### VPC Flow Logs

```bash
# Create CloudWatch log group
aws logs create-log-group --log-group-name /vpc/flow-logs/production

# Create flow logs
aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-ids vpc-xxx \
    --traffic-type ALL \
    --log-destination-type cloud-watch-logs \
    --log-group-name /vpc/flow-logs/production \
    --deliver-logs-permission-arn arn:aws:iam::123456789012:role/flow-logs-role \
    --tag-specifications 'ResourceType=vpc-flow-log,Tags=[{Key=Name,Value=production-flow-logs}]'
```

### Application Load Balancer

```bash
# Create ALB
aws elbv2 create-load-balancer \
    --name web-alb \
    --subnets subnet-public-1a subnet-public-1b subnet-public-1c \
    --security-groups sg-alb \
    --scheme internet-facing \
    --type application \
    --ip-address-type ipv4

# Create target group
aws elbv2 create-target-group \
    --name web-targets \
    --protocol HTTP \
    --port 8080 \
    --vpc-id vpc-xxx \
    --target-type instance \
    --health-check-path /health \
    --health-check-interval-seconds 30 \
    --healthy-threshold-count 2 \
    --unhealthy-threshold-count 3

# Create HTTPS listener
aws elbv2 create-listener \
    --load-balancer-arn arn:aws:elasticloadbalancing:region:account:loadbalancer/app/web-alb/xxx \
    --protocol HTTPS \
    --port 443 \
    --certificates CertificateArn=arn:aws:acm:region:account:certificate/xxx \
    --ssl-policy ELBSecurityPolicy-TLS13-1-2-2021-06 \
    --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:region:account:targetgroup/web-targets/xxx

# HTTP to HTTPS redirect
aws elbv2 create-listener \
    --load-balancer-arn arn:aws:elasticloadbalancing:region:account:loadbalancer/app/web-alb/xxx \
    --protocol HTTP \
    --port 80 \
    --default-actions 'Type=redirect,RedirectConfig={Protocol=HTTPS,Port=443,StatusCode=HTTP_301}'
```

## Sources

- [EC2 Best Practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- [Security Groups Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [VPC Design Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- [Transit Gateway Best Practices](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-best-design-practices.html)
- [AWS Networking VPC Architecture](https://newsletter.simpleaws.dev/p/advanced-networking-on-aws-vpc-design-transit-gateway)
