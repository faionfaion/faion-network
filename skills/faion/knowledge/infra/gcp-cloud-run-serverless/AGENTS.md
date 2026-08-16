# Gcp Cloud Run Serverless

## Summary

**One-sentence:** GCP Cloud Run and Cloud Functions Gen2 best practices: secure service deployment, VPC connector, blue-green traffic splitting, Secret Manager integration, and Cloud Run security/setup checklists.

**One-paragraph:** Cloud Run and Cloud Functions Gen2 best practices: deploy with a dedicated service account, Secret Manager secrets, VPC connector for private resource access, min-instances for production cold-start elimination, blue-green traffic splitting for safe rollouts, and Binary Authorization for image trust.

**Ефективно для:**

- HTTP/gRPC stateless API з автоскейлом 0→N за запитами.
- Event-driven worker через Pub/Sub push-subscription.
- Microservice patterns: концентрація бізнес-логіки + мінімальний runtime.
- Когнітивна навігація між services / jobs / generation gen1↔gen2.

## Applies If (ALL must hold)

- Deploying a containerized stateless API or web application on Cloud Run.
- Setting up Cloud Functions Gen2 for HTTP triggers or Pub/Sub event processing.
- Configuring blue-green or canary releases for a Cloud Run service.
- Adding VPC connector to reach private Cloud SQL or internal services.
- Auditing Cloud Run service security configuration.

## Skip If (ANY kills it)

- Long-running batch (>60 min) — use Cloud Run Jobs.
- Stateful workload requiring persistent disk.
- Custom kernel / privileged container needs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Application image | OCI image in Artifact Registry | build pipeline |
| Traffic shape | concurrency / RPS estimate | team |
| Cold-start tolerance | min-instances policy | product owner |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[gcp-networking-vpc]] | Sibling methodology that supplies context required here. |
| [[gcp-security-iam]] | Sibling methodology that supplies context required here. |

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
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-cloud-run-serverless.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-cloud-run-serverless.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-cloud-run-serverless.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[gcp-networking-vpc]]
- [[gcp-security-iam]]
- [[gcp-compute-gke]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-cloud-run-serverless vs an adjacent sibling).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/gcp-cloud-run-serverless.yaml`

```yaml
name: example-name
image: example-image
min_instances: 0  # int|number|string
max_instances: 0  # int|number|string
concurrency: 0  # int|number|string
cpu: example-cpu
memory: 0  # int|number|string
```

### `templates/_smoke-test.yaml`

```yaml
# minimum viable filled-in example of gcp-cloud-run-serverless.yaml
name: example-name
image: example-image
min_instances: 1
max_instances: 1
concurrency: 1
cpu: example-cpu
memory: 1
```
