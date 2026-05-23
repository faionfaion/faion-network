# Versioned Agent-Memory Files (decisions / patterns / mistakes)

## Summary

**One-sentence:** Persist long-term agent memory as four committed Markdown files (decisions.md, patterns.md, mistakes.md, session.md) versioned in-repo so the agent rehydrates context from disk, not chat.

**One-paragraph:** Versioned Agent-Memory Files (decisions / patterns / mistakes) produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Long-running project where conversational context resets between sessions.
- Team handoff where a new agent operator needs prior-decisions context.
- Self-improvement loop: agent records its own mistakes for future runs.
- SDD workflow where session.md tracks current feature + task state.

## Applies If (ALL must hold)

- Project spans > 1 month and / or > 5 sessions.
- Decisions and patterns repeatedly bite the agent across sessions.
- Repo allows .aidocs/memory/ or .claude/memory/ committed.
- Operator agrees to maintain the files (or wires a hook to update them).

## Skip If (ANY kills it)

- One-off task — no future session to remember.
- Solo author + memory in head — overhead > value.
- Files would leak secrets — keep memory ephemeral or encrypted.
- Team refuses to commit AI artefacts to the repo.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| .aidocs/memory/ dir | writable dir at repo root | repo lead |
| File templates | decisions.md / patterns.md / mistakes.md / session.md | this methodology |
| CLAUDE.md sync rule | agent loads memory on session start | agent config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[kb-agents-md-context-pyramid]] | Memory complements AGENTS.md context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `memory_init` | haiku | Mechanical template instantiation. |
| `session_close_update` | sonnet | Decide which lessons graduate to patterns.md. |
| `mistakes_classify` | sonnet | Tag mistakes for future avoidance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decisions.md` | Decisions log template. |
| `templates/patterns.md` | Patterns library template. |
| `templates/mistakes.md` | Mistakes log template. |
| `templates/session.md` | Session state template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kb-versioned-agent-memory-files.py` | Validate the memory-bundle structure. | pre-merge of memory change |

## Related

- [[kb-agents-md-context-pyramid]]
- [[kb-ai-assisted-lessons-learned-synthesis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
