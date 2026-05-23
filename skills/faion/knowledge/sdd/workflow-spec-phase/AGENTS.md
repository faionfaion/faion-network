# Workflow: Specification Phase

## Summary

**One-sentence:** Generates the spec.md artefact for a new feature — FR-X / NFR-X requirements, scope, success criteria, glossary, ready for Accepted gate.

**One-paragraph:** Step-by-step procedure for the SDD specification phase. Runs a Brainstorm → Research → Clarify → Draft → Review loop with human-in-loop checkpoints, then captures functional requirements (FR-X), non-functional requirements (NFR-X), in-scope / out-of-scope statements, success criteria, and a glossary. Output is a spec.md ready to be promoted from Draft to Accepted by the human owner. The Accepted gate is the prerequisite for `workflow-design-phase`.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'spec authoring' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- A new feature is requested where requirements are unclear or only partially defined.
- Backlog grooming OR fresh feature intake requires a written spec before design can start.
- The feature is large enough to warrant SDD discipline (not a one-line bugfix).
- A named human owner is available for the Accepted-gate review.

## Skip If (ANY kills it)

- Feature is a bugfix with a single clear root cause — skip spec, go straight to task.
- Requirements are fully documented in an existing PRD — extract, don't re-elicit.
- Constitution already exists and team agrees — skip Mode-1 discovery.
- Rapid prototype / spike where requirements will change after seeing output.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature intake note or stakeholder brief | markdown / text | `.aidocs/features/backlog/<feature>/intake.md` or chat log |
| Constitution / tech-decisions doc | markdown | `.aidocs/constitution.md` |
| Roadmap context | markdown | `.aidocs/roadmap.md` |
| Named human owner | identity | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/workflows` | Provides the route record that may have dispatched this phase. |
| `solo/sdd/sdd-planning/workflow-design-phase` | Downstream consumer of the Accepted spec produced here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec.md frontmatter + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: Brainstorm → Research → Clarify → Draft FR/NFR → Review → Accepted-gate | ~900 |
| `content/05-examples.xml` | medium | Worked example: spec.md for the JWT refresh feature | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `brainstorm-and-clarify` | opus | Open-ended elicitation; needs reasoning depth. |
| `draft-fr-nfr` | sonnet | Template-driven requirement capture. |
| `reviewer-pass` | opus | Cross-FR consistency + scope leakage audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Canonical spec.md skeleton with FR/NFR, scope, success criteria, glossary sections. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/backlog-audit.sh` | Print feature status table across SDD lifecycle stages to locate the feature being specced. | Before launching brainstorm to confirm the feature is in backlog and not already specced. |
| `scripts/validate-workflow-spec-phase.py` | Validate the spec.md frontmatter against the schema in `content/02-output-contract.xml`. | After subagent returns the spec.md, before human owner reviews for Accepted promotion. |

## Related

- [[workflow-design-phase]]
- [[workflows]]
- [[template-task]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (intake exists, owner named, requirements unclear) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether to run the full spec phase or take a shortcut.
