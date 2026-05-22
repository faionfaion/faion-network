---
slug: delivery-maturity-rubric
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a per-domain 1-5 maturity rubric with anchored behaviours so PMBoK 7 annual reviews score on evidence instead of opinion."
content_id: "5e5c17e562181a04"
complexity: medium
produces: rubric
est_tokens: 3800
tags: [pm, maturity, review, rubric, pmbok]
---
# Delivery Maturity Rubric

## Summary

**One-sentence:** Produces a per-domain 1-5 maturity rubric with anchored behaviours so PMBoK 7 annual reviews score on evidence instead of opinion.

**One-paragraph:** Produces a per-domain 1-5 maturity rubric with anchored behaviours so PMBoK 7 annual reviews score on evidence instead of opinion. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM-у на щорічному maturity-review — кожен бал прив'язаний до спостережуваної поведінки, не до думки.

## Applies If (ALL must hold)

- An annual or quarterly delivery-process maturity review is on the calendar.
- PMBoK 7 (or compatible) performance-domain vocabulary is the agreed reference.
- At least 2 raters are available so per-domain scores can be calibrated.
- Behaviour evidence from the past 90 days is accessible (releases, incidents, audits).

## Skip If (ANY kills it)

- No formal review cycle exists — single-team retros use a lighter rubric.
- Only one rater is available — rubric becomes opinion-tracking.
- Required behaviour evidence is older than 6 months — scores will be stale.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| PMBoK 7 performance-domain reference | doc | PMI publication or internal copy |
| Behaviour evidence | URLs/tickets/transcripts | release log + incident log + audit notes |
| Prior cycle's rubric (if any) | JSON/Markdown | team knowledge space |
| Calibration partner | named human | delivery-org roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager/cross-role-handoff-protocol` | Shared vocabulary for handoff stages the rubric scores. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-rubric` | haiku | Skeleton fill from domain list — template work. |
| `evidence-anchor-check` | sonnet | Per-anchor judgement: does it support the score band? |
| `rubric-synthesis` | opus | Cross-domain trend synthesis + write-up for review board. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Canonical JSON Schema the produced rubric artefact must validate against. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-delivery-maturity-rubric.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[engineering-ladder-and-growth-plan]]
- [[portfolio-evm-rollup-method]]
- [[cross-role-handoff-protocol]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether the rubric runs at all (≥2 raters + ≥3 anchors per domain) or is downgraded to a partial scoring with `not_assessed` markers. Use it during scoping for the review window — before any anchor is collected.
