# Lead Magnet for Solo Consultancy

## Summary

**One-sentence:** Picks one filtering lead-magnet format (audit / benchmark / calculator / pack) for a solo consultant and ships a versioned spec the consultant can build in a week.

**One-paragraph:** Solo-consultant lead magnets must filter to qualified buyers, not pad list size. SaaS-style 'top-10 tips' eBooks attract students, not buyers. This methodology evaluates four filtering formats (niche audit checklist, opinionated benchmark report, code snippet pack, calculator) against the consultant's positioning, then emits a spec covering audience, promised outcome, format, gating, conversion path, and follow-up sequence.

**Ефективно для:**

- Соло-консультант з вузьким ICP, який хоче відсіювати не-покупців на вході.
- Заміна загальних SaaS-чеклістів на вузький benchmark / audit / calculator.
- Lead magnet ship < 5 днів силами однієї людини без команди.
- Підготовка лійки 'magnet → 7-day email → consultation booking'.

## Applies If (ALL must hold)

- Solo consultant or independent specialist with one named ICP serving < 50 active prospects.
- Conversion path exists (landing page, scheduling link, or sales call slot).
- Operator can ship a focused asset in <= 1 working week (no committee approval).
- Existing organic traffic, audience, or referral pipeline already drives >=10 qualified visits/week to filter.

## Skip If (ANY kills it)

- Headcount > 5 marketing FTE — switch to growth-marketer/content-stack methodology.
- No defined ICP yet — run niche-positioning-for-solo-dev first.
- Buyers come exclusively from inbound referrals — lead magnet adds noise, not signal.

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
| `draft-lead-magnet-for-solo-consultancy` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md.j2` | Markdown spec skeleton |
| `templates/spec.md` | Markdown spec skeleton Generated from `templates/spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md.j2` | Minimum viable filled spec |
| `templates/_smoke-test.md` | Minimum viable filled spec Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lead-magnet-for-solo-consultancy.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output.json`

```json
{
  "artefact_id": "<SLUG-YYYY-Qx>",
  "template_version": "1.1.0",
  "owner": "<named-owner@example>",
  "summary": "<one paragraph>",
  "fields": {},
  "evidence": [
    {
      "source": "<URL>",
      "citation": "<verbatim quote>"
    }
  ],
  "status": "draft",
  "next_action": {
    "label": "<action>",
    "owner": "<named>",
    "due_cycle": "<YYYY-Www>"
  }
}
```
