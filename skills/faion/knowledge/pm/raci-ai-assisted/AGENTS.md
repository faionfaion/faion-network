# RACI AI Assisted

## Summary

**One-sentence:** AI-assisted RACI matrix builder: ingests project charter + WBS + team roster, emits a typed `RACIMatrix` with exactly-one A per row, flags orphaned R's and duplicate A's, and refreshes when the roster changes.

**One-paragraph:** The corpus covers RACI as a static doc but not the methodology that drafts, validates, and refreshes one. Without the loop, RACI rots within 4 weeks of project start. This methodology pins it: trigger fires on (a) project kickoff, (b) roster change, (c) quarterly review. Output is a typed `RACIMatrix` mapping each WBS-leaf id to {responsible[], accountable, consulted[], informed[]} with named-owner discipline, exactly one A per row, and evidence anchor per assignment (charter line, WBS dictionary entry, or stakeholder register row). Refreshed on roster delta; quarterly review removes orphaned entries.

**Ефективно для:**

- Multi-team coordination & dependency-graph reasoning (P6-product context).
- Roster onboarding / offboarding triggering RACI delta.
- Audit: every WBS leaf has exactly one accountable role.
- Quarterly review removing dead rows + flagging duplicates.

## Applies If (ALL must hold)

- A WBS spec from [[wbs-creation]] exists with leaf ids of the form `2.1` / `2.1.3` and an open / closed state per leaf; rows bind to open leaves only.
- A team roster names a role id and a person per entry, and HR or the stakeholder register posts joins, leaves and role changes with an effective date.
- The project charter, WBS dictionary or stakeholder register can be cited by section, entry or row as the anchor for an accountable assignment.
- One of the three triggers has fired: kickoff, a roster delta, or the quarterly date (`last_reviewed` approaching 90 days).
- A named PM owns the matrix, confirms `proposed` rows and can post to the team channel where R / A holders receive their rows.

## Skip If (ANY kills it)

- No WBS with leaf ids, or the work is tracked as a flat task list: there is nothing to bind rows to; build the WBS first.
- The project closes within one quarter and the roster will not change: a single hand-written RACI table, not a refreshed artefact.
- A regulated or client-mandated accountability format (RASCI, DACI, a contract annex) is imposed: fill that format instead.
- The roster has no stable role ids (everyone is "the team"): the exactly-one-A rule cannot be satisfied until roles exist.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project charter with section ids citable as `charter#<section>` | Markdown | sponsor |
| WBS spec: leaf ids matching `^[0-9]+(\.[0-9]+)*$`, parent / child structure, open / closed state per leaf, WBS dictionary entries citable as `wbs-dict#<id>` | JSON | [[wbs-creation]] |
| Team roster: role id + person per entry, as of the trigger date | YAML | HR / stakeholder register |
| Roster delta notice: person, role id, join / leave / role change, effective date | HR message or register row | HR / stakeholder register |
| Stakeholder register rows citable as `stakeholders#<row>` | table | PM |
| Prior `RACIMatrix` (rows, `review_log`) for carry-forward and the delta diff | JSON, this contract | this methodology (prior cycle) |
| Team channel where R / A holders are notified | chat channel name | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[wbs-creation]] | RACI rows reference WBS-leaf ids. |
| [[team-development]] | Skills matrix informs viable role assignments. |
| [[proposal-red-team-checklist]] | RACI inconsistencies surface during proposal red-team. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: exactly one A per row, roles in roster, rows bind to WBS leaves, anchor per assignment, trigger enum and roster-delta deadline, one column per role, notify on publish, 90-day review | ~1950 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for `RACIMatrix`: roster and open-leaf snapshot, one row per leaf with a single role-id A, anchors and `anchored` / `proposed` / `orphaned` status, roster-delta diff with deadline, publish notification record and quarterly counts; valid + invalid examples, forbidden patterns | ~4150 |
| `content/03-failure-modes.xml` | essential | 7 modes: cargo-cult, ownership ambiguity, drift, example-text leakage, no outcome review, trigger drift | ~1300 |
| `content/04-procedure.xml` | essential | 8 steps: confirm trigger and snapshot inputs, scaffold one row per open leaf, assign a single anchored A, fill R / C / I one column per role, apply the roster delta before the deadline, validate, publish and notify every R / A holder, quarterly review within 90 days | ~1850 |
| `content/05-examples.xml` | recommended | Complete checkout matrix refreshed on a security-lead departure with a note per non-obvious value, and a bad matrix with the validator output and what the PM sees beyond it | ~1950 |
| `content/06-decision-tree.xml` | essential | Tree: trigger present? owner named? evidence? per-row A count? → action + rule | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `raci-scaffold` | haiku | Mechanical fill from WBS rows + roster. |
| `raci-assign-A` | sonnet | Per-row judgment on the single accountable role. |
| `raci-validate` | haiku | Mechanical exactly-one-A + orphaned-R check. |
| `outcome-review-synthesis` | opus | Cross-quarter synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | RACI matrix skeleton with not_applicable markers |
| `templates/skeleton.md` | RACI matrix skeleton with not_applicable markers Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum-viable filled `RACIMatrix` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-raci-ai-assisted.py` | Validate `RACIMatrix`: exactly-one-A, evidence anchors, owner | Pre-merge |
| `scripts/staleness-check.py` | Flag matrices whose `last_reviewed` exceeds 90 days | Weekly cron |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[wbs-creation]]
- [[team-development]]
- [[proposal-red-team-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (trigger fired, owner named, A-count per row, evidence presence, staleness) to run / suppress / repair-A / refresh. Every leaf references a rule from `01-core-rules.xml`.
