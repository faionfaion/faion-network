# Team Mode CLI Flag (`--team-config` Overlay)

## Summary

**One-sentence:** Define `faion --team-config /etc/faion/team.yaml` (and `FAION_TEAM_OVERLAY=`) so a single owner-signed overlay file overrides personal preferences identically for every dev on a team.

**One-paragraph:** Faion CLI assumes a single user with personal preferences. Team usage needs `faion --team-config /etc/faion/team.yaml` or env `FAION_TEAM_OVERLAY=…` so the override-resolution order is consistent across 10 devs. This methodology produces a versioned, owner-signed `team.yaml` overlay file plus the CLI plumbing that loads it. Resolution order is: personal `~/.faion/config.yaml` < team overlay < CLI flags. The overlay carries a `version` + `signed_by` + `signature` block so downstream agents can prove a stale or unsigned overlay is in use.

**Ефективно для:**

- 10+ developer team, де inakshe drift конфігурацій неминучий.
- Compliance: model-whitelist + MCP allowlist мають бути единими.
- Onboarding: новий dev отримує overlay → ready to work з першого дня.
- Audit: signed overlay → можна довести, який baseline був активний.

## Applies If (ALL must hold)

- Team of 3+ developers shares one Faion configuration baseline.
- Some configuration values are non-negotiable (model whitelist, MCP server allowlist, secrets policy).
- The team owns a shared `/etc/faion/` or central config store.

## Skip If (ANY kills it)

- Solo developer — personal config is the whole config.
- No shared infra to host the overlay file.
- Team has not yet defined which fields are team-scoped vs personal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| List of team-scoped fields | Markdown | team lead |
| Signing key for overlay | ed25519 key | team key vault |
| Shared config host | /etc/faion/ or s3:// path | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/team-config-overlay.yaml` | YAML overlay skeleton with version/owner/signature/overrides blocks. |
| `templates/team-config-overlay.schema.json` | JSON Schema for the overlay's structural validation. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-mode-cli-flag.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[task-plan-mode-locked-execution]]
- [[uv-lockfile-floor]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
