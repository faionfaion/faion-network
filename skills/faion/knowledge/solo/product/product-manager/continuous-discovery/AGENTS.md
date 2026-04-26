# Continuous Discovery

## Summary

Integrate discovery as a recurring operational cadence rather than a one-time project-start activity. Allocate 15-20% of team capacity to discovery every sprint. Run three loops in parallel: daily behaviour-watcher (analytics diffs), weekly user-interview cycle with synthesis into a tagged research repository, and sprint-cadence opportunity-mapper updating the opportunity-solution tree. Every shipped feature must be traceable to a tagged opportunity; leakage above 30% is a signal that delivery has decoupled from discovery.

## Why

Discovery treated as a phase produces stale insights that cannot keep up with a product in motion. Without a recurring cadence, the same problems are "rediscovered" quarterly, and shipped features pile up without evidence of user impact. Continuous discovery closes the loop: behavioural data feeds experiment hypotheses, interview themes inform prioritization, and the opportunity-solution tree keeps delivery anchored to real user problems rather than internal requests.

## When To Use

- Product is past initial PMF and decisions have started feeling arbitrary; recurring discovery is needed to keep direction grounded.
- A delivery team has bandwidth to allocate ~15-20% to discovery without halting feature work.
- High-velocity environment (multiple releases per week) where one-off discovery cycles cannot keep pace.
- After a major launch, to monitor activation/retention while iterating.

## When NOT To Use

- Pre-PMF: continuous discovery dilutes effort across a wide problem space; concentrated discovery sprints work better.
- Solo founder with no recurring user pool yet — there is nothing to continuously sample.
- Frozen feature scope with imminent contractual deadline; findings cannot be acted on.
- Teams without analytics and a research repository; insights evaporate without structured storage.

## Content

| File | What's inside |
|------|---------------|
| `content/01-cadence.xml` | Three discovery loops (daily/weekly/sprint), capacity allocation rules, and the discovery-delivery leakage check. |
| `content/02-antipatterns.xml` | Discovery theatre, sample bias, insight burial, and synthesis agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/check-leakage.py` | Python script: flags releases unlinked to a research opportunity; fails when leakage exceeds 30%. |
