<!-- purpose: Golden Set Curation and Maintenance spec skeleton -->
<!-- consumes: Prerequisites bundle (see AGENTS.md) -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->


# Golden Set Curation and Maintenance — Spec

_Last reviewed: 2026-05-23_

## Ask summary

<one-paragraph stakeholder ask + source citation>

## Owner

`<named person / email / handle>`

## Stories

| ID | As a | I want | So that | AC ids |
|----|------|--------|---------|--------|
| story-1 | <persona> | <capability> | <outcome> | ac-1, ac-2 |

## Acceptance criteria

| ID | Criterion | Metric threshold |
|----|-----------|------------------|
| ac-1 | <criterion> | <metric op value> |

## AI boundary (per AC)

- ai_scope: <what AI does>
- deterministic_fallback: <what runs deterministically>
- handoff_signal: <confidence threshold OR refusal OR timeout>

## Fallback behavior

| Failure mode | UX |
|--------------|-----|
| low_confidence | <action> |
| refusal | <action> |
| timeout | <action> |

## Eval AC

| Metric | Threshold |
|--------|-----------|
| <metric> | <value> |

## Golden seeds (≥5 per AC)

| Input | Expected | Anti-output |
|-------|----------|-------------|
| <input> | <expected> | <plausible-wrong> |
