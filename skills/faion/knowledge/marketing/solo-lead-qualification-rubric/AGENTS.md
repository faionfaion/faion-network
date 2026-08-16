# Solo Lead Qualification Rubric

## Summary

**One-sentence:** Produces an ICE-style qualification score per lead (budget + authority + timeline + history) replacing BANT for one-person services.

**One-paragraph:** Solo freelancers waste discovery time on no-budget leads or get scarred by serial contractor-churn clients. This methodology pins an ICE-style rubric tuned to solo signals: 4 axes (budget clarity / decision authority on call / sane timeline / no scarring contractor history), each scored 0-3, no-budget auto-decline, authority confirmed on call (not assumed from title), and an explicit scar flag for triage. Output: a lead qualification score artefact per lead.

**Ефективно для:**

- готова основа для повторюваної задачі «solo-lead-qualification-rubric» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator runs ≥1 discovery call per week.
- Operator can decline leads (not desperate for every closeable deal).
- Pipeline tracking surface exists (CRM / spreadsheet / Notion).

## Skip If (ANY kills it)

- Operator is in launch mode and cannot afford to decline any lead.
- Operator runs only fixed-fee productised services with no discovery.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Lead intake fields | form / spreadsheet | intake |
| Discovery-call notes template | doc | operator |
| Pipeline tracking surface | Notion / sheet | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/marketing/conversion-optimizer/` | Parent role / operating context. |
| `solo/marketing/conversion-optimizer/testimonial-harvest-sop` | Post-engagement methodology for qualified-and-closed leads. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the lead-qualification-score artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/solo-lead-qualification-rubric.md.j2` | Markdown skeleton: artefact body + per-section table. |
| `templates/solo-lead-qualification-rubric.md` | Markdown skeleton: artefact body + per-section table. Generated from `templates/solo-lead-qualification-rubric.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/solo-lead-qualification-rubric.json` | lead-qualification-score JSON skeleton validating against scripts/. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-lead-qualification-rubric.py` | Validate the lead-qualification-score artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[testimonial-harvest-sop]]
- [[indie-mini-crm-notion]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/solo-lead-qualification-rubric.json`

```json
{
  "artefact_id": "solo-lead-qualification-rubric-<client>-<YYYY-MM-DD>",
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
