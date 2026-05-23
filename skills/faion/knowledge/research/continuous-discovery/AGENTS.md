# Continuous Discovery

## Summary

**One-sentence:** Teresa Torres weekly-rhythm discovery: 6-cadence pipeline (daily signals -> weekly interviews + competitor + assumption tests -> bi-weekly OST -> monthly review) with N>=5 evidence floor and 8 scheduled subagents.

**One-paragraph:** Teresa Torres' framework embedded into the weekly delivery rhythm via 8 scheduled subagents: daily signal collection (Haiku), weekly interviews/competitor monitoring/assumption testing (Sonnet), bi-weekly OST synthesis (Opus), monthly research review. Outputs land in .aidocs/product_docs/discovery/. The framework bans the word 'validated', enforces N>=5 observations across >=2 sources, and rejects solution-shaped intake.

**Ефективно для:**

- Live продукт з активними users де volume сигналів перевищує те що PM може прочитати.
- Product Trio workflow з weekly cadence customer touchpoints.
- Ринки з 6-місячним half-life на user-need validity (AI, fintech, dev tools).
- Solo операції: один operator симулює trio покриття через subagents.
- Після launch коли growth уповільнюється і треба ловити 'solution stopped working'.

## Applies If (ALL must hold)

- Live product with active users where signal volume exceeds what one PM can review unaided.
- Product Trio (PM + designer + engineer) needing a weekly cadence of customer touchpoints.
- Markets with 6-month half-life on user-need validity.
- Solopreneur stacks where one operator must simulate trio coverage via subagents.
- Post-launch slowdowns where the 6-month-ago solution no longer works.

## Skip If (ANY kills it)

- Pre-PMF zero-to-one with no users yet - start with customer-development first.
- Compliance-bound enterprise sales where contract cycles are 6-18 months.
- Hardware / regulated medical where each iteration ships in months.
- Crisis mode (active outage, churn cliff) - switch to root-cause first.
- When stakeholders demand 'validated' answers from a single interview.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Open OST | markdown / opportunity-solution-tree.md | previous discovery cycle |
| Open assumptions register | markdown | previous bi-weekly synth |
| Recurring recruit source | in-app prompt / panel / Userinterviews.com | research ops |
| Analytics + ticket sources | PostHog / Intercom / Zendesk | infrastructure |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[opportunity-solution-trees]] | consumed for the bi-weekly synthesis output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `analytics-watcher` | haiku | Mechanical daily metric pull. |
| `support-triage` | haiku | Daily ticket cluster + count + severity tagging. |
| `competitor-monitor` | haiku | Weekly RSS/changelog scrape diff. |
| `interview-synthesizer` | sonnet | Per-call transcript -> tagged notes + JTBD pulls. |
| `assumption-tester` | sonnet | Weekly test design + result rubric for OST leaves. |
| `discovery-synthesizer` | opus | Bi-weekly cross-source pattern recognition. |
| `research-reviewer` | opus | Monthly strategic memo + kill list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost-schema.json` | OST node schema (id/type/parent/evidence/status) |
| `templates/analytics-watcher.py` | Daily watcher: PostHog + tickets -> insight-log.md |
| `templates/crontab.txt` | Cron schedule for 4 discovery cadences |
| `templates/discovery-report.md` | Monthly research-review skeleton (kill list + doubled-down) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-continuous-discovery.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[opportunity-solution-trees]]
- [[user-research-at-scale]]
- [[persona-building]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
