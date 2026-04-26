# Methodology Research Brief (batch mode — 5-10 adjacent methodologies per agent)

You are researching a **batch of 5-10 adjacent methodologies** inside `skills/faion/knowledge/` and shipping the whole batch end-to-end: research each → write each file → update CHANGELOG (single entry for batch) → commit → merge into `main`.

You run inside an isolated git worktree (parent invoked with `isolation: "worktree"`). Worktree is on a fresh branch off `main`. Main repo path: `/home/nero/workspace/projects/faion-net/faion-network`.

## Inputs (provided to you)

- `TARGETS` — list of absolute paths (one per line) to methodology directories. Each contains `README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`.

## Step 1 — research each target

For EACH target path in turn, do the research steps below. Don't parallelize inside your agent — go sequentially, one methodology at a time. That's fine: the gain is fewer parent-agent turns, not per-target speed.

Research per target:
1. Read `README.md` (full), skim other four files.
2. **Agentic usage** — Claude subagent fit; look in `agents/` or `skills/*/agents/` via Glob. Name specific agents if relevant.
3. **CLI tools & APIs** — industry standard (WebSearch allowed).
4. **Services & apps** — SaaS/OSS with APIs/CLIs agents can drive.
5. **Templates & scripts** — inline ≤50-line script if it materially helps.
6. **When to use / NOT use / failure modes** — concrete situations.
7. **Best practices** — non-obvious real-world usage.
8. **AI-agent-specific gotchas** — LLM-execution breakpoints, human-in-loop checkpoints.

## Step 2 — write `agent-integration.md` for EACH target

Create `<TARGET_PATH>/agent-integration.md` using this exact skeleton:

```markdown
# Agent Integration — <Methodology Name>

## When to use
- <bullet>

## When NOT to use
- <bullet>

## Where it fails / limitations
- <bullet>

## Agentic workflow
<2–4 sentences on driving this methodology with Claude subagents.>

### Recommended subagents
- `<agent-name>` — <what>

### Prompt pattern
<1–2 short snippets>

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|

## Templates & scripts
<"See templates.md for X" OR inline script ≤50 lines>

## Best practices
- <bullet>

## AI-agent gotchas
- <bullet>

## References
- <URL or book/paper>
```

Rules per file:
- **Do not edit** existing methodology files. Only create `agent-integration.md`.
- No filler. Every bullet specific. "Use best practices" banned.
- Length: 100–300 lines (shorter OK for narrow topics).
- No emojis. English only.
- If methodology too thin for a useful deliverable: write a 20-30 line note explaining why — that's acceptable.

## Step 3 — update CHANGELOG.md (single batch entry)

Under `## [Unreleased]` → `### Added`, append ONE line summarizing the whole batch:

```
- Research: batch of N methodologies in <group>/<subgroup> — <methodology-slug-1>, <methodology-slug-2>, ... (see agent-integration.md per dir).
```

Keep to one line. Don't restructure. If the batch spans multiple groups, say "mixed group" and list slugs.

## Step 4 — commit in your worktree

```bash
# you're in the worktree root
git add skills/faion/knowledge/**/agent-integration.md CHANGELOG.md
git commit -m "research: enrich batch of N methodologies"
```

Commit message: 50-char title; optional body listing slugs; no "Co-Authored-By"; no emojis; no `--no-verify`. Pre-commit hook MUST pass — fix issues if it fails, re-stage, re-commit.

## Step 5 — merge into main (serialized via flock)

```bash
WORKTREE=$(pwd)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
MAIN_REPO=/home/nero/workspace/projects/faion-net/faion-network

flock /tmp/faion-research-merge.lock bash -euc "
  cd $MAIN_REPO
  git fetch $WORKTREE $BRANCH:refs/research/$BRANCH
  git merge --ff-only refs/research/$BRANCH || {
    cd $WORKTREE
    git fetch $MAIN_REPO main:refs/heads/main-latest
    git rebase refs/heads/main-latest
    cd $MAIN_REPO
    git fetch $WORKTREE $BRANCH:refs/research/$BRANCH
    git merge --ff-only refs/research/$BRANCH
  }
"
```

If merge still fails: return FAIL, don't force-push, don't reset main.

## Step 6 — return summary (one line only)

On success:
`OK batch of N — <short-batch-label>, merged to main`

On failure:
`FAIL batch of N — <step-name>: <reason>`

No other output, no per-file recap.

## Hard rules

- Never force-push, never `--no-verify`, never touch `main` except via locked ff-only merge.
- Never edit files outside target methodology dirs and CHANGELOG.md.
- One commit for the whole batch (not per-file).
- If mid-batch a target is already enriched (agent-integration.md exists), skip it and note in commit body.
- **NEVER write files via absolute paths** like `/home/nero/workspace/projects/faion-net/faion-network/skills/...`. Those resolve to the **main repo's working tree**, not your worktree, and leak files outside isolation. Always `cd` into your worktree first and use paths relative to it (or `$(pwd)/...`). The absolute TARGETS list is only for identifying *which* methodologies to enrich; convert to the matching relative path inside your worktree before any Write/Edit call.
