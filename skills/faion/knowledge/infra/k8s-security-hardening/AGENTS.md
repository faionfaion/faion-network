# Kubernetes Security Hardening

## Summary

**One-sentence:** Pod-and-namespace hardening config: PodSecurity Admission (Restricted), NetworkPolicy default-deny, NoNewPrivileges, dropped capabilities, readOnlyRootFS, image-policy.

**One-paragraph:** Pod-and-namespace hardening config: PodSecurity Admission (Restricted), NetworkPolicy default-deny, NoNewPrivileges, dropped capabilities, readOnlyRootFS, image-policy. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Onboarding a workload to a regulated cluster (PCI / HIPAA / SOC2).
- Migrating a namespace from PodSecurityPolicy to Pod Security Admission.
- Adding default-deny NetworkPolicy to a tenant namespace.
- Closing CIS Kubernetes Benchmark findings.

## Skip If (ANY kills it)

- Throw-away dev cluster where productivity beats security.
- Cluster managed by a vendor that already enforces these controls (verify and skip).

**Ефективно для:**

- Multi-tenant prod cluster.
- Regulated environments (PCI / HIPAA / SOC2).
- Service-mesh-protected services що потребують NetworkPolicy.
- Image-policy enforcement (Kyverno / Gatekeeper).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Kubernetes 1.25+ (PodSecurity Admission) | cluster | platform team |
| NetworkPolicy-capable CNI (Calico / Cilium) | cluster | platform team |
| Policy engine (Kyverno / OPA Gatekeeper) | addon | security team |
| Image signer / scanner (Cosign / Trivy) | tools | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-basics` | Baseline manifest conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Mechanical template fill from prerequisites table. |
| `populate-policy` | sonnet | Per-clause translation into config fields with judgment. |
| `review-breach-cases` | opus | Cross-engagement risk + failure-mode synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | Config skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-k8s-security-hardening.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[k8s-basics]]
- [[k8s-deployment-workloads]]
- [[gcp-security-iam]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
