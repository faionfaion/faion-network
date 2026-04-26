# Agent Integration — AWS Architecture Foundations

## When to use
- Bootstrapping a new AWS Organization, OU layout, and Control Tower / Landing Zone Accelerator (LZA) baseline.
- Auditing an existing account against the Well-Architected Framework (6 pillars) before a major release or compliance review.
- Designing the foundational VPC/IAM/KMS/CloudTrail layout for a workload that will live multi-account, multi-AZ.
- Producing reviewable Terraform/CloudFormation modules that encode security, logging, and network defaults.
- Cost optimization sweeps (RIs, Savings Plans, NAT consolidation, S3 lifecycle, right-sizing).

## When NOT to use
- A single-account hobby project — Control Tower/LZA overhead is wasteful.
- Pure application-level decisions (DB schema, framework choice) — use dev skills instead.
- Day-2 incident response — use AIOps / observability methodologies.
- Service-specific deep dives — point at `aws-ec2-ecs/`, `aws-lambda/`, `aws-s3-storage/`, `aws-networking/` siblings.
- Non-AWS clouds — use `gcp-arch-basics/` or Azure equivalents.

## Where it fails / limitations
- AWS console drift: agents can read state via CLI but cannot reliably reconcile manually clicked changes — pair with Config + drift detection.
- Quotas and Service Control Policies vary per account; an agent that succeeds in dev will hit `AccessDenied` or `LimitExceeded` in regulated accounts.
- IAM policy minimization is hard to automate without test workloads; agents tend to over-grant on first pass — require a human-reviewed least-privilege diff.
- Cost-optimization advice goes stale when AWS announces new instance families or pricing — verify recommendations against current AWS pricing API.
- Landing Zone Accelerator changes between minor versions; pinning to a known LZA release matters more than always-latest.

## Agentic workflow
Drive AWS foundation work as a pipeline: discovery (read-only Organizations + Config + IAM dump) → gap analysis against Well-Architected → emit Terraform plan or CloudFormation StackSet diff → human review → apply via IaC pipeline (never `aws ... create` from the agent in prod). Subagents specialize: one for security pillar, one for cost, one for reliability — converge their findings into a single report. Always run agents under a read-only role for assessment and only switch to a write role after explicit approval.

### Recommended subagents
- `faion-sdd-executor-agent` — drives Terraform/CFN module work with quality gates and review cycle.
- `password-scrubber-agent` — sanitizes any captured account IDs, ARNs, and credentials before persisting reports.
- Custom `aws-wafr-reviewer` (compose locally) — reads CloudTrail/Config/IAM and scores against the 6 pillars.
- Custom `aws-cost-auditor` — pulls Cost Explorer + Trusted Advisor and proposes RI/Savings Plan moves.

### Prompt pattern
"You are an AWS Well-Architected reviewer. Using read-only access via `aws sts get-caller-identity` first, dump Organizations OU tree, IAM Identity Center assignments, CloudTrail org-trail status, and Config aggregator state. Score each of the 6 pillars 1-5 with concrete evidence (resource ARNs, policy snippets). Return JSON: `{pillar, score, findings:[{severity, evidence, remediation_terraform}]}`. Do not call any mutating API."

"Generate a Terraform module for a 3-tier VPC across 3 AZs in eu-central-1, one NAT GW per AZ, VPC Flow Logs to a central log-archive S3 bucket via Kinesis Firehose, default SG locked down. Output `vpc.tf`, `variables.tf`, `outputs.tf` only — no `terraform apply`."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `aws` CLI v2 | Read state, scripted ops | https://docs.aws.amazon.com/cli/ |
| `aws-vault` | Local credential isolation per profile | https://github.com/99designs/aws-vault |
| `terraform` + `hashicorp/aws` | IaC for AWS resources | https://registry.terraform.io/providers/hashicorp/aws/latest |
| `awscdk` (TypeScript/Python) | Higher-level IaC | https://docs.aws.amazon.com/cdk/ |
| `Steampipe` (`aws` plugin) | SQL queries over AWS APIs for audits | https://steampipe.io/plugins/turbot/aws |
| `Prowler` | Multi-framework AWS security & WAFR audit | https://github.com/prowler-cloud/prowler |
| `cloudquery` | AWS state to Postgres for analytics | https://www.cloudquery.io/ |
| `aws-nuke` | Destroy non-prod accounts cleanly | https://github.com/rebuy-de/aws-nuke |
| `cfn-lint` / `cfn-guard` | CloudFormation linting + policy | https://github.com/aws-cloudformation/cfn-lint |
| `tfsec` / `checkov` / `kics` | IaC security scan | https://aquasecurity.github.io/tfsec/ |
| `infracost` | Cost-impact diff on Terraform plans | https://www.infracost.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| AWS Control Tower | Native AWS | Partial — UI-driven; LZA preferred for IaC | Bootstraps multi-account; bulk changes via Account Factory for Terraform (AFT) |
| Landing Zone Accelerator (LZA) | OSS (AWS) | Yes — config-driven YAML | Codify org policy, SCPs, network, logging |
| AWS Organizations + SCPs | Native AWS | Yes via API/Terraform | Apply guardrails at OU |
| IAM Identity Center | Native AWS | Yes via SCIM + API | Federate with Okta/Entra/Google Workspace |
| AWS Security Hub | Native AWS | Yes via API | Aggregates GuardDuty/Inspector/Macie/Config findings |
| AWS Config | Native AWS | Yes | Resource state + drift; required for WAFR |
| CloudTrail (org trail) | Native AWS | Yes | Send to log-archive account |
| Wiz / Orca / Lacework | SaaS CNAPP | Yes via API | Cross-account security posture beyond Security Hub |
| Vantage / CloudHealth / Cloudability | SaaS FinOps | Yes via API | Use when Cost Explorer is too thin |
| `cloud-custodian` (c7n) | OSS | Yes — YAML policies | Policy-as-code remediation, scheduled actions |

## Templates & scripts
See `templates.md` for Well-Architected review and IaC scaffolds. Inline read-only audit script (run with read-only role):

```bash
#!/usr/bin/env bash
# aws-foundations-audit.sh — read-only WAFR signal collection
set -euo pipefail
OUT=${1:-./audit-$(date +%Y%m%d)}
mkdir -p "$OUT"
aws organizations describe-organization > "$OUT/org.json"
aws organizations list-roots --query 'Roots[0].Id' --output text \
  | xargs -I{} aws organizations list-organizational-units-for-parent --parent-id {} > "$OUT/ous.json"
aws cloudtrail describe-trails --include-shadow-trails > "$OUT/cloudtrail.json"
aws configservice describe-configuration-aggregators > "$OUT/config-aggregators.json"
aws securityhub get-enabled-standards > "$OUT/securityhub-standards.json" || true
aws guardduty list-detectors > "$OUT/guardduty.json" || true
aws iam get-account-password-policy > "$OUT/iam-password-policy.json" || true
aws iam list-account-aliases > "$OUT/iam-aliases.json"
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock,FlowLogs:Tags}' > "$OUT/vpcs.json"
aws ec2 describe-flow-logs > "$OUT/flow-logs.json"
aws s3api list-buckets > "$OUT/s3-buckets.json"
aws kms list-aliases > "$OUT/kms-aliases.json"
echo "Audit complete: $OUT"
```

## Best practices
- One AWS account per workload-environment pair (prod-app-A, dev-app-A) — not per team or per microservice.
- Keep the management account empty of workloads; use it only for Organizations, billing, and IAM Identity Center.
- Org-level CloudTrail with log file validation, KMS encryption, and an immutable S3 destination in the log-archive account; deny `s3:DeleteObject` via bucket policy + Object Lock.
- VPC Flow Logs at REJECT or ALL to S3 (not CloudWatch — cheaper at scale).
- Default to private subnets for workloads; internet only via NAT GW or VPC endpoints (gateway endpoints for S3/DynamoDB are free — always enable).
- Enforce TLS 1.2+ on ALBs (`alb.idle_timeout`, `min_tls_version`), require IMDSv2 on all EC2 (`MetadataOptions.HttpTokens=required`).
- IAM Identity Center as the only human entry point; root account locked, MFA-required, contact-only credentials in a sealed envelope.
- Tag everything with `cost-center`, `owner`, `env`, `data-class` — enforce via SCP `aws:RequestTag/...` or `cloud-custodian`.
- Pin Terraform provider versions; `terraform.lock.hcl` committed.
- Never run `aws ... create-*` from an agent in prod without an IaC plan + human approve step.

## AI-agent gotchas
- Agents that see "no MFA" on a service account often suggest enabling it — service accounts (programmatic users / roles) shouldn't have MFA; that's only humans. Sanity-check before applying.
- Region defaults: agents that omit `--region` in scripts will silently use whatever the env defaults to and can pollute the wrong region — always require explicit region in generated code.
- Account ID and ARN leakage: scrub before posting reports anywhere outside the account; use `password-scrubber-agent` style filter.
- Wildcard cleanup: `aws-nuke`-style operations and `aws s3 rm --recursive` MUST be human-gated; LLMs underestimate blast radius.
- Cost Explorer data is delayed up to 24h; agents drawing conclusions from "today's spend" will mislead — anchor on rolling 7- or 30-day windows.
- LLMs frequently confuse Control Tower guardrails with SCPs — they overlap but are not the same; verify which layer enforces a given control.
- IAM policies generated by LLMs trend toward permissive `Resource: "*"` — require an automated tightening pass with `iam-policy-simulator` or `Access Analyzer`.

## References
- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Organizing Your AWS Environment Using Multiple Accounts: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html
- Landing Zone Accelerator on AWS: https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/
- Account Factory for Terraform (AFT): https://docs.aws.amazon.com/controltower/latest/userguide/aft-overview.html
- Prowler: https://github.com/prowler-cloud/prowler
- Steampipe AWS plugin: https://hub.steampipe.io/plugins/turbot/aws
- Cloud Custodian: https://cloudcustodian.io/
- AWS Security Reference Architecture: https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/
