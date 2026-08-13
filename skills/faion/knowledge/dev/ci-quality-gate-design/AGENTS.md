# CI Quality Gate Design

## Summary

**One-sentence:** An opinionated three-tier design (BLOCK / WARN / NIGHTLY) plus a per-PR time budget that stops teams from re-inventing which checks should fail the build versus comment on it.

**One-paragraph:** Every new project re-debates "should mutation testing block merge?" / "is 90% coverage a gate?" / "should the security scan fail on medium?". The result is either over-blocking (PRs sit for 25 minutes for low-signal checks) or under-blocking (security and contract tests run in a tab nobody opens). This methodology pins a three-tier classification (BLOCK = must pass, WARN = surfaces a comment, NIGHTLY = runs on schedule with alert) and a per-PR wall-clock budget (target &lt; 10 min, ceiling 15 min for solo teams). It also enforces a written tier rationale per check, so future debates start from "what changed?" not from scratch. Output: ci-design.md artefact committed alongside the CI config, reviewed when gates change.

**Ефективно для:**

- Solo dev hitting "CI takes 25 min and I don't know why" — the artefact surfaces the offenders.
- Outsource lead onboarding a team — gate rationale removes the "what does this check do?" debate.
- DORA-metric improvement: CI duration p50 &lt; 10 min is the single highest-leverage MTBF lever.
- AI-assisted CI tuning — the LLM can rebalance tiers against the budget when costs change.

## Applies If (ALL must hold)

- Project has a CI/CD pipeline (GitHub Actions, GitLab CI, CircleCI, Buildkite, etc.).
- More than one developer (or solo dev who plans to onboard contributors).
- At least 3 categories of checks present (lint, test, security, type-check, build, etc.).
- PR cycle-time is a felt pain or anticipated to be.

## Skip If (ANY kills it)

- Single-person hobby project with no scaling intent — design overhead exceeds benefit.
- Highly regulated env (HIPAA, PCI L1) where the regulator dictates the gate list — adopt the regulator's pattern.
- Pipeline does not yet exist — set up basic CI first; gate design comes after the floor.
- Monorepo with hundreds of packages — needs the pro-tier delivery-ops gate methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current CI config | YAML | `.github/workflows/` etc. |
| Check inventory + runtimes | CSV / JSON | CI dashboard |
| 30-day PR data | export | tracker |
| Tier proposal per check | spreadsheet | author |
| Wall-clock budget target | number | team handbook |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/trunk-based-dev-principles` | TBD makes fast CI mandatory; this design names what fast means. |
| `solo/dev/bug-pattern-to-lint-rule-conversion` | Detectors join the BLOCK tier here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ rules: three-tier, written rationale, time budget, signal-not-noise, escalation path, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for ci-design.md artefact + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: block-everything, hide-the-warn, no-budget, hard-coded thresholds, missing escalation, abandoned-warn | 800 |
| `content/04-procedure.xml` | medium | 5-step procedure: inventory → classify → budget → rationale → commit | 700 |
| `content/06-decision-tree.xml` | essential | Tree: signal-noise? infra-only? security-blocking? → tier assignment | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-existing-check` | sonnet | Apply tier rubric to a single check. |
| `budget-runtime-analysis` | sonnet | Compute parallel + serial timings. |
| `design-rationale-draft` | opus | Cross-check trade-off synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-quality-gate-design.json` | JSON Schema for the ci-design artefact. |
| `templates/ci-design.md` | Skeleton with three-tier tables and budget section. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ci-quality-gate-design.py` | Validate a ci-design JSON against schema + budget rule. | Pre-merge; monthly review. |

## Related

- [[trunk-based-dev-principles]] — fast CI is one of the four pillars.
- [[bug-pattern-to-lint-rule-conversion]] — detectors join the BLOCK tier.
- external: [Accelerate (Forsgren et al.)](https://nicolefv.com/book) · [DORA reports](https://dora.dev/)

## Decision tree

See `content/06-decision-tree.xml`. The tree first asks signal-strength (does this check, when it fires, indicate a real bug?). High-signal → BLOCK. Medium-signal infra/style → WARN. Slow / exploratory / heavy → NIGHTLY. It then checks the budget arithmetic — if BLOCK sum exceeds the wall-clock budget, the tree forces re-classification. Leaves emit `commit-design`, `block-budget-exceeded`, or `block-missing-rationale`. Each leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ci-quality-gate-design.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/ci-quality-gate-design.json",
  "type": "object",
  "required": [
    "artefact_id",
    "checks",
    "budget",
    "verdict",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^cgd-[a-z0-9-]{6,}$"
    },
    "checks": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "tier",
          "runtime_p50_min",
          "owner_email",
          "last_reviewed"
        ],
        "properties": {
          "name": {
            "type": "string",
            "minLength": 1
          },
          "tier": {
            "enum": [
              "BLOCK",
              "WARN",
              "NIGHTLY"
            ]
          },
          "runtime_p50_min": {
            "type": "number",
            "minimum": 0,
            "maximum": 120
          },
          "rationale": {
            "type": "string"
          },
          "owner_email": {
            "type": "string",
            "format": "email"
          },
          "escalation": {
            "type": "string"
          },
          "last_reviewed": {
            "type": "string",
            "format": "date"
          }
        }
      }
    },
    "budget": {
      "type": "object",
      "required": [
        "target_min",
        "block_critical_path_min",
        "headroom_min"
      ],
      "properties": {
        "target_min": {
          "type": "number",
          "minimum": 1,
          "maximum": 60
        },
        "block_critical_path_min": {
          "type": "number",
          "minimum": 0,
          "maximum": 120
        },
        "headroom_min": {
          "type": "number"
        },
        "remediation": {
          "type": "string"
        }
      }
    },
    "verdict": {
      "enum": [
        "commit-design",
        "block-budget-exceeded",
        "block-missing-rationale",
        "block-config-drift"
      ]
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
