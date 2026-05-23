---
slug: security-architecture
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Zero-Trust, defence-in-depth architecture spec: identity + authZ matrix, secrets handling, OWASP ASVS L2 controls, threat-model, and incident-response gates. Output: security spec + STRIDE diagram.
content_id: "fcfb7118c08f2a5a"
complexity: deep
produces: spec
est_tokens: 5000
tags: [security, zero-trust, owasp-asvs, threat-modeling, stride]
---
# Security Architecture

## Summary

**One-sentence:** Zero-Trust, defence-in-depth architecture spec: identity + authZ matrix, secrets handling, OWASP ASVS L2 controls, threat-model, and incident-response gates. Output: security spec + STRIDE diagram.

**One-paragraph:** Zero-Trust, defence-in-depth architecture spec: identity + authZ matrix, secrets handling, OWASP ASVS L2 controls, threat-model, and incident-response gates. Output: security spec + STRIDE diagram. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Service handles authentication, multi-tenant data, payment, PHI, or other regulated assets.
- External attack surface (public APIs, file upload, admin portals) exists.
- Compliance (SOC2 / HIPAA / PCI / GDPR) demands documented controls.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Service handles authentication, multi-tenant data, payment, PHI, or other regulated assets.
- External attack surface (public APIs, file upload, admin portals) exists.
- Compliance (SOC2 / HIPAA / PCI / GDPR) demands documented controls.

## Skip If (ANY kills it)

- Throwaway prototype with synthetic data, no real users, no public surface.
- Internal-only tool behind corporate SSO + WireGuard, no regulated data.
- Existing security spec ≤6 months old with no material context change.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Asset inventory (data classes + flows) | table + diagram | team / DPO |
| User / tenant role matrix | table | PM / sec |
| Existing IAM provider (OAuth/OIDC / SSO) | config | ops |
| Compliance scope (SOC2 / HIPAA / PCI / GDPR) | doc | legal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo/dev/software-architect/quality-attributes]] | Security scenarios live as ISO-25010 security NFRs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `threat-model` | opus | STRIDE walkthrough requires strongest judgement. |
| `authz-matrix` | sonnet | Bounded role × resource × operation enumeration. |
| `secrets-handling-plan` | sonnet | Pick provider + rotation + scoping rules. |
| `control-checklist` | haiku | Apply OWASP ASVS L2 checklist mechanically. |

## Templates

| File | Purpose |
|------|---------|
| `templates/threat-model-stride.md` | STRIDE threat-model skeleton + asset-attacker-control table. |
| `templates/authz-matrix.json` | Authorisation matrix (role × resource × operation). |
| `templates/security-spec.md` | Spec skeleton tying threat-model + controls + ASVS coverage. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-architecture.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[solo/dev/software-architect/quality-attributes]]
- [[solo/dev/software-architect/system-design-process]]
- [[solo/dev/software-architect/serverless-architecture-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (assets, roles, IAM provider, compliance scope)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
