---
slug: kb-ai-assisted-quarter-retro-synthesis
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: AI-assisted quarterly retro synthesis ingesting chat, tickets, DORA metrics, and incidents into a themed cross-squad report with DORA deltas and prioritized action items.
content_id: "0645e74235654f38"
complexity: deep
produces: report
est_tokens: 4700
tags: [retro, quarterly, multi-squad, dora, synthesis]
---
# AI-Assisted Multi-Squad Quarter Retro Synthesis

## Summary

**One-sentence:** AI-assisted quarterly retro synthesis ingesting chat, tickets, DORA metrics, and incidents into a themed cross-squad report with DORA deltas and prioritized action items.

**One-paragraph:** AI-Assisted Multi-Squad Quarter Retro Synthesis produces a report artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Quarterly review for 3+ engineering squads with shared platform.
- DORA-driven retros: lead time / change-failure / MTTR deltas tied to themed lessons.
- Cross-squad delivery audit where chat + tickets + incidents must converge.
- Programme reporting for VP Eng / CTO needing a 2-page summary with evidence.

## Applies If (ALL must hold)

- ≥ 3 squads with Slack/Discord export, ticket history, DORA snapshot, incident log for the quarter.
- DORA metrics actually instrumented (not just claimed).
- Programme manager / VP Eng owns the synthesis and presents it.
- LLM API access + budget; data residency cleared for the corpus.

## Skip If (ANY kills it)

- Squads don't share platform or release cadence — synthesis is forced.
- DORA not instrumented — start with DORA setup methodology first.
- < 3 squads — squad-level retro is enough.
- Confidential incidents in the corpus (security breach, HR) — exclude from LLM ingest.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Chat export | JSON / TXT for the quarter | Slack admin |
| Ticket export | CSV / Jira API | PM |
| DORA snapshot | CSV with 4 metrics × 3 months | platform-eng |
| Incident log | postmortem markdown set | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[kb-ai-assisted-lessons-learned-synthesis]] | Sibling pattern; shares clustering + citation discipline |
| [[kb-versioned-agent-memory-files]] | Prior quarter context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `source_ingest_and_redact` | sonnet | Bulk parse + PII strip. |
| `dora_delta_summarize` | haiku | Deterministic numeric deltas. |
| `theme_clustering` | opus | Cross-source semantic grouping. |
| `incident_attribution` | opus | Tie incidents to themes. |
| `action_item_synthesis` | opus | Quarter-bound recommendations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/quarter-retro-doc.md` | 2-page quarter retro report |
| `templates/squad-appendix.md` | Per-squad evidence appendix |
| `templates/dora-delta-table.md` | DORA quarter-on-quarter delta table |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-quarter-retro-synthesis.py` | Verify themes ≥ 2 sources + DORA numbers match snapshot | pre-publication |

## Related

- [[kb-ai-assisted-lessons-learned-synthesis]]
- [[inc-postmortem-auto-draft-no-publish]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
