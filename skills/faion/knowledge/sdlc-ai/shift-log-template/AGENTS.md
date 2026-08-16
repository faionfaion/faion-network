# Shift Log Template

## Summary

**One-sentence:** Produces a per-shift handover log: what changed, what's open, what the next operator must touch first.

**One-paragraph:** Multi-shift / multi-agent operations rot when handover is verbal. This methodology pins the shift-log template: changes (diffs + commits), open incidents, pending decisions, blocked dependencies, and the explicit 'pick-up first' pointer for the next operator. Output is one log per shift, validated against the schema before close-out.

**Ефективно для:**

- Solopreneur operator handing off to NERO overnight (or vice versa).
- Multi-agent pools where each agent inherits previous state with zero verbal context.
- Incident-on-call rotations — log makes the next responder productive in minutes.
- Audit trail: shifts close with a known artefact, not a Slack thread.

## Applies If (ALL must hold)

- Operator (human or agent) is wrapping up a shift / session.
- There exists at least one in-flight change, open incident, or pending decision.
- Next operator is named and reachable.

## Skip If (ANY kills it)

- Idle shift with no state change — use a one-line 'no-op' log.
- Brand-new project with no prior shift — use the bootstrap form, not this.
- Fully automated pipeline with deterministic state — no handover needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Shift window | ISO start/end timestamps | operator |
| Commits / diffs in window | git log --since/--until | git |
| Open incidents | incident tracker entries | tracker |
| Pending decisions | decision-record drafts | internal |
| Next operator | name + handle | rotation calendar |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| methodology-versioning-and-changelog | Logs may reference methodology versions touched during the shift. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: log-required, next-operator-named, pickup-first-explicit, open-items-stated, no-leaky-secrets | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the shift-log record + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: missing-log, vague-pickup, secret-leak, unreachable-next-operator, stale-open-items | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: collect → group → name pickup → scrub secrets → publish | 800 |
| `content/06-decision-tree.xml` | essential | Maps state signals (open items > 0? secrets in diff? next operator reachable?) to publish / block / clean-up | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect-changes` | haiku | Mechanical scrape of git + tracker. |
| `draft-log` | sonnet | Per-item summary with judgement on what matters. |
| `secret-scrub` | haiku | Regex-based scrub before publish. |

## Templates

| File | Purpose |
|------|---------|
| `templates/shift-log.md.j2` | Markdown skeleton with required sections. |
| `templates/shift-log.md` | Markdown skeleton with required sections. Generated from `templates/shift-log.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/shift-log.json` | JSON skeleton matching the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shift-log-template.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[methodology-versioning-and-changelog]]
- [[methodology-contribution-flow-open-authorship]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/shift-log.json`

```json
{}
```
