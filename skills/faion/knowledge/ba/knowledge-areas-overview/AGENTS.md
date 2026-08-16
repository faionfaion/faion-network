# BA Knowledge Areas Overview

## Summary

**One-sentence:** One-page L1 routing index over BABOK's six Knowledge Areas (KA-1..KA-6) producing a triage decision: which KA owns the current ask + which methodology to load next.

**One-paragraph:** BABOK organises BA work into six knowledge areas: BA Planning & Monitoring, Elicitation & Collaboration, Requirements Lifecycle, Strategy Analysis, Requirements Analysis & Design, Solution Evaluation. This methodology is the L1 index used at engagement start to route the ask to the right KA, then to drill down via knowledge-areas-detail for tasks and methodologies-detail for techniques.

**Ефективно для:**

- Перший роутинг ask при kickoff: який KA володіє питанням.
- Educational handout sponsor / junior BA, що таке шість KAs.
- Compliance mapping при L1, до яких KAs прив'язана evidence.
- Decision-record короткий, без drilldown в L2.

## Applies If (ALL must hold)

- Engagement kickoff: pick the entry KA.
- Ad-hoc ask routing during the BA cycle.
- Onboarding intro to BABOK for a junior BA.
- Sponsor education: 1-page handout naming the six KAs.
- Compliance evidence mapping at L1.

## Skip If (ANY kills it)

- Single specific KA already known — load knowledge-areas-detail directly.
- Mid-flight engagement using PMBOK only.
- Hot patches / hot fixes — no KA routing needed.
- When a more specific BA methodology already routes the task.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Engagement ask | Markdown / ticket | sponsor / BA |
| BABOK v3 reference | PDF / docs | IIBA |
| Methodology registry index | JSON | this skill |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/knowledge-areas-detail` | L2 drilldown after routing. |
| `pro/ba/business-analyst/methodologies-detail` | Per-method drilldown. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ka-routing-l1` | haiku | L1 ask → KA mapping; light judgement. |
| `sponsor-handout` | sonnet | Compose 1-page educational summary. |
| `onboarding-pack` | sonnet | Per-KA description for junior BA. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ka-overview-handout.md.j2` | 1-page sponsor handout of the six KAs. |
| `templates/ka-overview-handout.md` | 1-page sponsor handout of the six KAs. Generated from `templates/ka-overview-handout.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/onboarding-intro.md.j2` | Junior BA onboarding intro to BABOK structure. |
| `templates/onboarding-intro.md` | Junior BA onboarding intro to BABOK structure. Generated from `templates/onboarding-intro.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum filled-in routing record. |
| `templates/_smoke-test.md` | Minimum filled-in routing record. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ba-coverage-checklist.md.j2` | BA knowledge-area coverage checklist for a project |
| `templates/ba-coverage-checklist.md` | BA knowledge-area coverage checklist for a project Generated from `templates/ba-coverage-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ba-plan.md.j2` | Business Analysis plan envelope per BABOK KA-1 |
| `templates/ba-plan.md` | Business Analysis plan envelope per BABOK KA-1 Generated from `templates/ba-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-knowledge-areas-overview.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[knowledge-areas-detail]]
- [[methodologies-detail]]
- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
