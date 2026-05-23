# Docker

## Summary

**One-sentence:** Production-grade Docker containerization: image building, optimization, networking, storage, security hardening, and deployment best practices for 2025-2026.

**One-paragraph:** Production-Grade Container Development and Deployment (2025-2026). Docker containerization packages applications with dependencies into portable units. This methodology covers production-grade Docker infrastructure: image building, optimization, networking, storage, security hardening, and deployment best practices.

**Ефективно для:**

- Multi-stage Dockerfile для compiled-мов (Go, Java) з мінімальним runtime-шаром.
- Non-root container з обов'язковим USER + HEALTHCHECK для prod.
- BuildKit cache mounts для пришвидшення pip/npm/apt у CI.
- .dockerignore + layer-order оптимізації для cache-hit rate >80%.
- Distroless / alpine base для production з SBOM + scan.

## Applies If (ALL must hold)

- Packaging applications with all dependencies into portable, reproducible units.
- Building multi-stage CI/CD pipelines where images are built, scanned, signed, and promoted.
- Running multi-service stacks locally with Docker Compose during development.
- Deploying stateless workloads to any container-compatible runtime (ECS, Cloud Run, K8s).
- Enforcing security baselines: non-root users, read-only filesystems, capability dropping.

## Skip If (ANY kills it)

- Buildpacks-based deployment with no Dockerfile.
- Pre-built vendor images — no custom build step needed.
- Source-to-image platforms (e.g. Cloud Run from-source) for one-off prototypes.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Application source code | repo + entrypoint | team |
| Base image policy | approved registry + tag pinning | platform team |
| Vulnerability scanner | Artifact Analysis / Trivy | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cloud-run-jobs]] | Sibling methodology that supplies context required here. |
| [[cloud-run-monitoring]] | Sibling methodology that supplies context required here. |

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
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-docker.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/docker.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[cloud-run-jobs]]
- [[cloud-run-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. docker vs an adjacent sibling).
