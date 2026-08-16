# Competitive Analysis (UX)

## Summary

**One-sentence:** Examine 3-5 direct + 2-3 indirect + 1-2 aspirational competitors against pre-defined UX criteria; produce a feature matrix, per-competitor profile, and Must/Should/Could/Avoid recommendation set.

**One-paragraph:** Without competitive analysis, design teams reinvent solved problems, miss user expectations set by other products, and cannot answer 'what do competitors do?' This methodology pins the competitor set (3-5 direct, 2-3 indirect, 1-2 aspirational), defines evaluation criteria in advance (UX heuristics, feature parity, onboarding patterns, friction points), and converts findings into actionable Must-have (table stakes) / Should-have (parity) / Could (differentiation opportunities) / Avoid (observed failure modes) recommendations. Output: a competitive analysis spec artefact consumed by feature discovery, value-proposition design, and design critique.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Pre-design sprint for a new product when the competitive landscape is uncharted.
- Quarterly refresh after major competitor launches or category shifts.
- Positioning work — feeding differentiation candidates into value-proposition design.
- Stakeholder defence — having the canonical competitor profile ready before review meetings.

## Skip If (ANY kills it)

- A < 6-month-old competitive analysis already covers the same competitor set.
- The product is in an entirely new category with no comparable competitors.
- The decision is a UI polish, not a strategic positioning move — competitive analysis is overkill.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Competitor candidate list | 6-10 names | market scan |
| Evaluation criteria | UX + feature + friction | design-critique heuristics |
| Account access | free / trial / purchased | research operations |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/heuristic-evaluation` | supplies the evaluation rubric per competitor |
| `solo/ux/user-researcher/value-proposition-design` | downstream consumer of differentiation recommendations |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/competitive-analysis.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-competitive-analysis.py --self-test` |
| `templates/analysis-plan.md.j2` | Scoping plan for a competitive analysis engagement |
| `templates/analysis-plan.md` | Scoping plan for a competitive analysis engagement Generated from `templates/analysis-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/competitor-profile.md.j2` | Per-competitor observation profile filled during a competitive analysis |
| `templates/competitor-profile.md` | Per-competitor observation profile filled during a competitive analysis Generated from `templates/competitor-profile.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/feature-matrix.md.j2` | Feature-by-feature comparison matrix against direct competitors |
| `templates/feature-matrix.md` | Feature-by-feature comparison matrix against direct competitors Generated from `templates/feature-matrix.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/summary-report.md.j2` | Synthesised findings and Must/Should/Could/Avoid recommendations |
| `templates/summary-report.md` | Synthesised findings and Must/Should/Could/Avoid recommendations Generated from `templates/summary-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[heuristic-evaluation]]
- [[value-proposition-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/competitive-analysis.json`

```json
{
  "artefact_id": "competitive-analysis-2026-05-23",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "inputs_used": [
    {
      "name": "prerequisite-doc",
      "source": "docs/prereq.md"
    }
  ],
  "sections": [
    {
      "heading": "Context",
      "body": "bounded scope per Applies-If; named owner"
    },
    {
      "heading": "Decision",
      "body": "apply rules from 01-core-rules.xml end-to-end"
    }
  ],
  "decision": "Adopt the methodology as the engagement standard."
}
```

### `templates/_smoke-test.json`

```json
{
  "artefact_id": "competitive-analysis-smoke-2026-05-23",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "inputs_used": [
    {
      "name": "smoke-fixture",
      "source": "templates/_smoke-test.json"
    }
  ],
  "sections": [
    {
      "heading": "Context",
      "body": "smoke-test"
    },
    {
      "heading": "Decision",
      "body": "smoke-test"
    }
  ],
  "decision": "smoke-test artefact"
}
```
