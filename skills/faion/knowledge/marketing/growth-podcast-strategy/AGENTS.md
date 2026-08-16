# Two-Track Podcast Strategy

## Summary

**One-sentence:** Produces a two-track podcast plan artefact (guest appearances + owned show) gated by a 3-episode launch buffer and a niche-positioning lock.

**One-paragraph:** Solo operators launch a podcast with one episode, miss week 2, and watch the algorithm drop the show. This methodology pins two named tracks (guest appearances for faster ROI + owned show for authority), a 3-episode launch buffer, a niche positioning lock, per-guest prep doc with CTA placement, and a repurpose pipeline producing ≥3 derivative assets per episode. Output: a podcast plan spec.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-podcast-strategy» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator has authority / budget for ≥3 recorded episodes before launch.
- Niche positioning sentence exists or is achievable in 1 session.
- Repurposing capacity (clip + transcript + post) exists.

## Skip If (ANY kills it)

- Operator cannot commit to ≥3 buffer episodes — schedule will collapse.
- Generic 'business podcast' positioning operator refuses to narrow.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Niche positioning sentence | doc | operator |
| Guest shortlist (≥5) | spreadsheet | operator |
| Show artwork + description | image + markdown | designer / operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/search-everywhere-optimization` | Repurpose pipeline feeds search-everywhere distribution. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the podcast-plan artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/growth-podcast-strategy.md.j2` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-podcast-strategy.md` | Markdown skeleton: artefact body + per-section table. Generated from `templates/growth-podcast-strategy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/growth-podcast-strategy.json` | podcast-plan JSON skeleton validating against scripts/. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-podcast-strategy.py` | Validate the podcast-plan artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[growth-youtube-strategy]]
- [[search-everywhere-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/growth-podcast-strategy.json`

```json
{
  "artefact_id": "growth-podcast-strategy-<client>-<YYYY-MM-DD>",
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
