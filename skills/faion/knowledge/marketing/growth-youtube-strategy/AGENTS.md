# YouTube Strategy

## Summary

**One-sentence:** Produces a YouTube channel plan artefact (niche + format mix + hook structure + cadence) gated by search-intent priority and hook-first structure.

**One-paragraph:** Solo operators chase YouTube with generic channels and discovery-only content; the channel stalls. This methodology pins a plan: niche positioning sentence, search-intent first (tutorials / how-to), hook-first structure within 15 seconds, sustainable cadence (≤1/week for solos), and thumbnail-title pair tested as a unit. Output: a YouTube plan spec.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-youtube-strategy» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator can sustain ≥1 video / 2 weeks for ≥6 months.
- Niche positioning achievable (audience + topic + angle).
- Operator has access to keyword research (Ahrefs / TubeBuddy / VidIQ).

## Skip If (ANY kills it)

- Operator cannot sustain consistent cadence — burnout will drop the channel.
- Refuses to narrow to a niche — generic channels do not break threshold.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Niche positioning sentence | doc | operator |
| Search-intent keyword shortlist (≥20) | spreadsheet | research tool |
| Thumbnail style guide | image | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/search-everywhere-optimization` | Search-everywhere companion methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the youtube-plan artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-youtube-strategy.md.j2` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-youtube-strategy.md` | Markdown skeleton: artefact body + per-section table. Generated from `templates/growth-youtube-strategy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/growth-youtube-strategy.json` | youtube-plan JSON skeleton validating against scripts/. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-youtube-strategy.py` | Validate the youtube-plan artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[search-everywhere-optimization]]
- [[growth-podcast-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/growth-youtube-strategy.json`

```json
{
  "artefact_id": "growth-youtube-strategy-<client>-<YYYY-MM-DD>",
  "owner": "<Full Name> <email>",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "inputs_used": [
    {
      "name": "<input name>",
      "source": "<path or URL>"
    }
  ],
  "findings": [
    {
      "id": "f1",
      "summary": "<finding summary>",
      "severity": "medium"
    }
  ],
  "decision": "<verdict; one sentence>",
  "rationale": "<rationale citing \u22651 input by name; \u226520 chars>"
}
```
