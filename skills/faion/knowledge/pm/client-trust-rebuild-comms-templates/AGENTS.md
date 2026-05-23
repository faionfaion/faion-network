# Client Trust Rebuild Comms Templates

## Summary

**One-sentence:** Spec for the comms cadence when a client project goes red — apology email, reset deck, weekly recovery digest, exit-or-rebuild decision letter — with named owner, frozen window, and content guardrails per template.

**One-paragraph:** When a project goes red the comms register completely changes: more direct, shorter cycles, more written confirmations. No template set exists for the apology / reset / recovery cadence. This methodology specifies four templates (apology email, reset deck, weekly recovery digest, exit-or-rebuild decision letter), with content guardrails per template (no excuses, no blame, specific commitments with dates, named owner). Output: a comms spec the PM and the client jointly own through the rescue.

**Ефективно для:** PMs running distressed-project rescues; agency leads managing client recovery; founders salvaging a key contract.

## Applies If (ALL must hold)

- Project is in active distress (red status, missed milestones, client escalation)
- Client relationship is salvageable (not contractually terminated)
- PM has authority to commit to the comms cadence
- A six-week rescue plan exists or is being drafted

## Skip If (ANY kills it)

- Project is in steady state — different comms cadence applies
- Client relationship contractually terminated — different methodology (exit comms)
- Project is internal-only with no external client — different stakeholder set
- Compliance dictates a specific external comms template — defer

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Rescue plan with milestones + dates | Markdown | PM |
| Owner directory (PM, account exec, technical lead) | YAML | team |
| Client comms history (last 90 days) | Email export | CRM |
| Approved commitments with finance sign-off | Markdown | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill |
| [[ai-status-digest-pipeline]] | feeds the weekly digest |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_apology_email` | sonnet | Bounded sensitive comms |
| `draft_reset_deck` | sonnet | Bounded narrative for executive review |
| `draft_weekly_digest` | sonnet | Bounded weekly recap |
| `review_and_sign_off` | opus | Cross-template sign-off check |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-trust-rebuild-comms-templates.json` | JSON schema for the comms spec |
| `templates/apology-email.md` | Apology email template (no excuses, specific commitments) |
| `templates/reset-deck-outline.md` | Reset deck outline (problem, root cause, plan, milestones) |
| `templates/weekly-recovery-digest.md` | Weekly recovery digest template |
| `templates/_smoke-test.md` | Minimum-viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-trust-rebuild-comms-templates.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- [[ai-status-digest-pipeline]]
- [[anti-theater-retro-guardrails]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether client-trust-rebuild-comms-templates applies: root question — "Is the project in active rescue AND the client relationship salvageable AND finance available to sign commitments?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-no-excuses, r2-specific-commitments, r3-named-owner-on-record, r4-finance-sign-off, r5-versioned-record, r6-weekly-cadence.
