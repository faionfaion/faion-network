# AWS EC2 & ECS Templates

Production-ready templates for ECS task definitions, services, and Terraform modules.

## ECS Task Definition (Fargate)

### Basic Web Application

```json
{
  "family": "my-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/my-app:v1.0.0",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        { "name": "NODE_ENV", "value": "production" },
        { "name": "PORT", "value": "8080" }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:my-app/database-url"
        },
        {
          "name": "API_KEY",
          "valueFrom": "arn:aws:ssm:REGION:ACCOUNT_ID:parameter/my-app/api-key"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-app",
          "awslogs-region": "REGION",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "linuxParameters": {
        "initProcessEnabled": true
      },
      "readonlyRootFilesystem": true,
      "user": "1000:1000"
    }
  ],
  "tags": [
    { "key": "Environment", "value": "production" },
    { "key": "Project", "value": "my-app" }
  ]
}
```

### Multi-Container (App + Sidecar)

```json
{
  "family": "my-app-with-proxy",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/my-app:v1.0.0",
      "essential": true,
      "portMappings": [
        { "containerPort": 8080, "protocol": "tcp" }
      ],
      "environment": [
        { "name": "PORT", "value": "8080" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-app",
          "awslogs-region": "REGION",
          "awslogs-stream-prefix": "app"
        }
      },
      "dependsOn": [
        { "containerName": "envoy", "condition": "START" }
      ],
      "readonlyRootFilesystem": true,
      "user": "1000:1000"
    },
    {
      "name": "envoy",
      "image": "envoyproxy/envoy:v1.28-latest",
      "essential": true,
      "portMappings": [
        { "containerPort": 9901, "protocol": "tcp" }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:9901/ready || exit 1"],
        "interval": 10,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 10
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-app",
          "awslogs-region": "REGION",
          "awslogs-stream-prefix": "envoy"
        }
      },
      "cpu": 256,
      "memory": 512
    }
  ]
}
```

### Background Worker

```json
{
  "family": "my-worker",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsWorkerRole",
  "containerDefinitions": [
    {
      "name": "worker",
      "image": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/my-worker:v1.0.0",
      "essential": true,
      "command": ["python", "-m", "worker.main"],
      "environment": [
        { "name": "QUEUE_URL", "value": "https://sqs.REGION.amazonaws.com/ACCOUNT_ID/my-queue" }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:my-app/database-url"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-worker",
          "awslogs-region": "REGION",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "readonlyRootFilesystem": true,
      "user": "1000:1000"
    }
  ]
}
```

---

## Terraform Modules

### ECS Cluster

```hcl
# modules/ecs-cluster/main.tf

resource "aws_ecs_cluster" "this" {
  name = var.cluster_name

  setting {
    name  = "containerInsights"
    value = var.container_insights ? "enabled" : "disabled"
  }

  tags = var.tags
}

resource "aws_ecs_cluster_capacity_providers" "this" {
  cluster_name = aws_ecs_cluster.this.name

  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy {
    base              = 1
    weight            = 1
    capacity_provider = "FARGATE"
  }

  default_capacity_provider_strategy {
    weight            = 4
    capacity_provider = "FARGATE_SPOT"
  }
}

# Variables
variable "cluster_name" {
  type        = string
  description = "Name of the ECS cluster"
}

variable "container_insights" {
  type        = bool
  default     = true
  description = "Enable Container Insights"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags to apply to resources"
}

# Outputs
output "cluster_id" {
  value = aws_ecs_cluster.this.id
}

output "cluster_arn" {
  value = aws_ecs_cluster.this.arn
}

output "cluster_name" {
  value = aws_ecs_cluster.this.name
}
```

### ECS Service

```hcl
# modules/ecs-service/main.tf

resource "aws_ecs_service" "this" {
  name            = var.service_name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = var.security_group_ids
    assign_public_ip = false
  }

  dynamic "load_balancer" {
    for_each = var.target_group_arn != null ? [1] : []
    content {
      target_group_arn = var.target_group_arn
      container_name   = var.container_name
      container_port   = var.container_port
    }
  }

  deployment_configuration {
    minimum_healthy_percent = 100
    maximum_percent         = 200
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  health_check_grace_period_seconds = var.health_check_grace_period

  lifecycle {
    ignore_changes = [desired_count]
  }

  tags = var.tags
}

resource "aws_ecs_task_definition" "this" {
  family                   = var.service_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name      = var.container_name
      image     = var.container_image
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          protocol      = "tcp"
        }
      ]

      environment = var.environment_variables
      secrets     = var.secrets

      healthCheck = var.health_check

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = var.log_group_name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }

      linuxParameters = {
        initProcessEnabled = true
      }

      readonlyRootFilesystem = true
      user                   = "1000:1000"
    }
  ])

  tags = var.tags
}

# Auto Scaling
resource "aws_appautoscaling_target" "this" {
  count = var.enable_autoscaling ? 1 : 0

  max_capacity       = var.max_capacity
  min_capacity       = var.min_capacity
  resource_id        = "service/${var.cluster_name}/${aws_ecs_service.this.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "cpu" {
  count = var.enable_autoscaling ? 1 : 0

  name               = "${var.service_name}-cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.this[0].resource_id
  scalable_dimension = aws_appautoscaling_target.this[0].scalable_dimension
  service_namespace  = aws_appautoscaling_target.this[0].service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = var.cpu_target_value
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}
```

### IAM Roles

```hcl
# modules/ecs-iam/main.tf

# Task Execution Role (for ECS agent)
resource "aws_iam_role" "execution" {
  name = "${var.name}-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "execution" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "execution_secrets" {
  name = "${var.name}-execution-secrets"
  role = aws_iam_role.execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = var.secrets_arns
      },
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameters"
        ]
        Resource = var.ssm_parameter_arns
      }
    ]
  })
}

# Task Role (for application)
resource "aws_iam_role" "task" {
  name = "${var.name}-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "task" {
  name = "${var.name}-task-policy"
  role = aws_iam_role.task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = var.task_policy_statements
  })
}

# Outputs
output "execution_role_arn" {
  value = aws_iam_role.execution.arn
}

output "task_role_arn" {
  value = aws_iam_role.task.arn
}
```

---

## CloudFormation Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: ECS Fargate Service

Parameters:
  ClusterName:
    Type: String
  ServiceName:
    Type: String
  ContainerImage:
    Type: String
  DesiredCount:
    Type: Number
    Default: 2
  ContainerPort:
    Type: Number
    Default: 8080
  Cpu:
    Type: String
    Default: '512'
  Memory:
    Type: String
    Default: '1024'
  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
  SecurityGroupIds:
    Type: List<AWS::EC2::SecurityGroup::Id>
  TargetGroupArn:
    Type: String

Resources:
  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: !Ref ServiceName
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      Cpu: !Ref Cpu
      Memory: !Ref Memory
      ExecutionRoleArn: !GetAtt ExecutionRole.Arn
      TaskRoleArn: !GetAtt TaskRole.Arn
      ContainerDefinitions:
        - Name: app
          Image: !Ref ContainerImage
          Essential: true
          PortMappings:
            - ContainerPort: !Ref ContainerPort
              Protocol: tcp
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: ecs
          LinuxParameters:
            InitProcessEnabled: true
          ReadonlyRootFilesystem: true
          User: '1000:1000'

  Service:
    Type: AWS::ECS::Service
    Properties:
      Cluster: !Ref ClusterName
      ServiceName: !Ref ServiceName
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: !Ref DesiredCount
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets: !Ref SubnetIds
          SecurityGroups: !Ref SecurityGroupIds
          AssignPublicIp: DISABLED
      LoadBalancers:
        - TargetGroupArn: !Ref TargetGroupArn
          ContainerName: app
          ContainerPort: !Ref ContainerPort
      DeploymentConfiguration:
        MinimumHealthyPercent: 100
        MaximumPercent: 200
        DeploymentCircuitBreaker:
          Enable: true
          Rollback: true

  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub /ecs/${ServiceName}
      RetentionInDays: 30

  ExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

  TaskRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole

Outputs:
  ServiceArn:
    Value: !Ref Service
  TaskDefinitionArn:
    Value: !Ref TaskDefinition
```

---

*AWS EC2 & ECS Templates | faion-infrastructure-engineer*
