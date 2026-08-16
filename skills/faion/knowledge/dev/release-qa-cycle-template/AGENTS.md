# Release QA Cycle Template

## Summary

**One-sentence:** End-to-end release QA cycle: strategy → smoke pack → bug bash → perf verdict → rollback triggers → go/no-go review, with stage gates and named owners.

**One-paragraph:** End-to-end release QA cycle: strategy → smoke pack → bug bash → perf verdict → rollback triggers → go/no-go review, with stage gates and named owners. Composes six methodologies into a single ordered cycle. Each stage has an owner, an exit criterion, and a documented decision. The cycle output is a go/no-go record. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Releases at least monthly with multiple stakeholders and a real production user base.
- QA stages happen but are not ordered/owned consistently; gaps cause incidents.
- Need an auditable release record for compliance, postmortems, or customer reports.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Releases at least monthly with multiple stakeholders and a real production user base.
- QA stages happen but are not ordered/owned consistently; gaps cause incidents.
- Need an auditable release record for compliance, postmortems, or customer reports.

## Skip If (ANY kills it)

- Continuous deploy with sub-1% blast radius per change — different control surface.
- Solo developer release.
- Pre-product with no user base — release cycle overhead has no payback.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Release notes draft | Markdown | PM |
| Release ticket | tracker URL | tracker |
| All sub-methodology outputs prior | various | QA team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[qa-test-strategy-template]] | Stage 1 produces the strategy. |
| [[qa-rc-smoke-pack-template]] | Stage 2 runs the smoke pack. |
| [[qa-bug-bash-runbook]] | Stage 3 runs the bug bash. |
| [[qa-perf-run-verdict-template]] | Stage 4 produces the perf verdict. |
| [[qa-rollback-trigger-canon]] | Stage 5 locks rollback triggers. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `orchestrate-cycle` | opus | Cross-cutting orchestration of 5 sub-methodologies. |
| `compose-decision` | sonnet | Synthesise go/no-go from stage outputs. |
| `file-record` | haiku | Mechanical commit of the cycle record. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cycle_record.json` | JSON template scaffolding the artefact contract. |
| `templates/retro.md.j2` | Markdown skeleton for the artefact. |
| `templates/retro.md` | Markdown skeleton for the artefact. Generated from `templates/retro.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-release-qa-cycle-template.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[qa-test-strategy-template]]
- [[qa-rc-smoke-pack-template]]
- [[qa-bug-bash-runbook]]
- [[qa-perf-run-verdict-template]]
- [[qa-rollback-trigger-canon]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Does this release have multiple stages with stakeholders and real users?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cycle_record.json`

```json
{
  "cycle_id": "rel-2026-05-23-v2.4",
  "release_id": "v2.4.0",
  "stages": [
    {
      "id": "strategy",
      "owner": "alice",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/strategy.md"
    },
    {
      "id": "smoke",
      "owner": "bob",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/smoke.yaml"
    },
    {
      "id": "bug_bash",
      "owner": "carol",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/bug-bash-ledger.csv"
    },
    {
      "id": "perf",
      "owner": "dave",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/perf-verdict.json"
    },
    {
      "id": "rollback_triggers",
      "owner": "eve",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/rollback-canon.yaml"
    },
    {
      "id": "go_no_go",
      "owner": "frank",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/go-no-go.md"
    }
  ],
  "decision": "go",
  "approver": "frank",
  "retro_note": "keep: smoke pack speed; change: bug-bash needs earlier kickoff.",
  "recorded_at": "2026-05-23T16:00:00Z"
}
```

### `templates/_smoke-test.json`

```json
{
  "cycle_id": "rel-2026-05-23-v2.4",
  "release_id": "v2.4.0",
  "stages": [
    {
      "id": "strategy",
      "owner": "alice",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/strategy.md"
    },
    {
      "id": "smoke",
      "owner": "bob",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/smoke.yaml"
    },
    {
      "id": "bug_bash",
      "owner": "carol",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/bug-bash-ledger.csv"
    },
    {
      "id": "perf",
      "owner": "dave",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/perf-verdict.json"
    },
    {
      "id": "rollback_triggers",
      "owner": "eve",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/rollback-canon.yaml"
    },
    {
      "id": "go_no_go",
      "owner": "frank",
      "outcome": "pass",
      "waiver_reason": null,
      "artefact_link": "release/v2.4/go-no-go.md"
    }
  ],
  "decision": "go",
  "approver": "frank",
  "retro_note": "keep: smoke pack speed; change: bug-bash needs earlier kickoff.",
  "recorded_at": "2026-05-23T16:00:00Z"
}
```
