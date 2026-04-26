# Mob Programming

## Summary

A whole-team practice where 3–8 people share one screen and one keyboard, rotating the driver role every 5–15 minutes while all others navigate. The strong-style rule applies: any idea must pass through the driver's hands before reaching the computer. With agents, cap the mob at 4 humans + 1 agent, assign a human facilitator, and rotate the agent out of driver on the same timer.

## Why

Mob programming eliminates the knowledge-silo and review-queue bottlenecks: bugs are caught before they are typed, context is shared in real time, and no PR backlog forms. Woody Zuill's original report and widespread practitioner evidence show lower cycle time and higher code consistency for complex, cross-functional work. The `mob.sh` handoff tool makes rotation auditable via git.

## When To Use

- Complex features requiring multiple perspectives simultaneously.
- Critical system changes with high blast radius.
- Team onboarding and knowledge leveling.
- "Impossible" bugs that have stumped individuals.
- Learning mob: team encounters an unfamiliar API or framework.
- Mixed human-AI mob: agent plays navigator or driver for one rotation.

## When NOT To Use

- Simple, well-understood, parallelizable tasks — mob overhead is not justified.
- Quiet/individual deep-work tasks — the format itself is wrong.
- Sensitive material (security audits, PII, unreleased secrets) where streaming to an agent creates compliance risk.
- Teams new to both mobbing and agents — double the failure modes; try human-only mobbing first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-roles-and-styles.xml` | Driver, navigator, facilitator rules; TDD mob, learning mob, bug-hunt mob, Randori patterns. |
| `content/02-agent-workflow.xml` | Agent rotation rules, prompt patterns for driver/navigator turns, gotchas (dominance, drift, silent rewrites). |

## Templates

| File | Purpose |
|------|---------|
| `templates/rotation-log.sh` | Append rotation entry to MOB_LOG.md and trigger mob.sh handoff. |
| `templates/agent-driver-prompt.txt` | Agent driver prompt: only act on explicit navigator instruction, hand off after 7 min. |
| `templates/agent-navigator-prompt.txt` | Agent navigator prompt: propose one next step as intent, no code this rotation. |
