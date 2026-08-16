# Feature Flags for Trunk-Based Development

## Summary

**One-sentence:** Emits a per-flag spec artefact that wraps every incomplete-feature merge: id, owner, type (release / experiment / ops / permission), ramp plan, cleanup-ticket reference, and expiry SLA.

**One-paragraph:** Trunk-based development requires merging incomplete work daily — the only safe way to do that is behind feature flags. This methodology turns the "we put it behind a flag" wave of the hand into a deterministic artefact: every flag has an id, owner, type, ramp plan, kill-switch behavior, and a cleanup ticket filed at creation with a 30-day-after-100% SLA. Keystone Interface (build incrementally without exposing) and Dark Launch (test with live traffic before users see) are sub-types of the same artefact. Flags older than SLA without cleanup block the owner from creating new flags.

**Ефективно для:**

- Solo / outsource dev shipping incomplete work to trunk daily; needs the flag-discipline that prevents an unbounded flag pile.
- Team adopting TBD where one flag = one task = one cleanup ticket.
- AI-assisted dev — the LLM writes the flag check and the cleanup ticket in one go.
- Dark-launch backend rewrites where production traffic must hit new code before users do.

## Applies If (ALL must hold)

- A feature requires more than one commit (multi-day) — wrap each increment behind a flag.
- You want production traffic on new backend logic before exposing users → Dark Launch.
- A multi-step build where only the final wire-up exposes functionality → Keystone Interface.
- The team has a flag service (LaunchDarkly, Unleash, OpenFeature, or a config-driven home-grown one).

## Skip If (ANY kills it)

- No flag infrastructure and no plan to add one (see `feature-flags-types-lifecycle` before this).
- Mobile/desktop release gating where store review is the exposure gate, not a flag.
- One-commit feature completable same day with full tests.
- Codebase with no automated tests — broken flag state produces silent failures with no safety net.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Flag service handle | URL / config | infra |
| PR + ticket | text | tracker |
| Owner email | string | tracker |
| Ramp plan | text | author |
| Cleanup ticket id | string | tracker |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/trunk-based-dev-principles` | The umbrella branching model this flag-spec serves. |
| `solo/dev/behavior-parity-verification` | Dark-launch flags are how the shadow router is gated. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: one-flag-per-task, owner + SLA, ramp plan present, kill-switch arms, cleanup ticket linked, run-the-checklist + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for flag spec + valid/invalid + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: zombie flags, no-owner, no-cleanup-ticket, kill-switch untested | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: spec → wrap → pilot ramp → 100% → cleanup | 700 |
| `content/05-examples.xml` | reference | Worked example of a dark-launch flag for the shadow router | 500 |
| `content/06-decision-tree.xml` | essential | Tree: flag type? → spec fields required → verdict approve/block | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-flag-spec` | sonnet | Authoring task: name + owner + type + ramp text. |
| `validate-spec` | haiku | Schema check + cleanup-ticket existence lookup. |
| `aging-report` | haiku | Daily scan: flags past SLA without cleanup. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trunk-based-feature-flags.json` | JSON Schema for the flag-spec artefact. |
| `templates/flag-spec.md.j2` | Markdown skeleton the author fills before merge. |
| `templates/flag-spec.md` | Markdown skeleton the author fills before merge. Generated from `templates/flag-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trunk-based-feature-flags.py` | Validate a flag-spec JSON against the schema and cleanup-ticket rule. | On PR open; on flag creation; nightly aging scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trunk-based-dev-principles]] — the umbrella branching model.
- [[behavior-parity-verification]] — dark-launch flag is the shadow router's switch.
- [[ci-quality-gate-design]] — the CI gate that blocks PRs with missing flag-spec.

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks the flag's declared type (release / experiment / ops / permission) — each type requires a different field set. It then verifies ramp plan presence, cleanup-ticket link, and kill-switch arming. Leaves emit `approve`, `block-missing-cleanup-ticket`, `block-missing-ramp-plan`, or `block-zombie-flag-quota-exceeded`. Each leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/trunk-based-feature-flags.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/trunk-based-feature-flags.json",
  "type": "object",
  "required": [
    "artefact_id",
    "flag_id",
    "owner_email",
    "type",
    "ramp_plan",
    "kill_switch_tested",
    "cleanup_ticket_id",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^ff-[a-z0-9-]{6,}$"
    },
    "flag_id": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_.]{3,63}$"
    },
    "owner_email": {
      "type": "string",
      "format": "email"
    },
    "type": {
      "enum": [
        "release",
        "experiment",
        "ops",
        "permission"
      ]
    },
    "ramp_plan": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "pct",
          "gate"
        ],
        "properties": {
          "pct": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
          },
          "gate": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    },
    "kill_switch_tested": {
      "type": "boolean"
    },
    "kill_switch_test_run_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "cleanup_ticket_id": {
      "type": "string",
      "minLength": 1
    },
    "cleanup_sla_date": {
      "type": "string",
      "format": "date"
    },
    "dark_launch": {
      "type": "boolean"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```
