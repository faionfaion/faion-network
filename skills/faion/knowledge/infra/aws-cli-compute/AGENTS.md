# AWS CLI Compute and Storage Operations (EC2 S3 Lambda)

## Summary

**One-sentence:** Produces shell scripts using AWS CLI for EC2 / S3 / Lambda lifecycle operations with explicit profile handling and idempotent wait conditions.

**One-paragraph:** Reference shell scripts using AWS CLI commands covering EC2 instance lifecycle (launch / stop / terminate / AMI), S3 object and bucket management (lifecycle, versioning, sync), Lambda function management (deploy, invoke, alias), and shared credential configuration patterns. Scripts default to explicit `--profile` + region, use `aws ec2 wait` instead of sleep, and emit JSON for downstream pipeline consumption rather than human-formatted text.

**Ефективно для:**

- scripting EC2 lifecycle: launch / stop / terminate / AMI workflows.
- managing S3 bucket lifecycle, versioning, policies, sync operations.
- deploying / invoking Lambda functions + layers + aliases.
- setting up local AWS CLI profiles + env-var auth patterns.

## Applies If (ALL must hold)

- Operator has AWS CLI installed and credentials configured for the target account.
- Scripted operation is idempotent or the script handles the not-idempotent path explicitly.
- Output is consumable by downstream automation (JSON, not human-formatted text).
- Operation is one of: EC2 lifecycle, S3 bucket / object management, Lambda function ops.

## Skip If (ANY kills it)

- Standing up multi-resource infrastructure — use CloudFormation or Terraform instead; see aws-cfn-terraform-templates.
- Container workloads (ECS, EKS, ECR) — see aws-cli-containers-iac for those commands.
- CI/CD automation at scale — wire CLI calls through GitHub Actions or GitLab CI rather than bare shell scripts.
- Operation requires cross-account assume-role with MFA — script must not embed credentials.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| AWS CLI installed | v2+ | local / CI |
| Named profile + region | env / cfg file | operator |
| Target account id | numeric | platform |
| Operation scope (one of EC2 / S3 / Lambda) | string | task spec |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/aws-foundations` | account + region setup assumed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-operation` | haiku | Map intent to specific CLI command sequence |
| `compose-script` | sonnet | Wire credentials + waits + JSON output |
| `dry-run-review` | haiku | Linter pass over the script |

## Templates

| File | Purpose |
|------|---------|
| `templates/ec2-launch.sh` | EC2 launch + tag + wait shell snippet |
| `templates/s3-sync.sh` | S3 sync with retention pattern |
| `templates/lambda-deploy.sh` | Lambda zip + update-function-code skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-cli-compute.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[aws-cfn-terraform-templates]]
- [[aws-cli-containers-iac]]
- [[aws-foundations]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the AWS CLI Compute and Storage Operations (EC2 S3 Lambda) methodology when in doubt about scope or fit.
