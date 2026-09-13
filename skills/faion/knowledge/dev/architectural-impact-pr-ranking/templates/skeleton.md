<!--
purpose: Canonical skeleton for the `architectural-impact-pr-ranking` weekly report — one section per rule in content/01-core-rules.xml.
consumes: PR list for the window, git diff --name-status and --stat per PR, manifests, per-repo public API path lists, last session's hit / miss marks.
produces: A committed report at .product/architectural-impact-pr-ranking/<week>.md plus its JSON form validated by scripts/validate-architectural-impact-pr-ranking.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-architectural-impact-pr-ranking.py.
token-budget-impact: ~1200 tokens to fill for a week with N of 5.
-->
---
version: 0.1.0
window_from: <window_from>
window_to: <window_to>
session_slot: <session_slot>
time_box_minutes: <time_box_minutes>
ranker_run_url: <ranker_run_url>
---

# Header

- window: <window_from> to <window_to> (PRs opened or merged in the window; never state = open)
- repositories: <owner/repo: public API path list at <path> | no API surface list>
- session: <session_slot>; time_box_minutes <time_box_minutes>; top_n <n>; summed_read_minutes <m>
- signals_from_diff_only: true
- review_threshold: <score>
- previous_precision: <hits> of <n> = <value> (null on the first report)
- weights_changed: false | true (then fill Weight change)

# Weights

| Signal | Weight |
|---|---|
| modules_touched | <w> |
| public_api_delta | <w> |
| dependency_changes | <w> |
| contract_changes | <w> |
| infra_or_config_changes | <w> |

| Dependency kind | Weight |
|---|---|
| new_dependency | <w, above every patch bump> |
| major_bump | <w, above every patch bump> |
| minor_bump | <w> |
| patch_bump | <w, at most 0.5> |
| removal | <w> |
| lockfile_only | 0 |

## Weight change (only when weights_changed)

- previous_weights: <the five previous values>
- precision_weeks_cited: <at least 4>; precision_values: <four or more values>

# Ranked

| Rank | PR | Title (context only) | Score | modules | api delta | deps | contracts | infra/config | Changed lines | Read minutes | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | <owner/repo#n> | <title> | <score> | <n> | <n> | <n> | <n> | <n> | <lines> | <min> | pending |

# Deferred

| PR | Score | Changed lines | Read minutes |
|---|---|---|---|
| <owner/repo#n> | <score> | <lines> | <min> |

# Exclusions

| Rule | Count |
|---|---|
| population_total | <n> |
| bot_authors | <n> |
| reverts | <n> |
| docs_only | <n> |
| generated_files | <n> |
| below_threshold | <n> |

ranked + deferred + every exclusion count = population_total.

# Merged without architecture review

| PR | Score | Merged at | Merged by |
|---|---|---|---|
| <owner/repo#n> | <score> | <timestamp> | role:<handle> |

(print "none" explicitly when empty)

# Evidence

- <ranker_run_url>
- <public API path list URLs>
- <previous report URL>
