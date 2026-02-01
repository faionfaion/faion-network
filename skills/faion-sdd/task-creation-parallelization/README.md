# Task Creation & Parallelization

> Decompose complex features into LLM-executable tasks with optimal parallelization.

## When to Use

- Breaking down implementation plans into executable tasks
- Planning wave-based parallel execution
- Preparing context-rich tasks for AI coding agents
- Managing dependencies between tasks

## Why It Matters

| Problem | Without Decomposition | With Decomposition |
|---------|----------------------|-------------------|
| Context overflow | Model forgets parts of task | Each task fits in context |
| Inconsistency | "10 devs worked without talking" | Patterns propagate correctly |
| Wasted effort | Re-discovers patterns each time | Builds on prior work |
| No parallelization | Sequential bottleneck | 2-4x speedup via waves |
| Debugging hell | Can't isolate failures | Clear task boundaries |

## Key Principles

### 1. Right-Size Tasks (100k Token Rule)

| Complexity | Tokens | Description |
|------------|--------|-------------|
| Simple | <30k | Single file, clear pattern |
| Normal | 30-60k | Multiple files, some decisions |
| Complex | 60-100k | Architecture decisions, research |

**Maximum:** 100k tokens per task (single context window)

### 2. INVEST Criteria

- **Independent** - Can execute without other incomplete tasks
- **Negotiable** - Implementation details can be refined
- **Valuable** - Clear business value linkage
- **Estimable** - Token budget can be estimated
- **Small** - Fits in single context window
- **Testable** - Clear acceptance criteria (Given-When-Then)

### 3. Wave-Based Execution

```
Wave 1: [TASK-001, TASK-002] - No dependencies
    |
    v
Wave 2: [TASK-003, TASK-004] - Depend on Wave 1
    |
    v
Wave 3: [TASK-005, TASK-006] - Depend on Wave 2
```

**Benefits:**
- Parallel execution within waves
- Context learnings propagate between waves
- Pattern discovery in early waves benefits later tasks

### 4. Context Budget Allocation

| Phase | Budget | Purpose |
|-------|--------|---------|
| SDD Docs | 15% | constitution, spec, design |
| Task Tree | 10% | Completed dependency summaries |
| Research | 25% | Existing code patterns |
| Implementation | 40% | Actual coding |
| Testing | 10% | Verification |

## LLM-Specific Considerations

### Context Window Management

**Problem:** LLMs have fixed context limits (100k-200k tokens). Exceeding causes:
- Forgotten requirements
- Inconsistent patterns
- Incomplete implementations

**Solution:**
1. Break work into context-sized chunks
2. Include dependency task summaries (not full content)
3. Reference patterns by file path, not inline code

### Pattern Propagation

**Problem:** Each task session starts fresh. Without explicit patterns:
- Different naming conventions
- Inconsistent error handling
- Duplicated utilities

**Solution:** Task Dependency Tree section with:
- Summary of completed dependencies
- Key patterns to follow
- Critical code snippets

### One Task, One Focus

**Research shows:** LLMs fail when asked to plan and code simultaneously.

**Best Practice:**
- Planning tasks: Research and document approach
- Implementation tasks: Execute documented plan
- Never combine "figure out how" with "build it"

### Verification Without Human Feedback

For autonomous execution:
- Include specific test commands in AC
- Define success criteria programmatically
- Use linting/formatting as automated checks

## Tools & Integrations

### Claude Code

- Use `CLAUDE.md` for project conventions
- `/clear` between tasks to reset context
- Extended thinking: "think" < "think hard" < "ultrathink"
- Subagent verification for complex tasks

### Cursor

- Plan Mode for decomposition research
- Custom modes for planner vs executor separation
- `@File` references instead of pasting code
- Commit between tasks for rollback safety

### Taskmaster AI

- Automatic PRD-to-task decomposition
- Complexity analysis (1-10 scoring)
- IDE detection (Cursor, Cline, Claude Code, etc.)
- MCP integration for task management

### Generic Best Practices

- Commit after each task completion (save points)
- Use git worktrees for parallel experiments
- Cross-model review (write with Claude, review with GPT)
- Embed testing in every task

## External Resources

### Anthropic (Official)

- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Official tips for agentic coding
- [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) - Multi-window agent patterns
- [Long-Running Agent Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) - Context bridging techniques

### Practitioner Guides

- [Addy Osmani: LLM Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/) - Comprehensive workflow guide
- [Structured Agentic Workflow for Cursor](https://www.reinforcementcoding.com/blog/structured-agentic-workflow-template) - XML-based structured workflows
- [Task-Based AI Coding System](https://meelis-ojasild.medium.com/turning-cursor-into-a-task-based-ai-coding-system-31e1e3bf047b) - Cursor custom modes

### Research & Theory

- [Task Decomposition Architectures](https://mgx.dev/insights/task-decomposition-for-coding-agents-architectures-advancements-and-future-directions/a95f933f2c6541fc9e1fb352b429da15) - Academic overview
- [Decomposed Prompting (DecomP)](https://learnprompting.org/docs/advanced/decomposition/decomp) - Prompt engineering techniques
- [AutoGen Task Decomposition](https://microsoft.github.io/autogen/0.2/docs/topics/task_decomposition/) - Multi-agent approaches

### Tools

- [Taskmaster AI](https://www.task-master.dev/) - AI-powered task management for IDEs
- [Claude Task Master (GitHub)](https://github.com/eyaltoledano/claude-task-master) - Open source task management

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |

## Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [writing-implementation-plans](../writing-implementation-plans/) | Input for task creation |
| [writing-specifications](../writing-specifications/) | Source of FR-X requirements |
| [writing-design-documents](../writing-design-documents/) | Source of AD-X decisions |
| [quality-gates-confidence](../faion-sdd-execution/quality-gates-confidence/) | Task validation checkpoints |

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step decomposition checklist |
| [examples.md](examples.md) | Real-world decomposition examples |
| [templates.md](templates.md) | Task templates and scripts |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted decomposition |

---

*Version 3.0.0 | Updated for LLM coding agents (Claude Code, Cursor, Copilot)*
