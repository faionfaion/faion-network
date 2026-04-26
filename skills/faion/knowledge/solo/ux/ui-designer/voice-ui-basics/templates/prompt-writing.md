# Prompt: [Prompt Name]

## Context

- Where in flow: [Position in dialogue — initial / slot-fill / confirmation / error]
- User state: [What happened before this prompt]
- Goal: [What information or action we need from user]

## Primary Prompt

"[The main prompt text — under 20 words for smart speakers, 15 for IVR]"

## Variations

- Short: "[Shorter version for reprompts]"
- Longer: "[More detailed version for first-time users]"

## Reprompts (3-level chain)

**1st reprompt** (shorter, same intent):
"[First reprompt]"

**2nd reprompt** (with examples):
"[Second reprompt — offer 2-3 examples of valid responses]"

**3rd reprompt** (fallback):
"[Third reprompt — offer alternative path or human transfer]"

## Design Rationale

- [Why this wording was chosen over alternatives]
- [Trade-offs considered]

## Anti-patterns to Avoid

- No "I'm sorry" as a standalone response
- No URLs
- No numbers with 4+ digits spoken as digits
- No passive voice ("An order has been placed") — use active ("I've placed your order")
