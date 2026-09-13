# Geek-Tier Software Architect Skill Index

## Summary

**One-sentence:** Produces a curated geek-tier architect skill index — 50+ entries from sdlc-ai (spec-kit, plan-mode, RAG-for-arch, graph-reviewer) re-anchored from a software architect's point of view — closing the perceived coverage gap without authoring new content.

**One-paragraph:** Produces a curated geek-tier architect skill index — 50+ entries from sdlc-ai (spec-kit, plan-mode, RAG-for-arch, graph-reviewer) re-anchored from a software architect's point of view — closing the perceived coverage gap without authoring new content. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software architects opening Faion's geek tier for the first time who need a single index that maps existing sdlc-ai entries (spec-kit, plan-mode, RAG, graph reviewer) onto architecture tasks, not just dev tasks.

## Applies If (ALL must hold)

- The deliverable is an index over existing, active methodologies under skills/faion/knowledge — no new methodology bodies are to be written.
- The candidate targets (sdlc-ai, dev, sdd entries with an architecture angle) can be resolved against their meta.json for status and est_tokens.
- The reader is a software architect arriving with a task (boundary decision, ADR, view, review, drift), so clusters can be named by activity.
- A relink script can run in CI at the review cadence, so dangling slugs and stale est_tokens are caught before publication.

## Skip If (ANY kills it)

- The request is to author a new methodology; write it under its own slug first, then index it.
- Fewer than a handful of active targets have any architecture angle, so an index would be a shortfall block with no clusters; file the uncovered tasks as methodology requests instead.
- A current architect index already exists in the tier and passed its last relink; extend it in the same relink run rather than publishing a second one.
- The consumer is a developer looking for a tool-by-tool table of contents; the existing domain INDEX.xml files already serve that.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Candidate slug list | wikilink slugs with domain | sdlc-ai, dev and sdd domain INDEX.xml |
| Target metadata | meta.json per slug: status, est_tokens, summary | skills/faion/knowledge/<domain>/<slug>/meta.json |
| Architecture activity taxonomy | elicit, decide and record, document views, evaluate and review, govern drift | ISO/IEC/IEEE 42010 and this methodology's rules |
| Relink script and CI slot | script path plus a scheduled job at the review cadence | corpus scripts/ and CI |
| Uncovered-task requests | architecture tasks users asked for with no entry | support questions / tier feedback |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: entries resolve to active slugs, architect why not copied, clustered by activity, 50 distinct targets, fixed entry fields, uncovered tasks listed, relink at cadence | ~1600 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the index: activity-named clusters (tool names forbidden) with at least three entries, five fixed entry fields with slug pattern, non-copied architect_why, load_when, est_tokens and active status, entry_count with a mandatory shortfall block under 50, uncovered_tasks, relink run; a real 54-entry valid example and a five-entry invalid one | ~7650 |
| `content/03-failure-modes.xml` | essential | 6 subject-specific antipatterns with detector + repair | ~950 |
| `content/04-procedure.xml` | recommended | 7 steps: resolve slugs against meta.json, write architect_why and load_when, cluster by activity, count and record shortfall, list uncovered tasks, wire and run relink, validate and publish | ~1400 |
| `content/05-examples.xml` | recommended | Complete 54-entry index over active dev, sdd and sdlc-ai methodologies with notes on every non-obvious choice, plus the first five-entry draft breaking five rules and what the validator and reviewer say | ~6650 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~400 |

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
| `scripts/validate-architect-skill-index-geek-tier.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
