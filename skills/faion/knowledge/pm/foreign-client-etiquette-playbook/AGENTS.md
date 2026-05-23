# Foreign Client Etiquette Playbook

## Summary

**One-sentence:** Cross-culture communication artefact: per-region directness/indirectness map, named comms patterns (US/DE/JP/UK/AU), red-line phrasing, written-vs-verbal default per culture.

**One-paragraph:** Foreign Client Etiquette Playbook delivers a defensible playbook-step artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- P4 outsource lead, що працює з US-direct / German-precise / Japanese-indirect клієнтами одночасно.
- Founder-PM на першому foreign engagement, який не має in-house cross-culture playbook.
- Agency PMO, що навчає junior PM-ів адаптації comms patterns без зайвої формалізації.
- EU consultant, що відкриває US market і репетирує directness-without-rudeness каліброшку.

## Applies If (ALL must hold)

- the engagement crosses cultural boundaries (different first-language client + vendor team)
- communication missteps have material delivery impact (re-work, eroded trust)
- the PM has 2+ months engagement length to apply the playbook
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- short-term consultation under 2 weeks — playbook overhead doesn't pay back
- client team and vendor team share first language and culture — playbook orphaned
- playbook would be substituted for a real local contact — find the local, do not abstract them away

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
| `content/02-output-contract.xml` | essential | JSON Schema for the playbook-step + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-foreign_client_etiquette_playbook` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/foreign-client-etiquette-playbook.md` | playbook-step skeleton with required fields + 5-line header |
| `templates/foreign-client-etiquette-playbook.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-foreign-client-etiquette-playbook.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[foreign-client-kickoff-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
