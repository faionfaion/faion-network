# Agent Integration — Cloud Architecture

## When to use
- Drafting Well-Architected reviews for an existing AWS/Azure/GCP workload.
- Authoring Terraform / Bicep / Pulumi modules for landing zones, VPC topology, IAM baselines.
- Cost-optimization sweeps: right-sizing, RIs/Savings Plans, spot, scheduling.
- Multi-region failover design (RTO/RPO targets, DR runbooks).
- Reviewing IaC PRs for security (Zero Trust), tagging, and FinOps compliance.
- Migration assessments (lift-and-shift vs replatform vs refactor) for legacy workloads.

## When NOT to use
- Billing reconciliation / contract negotiations — agent has no provider context.
- Real-time incident triage in cloud — needs live console + telemetry access.
- Region/AZ failover decisions during an outage — human SRE only.
- Procurement of enterprise agreements, RIs, or commit deals.
- Compliance attestations (SOC2/HIPAA reports) — agent drafts evidence, never signs.

## Where it fails / limitations
- Service catalogs change monthly; agent emits deprecated services (e.g., proposing AWS App Mesh in 2025).
- Cross-cloud abstractions (Crossplane, Terraform multi-provider) suffer from outdated provider versions.
- Cost numbers are stale — never trust dollar figures the agent emits without reconfirming via Pricing API.
- IAM least-privilege is consistently too permissive; trust, not just grant, must be reviewed.
- Region availability for newer services (e.g., Bedrock, Vertex models) often wrong.
- Network design for hybrid/edge often missing latency math; agent draws diagrams without RTT budget.

## Agentic workflow
Use a cloud-architect to produce the Well-Architected scorecard + reference architecture, then an iac-coder to materialize Terraform/Bicep/Pulumi from the scorecard, then a security-reviewer (CIS/NIST + cloud-native scanners), then a finops-reviewer that calls the Pricing API. Every plan must include an explicit DR objective (RTO/RPO) and a tagging policy. Use Opus for architect + finops; Sonnet for IaC + reviewers.

### Recommended subagents
- `cloud-architect` (Opus) — Well-Architected pillars, region strategy, landing-zone shape.
- `iac-coder` (Sonnet) — Terraform/Bicep/Pulumi modules; OpenTofu compatible.
- `cloud-security-reviewer` (Sonnet) — IAM least-privilege, Zero Trust, CIS benchmarks.
- `finops-reviewer` (Opus) — sizing, commitment plan, savings rec; uses Pricing API.
- `dr-planner` (Sonnet) — RTO/RPO design, runbook, game-day script.

### Prompt pattern
```
You are cloud-architect. Workload: <stack>, traffic: 5k rps p95 200ms,
data: 4TB regulated (GDPR), team: 2 SREs. Pick AWS/Azure/GCP with rationale.
Output Well-Architected scorecard (6 pillars), reference arch, and 3 cost-savings
recommendations with stated assumptions. Pin provider service versions/APIs.
```

```
You are cloud-security-reviewer. Diff: <terraform plan>. Reject if:
- IAM policies use "*" on Resource without conditions,
- S3/Storage buckets without encryption + public-access-block,
- security groups 0.0.0.0/0 on non-LB resources,
- missing CloudTrail/Activity Log,
- KMS keys without rotation,
- secrets in tfvars instead of Secrets Manager / Key Vault.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `aws` / `az` / `gcloud` | Provider control planes | aws.amazon.com/cli, learn.microsoft.com/cli/azure, cloud.google.com/sdk |
| `terraform` / `tofu` | IaC plan/apply | terraform.io / opentofu.org |
| `pulumi` | IaC in Python/TS/Go | pulumi.com |
| `bicep` | Azure-native IaC | learn.microsoft.com/azure/azure-resource-manager/bicep/ |
| `cdk` (AWS / CDKTF) | High-level IaC | docs.aws.amazon.com/cdk/ |
| `crossplane` (`kubectl-crossplane`) | Cloud resources via K8s CRDs | crossplane.io |
| `infracost` | $$ cost diff in CI | infracost.io |
| `tflint` / `tfsec` / `checkov` / `kics` | IaC lint + security | tflint.dev / aquasec.com / checkov.io |
| `prowler` / `scout-suite` | Cloud config audit | prowler.com / github.com/nccgroup/ScoutSuite |
| `cloudquery` / `steampipe` | SQL over cloud assets | cloudquery.io / steampipe.io |
| `aws cur2` / `azure cost-mgmt` / `gcp billing` | Spend exports | provider docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Terraform Cloud / Spacelift / env0 | SaaS | Yes | Plan/apply with policy gates; agent edits modules. |
| AWS Control Tower / Azure CAF / GCP CFT | SaaS | Partial | Landing zones; agent extends, not creates from scratch. |
| Vantage / CloudHealth / Cloudability / Apptio | SaaS | Partial | FinOps; agent reads exports, doesn't replace analyst. |
| Wiz / Lacework / Prisma Cloud / Defender | SaaS | Partial | CSPM; agent triages findings. |
| HashiCorp Vault | SaaS + OSS | Yes | Secrets; agent emits policies + auth methods. |
| External Secrets Operator | OSS | Yes | K8s ↔ cloud secret stores. |
| Cloudflare / Akamai / Fastly | SaaS | Yes | Edge + WAF; APIs are agent-friendly. |
| Datadog / New Relic / Dynatrace / Grafana Cloud | SaaS | Yes | Observability; agent edits dashboards-as-code. |
| Snyk / Aqua / GitHub Advanced Security | SaaS | Yes | Supply chain; agent wires CI checks. |

## Templates & scripts
See `templates.md` for landing-zone modules, hub-spoke VPC, and DR templates. Inline guardrail script for IaC PRs:

```bash
#!/usr/bin/env bash
# cloud-iac-gate.sh
set -euo pipefail
terraform fmt -check -recursive
terraform validate
tflint --recursive
tfsec . --soft-fail=false
checkov -d . --quiet --compact
infracost diff --path . --format=table --terraform-plan-flags='-lock=false' \
  --usage-file infracost-usage.yml
# enforce tags
grep -RIn 'tags\s*=' . | grep -v 'CostCenter' && {
  echo "ERROR: missing CostCenter tag"; exit 1; } || true
# require CMK encryption on data stores
grep -RIn 'aws_s3_bucket"\|aws_rds_cluster"\|aws_dynamodb_table"' . | while read -r line; do
  f=${line%%:*}; grep -q 'kms_key_id\|server_side_encryption' "$f" || {
    echo "ERROR: data store without KMS in $f"; exit 1; }
done
echo "IaC gate OK"
```

## Best practices
- Force the agent to declare RTO/RPO BEFORE proposing architecture; otherwise design defaults to single-region.
- Always emit a tagging schema (Environment, Team, CostCenter, Owner, Lifecycle); reject IaC without it.
- Demand IAM least-privilege written as deny-by-default policy + scoped allows; "PowerUser" is a smell.
- Treat CIS / Well-Architected gaps as regression tests — re-run on every IaC PR.
- For multi-region: agent must specify replication SLA, conflict resolution (LWW vs CRDT vs custom), and failover drill cadence.
- Pin Terraform / provider versions per module; agents drift across major releases (AWS provider 5.x → 6.x).
- Use OpenTofu in regulated envs to avoid HCL license risk; agent should template both syntaxes.
- When the agent proposes serverless, demand cold-start budget + warmup plan before approval.

## AI-agent gotchas
- Agent emits IaM policies with `Action: ["*"]` and "least privilege" in the comment — read the JSON, not the prose.
- Region picks ignore data-residency; flag GDPR / FedRAMP and re-prompt.
- VPC CIDR overlaps when extending hub-spoke without listing existing ranges.
- Cost figures unverified — always require `infracost` output, not the agent's mental math.
- Human checkpoint REQUIRED before: applying Terraform to prod, IAM root changes, KMS key deletions, route-table edits, public-cloud egress changes, region failover.
- Spot/preemptible used for stateful workloads — agent doesn't know which jobs are interruptible.
- Backup/DR runbook generated but never tested; demand a game-day in the same PR.
- Models confuse encryption-at-rest with encryption-in-transit; require both, listed separately.

## References
- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/.
- Azure Well-Architected Framework: https://learn.microsoft.com/azure/well-architected/.
- Google Cloud Architecture Framework: https://cloud.google.com/architecture/framework.
- NIST SP 800-207 Zero Trust.
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks.
- FinOps Foundation + FOCUS spec: https://www.finops.org/, https://focus.finops.org/.
- "Cloud Native Patterns", Cornelia Davis.
- "Cloud FinOps", J.R. Storment & Mike Fuller.
