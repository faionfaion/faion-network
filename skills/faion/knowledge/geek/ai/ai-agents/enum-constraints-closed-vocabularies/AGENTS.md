# Enum Constraints for Closed Vocabularies

## Summary

Whenever the answer set is finite, declare it as a typed enum (`Literal[...]` in Pydantic, `enum` in JSON Schema) instead of a free-form string. Constrained decoders mask every non-enum token to probability zero, so a hallucinated label becomes mathematically impossible. The rule is a one-line schema change with the highest accuracy-per-token ratio of any structured-output trick.

## Why

LLMs default to producing the most likely token among the entire vocabulary. When the field truly has 5 valid values, 99.99% of vocabulary entries are wrong by construction, yet still receive non-zero probability mass and occasionally surface (mostly in long contexts, near token-budget exhaustion, or with smaller models). Strict-mode + enum decoding removes those tokens from the candidate set during sampling. Empirically, ohmeow (2024) and the vLLM Structured Outputs docs both show category-prediction tasks going from 80–95% raw to ~100% with `Literal[...]` + strict mode. The sampling-time mask, not the prompt, is what closes the gap.

## When To Use

- Any classification field — sentiment, intent, severity, routing label, language code, status state.
- Pick-one-of-N action selection inside an agent loop.
- Field that maps to a downstream switch/case or DB enum column.
- Pipelines where an unknown label silently breaks the next stage.

## When NOT To Use

- Open vocabularies (free-text tags, novel entity types, user names) — enum would clip valid answers.
- Semi-open sets — use `Literal[...] | str` plus a discriminated union or post-validation instead.
- JSON-mode-only fallback paths on mini/nano models — enums are advisory there, pair with strict mode or a constrained backend (XGrammar, Outlines) to actually enforce them.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | Core rule, mechanism, and stacked patterns (Literal + strict + description). |
| `content/02-edge-cases.xml` | Semi-open vocabularies, mini-model JSON-mode failure mode, multi-language label sets. |

## Templates

| File | Purpose |
|------|---------|
| `templates/enum_schema.py` | Pydantic model with `Literal[...]` enum fields wired for OpenAI strict mode. |
