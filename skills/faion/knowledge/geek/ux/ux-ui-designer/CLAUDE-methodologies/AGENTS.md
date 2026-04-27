# UX/UI Methodologies

## Summary

Index and selection guide for 32 core UX methodologies covering Nielsen's 10 usability heuristics, 6 research methods (interviews, usability testing, surveys, card sorting, personas, journey mapping), 9 design methods (wireframing, prototyping, A/B testing, heuristic evaluation, cognitive walkthrough, and others), and 7 advanced topics (IA framework, IA templates, mobile UX, voice UI, diary studies, competitive analysis, content audit). Agent role: select, scaffold, and synthesize — not replace human participant work.

## Why

Applying the wrong UX method wastes research budget and produces misleading artifacts. Method selection depends on the question type (qualitative vs. quantitative, generative vs. evaluative), user access level, and timeline. This index maps problem types to methods so agents route correctly instead of defaulting to the most familiar technique.

## When To Use

- Agent must select an appropriate UX research or design method for a given product problem
- Automated heuristic evaluation against Nielsen's 10 usability principles is needed
- Sprint requires a structured UX deliverable (persona, journey map, IA sitemap) that an agent can scaffold
- UX review of an existing design must be documented systematically before a critique session
- Cognitive walkthrough must be scripted for a new user flow

## When NOT To Use

- User interviews, usability testing, focus groups, diary studies — require real human participants; agent cannot substitute for moderation or empathy-based interpretation
- Card sorting, tree testing — require actual user responses; agent can analyze results but not generate them
- A/B testing — requires live traffic; agent can design the test and analyze results, not run it
- Any method where output quality depends on observed human behavior in context

## Content

| File | What's inside |
|------|---------------|
| `content/01-method-index.xml` | Full method index: 32 methodologies mapped to problem type, artifact, and input required |
| `content/02-agent-rules-and-gotchas.xml` | What agents can/cannot do per method, heuristic eval rules, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/heuristic-eval-template.py` | Prints a Nielsen heuristic evaluation scoring template |
| `templates/prompt-method-selection.txt` | Agent prompt: recommend 3 UX methods given problem, budget, and user access |
| `templates/prompt-heuristic-eval.txt` | Agent prompt: apply Nielsen's 10 heuristics to a UI description |
