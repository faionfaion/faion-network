# AWS Infra Prompt Library

## Summary

**One-sentence:** Curated, versioned, owner-signed prompt library for AI-assisted AWS IaC work (Terraform, Cloud Run, ECS, IAM) with required guardrails (no-secret-leak, source-of-truth pinning, idempotence checks) per prompt class.

**One-paragraph:** Curated, versioned, owner-signed prompt library for AI-assisted AWS IaC work (Terraform, Cloud Run, ECS, IAM) with required guardrails (no-secret-leak, source-of-truth pinning, idempotence checks) per prompt class. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Team uses AI assistants (Claude, Cursor, GitHub Copilot) for AWS IaC.
- Named platform-lead can curate + sign prompts before they enter the library.
- Prompt outputs feed into IaC PRs reviewed by humans.

## Skip If (ANY kills it)

- AI assistants are banned from IaC in the org — defer.
- Team prefers fully ad-hoc prompting and accepts the cost.
- Prompt library already exists with version control + owner sign-off.

**Ефективно для:**

- Команди де Claude/Cursor пишуть AWS Terraform / CloudFormation.
- Стандартизація AI-prompts для IaC щоб не винаходити кожен раз.
- Compliance вимоги per AI-output (хто схвалив, evidence, версія промпта).
- Onboarding інженерів з повторюваними AI-IaC задачами.

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
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Template fill of allow-lists + env-var blocks. |
| `populate-policy` | sonnet | Per-clause translation into config fields. |
| `breach-protocol-review` | opus | Cross-engagement risk + breach-response synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/policy.yaml` | YAML config skeleton with allow-list / deny-list / telemetry-overrides / audit-cadence. |
| `templates/_smoke-test.yaml` | Minimum viable filled policy. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-infra-prompt-library.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
