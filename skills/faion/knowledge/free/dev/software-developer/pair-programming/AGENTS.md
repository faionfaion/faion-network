# Pair Programming

## Summary

A practice where two programmers share one workstation: the Driver writes code while the Navigator reviews each line, thinks strategically, and catches errors. Pairs switch roles frequently. Four modes: classic Driver-Navigator, Ping-Pong (TDD), Strong-Style (idea must go through the other person's hands), and Tour Guide (expert narrates codebase to newcomer). With an AI agent, the human is always physically the driver; the agent acts as strategic navigator emitting one bounded instruction per turn.

## Why

Pairing produces fewer bugs, accelerates knowledge transfer, and eliminates single points of failure. Short feedback loops (navigator spots error in real-time) are cheaper than review cycles. With an agent as navigator, solo developers get strategic guidance, architectural second opinions, and live code review without a second human.

## When To Use

- Complex or unfamiliar code areas where a second perspective prevents wrong-path investment.
- Knowledge transfer: onboarding, cross-training, tour guide through legacy code.
- Critical business logic where correctness matters more than speed.
- TDD ping-pong to stay engaged and alternate test/impl roles.
- AI-assisted pairing: human drives, Claude navigates in strong-style mode.

## When NOT To Use

- Simple, routine tasks where overhead exceeds benefit.
- Privacy-sensitive code that cannot leave the local machine — skip cloud agent.
- High-velocity sprints where per-line explanation slows the team below solo velocity.
- Domains where the model is weak (DSP, embedded firmware, niche DSLs) — agent adds noise.
- True multi-developer pairing — adding an agent to a human-human pair fragments attention.

## Content

| File | What's inside |
|------|---------------|
| `content/01-roles-modes.xml` | Driver/Navigator responsibilities, four pairing modes, AI-navigator adaptation of Strong-Style. |
| `content/02-practices.xml` | Environment setup, time management (Pomodoro), communication patterns, skill-level pairings, remote tools. |
| `content/03-antipatterns.xml` | Keyboard hog, backseat driver, disengaged observer, forced pairing, silent pairing, remote fatigue, AI instruction creep. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pair-session.sh` | Shell script: start a logged pair session with `script(1)` for terminal transcript. |
| `templates/strong-style-prompt.txt` | Strong-style AI-navigator system prompt: one instruction per turn, explain why, wait for result. |
