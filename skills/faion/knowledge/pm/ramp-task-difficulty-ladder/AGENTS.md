# Ramp Task Difficulty Ladder

## Summary

**One-sentence:** Pins the ramp-task difficulty ladder for a product-dev team to a fixed shape (named trigger, bounded output, evidence anchors, named owner, outcome review) so onboarding stops being folklore and becomes a reviewable, owned, version-controlled operating tool.

**One-paragraph:** In project / programme management, the product-dev team runs "hire + onboard a new dev in 2 weeks" on a recurring cadence — but the corpus only covers the upstream concepts, not the artefact that closes the loop. Generic backlog selection produces inconsistent ramp quality, so onboarding buddies fall back to gut feel. `ramp-task-difficulty-ladder` pins the artefact: a fixed shape, named owner, evidence anchors, and a published review cadence. It is loaded when the product-dev team starts a hiring sprint and produces a committed artefact reviewed against onboarding outcomes at the next iteration. Mechanism: rule-bound output contract + per-application evidence + outcome review. Primary output: a versioned, owned, evidence-anchored ladder spec committed to the team's knowledge space.

**Ефективно для:** product-dev team lead, що хоче зробити 2-тижневий ramp нового розробника передбачуваним замість фольклорного.

## Applies If (ALL must hold)

- The team hires at least 3 developers a year onto a fixed ramp window (10 working days for a 2-week ramp) with a signed hire and a known start date.
- At least one previous newcomer has merged a PR on the production repo, with its actual duration recoverable, to anchor rung 1.
- The repository has observable scope markers a buddy can count: files, modules, a feature-flag mechanism and a design-review rule.
- The tracker supports labels (for example `ramp/rung-1`) and the sprint can reserve at least 2 tickets per rung off the committed scope.
- A named tech lead owns the ladder and a buddy is assigned per hire to pair on rung 1 and fade up the ladder.

## Skip If (ANY kills it)

- Fewer than 3 hires a year: write a one-off onboarding doc; the quarterly regrade costs more than the ramps it calibrates.
- No previous newcomer has merged anything on the production repo: every band would be a whiteboard guess; run one ad-hoc ramp first and come back with its PRs.
- Ramp tasks cannot be reserved off the sprint's committed scope (every ticket carries a delivery deadline): rungs 1 and 2 will be cannibalised on day one.
- The team's work has no code to merge to main (research, pure ops rotation): rung 1 as a merged change does not exist; use a shadowing plan instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Signed hire with start date and the ramp window length in working days | ATS record / calendar | HR or hiring manager |
| Merged PRs or closed tickets by previous newcomers, with actual durations, one per rung where available | PR urls or ticket ids | git hosting / tracker |
| Repository scope markers: module map, feature-flag mechanism, design-review rule | repo docs | tech lead |
| Backlog with at least 2 candidate tickets per rung taggable `<prefix><rung>` and reservable off the committed sprint scope | issue list (Jira / Linear / GitHub Issues) | team backlog |
| Named owner (`role:person`) and the buddy assigned to the hire | team roster | tech lead |
| Previous ladder version with its `ramps[]` and `outcome_review` | JSON, this contract | this methodology (prior cycle) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |
| `pro/pm/project-manager` | Upstream PM operating cadence the artefact slots into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: rungs by observable scope, monotonic durations with rung 1 under a day, rung 1 merges to main, buddy support fades, evidence is a prior ramp, tickets tagged before start date, no rung skip, outcome review regrades | ~2200 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for `RampLadder`: header with ramp window, cadence and label prefix; 4+ rungs by files / modules / flag / design-review scope with duration bands, fading buddy support, prior-newcomer evidence or `not_applicable: unvalidated`, 2+ tagged tickets; per-newcomer progressions with reclassification; outcome review with per-rung regrade; valid + invalid examples, forbidden patterns | ~6200 |
| `content/03-failure-modes.xml` | essential | 6 modes: story points as rungs, sandbox rung 1, rung skip under pressure, cannibalised ramp backlog, support never fades, whiteboard durations | ~900 |
| `content/04-procedure.xml` | essential | 8 steps: header and ramp window, rungs by observable scope, duration bands, fading buddy support, evidence from a completed prior ramp, tickets tagged before the start date, ramp run rung by rung with overrun reclassification, regrade at the outcome review | ~1800 |
| `content/05-examples.xml` | recommended | Complete five-rung payments ladder after two ramps and a review that rewrote rung 3, a note per non-obvious value, and a bad ladder with the validator output and what the tech lead sees | ~4000 |
| `content/06-decision-tree.xml` | essential | Decides whether the team is ready to commit to a versioned ladder vs ad-hoc onboarding | ~450 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change onboarding behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Canonical section list with `not_applicable: <reason>` markers per section. |
| `templates/skeleton.md` | Canonical section list with `not_applicable: <reason>` markers per section. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, ramp_window_days, review_cadence, rung_label_prefix. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ramp-task-difficulty-ladder.py` | Validate that filled artefact matches the canonical schema, carries evidence links, owner, and not-stale `last_reviewed`. | Pre-merge and quarterly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[stakeholder-sentiment-tracker]] — sibling operating artefact for the same PM space.
- [[team-charter-working-agreement]] — peer methodology shaping how the team operates around the ladder.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first asks whether the team has named-owner + evidence + ≥3 hires/year. If yes → fill the ladder spec; if no → skip the methodology and write a one-off onboarding doc instead. Run the tree the moment the product-dev team lead starts a hiring sprint — before they pull tickets from the backlog by hand.
