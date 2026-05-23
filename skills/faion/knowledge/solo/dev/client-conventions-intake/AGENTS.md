---
slug: client-conventions-intake
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a per-client conventions report captured at engagement start — branching, commit style, review SLA, naming, CI gates, security rules — so all downstream PRs comply from day one.
content_id: "ccintake1.0.0"
complexity: medium
produces: report
est_tokens: 3800
tags: [client-engagement, conventions, intake, freelance, outsource]
---
# Client Conventions Intake

## Summary

**One-sentence:** Captures the new client's conventions on day 1 — branching, commit style, review SLA, naming, CI gates, security rules, languages of communication — into a structured report committed to the repo so every subsequent PR complies.

**One-paragraph:** A solo dev or outsource lead joining a new client repo loses 1–3 weeks re-learning per-client conventions the hard way: PRs rejected for naming, branches refused for length, commits squashed because "we use squash-merge". This methodology turns intake into a deterministic interview + report: 8 dimensions, 3–5 questions each, answers captured as a versioned JSON artefact plus a Markdown summary the client signs off on. The artefact serves as the single source of truth for downstream automation (PR template generation, CI gate selection, AI-agent prompt context). It also surfaces gaps — clients who have never written conventions down do so collaboratively in the intake.

**Ефективно для:**

- Solo dev / outsource lead taking on a new client repo.
- Onboarding new AI agents (Claude Code, Cursor) onto a client repo — the report becomes their context.
- Multi-client agency / freelancer juggling 3+ codebases with different conventions.
- Client-side audit: surface that conventions are unwritten and propose codifying them.

## Applies If (ALL must hold)

- A new client engagement is starting OR an existing engagement lacks a captured conventions record.
- The client has at least one accessible repo / codebase.
- A contact-person on the client side can answer the intake questions.
- The engagement length warrants the intake overhead (typically ≥4 weeks).

## Skip If (ANY kills it)

- Single PR fix engagement (overhead exceeds benefit).
- Client repo has a complete CONVENTIONS.md / CONTRIBUTING.md already up-to-date — just read it.
- Client refuses to engage — escalate, don't proceed.
- Existing intake record &lt; 90 days old.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo access | URL + grant | client |
| Contact person | name + email | client |
| Existing CONVENTIONS.md / CONTRIBUTING.md (if any) | Markdown | repo |
| Sample PR template / CI config | YAML / Markdown | repo |
| Recent merged PR set | URL list | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/client-handover-package` | Sibling: the handover record produced at engagement end. |
| `solo/dev/ci-quality-gate-design` | The CI gate set is one of the intake dimensions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ rules: 8-dimension coverage, sourced answers, named owner, signed sign-off, versioned record, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the intake-report + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: assumed-conventions, unsigned report, missing dimensions, contact-handoff drift | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: interview → capture → cross-check repo → sign-off → commit | 700 |
| `content/06-decision-tree.xml` | essential | Tree: existing CONV doc? → dimensions covered? → sign-off? → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-from-repo` | haiku | Mechanical: parse `.github/`, `CONTRIBUTING.md`, recent merged PRs for signals. |
| `interview-script` | sonnet | Phrasing intake questions for non-engineer contact persons. |
| `gap-analysis` | sonnet | Cross-check stated conventions vs. observed-in-repo signals. |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-conventions-intake.json` | JSON Schema for the intake-report artefact. |
| `templates/conventions-interview.md` | 8-dimension interview script. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-conventions-intake.py` | Validate intake-report JSON against schema + sign-off rule. | End of intake; before first PR. |

## Related

- [[client-handover-package]] — sibling at engagement end.
- [[ci-quality-gate-design]] — CI gate dimension's input.
- [[changelog-automation-conventional-commits]] — commit-style dimension's downstream.

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks whether an up-to-date CONVENTIONS doc exists (if yes &lt; 90 days, skip). Otherwise: are all 8 dimensions answered? is the contact signed off? are the stated conventions consistent with the observed-in-repo signals? Leaves emit `commit-record`, `block-missing-dimensions`, `block-no-signoff`, or `block-stated-observed-mismatch`. Each leaf references a rule in `01-core-rules.xml`.
