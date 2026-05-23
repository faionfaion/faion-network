# Recognition Rather Than Recall

## Summary

**One-sentence:** Audit a UI surface against Nielsen Heuristic #6 and produce a Recognition Audit report — each finding (icon-only / hidden-option / missing-recents / no-context-carry-over / no-autocomplete) tagged with severity and a fix direction.

**One-paragraph:** Minimise memory load by making options, actions, and context visible rather than requiring users to remember them. Inputs: UI surface inventory + (where relevant) clickable prototype to detect cross-screen recall failures. Output: a Recognition Audit listing one finding per violation with category, severity, observed pattern, and concrete fix direction (e.g. "pair icon with text label", "add 5 most-recent items on focus").

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Auditing a UI surface (existing or wireframed) for hidden options or icon-only patterns.
- The product targets general users (not power-user tools where recall is intentional).
- A surface inventory or clickable prototype is reachable.

## Skip If (ANY kills it)

- Power-user tools where recall is intentional (vim, SQL terminals, CAD shortcuts).
- Pre-alpha micro-optimisation — heuristic is for refining, not architecting.
- The interface is already fully recognition-based and validated.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| UI surface inventory (route → screen → elements) | list | UX / engineering |
| Clickable prototype OR live build URL | URL / file | engineering |
| Icon allowlist (universally recognised exceptions) | list | UX |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/match-real-world` | Icon-with-label rule overlaps with H#2 vocabulary rules. |
| `solo/ux/ux-ui-designer/wireframing` | Cross-screen context tests require prototype-level fidelity. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the recognition-audit + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: inventory → categorise → cross-screen → severity → fix-direction | ~600 |
| `content/05-examples.xml` | medium | Worked audit example for icon toolbar + multi-step form | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `static-audit` | sonnet | Single-screen findings (icon-only, hidden options). |
| `cross-screen-audit` | opus | Detect recall failures across multi-step flows; requires reasoning over flow. |
| `severity-rate` | sonnet | Apply severity rubric. |

## Templates

| File | Purpose |
|------|---------|
| `templates/recognition-audit.md` | Recognition audit report skeleton. |
| `templates/prompt-audit.txt` | Agent prompt skeleton for the audit run. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-recognition-over-recall.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[match-real-world]]
- [[wireframing]]
- [[visibility-of-system-status]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, prototype reachable, audience type) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
