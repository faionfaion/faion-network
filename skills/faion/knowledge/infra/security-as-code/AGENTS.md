# Security as Code (Policy as Code)

## Summary

**One-sentence:** Embed security gates as code in every SDLC phase: OPA / Kyverno policies, SAST / SCA / DAST scans wired into CI, signed artifacts, runtime admission control with audit trail.

**One-paragraph:** Security as Code embeds protection mechanisms directly into every phase of the software delivery lifecycle. Instead of treating security as a final checkpoint, DevSecOps integrates security controls — SAST, SCA, DAST, secrets scanning, image signing, admission control, runtime policies — as automated gates in CI/CD and on the cluster. Policy-as-Code (OPA, Kyverno) replaces tribal-knowledge security reviews with machine-evaluable rules. Every gate produces an auditable artifact: scan reports, policy violations, signed attestations. The goal is shift-left: catch problems at PR time, not at the breach.

**Ефективно для:**

- Block PR з критичним CVE через CI-gate замість після-релізного breach.
- Замінити tribal-knowledge security review на OPA/Kyverno policy.
- Sign image + verify в admission controller (SLSA L3 supply-chain).
- Audit trail політик: яку policy порушено + ким + коли + чому.

## Applies If (ALL must hold)

- CI/CD pipeline exists and team controls it (not a hosted black-box)
- Compliance framework requires evidence of security controls (SOC2, ISO27001, PCI-DSS)
- Cluster runs Kubernetes with admission controller support (Kyverno, OPA Gatekeeper)
- Engineering culture accepts CI blocking on policy violations (not a 'security suggestion')

## Skip If (ANY kills it)

- Solo developer with one Lambda function — overhead exceeds value; use baseline scanners only
- Vendor SaaS pipeline with no policy hooks — wait for the platform to add hooks or migrate
- Compliance is informal / not audited — policy fatigue without external incentive

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CI/CD pipeline with conditional gates (GitHub Actions / GitLab CI / Jenkins) | workflow files | DevOps lead |
| Kubernetes cluster with admission controller | kube-system access | platform team |
| Container registry + signing infra (cosign / Notary) | registry credentials | platform team |
| Vulnerability database access (Trivy / Snyk / Grype) | scanner config | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[secrets-management]] | No static creds is a prerequisite policy |
| [[ssl-tls-setup]] | TLS posture is one of the policies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `policy_drafting` | sonnet | Bounded Rego/Kyverno synthesis from requirements |
| `waiver_evaluation` | opus | Cross-team tradeoff judgment on exceptions |
| `scanner_config_generation` | haiku | Template fill for Trivy/Semgrep config |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-as-code.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[secrets-management]]
- [[ssl-tls-setup]]
- [[external-secrets-operator-recipe]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
