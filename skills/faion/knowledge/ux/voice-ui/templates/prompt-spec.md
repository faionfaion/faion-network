<!-- purpose: Single voice prompt spec with reprompt variants and A/B copy -->
<!-- consumes: dialogue-first sample conversations, intent/slot definitions -->
<!-- produces: filled prompt spec markdown -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150 tokens filled -->

# Prompt Spec: <prompt_name>

## Context

- Where in flow: [Position — initial / reprompt 1 / reprompt 2 / confirmation / error]
- User state: [What happened before this prompt]
- Goal: [What the system needs from the user]

## Primary Prompt

"[The main prompt text — max 25 words]"

## Variants

- Short: "[Shorter version for re-prompt]"
- With examples: "[Version that includes valid input examples]"
- Fallback: "[Third-tier — offers escape or human transfer]"

## A/B Test Variants

- A: "[Version A]"
- B: "<version_b>"

## Design Rationale

- [Why this wording]
- <trade_offs_considered>
