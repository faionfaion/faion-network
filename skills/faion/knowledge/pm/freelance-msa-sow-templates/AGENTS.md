# Freelance MSA + SOW Templates

## Summary

**One-sentence:** Two-document contract pair: long-lived MSA (IP regime, payment cycle, IP, warranty bounds, termination), per-engagement SOW (scope, milestones, price, acceptance) signable in days.

**One-paragraph:** Freelance MSA + SOW Templates delivers a defensible spec artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Solo P3 freelancer, що підписує 1+ контракт на місяць і втомився від re-negotiation.
- Two-person practice без legal in-house — потрібен MSA+SOW patten, який можна показати юристу клієнта.
- Founder-PM, що переходить з handshake-deals на formal contracts вперше.
- Bootstrapper, який хоче кешфлоу-friendly payment terms (deposit + weekly) як умовчання.

## Applies If (ALL must hold)

- the operator is a solo or two-person freelancer signing contracts under their own name or single-member entity
- a new engagement is starting and there is no existing MSA or the existing MSA misses one of the five primitives
- the client is a business buyer (not a consumer) so IP, indemnity and warranty actually matter
- local jurisdiction permits the freelancer to assign IP and indemnify within ordinary commercial limits

## Skip If (ANY kills it)

- the client requires their own MSA which already covers all five primitives — read theirs, redline minimally
- the engagement is a one-off < €1k consultation — a single short SOW is sufficient overhead
- the freelancer operates inside a marketplace (Upwork, Toptal) whose ToS supersede private contracts

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| recent context for the triggering activity | log/doc/ticket | last 30 days |
| write-access to the artefact store | repo / wiki / decision log | team policy |
| named accountable owner downstream | handle / email / role | RACI / org chart |
| baseline conventions | CLAUDE.md / AGENTS.md / CONVENTIONS.md | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | testable rules with statement + rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/05-examples.xml` | essential | worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-freelance_msa_sow_templates` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelance-msa-sow-templates.md` | spec skeleton with required fields + 5-line header |
| `templates/freelance-msa-sow-templates.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-msa-sow-templates.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[freelancer-proposal-template-fixed-vs-tm]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
