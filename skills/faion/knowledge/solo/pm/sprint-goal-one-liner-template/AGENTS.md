---
slug: sprint-goal-one-liner-template
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: A fill-in-the-blank template that compresses a sprint into one outcome sentence ("In sprint NN, we will <verb> <user/system> so that <measurable benefit>, focusing on <surface>, deferring <out-of-scope>"), recitable by every team member at standup.
content_id: "f53531ef5b14b308"
tags: [product-manager, sprint-planning, sprint-goal, recitable, template, solo-pm]
---
# Sprint Goal One-Liner Template

## Summary

**One-sentence:** A fill-in-the-blank template producing one recitable sentence — `In sprint NN, we will <verb> <user/system change> so that <measurable benefit>, focusing on <surface>, deferring <out-of-scope>` — that every team member can repeat at standup without looking it up.

**One-paragraph:** Where `sprint-goal-formula` defines WHAT a sprint goal must contain, this template defines the exact lexical shape PMs use to write it. The shape forces a verb-led, benefit-tied, scope-bounded sentence. The output gets pinned to the team's standup channel header, repeated in every standup opener, and used as the call-and-response check during sprint review. The muscle this builds — "compress a sprint into one sentence the team can recite" — is the part that scrum-ceremonies methodology does not teach. Solo and small-team PMs use this as their default sprint-goal writing pattern; senior teams may relax the shape after 5+ sprints of demonstrated recitability.

## Applies If (ALL must hold)

- A team works in fixed-cadence sprints with a designated PM facilitating planning.
- The goal needs to be communicated to people who did not attend planning (engineers, designers, stakeholders).
- The team has a single primary communication channel (Slack/Discord/Teams) where the goal can be pinned.
- The PM has the authority to refuse a "list of tasks" framing and push back for a single sentence.

## Skip If (ANY kills it)

- Solo developer with no team to recite to — template adds ceremony without value.
- Engineering-led teams that have proven sprint-goal discipline over many sprints — the shape becomes overhead.
- Continuous-flow teams without sprint boundaries — there is no sprint to template.
- Hard-bound contractual sprint with no PM discretion — the goal is the contract, not a sentence.

## Prerequisites

- Output of sprint planning: candidate items, primary outcome theme, named in-scope surface.
- Access to the team channel where the pinned message will live.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/sprint-goal-formula` | Defines the three required parts the template lexicalises. |
| `solo/pm/async-standup-methodology` | Standup cadence that re-uses the recited goal. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: literal template slots, max length, pin location, standup repetition, retire-on-completion. | ~900 |

## Related

- parent skill: `solo/pm/project-manager/`
- peer: `sprint-goal-formula`, `async-standup-methodology`, `retro-facilitation-multistyle`
- external: Scrum Guide 2020 §Sprint Goal
