# Loop Prompt — Agent Methodologies Brainstorm Cycle

**Working directory:** `/home/nero/workspace/projects/faion-net/faion-network`
**State:** `.aidocs/agent-methodologies/`

## Each tick (5 min cadence) — do this:

### 1. Read state

```
Read: .aidocs/agent-methodologies/state.json
Read: .aidocs/agent-methodologies/candidates.md  (last 200 lines)
Read: .aidocs/agent-methodologies/methodologies.jsonl  (last 50 lines)
```

If `state.json.accepted >= 50` → STOP. Output `loop done — 50/50 reached. Stop the loop.` and do nothing else.

### 2. Decide phase

| accepted | phase | action |
|----------|-------|--------|
| 0 | bootstrap | If research subagents not yet dispatched, dispatch them (Task #3). If dispatched but pending, do project-mining (Task #4). |
| 0–10 | seed-from-research | Read `research/AGENT-*.md`, extract candidates into `candidates.md`, accept the strongest 3-5 into `methodologies.jsonl` + write README+checklist+templates+examples+llm-prompts in `geek/ai/ai-agents/<slug>/` |
| 10–30 | expand | Brainstorm 5 new candidates in `brainstorm/CYCLE-NN.md` (avoid duplicating accepted), promote 2-3 into accepted, write methodology files |
| 30–50 | fill-gaps | Look at `state.json.categories` — find under-target categories, brainstorm specifically for those |
| 50 | publish | Generate site articles for any accepted methodology not yet in `articles-published/MAP.md` |

### 3. Each tick MUST commit progress

- Update `state.json` (accepted count, cycle++)
- Append to `progress.md` what was done
- `git add .` then `git commit -m "agents: cycle N — added M methodologies"` (50-char title rule)

### 4. Quality gates before accepting a candidate

- [ ] Concrete, testable rule (not vague)
- [ ] Cited source (URL) OR cited project path
- [ ] When-to-use AND when-NOT-to-use both stated
- [ ] Not a near-duplicate of an accepted one (search `methodologies.jsonl`)
- [ ] Mapped to one of the 10 categories (state.json.categories keys)

### 5. Methodology file shape

Each accepted methodology lives at:
`skills/faion-knowledge/knowledge/geek/ai/ai-agents/<slug>/`

5 files (existing convention):
- `README.md` (the rule, when-to-use, examples, references)
- `checklist.md` (apply-step-by-step)
- `templates.md` (code/prompt/schema templates)
- `examples.md` (real examples — at least one from our projects when possible)
- `llm-prompts.md` (prompts that exemplify the rule)

### 6. Site article shape (only at phase=publish)

Each accepted methodology → MDX article at:
`/home/nero/workspace/projects/faion-net/faion-net-fe/content/knowledge/agents/AGT-A-NNN.mdx`

Use existing CNT-A-001.mdx frontmatter shape:
```yaml
---
id: "AGT-A-NNN"
title: "<methodology title>"
subtitle: "<one-line hook>"
tier: "advanced"
domain: "agents"
description: "<2 sentences>"
keywords: [...]
author: "faion.net"
created: "2026-04-25"
updated: "2026-04-25"
readingTime: "X min"
---
```

Then update `articles-published/MAP.md`: `<methodology-slug> → AGT-A-NNN`.

### 7. End-of-tick output

One short paragraph back to the harness telling the user what changed this cycle. No long summaries.

### 8. Self-pacing

Use ScheduleWakeup with `delaySeconds: 270` (4m30s — under 5m to stay in cache window) when:
- A research subagent is still running and you're waiting on its output
- Otherwise use 1200s (20 min) for idle ticks

If 50 reached → DO NOT call ScheduleWakeup. Loop ends.
