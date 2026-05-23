# Agency Case Study Template

## Summary

**One-sentence:** Five-part case-study skeleton (Context, Problem, Approach, Outcome, Lessons) for freelancers and micro-agencies, with quantified outcomes, one verbatim client quote, and a named approver per study — a portfolio asset that converts inbound to qualified calls.

**One-paragraph:** Five-part case-study skeleton (Context, Problem, Approach, Outcome, Lessons) for freelancers and micro-agencies, with quantified outcomes, one verbatim client quote, and a named approver per study — a portfolio asset that converts inbound to qualified calls. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Agency / freelancer has ≥ 1 completed engagement with quantifiable outcome.
- Client is willing to sign off on a verbatim quote + named attribution (or anonymised role).
- Named portfolio owner can produce + publish the study within 4 weeks.

## Skip If (ANY kills it)

- No quantifiable outcome data — collect baseline + post-engagement metric first.
- Client refuses any attribution (even anonymised) — use a generic 'pattern' case study instead.
- Engagement < 30 days old — wait for the outcome to stabilise before writing.

**Ефективно для:**

- Фрилансери і мікро-агенції що збирають перші 3-5 proof-asset для website.
- Команди з минулим успіхом але без чітких case studies для inbound conversion.
- Засновники що готують rebrand / niche positioning і потребують aligned portfolio.
- Аудит-ready середовища з вимогою quantified outcome + client quote evidence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing-manager` | Parent role context — agency operating discipline. |
| `solo/marketing/content-marketer` | Adjacent role context — content + portfolio surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-case-study-template.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[agency-niche-positioning]]
- [[agency-case-study-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
