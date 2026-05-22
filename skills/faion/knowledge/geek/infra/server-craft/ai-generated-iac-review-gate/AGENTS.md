---
slug: ai-generated-iac-review-gate
tier: geek
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Review rubric and CI gate for AI-generated infrastructure-as-code: secrets scan, drift check, blast-radius classification, human sign-off thresholds."
content_id: "a5e49dcf69bc1a80"
complexity: medium
produces: rubric
est_tokens: 3800
tags: [iac, ai, review-gate, terraform, pulumi, security, geek, infra]
---

# AI-Generated IaC Review Gate

## Summary

**One-sentence:** Review rubric and CI gate for AI-generated infrastructure-as-code: secrets scan, drift check, blast-radius classification, human sign-off thresholds.

**One-paragraph:** Review rubric and CI gate for AI-generated infrastructure-as-code: secrets scan, drift check, blast-radius classification, human sign-off thresholds. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`rubric`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Team uses AI assistants (Copilot, Claude Code, Cursor) for IaC authoring.
- Production blast-radius of IaC changes is non-trivial (multi-tenant / regulated).
- Existing CI pipeline can host additional gates.

## Skip If (ANY kills it)

- All IaC changes are human-authored.
- Sandbox/dev-only environment with no production blast radius.
- Existing rigorous review gate already covers AI-generated IaC.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| AI-authoring policy | Markdown | engineering lead |
| CI pipeline | GitHub Actions / GitLab CI | infra |
| Secrets scanner | gitleaks / trufflehog | security |
| Policy-as-code | OPA / Sentinel / Checkov | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/code-generation-review` | How to review AI-generated code generally. |
| `pro/infra/devops-engineer/iac-baseline` | IaC tooling and conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `rubric_check_automated` | haiku | Mechanical pattern checks. |
| `blast_radius_classify` | sonnet | Classify change blast radius. |
| `human_review_synthesis` | opus | Cross-input judgment for high-blast changes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/review-rubric.md` | AI-IaC review rubric with weighted criteria. |
| `templates/ci-gate.yaml` | GitHub Actions workflow with the gate steps. |
| `templates/blast-radius-matrix.md` | Classification rubric (low/medium/high). |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-generated-iac-review-gate.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[code-generation-review]]`
- `[[iac-baseline]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-generated-iac-review-gate applies: root question — "Is the IaC change AI-assisted AND targets production blast radius?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
