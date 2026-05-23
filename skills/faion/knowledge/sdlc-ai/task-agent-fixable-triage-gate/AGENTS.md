# `agent-fixable` Triage Gate (Humans Pick, Agents Work)

## Summary

**One-sentence:** Insert a human-applied `agent-fixable` label as the precondition coding agents listen for, so the fleet stops burning tokens on unspeccable tickets.

**One-paragraph:** Coding agents that turn issues into PRs waste tokens spinning on tickets they cannot solve: no acceptance criteria, no reproducible bug, blocked on product decisions, or duplicates. Insert a triage gate as a label (`agent-fixable`) applied by a human or by a read-only triage bot AFTER spam/duplicate/scope checks. The coding agent only listens for that label, never for `issue opened`. Cognition's published Devin numbers show PR merge rate climbing from 34% to 67% over 2025 once gating was added; the same shape works for any coding-agent fleet.

**Ефективно для:**

- Mixed coding-agent fleets де треба один common precondition label.
- Backlog із 50+ open issues, де агенти інакше підбирали би сміття.
- Strict CODEOWNERS repos: stale agent PRs створюють шум для review.
- Onboarding першого coding agent — стартує з вузького allowlist.

## Applies If (ALL must hold)

- Issue trackers with more than 50 open items where agents would otherwise pick the wrong ones.
- Mixed agent fleets (Devin + Copilot + Codex + Cursor) sharing the same backlog.
- Repos with strict CODEOWNERS where mis-routed agent attempts produce noisy stale PRs.

## Skip If (ANY kills it)

- Tiny backlogs (fewer than 10 open issues) where a human picks each issue manually anyway.
- Tickets needing product discovery, not code — those should carry needs-spec, never agent-fixable.
- Teams that have not yet defined what 'fixable by an agent' means — write the criteria first, label after.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Issue tracker config | YAML / JSON | infra repo |
| Agent fleet inventory | Markdown table | platform team |
| CODEOWNERS file | text | repo root |

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
| `templates/agent-pickup.yml` | GitHub Actions workflow dispatching an agent only on `agent-fixable` label-add. |
| `templates/triage-checklist.md` | Pre-label checklist a human or read-only triage bot must satisfy before applying agent-fixable. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-task-agent-fixable-triage-gate.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[task-plan-mode-locked-execution]]
- [[tracker-ai-triage-classify-route]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
