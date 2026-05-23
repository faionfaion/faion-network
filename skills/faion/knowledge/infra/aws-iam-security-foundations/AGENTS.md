# AWS IAM Security Foundations

## Summary

**One-sentence:** Baseline IAM hygiene: root account hardened, CloudTrail org-wide multi-region, GuardDuty + Security Hub enabled, password policy + MFA + access-key rotation policy, AWS Config rules pinned to CIS baseline.

**One-paragraph:** Baseline IAM hygiene: root account hardened, CloudTrail org-wide multi-region, GuardDuty + Security Hub enabled, password policy + MFA + access-key rotation policy, AWS Config rules pinned to CIS baseline. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Account is new OR has not been baselined against CIS AWS Benchmark in last 12 months.
- Named security-lead can sign off on baseline.
- AWS Organizations is in use (or will be) for multi-account management.

## Skip If (ANY kills it)

- Account is already CIS-compliant and externally audited within the last 12 months.
- Account is throwaway sandbox with no production exposure.
- Team has a mature security baseline pipeline (Control Tower + Security Lake) — use that.

**Ефективно для:**

- Нові AWS-акаунти при onboarding (security baseline day-0).
- Команди що готуються до SOC2 / ISO27001 / PCI аудиту.
- Org-level рішення з ≥ 3 акаунтами під AWS Organizations.
- Аудит існуючої posture після інциденту.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-iam-security-foundations.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
