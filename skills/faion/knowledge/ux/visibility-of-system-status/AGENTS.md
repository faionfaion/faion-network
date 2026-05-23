# Visibility of System Status

## Summary

**One-sentence:** Produce a Status Audit report (Nielsen Heuristic #1) — per-action three-state coverage (loading/success/error), feedback latency thresholds (≤100ms response, spinner 1-3s, progress bar ≥3s, percentage+cancel ≥10s), and aria-live correctness.

**One-paragraph:** Every user action MUST produce visible feedback within the appropriate threshold. Inputs: action inventory + session recordings (LogRocket / FullStory) + Playwright spec. Output: an audit report with one row per interactive action covering loading/success/error states, feedback latency, double-submission prevention, and aria-live attribute correctness.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Auditing an interactive UI where actions trigger async operations.
- An action inventory (button / link / form per route) is reachable.
- Either Playwright traces OR session-recording tooling is available to verify states.

## Skip If (ANY kills it)

- Static informational pages with no interactive elements.
- Background operations users do not need to know about (≤100ms cache refresh).
- Findings already tracked and being fixed; re-audit adds noise.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Action inventory (route → action → async-op) | list | engineering |
| Session recordings or Playwright traces | file / URL | engineering |
| aria-live policy | doc | a11y owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/user-control-freedom` | Loading-state failures often pair with confirmation patterns. |
| `solo/ux/ux-ui-designer/mobile-ux` | Core Web Vitals thresholds reinforce status feedback timing. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the status-audit + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: inventory → measure → categorise → aria-live-check → fix-direction | ~600 |
| `content/05-examples.xml` | medium | Worked example: pay-now button without loading state | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `static-audit` | sonnet | Three-state coverage check per action. |
| `playwright-latency` | haiku | Mechanical latency measurement. |
| `aria-live-judgement` | opus | Polite vs assertive decisions need context. |

## Templates

| File | Purpose |
|------|---------|
| `templates/status-audit.md` | Status audit report skeleton. |
| `templates/loading-state.spec.ts` | Playwright spec verifying loading / success / error states + latency. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-visibility-of-system-status.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[user-control-freedom]]
- [[mobile-ux]]
- [[recognition-over-recall]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, tooling available, async-op present) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
