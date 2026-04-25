# Agent Integration — Reflexion Learning

## When to use
- In any multi-task SDD workflow where agent quality must improve across tasks within a session or project
- When an agent has failed the same type of task more than once — Reflexion provides the verbal feedback loop to break the cycle
- When running unattended overnight agent batches where no human is available to correct mid-task failures
- When setting up a new project's `.aidocs/memory/` structure — Reflexion defines the memory architecture (patterns.md, mistakes.md, session.md)

## When NOT to use
- Single-shot one-off tasks with no follow-up (no memory to accumulate)
- Tasks where external ground truth is unavailable (tests, linter, type checker) — Reflexion requires external feedback signals; self-evaluation alone degrades quality
- Projects under 1 week old with fewer than 10 completed tasks — the memory corpus is too thin to provide useful patterns
- When speed is the constraint and the memory loading overhead is unacceptable (rare for text-based tasks)

## Where it fails / limitations
- Reflexion only works with external feedback signals (tests, CI, linter) — self-correction without external signals has a 64.5% blind spot rate (per TACL 2024 survey)
- Memory files grow without bound; without periodic pruning, loading mistakes.md and patterns.md may consume significant context budget (~10-20k tokens for large projects)
- Confidence scores require consistent tracking; agents that update confidence manually introduce drift; scores become meaningless after several inconsistent updates
- Pattern decay (90-day unused patterns) is difficult to implement in a Markdown file without tooling; most projects skip it and accumulate stale patterns
- The PDCA cycle adds overhead per task; for very small tasks (< 5k tokens to execute), the overhead may exceed the value of the learning loop

## Agentic workflow
The full PDCA-Reflexion cycle operates as follows: (Plan) the agent loads session.md, queries patterns.md for relevant patterns, and queries mistakes.md for domain warnings; (Do) the agent executes the task with loaded context; (Check) the agent evaluates output against acceptance criteria, generates a verbal reflection on what succeeded or failed; (Act) the agent updates patterns.md with new successful patterns, appends to mistakes.md if a failure occurred, and updates session.md for continuity. The `faion-sdd-executor-agent` implements this cycle implicitly through its pre-task and post-task phases.

### Recommended subagents
- `faion-sdd-executor-agent` — the primary implementation of the PDCA-Reflexion cycle in this project; pre-task loads memory, post-task writes reflections
- Opus-tier subagent — verbal reflection generation after complex failures; needs reasoning depth to produce useful Five Whys chains
- Sonnet-tier subagent — pattern extraction after successful tasks; pattern writing is less demanding than failure analysis

### Prompt pattern
```
[PLAN PHASE] Before executing TASK-042:
1. Load patterns.md — list patterns matching keywords: [auth, jwt, middleware]
2. Load mistakes.md — list warnings matching keywords: [auth, jwt, middleware]
3. Summarize: what should I apply, what should I avoid?
Output a 5-bullet context summary, then proceed to execution.
```

```
[CHECK PHASE] TASK-042 is complete. Evaluate against acceptance criteria:
AC-1: [criterion text] — PASS/FAIL + evidence
AC-2: [criterion text] — PASS/FAIL + evidence
[ACT PHASE] Based on the evaluation:
- If any PASS: extract a new PAT-NNN entry for patterns.md
- If any FAIL: extract a new MIS-NNN entry for mistakes.md
- Update session.md with current state and open questions
Write all three updates now.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rg` (ripgrep) | Fast keyword search in patterns.md and mistakes.md | `brew install ripgrep` / [docs](https://github.com/BurntSushi/ripgrep) |
| `jq` | Query structured memory (mistakes.jsonl, patterns.jsonl) | `brew install jq` / [docs](https://jqlang.github.io/jq/) |
| `pytest` | External feedback signal for Python tasks (test results drive reflection) | `pip install pytest` / [docs](https://docs.pytest.org/) |
| `eslint` / `tsc` | External feedback signals for TypeScript/JavaScript tasks | `npm i -g eslint typescript` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS CI | Yes | CI results are external feedback; pipe results back into agent context via artifacts |
| Sentry | SaaS | Yes — API | Production error signals can trigger retrospective Reflexion cycles |
| noahshinn/reflexion | OSS | Yes | Official Reflexion implementation; useful as reference, not plug-in |

## Templates & scripts
See `templates.md` for PAT-NNN and MIS-NNN entry formats and the session.md structure.

Confidence updater (Python, updates pattern confidence in patterns.md):
```python
#!/usr/bin/env python3
"""Update confidence score for a pattern after task outcome."""
import re, sys

def update_confidence(path: str, pat_id: str, outcome: str) -> None:
    text = open(path).read()
    # Find confidence line for this pattern
    pattern = rf'(## {re.escape(pat_id)}.*?)(Confidence: )(\d+\.\d+)'
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        print(f"Pattern {pat_id} not found"); return
    old = float(m.group(3))
    if outcome == "success": new = min(0.95, old + 0.05)
    elif outcome == "partial": new = old * 0.95
    else: new = max(0.30, old - 0.15)
    updated = text.replace(f"Confidence: {old}", f"Confidence: {round(new, 2)}", 1)
    open(path, "w").write(updated)
    print(f"{pat_id}: {old} -> {round(new, 2)} ({outcome})")

if __name__ == "__main__":
    update_confidence(sys.argv[1], sys.argv[2], sys.argv[3])
```

## Best practices
- Never skip the external feedback step — tests, linter, type checker; without it, verbal reflection is self-referential and degrades quality
- Load only relevant patterns (keyword-filtered), not the entire patterns.md; full file loads burn 5-15k tokens of context budget
- Write reflections immediately after task completion, not at the end of a session; memory of what failed fades within a single conversation turn
- Keep PAT-NNN patterns action-oriented: "When X, do Y" format; descriptions of what worked are less useful than prescriptions
- Set a maximum of 3 retry attempts per task before escalating to human review; Reflexion improves on retry but has diminishing returns past 3 cycles
- Archive patterns with confidence < 0.3 or older than 90 days without usage; stale patterns introduce noise into context

## AI-agent gotchas
- LLMs performing self-evaluation in the Check phase exhibit systematic optimism: they report AC as "PASS" when they would fail against an independent test suite; external tests must be the authoritative signal
- Reflexion memory loaded from a previous session may contain context from a different codebase if session.md is not cleared between projects — always initialize session.md at project start
- Agents asked to "reflect on the session" at the end of many tasks produce generic patterns ("write tests first") rather than project-specific ones; require the reflection to reference specific task IDs and file names
- The confidence decay rule (0.9x after 90 days) is impossible to enforce in Markdown without tooling; in practice, confidence scores become stale optimistically (high scores for unused patterns); treat all confidence scores over 90 days old as unreliable
- Multi-agent pipelines where multiple agents share the same patterns.md can produce write conflicts; serialize memory writes through a single coordinator agent

## References
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) — NeurIPS 2023 (original paper)
- [When Can LLMs Actually Correct Their Own Mistakes?](https://arxiv.org/abs/2406.01297) — TACL 2024 (self-correction blind spot study)
- [Training Language Models to Self-Correct via RL (SCoRe)](https://arxiv.org/abs/2409.12917) — ICLR 2025
- [noahshinn/reflexion — Official Implementation](https://github.com/noahshinn/reflexion)
- [PDCA Cycle for AI Code Generation — InfoQ](https://www.infoq.com/articles/PDCA-AI-code-generation/)
- [PDCA Cycle — Wikipedia](https://en.wikipedia.org/wiki/PDCA)
- [Kaizen — Wikipedia](https://en.wikipedia.org/wiki/Kaizen)
