# Incident Decision Template

## Summary

**One-sentence:** Produces a 2-minute written incident-decision record — options considered, decision, blast radius, rollback trigger, owner — so calls made on voice during incidents stop vanishing the moment the bridge ends.

**One-paragraph:** Produces a 2-minute written incident-decision record — options considered, decision, blast radius, rollback trigger, owner — so calls made on voice during incidents stop vanishing the moment the bridge ends. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** incident commanders and on-call engineers making code / release / perf calls during a live incident who need a 2-minute written template to pin the decision before the bridge ends and memory fades.

## Applies If (ALL must hold)

- A named trigger has fired (release, incident, schedule, scope change) that warrants producing the artefact.
- The owner is a named person (role:handle), not a team alias or channel.
- The required input artefacts in `## Prerequisites` are available and machine-readable.
- The downstream consumer for the produced artefact is known (review board, CI gate, customer, regulator).

## Skip If (ANY kills it)

- Trigger is vague ("when needed", "soon"); rewrite the trigger first.
- No named owner — refuse to produce; assign first.
- Inputs are missing or non-deterministic; fix the upstream observability before applying.
- A different, already-pinned methodology handles this exact decision (avoid duplicate artefacts).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Trigger record | text / ticket link | upstream alerting / planning queue |
| Owner identity | `role:handle` string | RACI / org directory |
| Input artefacts | as listed in `02-output-contract.xml` `required` | upstream methodology output |
| Prior artefact (if exists) | JSON matching the output contract | repo `.product/incident-decision-template/` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | Step-by-step procedure with input/action/output | ~700 |
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
| `templates/skeleton.md` | Markdown skeleton of the artefact with all required sections. |
| `templates/header.yaml` | Frontmatter schema (owner, version, last_reviewed, trigger_url). |
| `templates/_smoke-test.json` | Minimum-viable filled JSON instance, parseable by the validator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-incident-decision-template.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
