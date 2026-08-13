# AWS Serverless API (Lambda + API Gateway + DynamoDB + EventBridge)

## Summary

**One-sentence:** Produces a Terraform config for a serverless API: API Gateway HTTP API + Lambda arm64 + X-Ray Active + DynamoDB single-table + EventBridge + SQS DLQ + Step Functions, with throttling + custom domain.

**One-paragraph:** Serverless API pattern eliminates server management, scales to zero, and pays only for invocations. The non-negotiables: API Gateway HTTP API (v2, cheaper + faster than REST v1), Lambda on arm64 (Graviton, ~20% cheaper + faster for Python/Node), X-Ray tracing Active, DynamoDB single-table on-demand, EventBridge for routing, SQS with DLQ for async, Step Functions for multi-step orchestration. CORS explicit allow_origins (not *). Custom domain via ACM. Throttling burst+rate set. Cost saving 60-80% vs always-on containers for variable traffic.

**Ефективно для:**

- REST/GraphQL APIs з variable / spiky traffic.
- Event-driven async processing, tasks <15 min.
- Workloads, що масштабуються до нуля вночі.
- GenAI RAG pipelines на Bedrock — Lambda + API GW + DDB glue.

## Applies If (ALL must hold)

- API request handler completes in < 15 min.
- Variable or spiky traffic (not steady-state high-throughput).
- Stateless per invocation acceptable (state in DDB / external store).

## Skip If (ANY kills it)

- Long-running tasks > 15 min — use Fargate / EKS.
- High-throughput steady-state — containers cheaper above ~80% CPU baseline.
- Complex relational queries — DynamoDB is key-value; use Aurora Serverless v2 instead.
- In-process state / shared memory required.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| API spec | OpenAPI v3 / GraphQL schema | product team |
| Domain + ACM cert | FQDN + cert ARN | DNS / cert-manager |
| DDB access pattern | single-table design (PK + SK + GSI) | data modelling exercise |
| Auth model | Cognito / API key / IAM | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[devops-aws-service-selection]] | Serverless decision lives upstream |
| [[devops-aws-terraform-cicd]] | IaC pipeline owns delivery |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: lambda-arm64-active-xray, http-api-not-rest, cors-explicit, throttling-set, custom-domain, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for serverless config artefact + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: x86-lambda, cors-wildcard, no-throttling, default-execute-api-url | 800 |
| `content/04-procedure.xml` | essential | 5 steps: ddb-design → lambda → api-gw → eventbridge/sqs → step functions | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on workload shape → pattern | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ddb-single-table-design` | opus | Strategic — single-table design is the hardest decision. |
| `compose-terraform` | sonnet | Assemble terraform-aws-modules calls. |
| `set-throttling` | haiku | Mechanical rps math. |

## Templates

| File | Purpose |
|------|---------|
| `templates/main.tf` | Terraform skeleton: Lambda + API Gateway HTTP API + DynamoDB + EventBridge + SQS DLQ |
| `templates/step-function.tf` | Step Functions state machine for multi-step orchestration |
| `templates/_smoke-test.json` | Minimum config artefact used by validate-devops-aws-serverless-api.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-aws-serverless-api.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[devops-aws-service-selection]]
- [[devops-aws-terraform-cicd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when scoping a new serverless API or auditing an existing one.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/main.tf`

```hcl
module "lambda" {
  source        = "terraform-aws-modules/lambda/aws"
  version       = "~> 7.0"
  function_name = "${var.project}-handler"
  handler       = "app.handler"
  runtime       = "python3.12"
  architectures = ["arm64"]
  tracing_mode  = "Active"
  publish       = true
  environment_variables = { TABLE = aws_dynamodb_table.main.name }
}

module "api_gateway" {
  source        = "terraform-aws-modules/apigateway-v2/aws"
  version       = "~> 5.0"
  name          = "${var.project}-http"
  protocol_type = "HTTP"
  cors_configuration = {
    allow_origins = ["https://app.example.com"]
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_headers = ["content-type", "authorization"]
  }
  domain_name = var.domain
  default_route_settings = {
    throttling_burst_limit = 5000
    throttling_rate_limit  = 1000
  }
}

resource "aws_dynamodb_table" "main" {
  name         = "${var.project}-main"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  range_key    = "sk"
  attribute { name = "pk" type = "S" }
  attribute { name = "sk" type = "S" }
  point_in_time_recovery { enabled = true }
}

resource "aws_sqs_queue" "dlq" {
  name = "${var.project}-dlq"
}
```

### `templates/step-function.tf`

```hcl
resource "aws_sfn_state_machine" "main" {
  name     = "${var.project}-orchestrator"
  role_arn = aws_iam_role.sfn.arn
  definition = jsonencode({
    Comment = "Order processing"
    StartAt = "Validate"
    States = {
      Validate = { Type = "Task", Resource = module.lambda.lambda_function_arn, Next = "Process", Retry = [{ ErrorEquals = ["States.ALL"], MaxAttempts = 3 }] }
      Process  = { Type = "Task", Resource = module.lambda.lambda_function_arn, End = true }
    }
  })
}
```

### `templates/_smoke-test.json`

```json
{
  "project": "checkout-api",
  "lambda": {
    "architecture": "arm64",
    "runtime": "python3.12",
    "tracing_mode": "Active",
    "timeout_s": 30
  },
  "api_gateway": {
    "protocol_type": "HTTP",
    "cors_origins": [
      "https://app.example.com"
    ],
    "throttling_burst": 5000,
    "throttling_rate": 1000,
    "custom_domain": "api.example.com"
  },
  "dynamodb": {
    "billing_mode": "PAY_PER_REQUEST",
    "pitr": true
  },
  "dlq": true,
  "step_functions": false
}
```
