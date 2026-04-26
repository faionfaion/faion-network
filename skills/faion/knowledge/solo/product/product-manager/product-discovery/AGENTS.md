# Product Discovery

## Summary

Systematically de-risk ideas before committing engineering capacity by testing four risk types: Value (will customers use it?), Usability (can they figure it out?), Feasibility (can we build it?), and Business Viability (does it work for the business?). Map all assumptions, tag each by risk type and severity, then design the cheapest experiment that could falsify the highest-severity assumption first. Every experiment requires a hypothesis, a success threshold, and an explicit kill threshold. Timebox each discovery cycle to 1-4 weeks.

## Why

Teams that skip discovery build features nobody wants and discover problems after launch. The four-risk framework forces prioritization of dangerous assumptions over easy ones — the lethal risk is almost never the most comfortable one to test. Cheap-to-fail experiments (prototypes over code, scripts over services, fakes over builds) mean the cost of being wrong is a week of time, not a quarter of engineering.

## When To Use

- Before committing engineering capacity to a new feature, product, or market segment.
- When a stakeholder request lacks evidence and needs a structured assumption test.
- After analytics flags a divergence (drop-off, churn) and the team needs root cause before solutioning.
- When entering an unfamiliar domain where all four risks are unknown.

## When NOT To Use

- Pure execution work where all four risks are already addressed by existing evidence.
- Time-bounded compliance or contractual deliverables — discovery cannot move the deadline.
- Trivial features (less than 2 days) where running an experiment costs more than building.
- When the team will not act on results — discovery without decision power is theatre.

## Content

| File | What's inside |
|------|---------------|
| `content/01-risk-framework.xml` | Four risk types, discovery technique tables by risk category, and severity-first prioritization rule. |
| `content/02-process.xml` | Five-step discovery process (identify assumptions, prioritize risks, design experiments, run, decide) with examples and antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/discovery-kickoff.md` | Discovery session template: context, team, core questions, assumption matrix, success criteria. |
| `templates/experiment-report.md` | Experiment report: hypothesis, setup, results table, learnings, decision. |
| `templates/validate-experiment.py` | Python gate: verifies experiment has hypothesis, kill threshold, sample size, and a power-calculation check. |
