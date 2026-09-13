# Incident Decision Template

## Summary

**One-sentence:** Produces a 2-minute written incident-decision record — options considered, decision, blast radius, rollback trigger, owner — so calls made on voice during incidents stop vanishing the moment the bridge ends.

**One-paragraph:** Produces a 2-minute written incident-decision record — options considered, decision, blast radius, rollback trigger, owner — so calls made on voice during incidents stop vanishing the moment the bridge ends. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** incident commanders and on-call engineers making code / release / perf calls during a live incident who need a 2-minute written template to pin the decision before the bridge ends and memory fades.

## Applies If (ALL must hold)

- A decision is being made on a live incident bridge right now: mitigation, rollback, release hold, traffic shift.
- An incident commander (or a delegate named on the bridge) exists and can be recorded as `role:handle`.
- A scribe or the commander can type the record and commit it within 2 minutes of the call.
- A dashboard, alert or log query showing the affected system is open and its time range can be pinned in a URL.
- A postmortem date is set or will be set before the incident closes, so the record has a review date.

## Skip If (ANY kills it)

- The incident is over and this is a retrospective write-up; that belongs in the postmortem document, not an incident decision record.
- The change is planned rather than reactive (a migration, an architecture choice); write an ADR instead.
- No metric exists yet for the affected system, so a numeric rollback trigger cannot be written; page the observability owner first.
- The call is fully specified by an existing runbook step with its own rollback criteria; link the runbook in the incident timeline instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Incident ticket or PagerDuty incident | URL plus incident id | alerting / incident tooling |
| Commander and executor handles | `role:handle` | the bridge roster / on-call schedule |
| Dashboard with the incident window | URL with `from`/`to` (or equivalent) pinned | the dashboard open on the bridge |
| Rollback command or runbook | shell command or runbook URL | deploy tooling / runbook repo |
| Postmortem date | YYYY-MM-DD | incident process / calendar |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: record before bridge closes, options considered, blast radius quantified, rollback trigger measurable, one-sentence decision, commander as owner, timestamped evidence, review at postmortem | ~1650 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the incident decision record: incident trigger with decided_at / committed_at, commander as owner, named inputs (options_considered with do-nothing, blast_radius with a number, rollback_trigger as metric / threshold / window / rollback, executor, reconstructed), one-sentence decision, pinned evidence, review at the postmortem; valid and invalid records; 8 forbidden patterns | ~3150 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | 7 steps on the bridge: open the record, one-sentence decision, options including do-nothing, blast radius from the open dashboard, numeric rollback trigger, pin evidence and commit within 2 minutes, review at the postmortem | ~1350 |
| `content/05-examples.xml` | recommended | Complete INC-2417 record (sidecar disabled in eu-west-1, three options, 38% blast radius, helm rollback trigger, pinned Grafana and Slack links, postmortem outcome) with a note per value, plus the same call written the usual way and what the validator prints | ~1450 |
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
| `scripts/validate-incident-decision-template.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
