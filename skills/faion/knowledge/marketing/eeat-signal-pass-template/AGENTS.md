# EEAT Signal Pass Template

## Summary

**One-sentence:** Produces a per-post EEAT signal pass artefact (author bio + last-updated + citations + original quotes + schema) gated by the 5-signal completeness rule.

**One-paragraph:** EEAT is talked about everywhere but no operational checklist exists at faion. This methodology pins a per-post pass: author bio link with credentials, last-updated date ≤12 months, ≥3 outbound citations, ≥1 original quote or data point, and article schema markup. Output: a per-post EEAT pass checklist artefact.

**Ефективно для:**

- готова основа для повторюваної задачі «eeat-signal-pass-template» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Post is targeting search visibility (Google / AI engines).
- Author identity is available (real human with credentials).
- CMS supports schema markup injection.

## Skip If (ANY kills it)

- Post is internal-only with no public search target.
- Author refuses to attach name or credentials.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Draft post | markdown / CMS draft | author |
| Author bio + credentials | doc | operator |
| CMS schema config | JSON-LD template | developer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/` | Parent group / operating context. |
| `solo/marketing/content-marketer/search-everywhere-optimization` | Parent plan methodology this checklist supports. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the eeat-pass artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/eeat-signal-pass-template.md.j2` | Markdown skeleton: artefact body + per-section table. |
| `templates/eeat-signal-pass-template.md` | Markdown skeleton: artefact body + per-section table. Generated from `templates/eeat-signal-pass-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/eeat-signal-pass-template.json` | eeat-pass JSON skeleton validating against scripts/. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-eeat-signal-pass-template.py` | Validate the eeat-pass artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[search-everywhere-optimization]]
- [[growth-landing-page-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/eeat-signal-pass-template.json`

```json
{
  "artefact_id": "eeat-signal-pass-template-<client>-<YYYY-MM-DD>",
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
