# Loop Prompt — SDLC+AI Methodologies Cycle

**Working directory:** `/home/nero/workspace/projects/faion-net/faion-network`
**State:** `.aidocs/sdlc-ai-methodologies/`

## Each tick (5 min cadence) — do this:

### 1. Read state

```
Read: .aidocs/sdlc-ai-methodologies/state.json
Read: .aidocs/sdlc-ai-methodologies/candidates.md  (last 200 lines)
Read: .aidocs/sdlc-ai-methodologies/methodologies.jsonl  (last 50 lines)
```

If `state.json.accepted >= 52` → STOP. Output `loop done — 52/52 reached. Stop the loop.` and do nothing else.

### 2. Decide phase

| accepted | phase | action |
|----------|-------|--------|
| 0 | bootstrap | If research subagents not yet done, wait (do nothing this tick). Otherwise transition to seed-from-research. |
| 0–10 | seed-from-research | Read `research/AGENT-*.md`, extract candidates into `candidates.md`, accept the strongest 3-5 into `methodologies.jsonl` + write README+checklist+templates+examples+llm-prompts in `geek/sdlc-ai/<slug>/` |
| 10–35 | expand | Brainstorm 5 new candidates in `brainstorm/CYCLE-NN.md` (avoid duplicating accepted), promote 2-3, write methodology files |
| 35–52 | fill-gaps | Look at `state.json.categories` — find under-target categories, brainstorm specifically for those |
| 52+ | publish | Generate site articles for any accepted methodology not yet in `articles-published/MAP.md`, then STOP the loop |

### 3. Each tick MUST commit progress

- Update `state.json` (accepted count, cycle++)
- Append to `progress.md` what was done
- `git add .` then `git commit -m "sdlc-ai: cycle N — added M methodologies"` (50-char title)
- Update `CHANGELOG.md` under `## [Unreleased]` (faion-network has a pre-commit hook requiring this)

### 4. Quality gates before accepting a candidate

- [ ] Concrete, testable rule (not vague)
- [ ] Cited source (URL) OR cited project path
- [ ] When-to-use AND when-NOT-to-use both stated
- [ ] Not a near-duplicate of an accepted one
- [ ] Mapped to one of the 10 categories

### 5. Methodology file shape

`skills/faion-knowledge/knowledge/geek/sdlc-ai/<slug>/`

- `README.md` (rule, when-to/when-NOT, examples, references)
- `checklist.md` (apply-step-by-step)
- `templates.md` (code/config templates)
- `examples.md` (real cases)
- `llm-prompts.md` (prompts that exemplify the rule)

### 6. Site article shape (only at phase=publish)

Each accepted methodology → MDX article at:
`/home/nero/workspace/projects/faion-net/faion-net-fe/content/knowledge/sdlc/SDL-A-NNN.mdx`

Use existing CNT-A-001.mdx frontmatter shape. `domain: "sdlc"`, `tier: "advanced"`.

Update `articles-published/MAP.md`: `<methodology-slug> → SDL-A-NNN`.

### 7. End-of-tick output

One short paragraph back. No long summaries.

### 8. Stop condition

When `state.json.accepted >= 52` AND every methodology has a published article: stop the cron with `CronDelete` (don't re-fire).
