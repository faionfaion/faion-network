# Agent Integration — Problem Validation 2026

## Scope note

This methodology file is a thin variant of `problem-validation` (adjacent directory), covering the same evidence-based validation hierarchy and Mom Test question reframing with a 2026 framing. It does not introduce new techniques beyond its parent.

For full agent integration guidance — CLI tools, services, prompt patterns, scripts, and best practices — refer to:
`skills/faion/knowledge/solo/ux/user-researcher/problem-validation/agent-integration.md`

The additions specific to this file are:

## What this file adds over problem-validation

- Explicit validation hierarchy ordering with numeric rank (1 = strongest: paid; 5 = weakest: stated)
- Mom Test question reframes as a ready-to-paste replacement table
- Interview Opening Framework: Vision → Framing → Weakness → Pedestal → Ask (5-step opener)
- Commitment signal taxonomy: Time / Reputation / Money
- Red flag pattern list: compliments, hypotheticals, generic statements, approval-fishing

## Agent-specific notes

These additions are directly usable in agent prompts without modification:

```
Before conducting a validation interview, use this opener sequence:
1. Vision: state the problem you want to solve (one sentence)
2. Framing: explain you have nothing to sell — just learning
3. Weakness: humbly acknowledge you don't know if this matters
4. Pedestal: ask for their expertise on the topic
5. Ask: request 20 minutes of their time
```

```
After a validation interview, classify each piece of evidence by commitment signal:
- Time signal: did they schedule a follow-up or try the prototype unprompted?
- Reputation signal: did they offer to introduce you to a colleague or boss?
- Money signal: did they offer a pre-order, LOI, or payment before the product exists?
If none of the above, the interview produced only stated interest — insufficient for PROCEED.
```

## Key 2026 principle for agents

Validation is an ongoing loop, not a gate. Agents should model it as a recurring task (weekly during discovery) rather than a one-time check. A single round of validation produces a hypothesis; repeated rounds produce confidence.

## References
- Rob Fitzpatrick, "The Mom Test" (momtestbook.com)
- `problem-validation/agent-integration.md` (this repo) — full tool and service coverage
