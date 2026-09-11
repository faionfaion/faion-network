# Roadmap Design

## Summary

**One-sentence:** Picks the roadmap format from the uncertainty level, then designs the roadmap in that format with explicit confidence per item, an internal source-of-truth plus one derived external view, and a named review cadence — so the roadmap steers instead of listing wishes.

**One-paragraph:** Replaces feature lists with outcome statements per horizon. Format comes first: uncertainty low → timeline, medium → Now/Next/Later, high → outcome-themed. Now items carry committed scope + owner; Next items carry hypotheses + dependencies; Later items carry bets + open questions. Confidence labels (high/medium/low) prevent the document from being read as a contract. One internal source-of-truth is maintained and every external view is derived from it with metric targets, confidence labels and owners stripped; both artefacts carry an explicit not-doing list and a published cadence.

**Ефективно для:**

- Solo founder or small-team PM whose roadmap doc drifts every 2 weeks; needs a structure that holds shape under reprioritisation without lying about commitments.
- Teams serving ≥2 audiences (internal team, customer, board) from one plan without maintaining two copies by hand.
- Anyone under stakeholder pressure for dates on work whose uncertainty does not support them.
- Audit / review surface: every artefact has an owner, evidence anchors and a review beat.

## Applies If (ALL must hold)

- Multi-stakeholder product where alignment beats individual feature scope.
- Quarterly planning cadence exists or is being established.
- Roadmap will be shared externally or with non-PM stakeholders.
- Uncertainty over the horizon can be assessed as low / medium / high.

## Skip If (ANY kills it)

- Single-developer 1-week scope where a plain task list is sufficient.
- Pre-product phase where there are no users to align with.
- Stable maintenance product with no strategic direction.
- Contract-defined deliverables — the timeline format is forced, so there is no format to design.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Strategic outcomes / OKRs | markdown | Strategy doc |
| Uncertainty assessment over the horizon | low/medium/high | Team |
| Confidence rubric | table | PM doc |
| Audience list for the roadmap (internal/external) | list | CRM / team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/okr-setting` | Outcomes anchor the roadmap horizons. |
| `solo/product/product-planning/outcome-based-roadmaps` | Format option when uncertainty over the horizon is high. |
| `solo/product/product-operations/feature-prioritization-rice` | Within-horizon ranking when items contend. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 19 testable rules (format selection, horizons, confidence + 30% distribution floor, Now cap 5, 3–5 themes, objective links, cadence, audience split, human review of external, not-doing, one-screen, LLM prompt constraints) + skip + run rules; format catalogue + selection matrix | 3600 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns with symptom + root-cause + fix (dated features, missing confidence, external leak, audience-forced format, never revisited, orphaned initiatives, Later graveyard, one roadmap for all audiences) | 1200 |
| `content/04-procedure.xml` | essential | 9-step procedure: strategy inputs -> uncertainty -> format -> outcomes -> themes -> horizons -> external view -> cadence -> publish; lint-roadmap.py reference | 1000 |
| `content/05-examples.xml` | essential | Worked example end-to-end + B2B SaaS and solo product Now-Next-Later sketches | 850 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs (format, external view, human review, not-doing, objective links, Now cap, theme count) to a rule id in 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-roadmap-design` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-roadmap-design` | haiku | Schema check + threshold checks; deterministic. |
| `review-roadmap-design` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/roadmap-design.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/roadmap-design.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/roadmap-design.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/roadmap-design.json` | JSON skeleton conforming to the output contract schema. |
| `templates/roadmap-diff.py` | Diffs two roadmap snapshots (moved / added / dropped) for the monthly review beat in r9. |
| `templates/external-roadmap.md.j2` | Customer-facing roadmap derived from the internal source of truth. |
| `templates/external-roadmap.md` | Customer-facing roadmap derived from the internal source of truth. Generated from `templates/external-roadmap.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/now-next-later.md.j2` | Internal Now/Next/Later roadmap (medium-uncertainty format). |
| `templates/now-next-later.md` | Internal Now/Next/Later roadmap (medium-uncertainty format). Generated from `templates/now-next-later.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/quarterly-outcome.md.j2` | Quarterly outcome-themed roadmap (high-uncertainty format). |
| `templates/quarterly-outcome.md` | Quarterly outcome-themed roadmap (high-uncertainty format). Generated from `templates/quarterly-outcome.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-roadmap-design.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[okr-setting]]
- [[outcome-based-roadmaps]]
- [[feature-prioritization-rice]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
