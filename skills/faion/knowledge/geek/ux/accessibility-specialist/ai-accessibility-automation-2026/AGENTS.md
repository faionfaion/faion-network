---
slug: ai-accessibility-automation-2026
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a full continuous-a11y pipeline (axe-playwright + AI ranking + VPAT 2.5 draft + alt-text + caption) with a human accessibility lead gating every AI artifact.
content_id: "8dc65b2e896ba292"
complexity: deep
produces: spec
est_tokens: 5100
tags: [accessibility, wcag, ada-compliance, automation, vpat]
---
# AI Accessibility Automation 2026

## Summary

**One-sentence:** Wire axe-playwright into every deploy, an AI ranks/de-duplicates violations, code fixes are AI-suggested per issue, VPAT 2.5 drafts are AI-generated from scan summaries, alt-text + captions pipelines run on every media upload, and a human a11y lead gates every AI output.

**One-paragraph:** Full continuous accessibility automation pipeline for products with frequent deployments: axe-playwright scans every deploy, AI ranks and de-duplicates violations, code fixes are suggested per issue, VPAT 2.5 drafts are generated from scan summaries, and caption/alt-text pipelines run on every media upload. All AI outputs are gated by a human accessibility lead before entering the developer backlog.

**Ефективно для:**

- Continuous-deploy products з частими a11y regressions.
- VPAT-driven sales: AI drafts → human lead signs.
- Bulk alt-text generation для media-heavy sites.
- Org з human lead, що caps AI output backlog.

## Applies If (ALL must hold)

- Product deploys ≥ weekly (continuous integration required).
- Org carries a human accessibility lead with capacity to gate AI output.
- Media uploads (images / video) are common and need alt / caption pipelines.

## Skip If (ANY kills it)

- Static brochure site with one release per quarter — manual audit cheaper.
- No human a11y lead available — AI output cannot be gated.
- Product has no media uploads (alt/caption pipelines wasted).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Playwright + axe-playwright installed | deps | test infra |
| Human accessibility lead | role | team roster |
| Media upload pipeline | code | media service |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-a11y-gate.sh` | Shell script wiring axe-playwright into CI as a deploy gate. |
| `templates/prompt-scan-triage.txt` | Prompt ranking + de-duplicating axe violations for the human lead. |
| `templates/prompt-vpat-draft.txt` | Prompt drafting a VPAT 2.5 section from scan summaries. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-accessibility-automation-2026.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[ai-assisted-accessibility]]
- [[test-self-healing-locators-audited]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
