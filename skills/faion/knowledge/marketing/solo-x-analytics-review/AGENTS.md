# Solo X Analytics Review

## Summary

**One-sentence:** Produces a 20-minute weekly X analytics report (5 fixed metrics + 3x-baseline outlier rule + one named next-week experiment) for indie audience growth.

**Ефективно для:** Indie operators using X as the primary audience channel where 'engagement isn't compounding' because there's no weekly diagnostic rhythm and the wrong metrics get tracked.

**One-paragraph:** `plausible-analytics` covers site traffic, not platform analytics. An indie hacker using X as the primary audience channel needs a specialised weekly review that surfaces what kind of post the algorithm is rewarding for THEM right now, separates outliers from baseline, and converts the review into exactly one named experiment for the following week. This methodology fixes the five metrics (impressions, profile visits, follows, replies-from-strangers, link clicks), the outlier-detection rule (≥3x trailing-4-week median), and the experiment-naming convention.

## Applies If (ALL must hold)

- X / Twitter is the primary audience channel.
- Operator posts at least 4 times/week.
- There are at least 4 weeks of data to compare against.
- Operator wants audience-growth or product-pipeline outcomes (not vanity follows).

## Skip If (ANY kills it)

- Operator posts <4 times/week — sample size too small.
- X is a secondary channel — invest review time elsewhere.
- Goal is vanity follows; this rubric will reject the metric.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| X analytics CSV/JSON export (last 4 weeks) | csv | X analytics dashboard |
| trailing-4-week median per metric | computed table | self-managed |
| posting log with timestamps + hooks | list | internal log |
| named operator (single account owner) | name + handle | founder |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/single-operator-funnel-rubric` | Adjacent solo metrics rhythm. |
| `solo/marketing/smm-manager/growth-twitter-x-growth` | Growth playbook this review feeds. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `compute_outliers` | haiku | Deterministic 3x-baseline filter. |
| `draft_next_week_experiment` | sonnet | Hypothesis + variable + success metric. |
| `review_qualified_followers` | opus | Quality judgement on follower mix. |

## Templates

| File | Purpose |
|---|---|
| `templates/solo-x-analytics-review.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/solo-x-analytics-review.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-solo-x-analytics-review.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[single-operator-funnel-rubric]] — paired Friday rhythm.
- [[growth-twitter-x-growth]] — growth playbook downstream.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
