# Scope-Creep Email Language Pack

## Summary

**One-sentence:** Indexed pack of polite-firm push-back phrasings for 7 recurring scope-creep moments; the founder pastes from it instead of wording each reply.

**One-paragraph:** Indexed pack of polite-firm push-back phrasings for 7 recurring scope-creep moments; the founder pastes from it instead of wording each reply. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned checklist artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- паст-готовий push-back на out-of-scope запит у фіксованому проєкті.
- ротація формулювань між клієнтами — щоб не виглядати як шаблон.
- переведення «крихітного твіку» у платний change-order без скандалу.
- комерційний фрейм відмови з конкретним наступним кроком.
- лог тренду creep на engagement → сигнал «час перепрайсити».

## Applies If (ALL must hold)

- the engagement has a written scope of work, statement of work, or signed proposal.
- the operator (founder/freelancer) handles their own client comms (no account manager intermediary).
- the engagement is active or within 30 days of close.
- tier == pro or higher.

## Skip If (ANY kills it)

- the relationship is so adversarial that any template phrasing will be parsed as hostile — book a call instead.
- the engagement explicitly priced as time-and-materials with no scope cap.
- the ask is a genuine goodwill investment — log explicitly as goodwill instead of pushing back.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the checklist artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scope-creep-email-language-pack.md` | Working checklist skeleton with 5-line header |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-scope-creep-email-language-pack.py` | Validate the checklist artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[scope-creep-firewall]]
- [[change-request-impact-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
