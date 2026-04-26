# Product Discovery

## Summary

Product discovery is a time-boxed process (1–4 weeks) for de-risking an idea before committing build resources. It tests four risk types — value (will customers buy/use it?), usability (can they figure it out?), feasibility (can we build it?), and business viability (does it work for the business?) — using the cheapest technique that gives sufficient confidence at each stage.

## Why

Teams that skip discovery build features nobody wants. Marty Cagan's research shows that roughly half of features shipped by product teams deliver zero measurable value — not because of poor execution but because the wrong things were built. Discovery is cheap compared to the engineering cost of a feature that fails post-launch.

## When To Use

- Pre-build validation of any significant feature or product idea.
- High-risk assumptions that would kill the idea if wrong (value risk, feasibility risk).
- Before committing to a 4+ week development effort.
- When the team disagrees on whether users actually have the problem being solved.

## When NOT To Use

- Tiny bug fixes or incremental improvements with known user impact — just ship.
- Compliance or security requirements with no alternative — no discovery needed, build it.
- Post-PMF continuous learning — use continuous-discovery instead (recurring cadence vs one-time deep dive).
- Discovery that would take longer than the build itself — run a spike instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-risk-framework.xml` | Four risk types with technique selection matrix (effort vs confidence) |
| `content/02-process.xml` | 5-step discovery process: identify assumptions, prioritize risks, design experiments, run and learn, decide |
| `content/03-examples.xml` | New feature discovery and market expansion discovery with assumption test tables |
| `content/04-antipatterns.xml` | Confirmation bias, discovery theater, building during discovery, taking too long |

## Templates

| File | Purpose |
|------|---------|
| `templates/discovery-kickoff.md` | Discovery kickoff document with context, team, questions, assumptions, success criteria |
| `templates/experiment-report.md` | Experiment hypothesis, setup, results, learnings, and go/no-go decision |
