---
slug: glossary-management-as-code
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Domain glossary kept as versioned YAML next to code: terms, definitions, synonyms, deprecated aliases, owner, last-reviewed date.
content_id: "8999e0e5a79fee6d"
complexity: medium
produces: config
est_tokens: 4400
tags: [ba, pro, glossary, domain-language, as-code, yaml]
---
# Glossary Management as Code

## Summary

**One-sentence:** Domain glossary kept as versioned YAML next to code: terms, definitions, synonyms, deprecated aliases, owner, last-reviewed date.

**One-paragraph:** Glossary Management as Code pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Outsource projects where client and team build a shared domain language.
- Multi-team monorepos where vocabulary drift becomes a bug pattern.
- Compliance-heavy domains (HealthTech, FinTech) where term equivalence is regulated.
- Migration engagements where legacy terms map to new terms.

## Applies If (ALL must hold)

- Project has a domain glossary referenced by both BA and engineering teams.
- Engineers + BA + product use overlapping but not identical terms (synonyms drift).
- Repo supports YAML + PRs as the change-control mechanism.
- Glossary changes happen at least monthly.

## Skip If (ANY kills it)

- Single-author project where no terminology drift exists.
- Glossary lives in a wiki that all stakeholders edit freely (no PR discipline possible).
- Domain vocabulary is fully covered by an external standard you reference (e.g. FHIR).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing glossary draft | markdown / yaml | BA repo |
| Engineer vocabulary sample | extracted from code identifiers | Repo grep |
| Product vocabulary sample | from product docs | Product repo |
| PR-review process | markdown | Team process doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-glossary-management-as-code` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/glossary-management-as-code.yaml` | YAML config skeleton with required keys |
| `templates/glossary-management-as-code.schema.json` | JSON Schema for the config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-glossary-management-as-code.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
