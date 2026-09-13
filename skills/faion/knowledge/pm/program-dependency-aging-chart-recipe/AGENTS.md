# Program Dependency Aging Chart Recipe

## Summary

**One-sentence:** Builds a program-dependency aging chart (count-of-blocked-tasks vs days-since-dependency-opened) so program managers spot dependency rot before milestones slip.

**One-paragraph:** Builds a program-dependency aging chart (count-of-blocked-tasks vs days-since-dependency-opened) so program managers spot dependency rot before milestones slip. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** Програмному PM-у — щоб залежність, яка 'тихо лежить' три тижні, не зривала milestone у 6-му.

## Applies If (ALL must hold)

- At least 3 teams exchange dependencies that exist as typed `blocks / is blocked by` links in one tracker (Jira, Linear, GitHub Projects), each with producer team, consumer team, type and a link creation timestamp.
- A typed dependency graph (from `dependency-graph-reasoning`) gives the downstream task count per edge, and milestones carry dates that edges can be `needed_by`.
- A weekly checkpoint on a fixed weekday consumes the chart, and a script with tracker API access can regenerate it before each one.
- A named program PM owns the chart and can move a milestone, cut scope or swap a producer team when an edge crosses the top band.

## Skip If (ANY kills it)

- One team, or dependencies that live only in standups and chat with no tracker link — there is no `opened_at` to age from.
- No dependency graph and no milestone dates — blocked-task counts and slack cannot be computed, so the y-axis and the red override are guesses.
- The checkpoint is monthly or ad hoc — a 14-day escalation band is crossed twice between two readings.
- The program cannot fix its age bands (they are renegotiated whenever the chart looks bad) — week-over-week comparison is the whole value.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Typed dependency graph with producer, consumer, type and downstream tasks per edge | JSON or Mermaid | `dependency-graph-reasoning` output |
| Open `blocks / is blocked by` links with creation timestamps, and closed links with resolution dates | tracker API export from a saved query | Jira / Linear / GitHub Projects |
| Milestone dates per consuming team (the `needed_by` of each edge) | program plan or roadmap | program PM |
| Adopted age bands and adoption date (default 0-7, 8-14, 15-28, over 28) | header of the previous artefact, `templates/header.yaml` | program PM, set once at adoption |
| Previous weeks' resolved log (for the 12-week SLE) | JSON artefact matching `content/02-output-contract.xml` | last week's chart artefact |
| Weekly checkpoint weekday | calendar | program rituals |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/pm/dependency-graph-reasoning` | Source of the typed dependency graph. |
| `geek/pm/okr-cascade-team-to-company` | Cross-team OKR dependencies surface here too. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the weekly chart artefact: program PM as owner, chart date on the checkpoint weekday with query and extraction time, bands fixed at adoption, edges with producer / consumer / type / opened_at / needed_by / link id / blocked tasks / age / band / slack / superseded_from, owned and dated actions from the second band, re-baseline in the top band, red-first action table, resolved log, p85 SLE; valid and invalid artefacts; 8 forbidden patterns | ~4850 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | recommended | 8 steps by script before each checkpoint: extract typed edges, age from opened_at in adopted bands, inherit age on re-ticketed edges, count blocked tasks and slack, sort red-first, assign actions and re-baseline, append resolved log and SLE, publish and close | ~1700 |
| `content/05-examples.xml` | recommended | Complete Monday chart for a five-team checkout program (48-day contract with cut-scope, young red edge first, re-ticketed review keeping its age, twelve resolved edges giving a 33-day SLE) with a note per value, plus the same week as usually shown and what the validator prints | ~2800 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `age-band-compute` | haiku | Pure age math against graph timestamps. |
| `remediation-action-pick` | sonnet | Bounded judgement per edge. |
| `ritual-narrative` | opus | Cross-band synthesis for program review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Checkpoint page for the weekly chart: header with query, extraction time and adopted bands, the chart image, the red-first action table with owner and due date per escalated edge, re-baseline decisions, re-ticketed edges, resolved log and SLE. |
| `templates/skeleton.md` | Checkpoint page for the weekly chart (header, chart image, red-first action table, re-baseline decisions, resolved log, SLE). Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Header block of the artefact: program, owner, chart_date, checkpoint_weekday, tracker_query, extracted_at, age_bands, bands_adopted_on. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-program-dependency-aging-chart-recipe.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[dependency-graph-reasoning]]
- [[okr-cascade-team-to-company]]
- [[portfolio-evm-rollup-method]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to plot the chart weekly (graph + ≥3 teams + weekly cadence + PM), block (no graph), or skip (single team / sparse cadence). Run before the chart is added to the program ritual.
