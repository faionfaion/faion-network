---
slug: adopt-faion-org-wide-overrides
tier: geek
group: team-ops
persona: P6
goal: migrate-rebuild
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Fragmented per-dev tooling → all 2-10 devs reference the same faion playbook set with company-specific overlays cleanly shadowing defaults.
content_id: 0c134507f12ecaa2
methodology_refs:
  - design-doc-structure
  - kb-agents-md-context-pyramid
  - kb-versioned-agent-memory-files
  - team-development
  - onboarding-30-day
  - architecture-decision-records
  - pattern-memory
---

# Adopt faion org-wide and override with company patterns

**Playbook slug:** `adopt-faion-org-wide-overrides`
**Tier:** geek
**Complexity:** deep
**Persona:** P6 — Product-Dev Team

## Intent

Fragmented per-dev tooling → all 2-10 devs reference the same faion playbook set with company-specific overlays cleanly shadowing defaults.

## Scope

A product-dev team adopts faion as the shared methodology base. Company-specific overlays (security policy, ADR template, RFC format, internal tech-radar) cleanly shadow faion defaults without forking the corpus. Devs reference the same playbooks; the company prompt library, role cheatsheets, and team charter overlay where needed.

### What this playbook covers

Three stages: baseline + overlay design, charter + cheatsheets, commit overlays. The chain is opinionated against forking: forks always drift and always lose access to upstream improvements. Overlays must be designed so deleting them yields the faion default cleanly — that's the test for whether the overlay is well-scoped.

### Non-goals

- Forking the faion corpus — overlays only
- Replacing OKR or release cadence — see `quarter-planning-okr-reset` and `feature-flag-rollout-decision`
- Migrating away from existing tracker — handled separately

### Prerequisites

- Team agrees to a single methodology base
- Versioned agent-memory files in repo (mistakes.md, patterns.md, decisions.md)
- AGENTS.md / CLAUDE.md context pyramid in place

## Success criteria

The playbook is done when:
- Every dev references the same faion playbook set
- Company overlays defined for: security policy, ADR template, RFC format, tech-radar
- Team charter / working agreement written
- Role cheatsheets generated per role
- Prompt library shared in repo
- Onboarding folds the overlay in by day 30

## Stages

### Stage 1: Baseline + overlay design

**Intent:** Pick the faion baseline + design the overlay shape that doesn't fork.

**Methodologies in chain:**
- `design-doc-structure` → `solo/sdd/sdd-planning/design-doc-structure`
- `kb-agents-md-context-pyramid` → `geek/sdlc-ai/kb-agents-md-context-pyramid`
- `kb-versioned-agent-memory-files` → `geek/sdlc-ai/kb-versioned-agent-memory-files`

**Decision gate:**
> Advance only with explicit overlay-vs-fork choice on paper. Forking is the failure mode.

### Stage 2: Wire team charter + role cheatsheets

**Intent:** Working agreement + per-role cheatsheets land in repo.

**Methodologies in chain:**
- `team-development` → `pro/pm/pm-agile/team-development`
- `onboarding-30-day` → `pro/comms/hr-recruiter/onboarding-30-day`

**Decision gate:**
> Advance when charter + cheatsheets are merged. Verbal agreements decay in 4 weeks.

### Stage 3: Commit overlays + decisions

**Intent:** Overlay artefacts (ADR template, RFC template, tech-radar) live in repo with ADRs explaining why.

**Methodologies in chain:**
- `architecture-decision-records` → `solo/sdd/sdd/architecture-decision-records`
- `pattern-memory` → `solo/sdd/sdd/pattern-memory`

**Decision gate:**
> Required output: ADRs + overlay artefacts. Without ADRs, a new dev re-litigates the overlay.

## Common pitfalls

- Forking faion "just to fix one thing" — diverges in 6 weeks
- Overlays without ADRs — re-debated every quarter
- Role cheatsheets out of date — agents stop using them
- Team charter is a slide, not a checked-in file — bus-factor failure

## Quality checklist (self-review)

- If I delete the overlay, does the team fall back to the faion default cleanly?
- Do all 5+ roles have a current cheatsheet?
- Are the overlays explained by ADRs?

## Related playbooks

- `hire-onboard-product-dev-2-weeks`
- `cross-role-handoff-pm-architect-dev-qa-devops`
- `quarter-planning-okr-reset`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **team-methodology-overlay-mechanism** (tier `geek`, blocks stage 1) — Baseline stage needs a concrete overlay mechanism (file naming, precedence, validation) so it isn't ad-hoc
- **company-prompt-library-pattern** (tier `geek`, blocks stage 3) — Commit stage needs a structured prompt-library pattern (file layout, sharing rules)
- **team-charter-working-agreement** (tier `geek`, blocks stage 2) — Charter stage needs a written team-charter template tuned for product-dev teams
- **role-cheatsheet-generator** (tier `geek`, blocks stage 2) — Cheatsheets stage needs an AI generator that keeps role cheatsheets in sync with faion updates

## CLI usage

```
faion get-content adopt-faion-org-wide-overrides --format md       # human-readable rendering
faion get-content adopt-faion-org-wide-overrides --format context  # agent-optimised context bundle
faion get-content adopt-faion-org-wide-overrides --format json     # raw structured form
```
