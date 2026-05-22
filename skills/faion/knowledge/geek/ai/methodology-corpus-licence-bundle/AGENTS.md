---
slug: methodology-corpus-licence-bundle
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Per-customer methodology corpus licence record: scope (which tiers + which domains), redistribution rights, attribution, audit hooks, renewal cadence.
content_id: "be69f0405be5ba46"
complexity: medium
produces: spec
est_tokens: 4200
tags: [methodology, corpus, licence, audit, renewal]
---
# Methodology Corpus Licence Bundle

## Summary

**One-sentence:** Per-customer methodology corpus licence record: scope (which tiers + which domains), redistribution rights, attribution, audit hooks, renewal cadence.

**One-paragraph:** Codifies the «sell our methodology corpus to a customer team» recurring decision into one auditable artefact. Defines: what is licensed (tiers, domains, slugs), what is forbidden (resale, ML training without consent), attribution requirements, the audit path that proves usage stayed in scope, and the renewal cadence with named approver. Pulls from F-026 corpus-integration playbook into a deal-ready record.

**Ефективно для:** Sales + legal, що мають клієнта на 2-тижневу інтеграцію Faion-corpus і потребують один файл замість листа з 6 нитями обговорень.

## Applies If (ALL must hold)

- a customer has signed a paid Faion plan with corpus access
- the customer wants to embed corpus content in their internal agent
- you need an artefact to point auditors / lawyers at
- a named approver on Faion side is available for the deal
- redistribution policy questions have arisen

## Skip If (ANY kills it)

- customer uses Faion via CLI only — no corpus embedding
- free tier — no licence bundle needed; standard ToS applies
- internal team usage — no licence required
- deal not yet closed — wait for signed plan

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=spec + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=spec`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-methodology-corpus-licence-bundle.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/licence-bundle.md` | Per-customer licence bundle skeleton with all 5 sections |
| `templates/audit-attestation.md` | Quarterly self-attestation form |
| `templates/renewal-memo.md` | Renewal go/no-go memo |
| `templates/attribution-snippet.md` | Suggested attribution placements + screenshots |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodology-corpus-licence-bundle.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-scope-explicit`, `r2-redistribution-clause`, `r3-attribution-required`, `r4-audit-hook`, `r5-renewal-cadence` from `content/01-core-rules.xml`.
