---
slug: team-methodology-overlay-mechanism
tier: geek
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Specifies the per-user and per-repo overlay layer that lets in-house teams substitute their own ADR templates, RFC formats, and policies on top of the shipped faion corpus with deterministic precedence.
content_id: "22b1615e63b3afcf"
complexity: deep
produces: config
est_tokens: 3400
tags: ["sdd", "team", "overlay", "customisation", "precedence"]
---
# Team Methodology Overlay Mechanism

## Summary

**One-sentence:** Specifies the per-user and per-repo overlay layer that lets in-house teams substitute their own ADR templates, RFC formats, and policies on top of the shipped faion corpus with deterministic precedence.

**One-paragraph:** Team Methodology Overlay Mechanism produces a config that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Enterprise team має власні ADR templates — overlay над faion corpus.
- Per-repo policy: різні правила code review per project.
- Per-user override: дозволити solo customisation у monorepo.
- Deterministic precedence: known winner коли overlay конфліктує з base.
- Audit: видно exactly які rules діють у даний момент.

## Applies If (ALL must hold)

- Team uses faion methodology corpus but needs deviations.
- Multiple repos or users need distinct policies.
- Conflicts between layers must be resolved deterministically.

## Skip If (ANY kills it)

- Team uses base corpus unchanged.
- No conflicting policies exist between teams / repos.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Base faion methodology corpus | filesystem | faion-network |
| Override candidates inventory | Markdown | tech lead |
| Conflict log (if any) | Markdown | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-team-methodology-overlay-mechanism` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/overlay-manifest.yml` | YAML manifest declaring overlay scope + precedence |
| `templates/conflict.log.tmpl` | Conflict log template line shape |
| `templates/overlay.schema.json` | JSON Schema for overlay manifest |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-methodology-overlay-mechanism.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[adr-consequence-evidence-binding]]
- [[internal-rfc-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
