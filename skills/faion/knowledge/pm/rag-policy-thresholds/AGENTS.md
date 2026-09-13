# RAG Policy Thresholds

## Summary

**One-sentence:** A typed RAG (Red/Amber/Green) policy that pins numeric thresholds per signal (schedule variance, budget variance, defect escape rate, blocker count) so PM status reporting becomes a reproducible decision rule instead of weekly gut-call.

**One-paragraph:** PM status reporting is dominated by "I feel this is Amber" — bias, fatigue, and stakeholder pressure all push the colour. This methodology pins a `RAGPolicy` per project: named numeric inputs, published thresholds (no "significant" or "material" without a number), a default action per colour, and a quarterly review. Output is a typed decision-record that downstream stakeholder reports cite by version + last_reviewed. Refresh cadence ≤ 90 days; reviews remove unused thresholds and add new ones tied to incident history.

**Ефективно для:**

- Weekly PM client / leadership status reporting across multiple projects with consistent rules.
- Distressed-project rescue trigger (Red colour fires escalation playbook).
- Audit defensibility: every colour ties to a published numeric threshold.
- Quarterly review: thresholds tied to actual incident history, not vibes.

## Applies If (ALL must hold)

- Schedule and budget are tracked against a plan, so earned-value percent variances (SV%, CV%) can be computed from Jira, the finance export or a DORA dashboard.
- Each candidate signal has a system and a saved query, filter or export a second person can run for the same number.
- An incident, post-mortem, PMO tolerance policy or cohort baseline exists to anchor each threshold to.
- Status is reported on a recurring cadence (weekly or fortnightly) to a sponsor who will act on Red inside an hour bound.
- A named PM owns the policy, logs overrides under their own name and runs the review within 90 days.

## Skip If (ANY kills it)

- Fewer than three status reports a year, or a project that ends inside one cycle: a threshold policy costs more than the reports it governs.
- No plan to measure variance against (no baseline schedule or budget): schedule and budget signals cannot be percent variances, and those are the ones that matter.
- A client or regulator mandates its own status framework (PRINCE2 exception report, a contractual RAG annex): fill that scheme instead.
- The sponsor will not commit to an escalation path for Red: the colour has no consequence and the policy is decoration.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Baseline schedule and budget (PV per period, planned cost) for the earned-value variances | plan export | PM / finance |
| Signal sources: Jira dashboard or JQL, Sentry saved search, finance export name, DORA panel, with read access | saved query per signal | platform |
| Incident and post-mortem corpus with ids citable as `incident-<id>` / `postmortem-<id>` | Markdown | engineering |
| PMO tolerance policies citable as `policy://<path>` and cohort baselines citable as `baseline-<id>` | policy docs | PMO |
| Reporting calendar (cadence in days) and the sponsor's escalation path for Red | calendar invite, playbook name | PM / sponsor |
| Previous policy with its `colour_history` and `review_log` | JSON, this contract | this methodology (prior cycle) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[value-stream-management]] | Flow + DORA metrics feed RAG signal inputs. |
| [[team-morale-pulse-survey]] | eNPS / clarity feed the team-health signal. |
| [[proposal-red-team-checklist]] | Red trigger inputs into the next proposal's red-team. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: numeric thresholds with comparator, red beyond amber, queryable input source, worst signal wins, logged override never downgrades Red, evidence anchor per signal, time-bound Red action, 90-day review | ~2150 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for `RAGPolicy`: per-signal unit, system + query, comparator, numeric Amber / Red and anchors; Amber step with in-cycle deadline, Red playbook with hour bound firing at compute time; review and override log entries (Red never reported lower); colour history citing the policy version; valid + invalid examples, forbidden patterns | ~4750 |
| `content/03-failure-modes.xml` | essential | 6 modes: watermelon report, prose threshold, collapsed Amber band, opinion input source, Red without consequence, fossil thresholds | ~900 |
| `content/04-procedure.xml` | essential | 7 steps: header and cadence, signals as named queries in a unit, numeric thresholds with anchors, time-bound action per colour, validate and publish citing version, compute worst-signal colour each cycle with logged overrides, review within 90 days | ~1800 |
| `content/05-examples.xml` | recommended | Complete checkout policy with four signals, a logged data-glitch override and a Red fired inside 4 hours, a note per non-obvious value, and a bad policy with the validator output and what the sponsor sees | ~2600 |
| `content/06-decision-tree.xml` | essential | Tree: signal value vs threshold → colour + escalation rule | ~450 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `set-thresholds` | sonnet | Per-signal judgment anchored in incident history. |
| `compute-colour` | haiku | Mechanical threshold comparison. |
| `outcome-review-synthesis` | opus | Cross-quarter calibration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | RAG policy skeleton with default thresholds |
| `templates/skeleton.md` | RAG policy skeleton with default thresholds Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `RAGPolicy` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-policy-thresholds.py` | Validate `RAGPolicy`: numeric thresholds, named inputs, evidence, owner | Pre-merge |
| `scripts/staleness-check.py` | Flag policies whose `last_reviewed` > 90 days | Weekly cron |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[value-stream-management]]
- [[team-morale-pulse-survey]]
- [[regulatory-uncertainty-buffer]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps signal values to colour + default action — Green continues, Amber triggers PM review, Red triggers escalation playbook. Every leaf references a rule from `01-core-rules.xml`.
