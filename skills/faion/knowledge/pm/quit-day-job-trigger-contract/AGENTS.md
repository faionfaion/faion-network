# Quit Day Job Trigger Contract

## Summary

**One-sentence:** A pre-commitment artefact that defines the exact numeric trigger to quit the day job, the named owner accountable for executing it, the evidence anchors used to verify the trigger fires, and the reversal clause.

**One-paragraph:** The bootstrap journey ($0→$4k MRR while keeping the day job) collapses into folklore without an artefact that names the trigger and the reversal. This methodology pins a contract with five fields — trigger (numeric, dated, named — not "when needed"), output shape (bounded), evidence anchors, named owner, outcome review cadence — so the solo SaaS builder has a reviewable instrument instead of a feeling. Output is a versioned contract committed to the team's knowledge space.

**Ефективно для:**

- Solo SaaS builder approaching the $4K MRR full-time leap.
- Pre-commitment device that pairs with the financial-runway model.
- Documenting the reversal clause (when to return to a day job) before the decision is emotional.
- Quarterly review of the contract against actual MRR + savings trajectory.

## Applies If (ALL must hold)

- A solo SaaS builder on a bootstrap toward roughly 4,000 USD MRR while employed, with a billing provider (Stripe Billing, Baremetrics, ChartMogul or equivalent) producing a net MRR report.
- A runway model exists with liquid savings and a monthly burn that includes self-employment tax, health insurance and business costs.
- Customer-level MRR and monthly gross MRR churn can be read from the provider, so the concentration and churn gates can be checked at each month-end.
- No month-end reading has yet reached the intended threshold, or the builder accepts a post_hoc label and a void first window.
- The contract can live in version control with a monthly or quarterly review the builder will actually run.

## Skip If (ANY kills it)

- No provider MRR report or no runway model: there is nothing to trigger on; instrument billing and build the runway model first.
- The builder wants the trigger on gross cash, a single good month, or a feeling of readiness rather than net MRR over consecutive month-ends.
- The builder will not write a reversal clause below the trigger or a runway floor; the contract would flip-flop on noise.
- Fewer than 3 reviews a year are realistic; without readings at a cadence the contract becomes folklore.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Provider MRR report | net MRR at each month-end from Stripe Billing, Baremetrics, ChartMogul or equivalent, with its URL or dated export | billing provider |
| Runway model | liquid savings, monthly burn broken into living costs, self-employment tax, health insurance and business costs, with the date computed | builder's runway model file (side-project-financial-runway) |
| Customer share and churn | top customer's share of MRR and gross MRR churn per month-end | billing provider |
| Employment terms | notice period and the people to inform | employment contract; builder |
| Version-controlled store | repository path where the contract and its change log live | builder's repo or wiki |
| `templates/contract-skeleton.md.j2`, `templates/header.yaml` | contract sections; frontmatter with version, commit date and post_hoc | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[side-project-financial-runway]] | Runway model feeds the trigger and reversal clause. |
| [[solo-mrr-dashboard-template]] | Canonical MRR is the numeric trigger input. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: net MRR from provider report, 3+ consecutive month-ends, runway co-condition, reversal hysteresis, concentration and churn gates, pre-commit before threshold, provider-export evidence, dated conclusion, reviews with readings | ~2200 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the contract: header with version, commit date, post_hoc and change log, net MRR trigger from a named provider with threshold and 3+ month-end window, runway co-condition with burn components and months, concentration and churn gates, reversal below the trigger with a 2+ month window, dated conclusion with evidence links per month-end, reviews with readings, runway, gate values and verdict; valid and invalid contracts; 8 forbidden patterns | 4450 |
| `content/03-failure-modes.xml` | essential | 7 known failure modes with detector + repair | ~1300 |
| `content/04-procedure.xml` | essential | 8 steps: pin the metric to the provider report, set the threshold and window, compute the runway floor, set the gates, write the reversal clause, write the dated conclusion and evidence links, commit 1.0.0 before the threshold and validate, record readings and a verdict at every review | 1650 |
| `content/05-examples.xml` | recommended | Complete Stripe contract (4,000 USD for 3 month-ends, 12-month runway floor, gates at 20 and 5 percent, reversal at 3,000, committed in February, fired at the September review on 4,150 / 4,300 / 4,420) with a note per value, plus a post-hoc gross-cash contract and what the validator prints | 1900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold_contract` | haiku | Template fill from header + section list. |
| `populate_evidence` | sonnet | Per-section judgement: select correct evidence, summarise. |
| `outcome_review_synthesis` | opus | Cross-cycle synthesis: does the contract change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/contract-skeleton.md.j2` | Canonical contract sections (trigger / reversal / evidence / owner / review) |
| `templates/contract-skeleton.md` | Canonical contract sections (trigger / reversal / evidence / owner / review) Generated from `templates/contract-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, evidence_root |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-quit-day-job-trigger-contract.py` | Validate the filled contract against 02-output-contract schema | Pre-merge + quarterly review |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[side-project-financial-runway]]
- [[solo-mrr-dashboard-template]]
- [[solo-burnout-tripwires]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by trigger specificity, output shape, evidence presence, owner naming, and review staleness onto a rule from `content/01-core-rules.xml`. Walk it on every quarterly review.
