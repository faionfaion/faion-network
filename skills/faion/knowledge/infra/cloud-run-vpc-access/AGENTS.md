# Cloud Run Vpc Access

## Summary

**One-sentence:** Cloud Run networking: Direct VPC egress vs Serverless VPC connectors, ingress controls, multi-container sidecars (Cloud SQL proxy, OpenTelemetry), Private Service Connect, and firewall configuration.

**One-paragraph:** Cloud Run services connect to private VPC resources via Direct VPC egress (preferred) or Serverless VPC Access connectors. Direct VPC egress provides 2x throughput, lower cost, and lower latency compared to connectors. Multi-container support (up to 10 containers per instance) enables sidecar patterns for database proxies, observability agents, and security middleware.

**Ефективно для:**

- Cloud Run сервіс, що звертається до Cloud SQL / Memorystore у VPC.
- Доступ до on-prem ресурсів через VPN/Interconnect із Cloud Run.
- Direct VPC egress (без Serverless VPC Access connector) у gen2-сервісах.
- Privately-routed inbound (internal-only) через Internal HTTPS LB.

## Applies If (ALL must hold)

- Connecting a Cloud Run service to private Cloud SQL, AlloyDB, or Memorystore (Redis).
- Reaching internal GCP services or on-premises resources via VPN/Interconnect.
- Adding Cloud SQL Proxy sidecar to avoid IAP or public Cloud SQL IP exposure.
- Adding OpenTelemetry collector sidecar for metrics and tracing.
- Migrating from Serverless VPC Access connectors to Direct VPC egress.
- Restricting Cloud Run ingress to internal load balancer only.

## Skip If (ANY kills it)

- Service only calls public APIs — no VPC integration needed.
- GKE workloads — use Workload Identity + VPC-native cluster.
- Cloud Run Job that doesn't need VPC reachability.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target private resource | Cloud SQL / Memorystore / on-prem | team |
| VPC + subnet | existing or to-create | network owner |
| Egress preference | all-traffic vs private-ranges-only | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-networking-vpc]] | Sibling methodology that supplies context required here. |
| [[gcp-cloud-run-serverless]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-config` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-cloud-run-vpc-access.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cloud-run-vpc-access.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cloud-run-vpc-access.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-networking-vpc]]
- [[gcp-cloud-run-serverless]]
- [[cloud-run-deployment]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. cloud-run-vpc-access vs an adjacent sibling).
