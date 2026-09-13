# RFC Template for Product Dev Team

## Summary

**One-sentence:** Produces a product-dev RFC artefact — problem, options, decision, blast radius, rollback, owner, review cadence — that pins the 3–6-week feature-delivery loop into a reviewable, versioned record.

**One-paragraph:** Produces a product-dev RFC artefact — problem, options, decision, blast radius, rollback, owner, review cadence — that pins the 3–6-week feature-delivery loop into a reviewable, versioned record. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** tech leads on a product-dev team running 3–6-week features who need a fixed RFC shape with named owner, evidence anchors, and a published outcome review — not a free-form Notion doc.

## Applies If (ALL must hold)

- The change takes more than a few engineer-days and touches a shared service, a data schema, a public API or another team's code.
- A metric that describes the problem exists on a dashboard or query today, so current value, target and date can be written down.
- The work fits in one 3 to 6 week cycle, or can be split into RFCs that each ship alone.
- Owners of every touched service, store and API can be named as `role:handle` and given a comment deadline.
- A staging environment exists where the rollback can be exercised before review.

## Skip If (ANY kills it)

- The change lives inside one team's own code with no shared surface; write a ticket with a PR, not an RFC.
- There is no measurable problem metric and none can be instrumented first; an RFC without a number cannot be reviewed or outcome-checked.
- The change is an emergency mitigation on a live incident; use the incident decision record and write the RFC afterwards if the fix stays.
- An accepted RFC already covers the same problem and metric; a change of decision is a superseding RFC, not a new one on the same problem.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Problem metric | dashboard or query URL with current value, target and date | observability / product analytics |
| Service map and PR diff | list of services, data stores, APIs, jobs and user segments the change touches, with owners | architecture docs / repo |
| Staging rollback run | CI or runbook run URL showing the rollback executed, with its duration | staging environment |
| Traffic and tenant counts | percent of traffic, tenant count, API consumer count per user-facing item | analytics / API gateway |
| Reviewer handles | `role:handle` for every blast-radius owner | org directory / service catalogue |
| Prior RFC on the same problem | URL, or none | `.product/rfc-template-product-dev-team/` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: problem with metric + target, two options with rejection reasons, blast radius enumerated, rollback named + tested, scope fits one cycle, decision status + supersession, reviewers + deadline, outcome review re-measures metric | ~2100 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the RFC: problem with metric / current / target / date and no solution, two or more options with one chosen and rejection reasons, enumerated blast radius with owners and four flags, rollback with mechanism / minutes / executor / staging run / points of no return, dated milestones inside 42 days, status, decided_on, reviewers with commented flag, comment deadline, one-sentence decision, supersession links, outcome review re-measuring the metric; valid and invalid RFCs; 8 forbidden patterns | ~5350 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | ~1200 |
| `content/04-procedure.xml` | recommended | 9 steps: state the problem as a metric, options with rejection reasons, enumerate blast radius, name and test rollback, date milestones inside six weeks, name reviewers with deadline, decide and set status, supersede not edit, outcome review re-measures the metric | ~1650 |
| `content/05-examples.xml` | recommended | Complete RFC-118 (checkout p95 2.4 s to 1.2 s: three options, five blast-radius items with owners, flag-off rollback exercised in staging, three milestones in five weeks, accepted after the deadline, outcome 1.1 s met) with a note per value, plus the 'move to GraphQL' RFC and what the validator prints | ~2300 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~750 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Parse inputs + check preconditions | haiku | Mechanical schema parse. |
| Author the artefact body | sonnet | Bounded synthesis from typed inputs. |
| Review for compliance + cross-cutting impact | opus | Cross-input judgement when stakes are high. |
| Outcome-review synthesis at cadence | opus | Did the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown skeleton of the artefact with all required sections. |
| `templates/skeleton.md` | Markdown skeleton of the artefact with all required sections. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum-viable filled JSON instance, parseable by the validator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rfc-template-product-dev-team.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
