---
name: claude-code-subagents-slash
description: Define a Claude Code subagent and expose it as a slash command; wire parallel invocation via the Agent tool and isolate long-running work in a worktree.
tier: geek
group: claude-code-skills
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working `/code-review` slash command that spawns a `code-reviewer` subagent, runs review logic in an isolated context window, and returns structured findings — without polluting the orchestrator's context.

## Prerequisites

- Claude Code installed and configured (≥ version with Agent tool support).
- A project with `.claude/agents/` and `.claude/commands/` directories (or willingness to create them).
- Familiarity with YAML/Markdown front-matter.
- Understanding of what an isolated context window means: the subagent starts fresh, sees only what you pass in, cannot read the caller's conversation history.

## Steps

1. Create the agents directory if it does not exist.

   ```bash
   mkdir -p .claude/agents
   ```

2. Author the subagent definition at `.claude/agents/code-reviewer.md`. Front-matter controls model, allowed tools, and a description that Claude Code uses to decide when to auto-delegate.

   ```markdown
   ---
   name: code-reviewer
   description: >
     Performs a structured code review: checks for logic bugs, security issues,
     test coverage gaps, and style violations. Returns a Markdown report with
     severity ratings (critical / major / minor / nit).
   model: claude-sonnet-4-6
   tools:
     - Read
     - Glob
     - Grep
     - Bash
   ---

   You are a senior engineer performing a focused code review.

   You will receive:
   - `DIFF` — the unified diff of changes to review
   - `CONTEXT` — optional background (ticket ID, design doc link)

   Return ONLY the Markdown review report in this structure:

   ## Summary
   One paragraph: overall quality signal.

   ## Findings
   | Severity | File:Line | Issue | Suggestion |
   |----------|-----------|-------|------------|

   ## Verdict
   APPROVE / REQUEST_CHANGES / NEEDS_DISCUSSION
   ```

   Key front-matter fields:
   - `model` — `claude-opus-4-7` for reasoning-heavy tasks; `claude-sonnet-4-6` for throughput; `claude-haiku-4-5-20251001` for cheap classification.
   - `tools` — whitelist only what the agent needs. A reviewer does not need `Write` or `Edit`.
   - `description` — written for Claude Code's router, not for humans. Starts with the action the agent performs.

3. Author the slash command at `.claude/commands/code-review.md`. Commands are lightweight: they inject context and delegate to the agent.

   ```markdown
   ---
   allowed-tools:
     - Agent
     - Bash
   ---

   Run a structured code review on the current working tree changes.

   Steps:
   1. Capture the diff: `!git diff HEAD`
   2. Pass it to the code-reviewer subagent via the Agent tool with the prompt:
      "Review this diff. DIFF:\n<diff output>"
   3. Print the returned report verbatim.
   ```

   The `!`-prefix executes the Bash command at invocation time and injects its stdout inline. This means the command always reviews the *current* diff, not a stale snapshot.

4. Verify the subagent appears in Claude Code's agent roster.

   ```bash
   # List agents Claude Code can see (project-level)
   ls .claude/agents/
   # Expected: code-reviewer.md
   ```

   Reload your Claude Code session if you added the file mid-session — agents are loaded at startup.

5. Invoke the slash command manually to confirm end-to-end wiring.

   Type `/code-review` in the Claude Code chat. Claude Code will:
   - Execute `git diff HEAD` via the `!`-prefix.
   - Call the Agent tool targeting `code-reviewer`.
   - Stream the subagent's structured report back into the conversation.

6. Add a second subagent for parallel invocation. Create `.claude/agents/security-scanner.md` following the same pattern (model: `claude-sonnet-4-6`, tools: `Read, Grep, Bash`). Update the command to spawn both agents concurrently via two Agent tool calls in the same response turn.

   Claude Code executes multiple Agent tool calls issued in the same response turn in parallel. This halves wall-clock time when the two tasks are independent (review logic vs. scan secrets).

7. Isolate a long-running subagent in a worktree to prevent file-system conflicts when it runs concurrently with the main session.

   ```bash
   # Create a dedicated worktree for the agent
   git worktree add .claude/worktrees/review-agent HEAD
   ```

   Pass the worktree path as context in the Agent tool call:

   ```
   Working directory for this task: .claude/worktrees/review-agent
   DIFF: <diff output>
   ```

   The agent operates on its own checkout. When done, prune the worktree:

   ```bash
   git worktree remove .claude/worktrees/review-agent
   ```

   Use this pattern when the subagent might write files (e.g., auto-fix mode). Skip it for read-only reviewers — it adds overhead for no benefit.

8. Scope the subagent to global if you need it across all projects. Move the file to `~/.claude/agents/code-reviewer.md`. Project-level agents (`.claude/agents/`) override global agents with the same name.

## Verify

Run `/code-review` against a branch with at least one staged change:

```bash
git diff HEAD --stat
# Should show at least 1 file changed
```

Then invoke `/code-review` in Claude Code. Expected output:

```
## Summary
...
## Findings
| Severity | File:Line | Issue | Suggestion |
...
## Verdict
APPROVE  (or REQUEST_CHANGES)
```

If the agent was spawned correctly, the conversation shows a nested "Subagent: code-reviewer" span in the tool-use trace. The orchestrator context window does NOT show the full review reasoning — only the final report.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `/code-review` not in the `/` menu | Command file not loaded or front-matter invalid | Check `.claude/commands/code-review.md` exists; verify YAML front-matter is valid (no tabs, correct `allowed-tools` key) |
| Agent tool call returns empty | `description` in agent front-matter does not match the Agent tool's routing heuristic | Rewrite description to start with the action verb and include the domain term (e.g., "Performs code review") |
| Subagent reads stale diff | `!git diff HEAD` ran at command-load time, not invocation time | Ensure the `!`-prefix command is inside the command body, not in front-matter |
| Two parallel agents produce conflicting writes | Both agents share the same working directory | Add a dedicated worktree per agent (Step 7); or confirm both agents are read-only before running parallel |
| `claude-opus-4-7` model errors with "model not found" | Typo in model field or model not available in your API tier | Use exact model IDs: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001` |
| Worktree add fails: "already exists" | Previous run left a stale worktree | `git worktree remove --force .claude/worktrees/review-agent` then re-add |
| Agent ignores the tool whitelist | Front-matter `tools` key parsed as a string, not a list | Each tool on its own line under `tools:` with a leading `- ` |

## Next

- Add a `/fix-review` command that pipes the report back into a `code-fixer` subagent, completing a review-then-fix loop without human intervention.
- Read [claude-code-skill-authoring](../claude-code-skill-authoring/playbook.md) to package the reviewer into a reusable skill with its own `SKILL.md` and trigger keywords, making it discoverable across projects.
- Explore model routing: use `claude-haiku-4-5-20251001` for the initial triage pass (cheap, fast) and escalate to `claude-opus-4-7` only when the triage agent returns `NEEDS_DISCUSSION`.

## References

- [knowledge/geek/ai/claude-code/agents](../../../../../knowledge/geek/ai/claude-code/agents) — defines the subagent front-matter contract (model, tools, description), context-isolation guarantee, and parallel execution semantics used in Steps 2, 6, and 7.
- [knowledge/geek/ai/claude-code/commands](../../../../../knowledge/geek/ai/claude-code/commands) — covers the slash-command front-matter (`allowed-tools`), the `!`-prefix live-context injection pattern used in Step 3, and the ≤250-line size limit.
