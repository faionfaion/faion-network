# Provider Deprecation Runbook

## Summary

**One-sentence:** Runbook for safe LLM provider/model deprecation — phased rollout, canaries, kill-switch, run-record so deprecation becomes a calendar item, not a fire.

**One-paragraph:** Providers deprecate on their own schedule (Anthropic retires models, OpenAI sunsets endpoints, Gemini bumps versions). Without a runbook, teams discover the deprecation at the 4xx error rate spike. This methodology produces a `provider-deprecation-runbook.json` artefact with phased steps (precondition / actor / action / artefact / rollback / phase budget) and a run-record schema. Output is consumable by ops automation; deprecation becomes a calendar event.

**Ефективно для:**

- Plan model deprecation як calendar item, не fire.
- Phased rollout: canary → 5% → 50% → 100%.
- Kill-switch + rollback path explicit на кожному step'у.
- Run-record schema для post-run audit.
- Coordinate cross-team handoffs (ML-eng → on-call → product).

## Applies If (ALL must hold)

- Production AI feature relies on a single provider/model.
- Deprecation calendar known (date or signalled).
- Named accountable owner + on-call escalation path.
- Repo hosts the versioned runbook.

## Skip If (ANY kills it)

- Multi-provider portability already locked (use rollback path of the portability spec).
- Provider has not announced deprecation AND no quarterly drill needed.
- Single-person team without on-call rotation.
- No named owner.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Deprecation announcement / date | text + url | provider docs |
| Current provider config | YAML | service repo |
| Replacement provider config (drafted) | YAML | service repo |
| Eval harness baseline | JSON | eval repo |
| Kill-switch hook | code reference | platform |
| Named accountable owner + on-call | strings | ownership log |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[prompt-portability-across-providers]]` | Spec defines the abstracted interface. |
| `[[prompt-portability-audit]]` | Pre-migration audit feed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for runbook + run-record | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns | ~900 |
| `content/04-procedure.xml` | essential | 5-step: announce → canary → 5% → 50% → 100% with kill-switch | ~800 |
| `content/05-examples.xml` | essential | Worked example: Claude Opus 3.x → 4.7 deprecation | ~700 |
| `content/06-decision-tree.xml` | essential | Routes deprecation state to phase | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-runbook` | sonnet | Step-list judgment with rollback per step. |
| `compute-phase-budgets` | haiku | Mechanical timing. |
| `incident-response` | opus | Live triage under stress. |

## Templates

| File | Purpose |
|------|---------|
| `templates/provider-deprecation-runbook.json` | JSON skeleton matching 02-output-contract. |
| `templates/provider-deprecation-runbook.md` | Narrative runbook template. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-provider-deprecation-runbook.py` | Validate runbook | Pre-commit + before deprecation day |

## Related

- [[prompt-portability-across-providers]]
- [[prompt-portability-audit]]
- [[prompt-pr-review-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree picks the current phase (precondition / canary / 5% / 50% / 100%) based on canary-eval delta + error rate. Walk it before every phase transition.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/provider-deprecation-runbook.json`

```json
{
  "artefact_id": "deprecate-<model>-<period>",
  "owner": "<handle>@faion.net",
  "on_call": "ml-oncall-rotation",
  "deprecation_date": "2026-09-01",
  "phases": [
    {
      "name": "canary",
      "budget_min": 60,
      "steps": [
        {
          "id": "s1",
          "precondition": "replacement config ready",
          "actor": "ml-engineer:platform",
          "action": "flip 1% traffic to replacement",
          "artefact": "ops-dashboard-url",
          "rollback": "set traffic_share=0; clear cache"
        }
      ]
    },
    {
      "name": "5pct",
      "budget_min": 240,
      "steps": [
        {
          "id": "s2",
          "precondition": "canary green",
          "actor": "ml-engineer:platform",
          "action": "raise to 5%",
          "artefact": "ops-dashboard-url",
          "rollback": "rollback to 1%"
        }
      ]
    },
    {
      "name": "50pct",
      "budget_min": 720,
      "steps": [
        {
          "id": "s3",
          "precondition": "5pct green",
          "actor": "ml-engineer:platform",
          "action": "raise to 50%",
          "artefact": "ops-dashboard-url",
          "rollback": "rollback to 5%"
        }
      ]
    },
    {
      "name": "cutover",
      "budget_min": 240,
      "steps": [
        {
          "id": "s4",
          "precondition": "50pct green",
          "actor": "ml-engineer:platform",
          "action": "raise to 100% + commit run-record",
          "artefact": "git://<repo>/run-records/<file>.json",
          "rollback": "rollback to 50%"
        }
      ]
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
