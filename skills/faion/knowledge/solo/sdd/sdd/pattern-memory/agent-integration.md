# Agent Integration — Pattern Memory

## When to use
- After a successful task execution where a non-obvious solution was applied — capture before the session ends
- When the same problem appears for the second time in a different context — that's a pattern, not a one-off
- Before starting a new task wave — inject high-confidence patterns (0.8+) into the task context header
- During CLAUDE.md maintenance: sync established patterns (0.9+) into the project rules file
- When onboarding a new agent session that lacks project history — load `patterns.md` as working memory

## When NOT to use
- Capturing well-known best practices already documented in framework docs (e.g., "use async/await for async operations")
- One-off fixes specific to a single file or edge case — not reusable enough to be a pattern
- Patterns with confidence < 0.5 (only one use, unverified) — capture as candidate, don't promote to active patterns.md
- Project-specific configuration values (API keys, service URLs) — those go in `.env`, not patterns

## Where it fails / limitations
- Pattern confidence scores are self-assessed by agents; without external validation they inflate over time
- The confidence decay formula (−0.05 per 90 days unused) is not automatically applied — requires a maintenance cron or manual review
- Working memory (current task) and project memory (patterns.md) are separate; agents forget to propagate discoveries upward after task completion
- Duplicate patterns accumulate across waves when different agents capture the same solution independently; no deduplication mechanism is built in
- CLAUDE.md sync is manual — if patterns.md is updated but CLAUDE.md isn't, the next agent session won't see the new patterns

## Agentic workflow
At task completion, the execution agent runs a "pattern extraction" step: it reviews what it implemented and identifies solutions that (a) solved a recurring problem, (b) are not obvious from framework docs, and (c) worked in this context. It writes candidate patterns to `patterns.md` at confidence 0.5. After 2-3 confirmations across different tasks, confidence rises to 0.8 and the pattern is synced to CLAUDE.md. A maintenance agent (can run on schedule) reviews patterns.md and archives entries with confidence < 0.4 or last-used > 90 days.

### Recommended subagents
- `faion-sdd-execution` skill — includes reflexion learning which captures patterns post-review
- Post-task extraction agent (haiku) — mechanical pattern capture from execution report
- Pattern review agent (sonnet) — validates pattern quality, checks for duplicates, assigns confidence

### Prompt pattern
```
You have just completed task [TASK-ID]. Review your implementation.
Identify patterns worth capturing: solutions to recurring problems, non-obvious insights,
approaches that prevented a mistake.
For each candidate pattern, output:
- ID: PAT-XXX
- Problem: [what triggers this]
- Context: [when to apply]
- Solution: [the approach, ≤ 10 lines of code if applicable]
- Evidence: [TASK-ID]
- Confidence: 0.5
Do NOT capture: obvious practices, one-off fixes, config values.
```

```
Review patterns.md. For each pattern:
1. Is it specific and generalizable? (not too narrow, not too broad)
2. Has it been used in 2+ different contexts? (raise confidence to 0.7)
3. Has it been validated by a reviewer? (raise to 0.8)
4. Is it duplicated by another pattern? (merge if so)
5. Last used > 90 days? (lower confidence by 0.05, consider archiving)
Output: updated confidence scores and archive candidates.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code) | Pattern extraction + CLAUDE.md sync within session | https://docs.anthropic.com/en/docs/claude-code |
| `git log --follow` | Track pattern evolution across commits | Built-in |
| `jq` | Parse structured pattern metadata if stored as JSON | `apt install jq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Mem0 | OSS/SaaS | Yes | Dedicated agent memory layer; API-driven; supports hierarchical memory (working/session/project/global) |
| LangChain LangMem | OSS | Yes | Long-term memory for LangChain agents; project-level storage |
| MemGPT | OSS | Yes | OS-paradigm memory management; paging between context and storage |
| CLAUDE.md (file) | N/A | Yes | Primary in-context pattern delivery for Claude Code sessions |

## Templates & scripts
See `templates.md` for pattern entry format and patterns.md structure.

Pattern sync to CLAUDE.md script (inline):
```bash
#!/usr/bin/env bash
# sync-patterns.sh
# Extracts high-confidence patterns from patterns.md and appends to CLAUDE.md
set -euo pipefail
PATTERNS_FILE=".aidocs/memory/patterns.md"
CLAUDE_FILE="CLAUDE.md"
if [ ! -f "$PATTERNS_FILE" ]; then
  echo "No patterns.md found"
  exit 0
fi
# Extract patterns with confidence >= 0.8
HIGH_CONF=$(awk '/Confidence: 0\.[89]|Confidence: 1\.0/{found=1} found{print} /^---/{found=0}' "$PATTERNS_FILE")
if [ -z "$HIGH_CONF" ]; then
  echo "No high-confidence patterns to sync"
  exit 0
fi
# Check if Learned Patterns section exists
if grep -q "## Learned Patterns" "$CLAUDE_FILE"; then
  echo "CLAUDE.md already has Learned Patterns section — update manually"
else
  echo "" >> "$CLAUDE_FILE"
  echo "## Learned Patterns" >> "$CLAUDE_FILE"
  echo "$HIGH_CONF" >> "$CLAUDE_FILE"
  echo "Synced $(echo "$HIGH_CONF" | grep -c "^###" || echo 0) patterns to CLAUDE.md"
fi
```

## Best practices
- Capture patterns immediately after task completion while the implementation context is fresh — don't defer to "end of sprint"
- Use the confidence scoring formula objectively; require 2+ distinct context uses before raising above 0.6
- Store patterns in `.aidocs/memory/patterns.md` (project-local), not in global Claude memory — patterns are project-specific
- Include "when NOT to use" for each pattern — a pattern applied in the wrong context is worse than no pattern
- Archive patterns unused for 90+ days to `patterns-archive.md` rather than deleting — they may be relevant for seasonal or infrequent tasks

## AI-agent gotchas
- Agents conflate "pattern" with "code snippet" — a pattern must include the problem context and when-to-use, not just the code
- Without explicit extraction prompt at task end, agents never capture patterns — build extraction into the task completion checklist
- Loading all patterns.md into every task context wastes tokens; filter by relevance to current task domain before injecting
- High-confidence patterns that become outdated (library upgrade, architectural change) mislead agents — require patterns to reference the version/context they were validated in
- The CLAUDE.md sync step is the most skipped; if skipped, each new agent session relearns patterns from scratch — treat sync as mandatory, not optional

## References
- https://arxiv.org/abs/2303.11366 — Reflexion: Language Agents with Verbal Reinforcement Learning
- https://mem0.ai/blog/memory-in-agents-what-why-and-how — Mem0 memory layer
- https://langchain-ai.github.io/langmem/concepts/conceptual_guide/ — LangChain LangMem
- https://refactoring.guru/design-patterns — Software Design Patterns reference
- https://martinfowler.com/eaaCatalog/ — Patterns of Enterprise Application Architecture
