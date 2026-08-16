# Objection FAQ Library

## Summary

**One-sentence:** Curates a reusable objection FAQ library (top 10-15 objections + pre-empt copy + supporting evidence) embeddable into proposals, landing pages, and discovery calls.

**One-paragraph:** Proposals lose to silence, not 'no' — buyers stall when an unanswered objection lingers. This methodology mines past lost-deal transcripts, win/loss calls, sales-rep notes, and support tickets to surface the top 10-15 recurring objections, then drafts pre-empt copy + evidence per objection, indexed by funnel-stage. Output: FAQ library spec with copy variants for proposals, landing-page FAQ blocks, and inline rebuttals.

**Ефективно для:**

- Solo або agency з proposal close rate < 30% і > 5 proposals/month.
- Lost-deal mining з calls + emails + tickets для top objections.
- Pre-empt copy для proposals + landing pages + sales decks.
- Onboarding нового sales-rep із готовою библиотекою rebuttals.

## Applies If (ALL must hold)

- Proposal close rate < 30% with > 5 proposals/month.
- At least 10 lost-deal artifacts available (calls, emails, ticket-close reasons).
- Operator can curate + maintain library (named owner).
- Sales cycle long enough that objections recur (>= 14 days first-touch to close).

## Skip If (ANY kills it)

- Single-objection product (price-only) — pricing-strategy methodology fits better.
- < 10 lost-deal artifacts — no statistical signal yet.
- Sales-cycle < 7 days — FAQ library not actionable at speed.

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
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-objection-faq-library` | opus | Synthesis under output contract; final write-up. |
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
| `scripts/validate-objection-faq-library.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

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
