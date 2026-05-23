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
| `templates/flag-spec.md` | Markdown skeleton the author fills before merge. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trunk-based-feature-flags.py` | Validate a flag-spec JSON against the schema and cleanup-ticket rule. | On PR open; on flag creation; nightly aging scan. |

## Related

- [[trunk-based-dev-principles]] — the umbrella branching model.
- [[behavior-parity-verification]] — dark-launch flag is the shadow router's switch.
- [[ci-quality-gate-design]] — the CI gate that blocks PRs with missing flag-spec.

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks the flag's declared type (release / experiment / ops / permission) — each type requires a different field set. It then verifies ramp plan presence, cleanup-ticket link, and kill-switch arming. Leaves emit `approve`, `block-missing-cleanup-ticket`, `block-missing-ramp-plan`, or `block-zombie-flag-quota-exceeded`. Each leaf references a rule in `01-core-rules.xml`.
