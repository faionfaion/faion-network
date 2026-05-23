---
slug: ads-ab-testing-ads
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Specifies a pre-registered A/B test for ad creative (one variable, sample-size calculation, 95% confidence, learnings logged) ordered offer → hook → creative-type → visual → copy → CTA.
content_id: "9a9dd3a6d58bf8fa"
complexity: deep
produces: spec
est_tokens: 6500
tags: ["marketing", "ppc", "ab-testing", "experimentation", "statistics", "pro"]
---
# A/B Testing Ads

## Summary

**One-sentence:** Specifies a pre-registered A/B test for ad creative (one variable, sample-size calculation, 95% confidence, learnings logged) ordered offer → hook → creative-type → visual → copy → CTA.

**One-paragraph:** Most paid-ads A/B tests fail because they change >1 variable, stop early, or never log the verdict. This methodology imposes scientific discipline: one variable per test, sample-size pre-calculation, equal budget control vs. variant, 95% confidence threshold, mandatory learnings log. Test priority order: offer → hook/headline → creative type → visual style → copy length → CTA. Output: A/B test spec + sample-size calculation + verdict template.

**Ефективно для:**

- PPC manager шукає scientific discipline для creative iteration.
- Заміна 'we changed everything and CTR went up' на pre-registered single-variable test.
- Перехід від platform-built-in 'A/B test' tools на cross-platform pre-registration.
- Onboarding нового team member з standardized test discipline.

## Applies If (ALL must hold)

- Continuous testing cadence (>=1 test per 2 weeks).
- Spend per test >= $500 (enough volume for 95% confidence in <= 14 days).
- Operator can compute or has access to sample-size calculator (Optimizely, Evan Miller, etc.).
- Tests registry exists (learnings-database-schema methodology or equivalent).

## Skip If (ANY kills it)

- Spend per test < $200 — confidence unreachable.
- Operator changes >1 variable per test — methodology cannot enforce discipline post-hoc.
- No tests registry — verdicts lost; methodology ineffective.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ads-ab-testing-ads` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md` | Minimum viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-ab-testing-ads.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
