# Client Firing and Graceful Offboarding

## Summary

**One-sentence:** Criteria for firing a toxic client, structured offboarding sequence (notice, transition window, handoff docs, post-mortem) and contract-clean-exit terms — a versioned spec the founder can run without re-deriving the rationale.

**One-paragraph:** Criteria for firing a toxic client, structured offboarding sequence (notice, transition window, handoff docs, post-mortem) and contract-clean-exit terms — a versioned spec the founder can run without re-deriving the rationale. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Client relationship has > 3 documented friction events in 90 days (scope creep, abuse, payment delays).
- Founder has named handoff alternatives (referral partner or self-service docs) for the client.
- Contract permits termination on agreed notice (typically 30-60 days).

## Skip If (ANY kills it)

- Friction is one-off / situational — schedule a difficult conversation first.
- No contract clause permits termination at desired timeline — defer to legal counsel first.
- Single-client agency where firing means closure — see business-pivot methodology instead.

**Ефективно для:**

- Засновники-фрилансери що масштабуються в SaaS і змушені скорочувати client work.
- Мікро-агенції з 1-2 токсичними клієнтами що з'їдають 50%+ часу.
- Команди що йдуть в нову нішу і треба погасити out-of-niche legacy retainers.
- Аудит-ready середовища з вимогою structured offboarding evidence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing-manager` | Parent role context — agency operating discipline. |
| `solo/marketing/content-marketer` | Adjacent role context — content + portfolio surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-firing-and-graceful-offboarding.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[agency-niche-positioning]]
- [[agency-case-study-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
