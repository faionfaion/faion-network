# AWS CLI Containers Databases IaC Identity Monitoring

## Summary

**One-sentence:** Produces shell scripts using AWS CLI for ECS / EKS / RDS / CloudFormation / IAM / CloudWatch operations with change-set discipline and rollback paths.

**One-paragraph:** Reference shell scripts using AWS CLI covering RDS / Aurora databases, ECS / EKS / ECR container services, CloudFormation stack management with change sets, IAM user / role / policy operations with permission boundaries, and CloudWatch logs / alarms / dashboards. Scripts follow the change-set discipline: create change-set, review diff, then execute — never `update-stack` directly in production. Every IAM mutation is paired with a rollback path.

**Ефективно для:**

- managing RDS / Aurora instances, snapshots, parameter groups via CLI.
- ECS cluster + task definition + service + ECR image lifecycle.
- EKS cluster creation, node-group scaling, add-on management.
- CloudFormation stack create/update з change sets + output extraction.

## Applies If (ALL must hold)

- Operator has AWS CLI installed and credentials configured for the target account.
- Operation is one of: ECS / EKS / ECR, CloudFormation stack, IAM, CloudWatch logs / alarms / dashboards.
- Change-set discipline applies to CloudFormation: create-change-set + describe + execute.
- IAM mutations are paired with an explicit rollback path.

## Skip If (ANY kills it)

- EC2, S3, and Lambda operations — see aws-cli-compute for those commands.
- Repeatable multi-resource deployments — use templates from aws-cfn-terraform-templates instead.
- Production IAM changes without peer review — IAM modifications are high-risk; use IaC with version control.
- Cross-account assume-role with MFA — script must not embed credentials.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| AWS CLI installed | v2+ | local / CI |
| Named profile + region | env / cfg file | operator |
| Stack / cluster / role name | string | task spec |
| Rollback plan | Markdown | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/aws-foundations` | account + region setup assumed |
| `pro/infra/devops-engineer/aws-cli-compute` | sibling CLI methodology |

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
| `compose-change-set` | sonnet | Wire create-change-set + describe + execute |
| `rollback-path-draft` | sonnet | Per-mutation rollback sequence |

## Templates

| File | Purpose |
|------|---------|
| `templates/ecs-service-update.sh` | ECS service rolling update skeleton |
| `templates/cfn-changeset.sh` | CloudFormation change-set + execute skeleton |
| `templates/iam-role.sh` | IAM role + policy attach skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-cli-containers-iac.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[aws-cfn-terraform-templates]]
- [[aws-cli-compute]]
- [[aws-foundations]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the AWS CLI Containers Databases IaC Identity Monitoring methodology when in doubt about scope or fit.
