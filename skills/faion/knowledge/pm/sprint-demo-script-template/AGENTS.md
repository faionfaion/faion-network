# Sprint Demo Script Template (Senior-Dev-Runs-The-Demo Variant)

## Summary

**One-sentence:** A 45-minute sprint demo script for an outsource senior dev presenting to an executive client, where every acceptance criterion is presented with an explicit accept/reject prompt and the decision is captured before the next AC starts.

**One-paragraph:** Generic sprint review ceremonies assume a Scrum-Master-led, full-team format. P4 outsource engagements often have the senior developer alone with the client exec — no PM in the room, no team to absorb tough questions. This script replaces the "let me show you what we built" narration with a per-AC structured loop: state the AC verbatim → demonstrate it on the staging build → ask "accept / accept-with-defect / reject" → log the answer + named owner → only then move on. Output is a signed acceptance log the engagement manager can use for invoicing and for change-request triggering. Replaces the soft "any feedback?" close that historically gives outsource shops no defensible record.

**Ефективно для:**

- Outsource-розробник веде sprint demo з exec-клієнтом без PM у кімнаті.
- Кожен acceptance criterion потребує явного accept / accept-with-defect / reject рішення.
- Інвойсинг гейтиться signed acceptance log — без нього milestone billing не captured.

## Applies If (ALL must hold)

- Engagement is fixed-price or milestone-billed AND demos gate invoice approval.
- The senior developer (not a PM) is leading the demo for the client side.
- Sprint has at least one acceptance criterion with a verifiable demo path.
- Client has an exec-level signer attending (not a delegate without authority).

## Skip If (ANY kills it)

- Internal product where the team is also the customer — use a peer sprint review instead.
- Engagement is pure T&M with no milestone gate — over-engineered for the value at stake.
- Demo is a continuous "show me as you build" cadence, not a sprint-boundary review.
- Client refuses to sign anything during the meeting — the script's output is a signed log; without it, the artefact does not exist.

## Prerequisites

- List of acceptance criteria for the sprint, each with a numbered ID and a verifiable demo path.
- Staging build URL/credentials shared with the client at least 24h before the demo.
- Decision log file (`demos/sprint-NN-decisions.md`) created before the meeting starts.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/` | Acceptance criteria authoring conventions. |
| `pro/pm/client-status-report-multistyle` | Status reporting that consumes the demo log output. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-if` | sonnet | Decision tree application against typed inputs. |
| `gather-typed-inputs` | haiku | Mechanical fetch + source-pin. |
| `produce-artefact` | sonnet | Per-instance judgment; bounded inputs. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-demo-script-template.md.j2` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/sprint-demo-script-template.md` | Filled artefact skeleton conforming to 02-output-contract.xml Generated from `templates/sprint-demo-script-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/sprint-demo-script-template.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md.j2` | Minimum-viable filled-in version exercised by scripts/validate-sprint-demo-script-template.py --self-test |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-sprint-demo-script-template.py --self-test Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sprint-demo-script-template.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/pm/project-manager/`
- peer: `client-status-email-template-agency`, `cr-impact-memo-template`, `handover-pack-template-outsource`
- external: Scrum Guide 2020 §Sprint Review (baseline ceremony being specialised here)

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/sprint-demo-script-template.schema.json`

```json
{
  "__faion_header__": {
    "purpose": "JSON Schema for sprint-demo-script-template",
    "consumes": "validated against artefacts produced by the methodology",
    "produces": "schema document for validator script",
    "depends_on": "content/02-output-contract.xml",
    "token_budget_impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/sprint-demo-script-template.json",
  "type": "object",
  "required": ["artefact_id", "owner", "decision", "version", "last_reviewed", "inputs_used"],
  "properties": {
    "artefact_id": { "type": "string", "pattern": "^[a-z][a-z0-9-]+$" },
    "owner": { "type": "string", "minLength": 2 },
    "decision": { "type": "string", "minLength": 2 },
    "rationale": { "type": "string" },
    "version": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "last_reviewed": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$" },
    "inputs_used": { "type": "array", "items": { "type": "string" }, "minItems": 1 }
  }
}
```
