# User Control and Freedom

## Summary

**One-sentence:** Produce a User Control Audit — per-action table covering undo, cancel, exit, recovery — flagging missing emergency exits and confirmation-overuse with severity and fix direction (Nielsen Heuristic #3).

**One-paragraph:** Every interface must provide clearly marked emergency exits (undo, cancel, back, close, reset). Inputs: action inventory + DOM snapshots / Playwright traces. Output: an audit table with one row per user-facing action covering undo availability, cancel availability, exit mechanism, recovery method, and severity (irreversible-no-undo = severity 1).

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Heuristic audit of a feature spec or live UI for missing exits.
- Action inventory (every user-facing destructive or state-changing action) is reachable.
- Accessibility tooling (axe-core / pa11y / Playwright) is available for focus-trap verification.

## Skip If (ANY kills it)

- Substitute for usability testing — structural audit detects absence, not user feeling.
- System cannot support undo (sent email, executed finance transaction); design solution requires human decision.
- Complex DB-undo architecture decisions — engineering judgement required, not heuristic.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Action inventory (route → action → reversibility) | list | engineering / PM |
| DOM snapshots OR Playwright trace | file | engineering |
| Modal / dialog inventory | list | UX |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/usability-testing` | Validates whether structurally present exits actually feel reachable. |
| `solo/ux/ux-ui-designer/visibility-of-system-status` | Loading states pair with undo affordances. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the control-audit + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: inventory → control-check → focus-trap-test → severity → fix-direction | ~600 |
| `content/05-examples.xml` | medium | Worked audit example for a settings page + a delete-account modal | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `static-audit` | sonnet | Action-table composition from inventory. |
| `playwright-verify` | haiku | Mechanical execution of Escape / outside-click / Ctrl-Z. |
| `severity-rate` | opus | Edge-case judgement on reversibility tier. |

## Templates

| File | Purpose |
|------|---------|
| `templates/control-audit.md` | Control audit report skeleton. |
| `templates/verify-escape-exits.spec.js` | Playwright spec verifying Escape + outside-click + back-button. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-control-freedom.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[usability-testing]]
- [[visibility-of-system-status]]
- [[recognition-over-recall]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, action inventory reachable, undo-supportable) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
