# Methodology Research Brief (subagent prompt template)

You are researching ONE methodology inside `skills/faion-knowledge/knowledge/` and shipping the change end-to-end: research → write file → update CHANGELOG → commit in your worktree → merge into `main`.

You run inside an isolated git worktree (your parent invoked you with `isolation: "worktree"`). The worktree is on a fresh branch off `main`. The main repo path is `/home/nero/workspace/projects/faion-net/faion-network`.

## Inputs (provided to you)

- `TARGET_PATH` — absolute path to the methodology directory inside the worktree.
  (It contains `README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`.)

## Step 1 — research (deep, multi-angle)

1. Read the existing methodology (README first, then skim the other 4 files).
2. **Agentic usage** — how does this methodology fit with Claude subagents? Which subagents in this repo (look in `agents/` or `skills/*/agents/` — use Glob) are relevant? What prompt patterns work best?
3. **CLI tools & APIs** — industry standard for this methodology (WebSearch allowed).
4. **Services & apps** — SaaS/OSS with APIs/CLIs agents can drive.
5. **Templates & scripts** — reusable script/config/boilerplate. Inline a small script (≤50 lines bash/python) if it materially helps.
6. **When to use / when NOT to use / where it fails** — concrete situations, not hand-waving.
7. **Best practices** — non-obvious, from real-world usage.
8. **AI-agent-specific gotchas** — where LLM execution breaks; human-in-the-loop checkpoints.

## Step 2 — write `agent-integration.md`

Create `<TARGET_PATH>/agent-integration.md` with this exact skeleton:

```markdown
# Agent Integration — <Methodology Name>

## When to use
- <bullet: concrete situation>

## When NOT to use
- <bullet>

## Where it fails / limitations
- <bullet>

## Agentic workflow
<2–4 sentences on how to drive this methodology with Claude subagents. Name specific subagents from this repo if relevant.>

### Recommended subagents
- `<agent-name>` — <what it does in this flow>

### Prompt pattern
<1–2 short prompt snippets>

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|

## Templates & scripts
<Either: "See `templates.md` for X" OR inline a new script/template. Keep inline ≤50 lines.>

## Best practices
- <bullet>

## AI-agent gotchas
- <bullet>

## References
- <URL or book/paper>
```

Rules for the file:
- **Do not edit** existing methodology files. Only create `agent-integration.md`.
- No filler. Every bullet specific. "Use best practices" banned.
- Length: 150–300 lines; shorter if topic is narrow.
- No emojis. English only.
- If methodology is too thin for a useful deliverable, write a 30-line note explaining why — that's acceptable.

## Step 3 — update CHANGELOG.md (in your worktree root)

Under `## [Unreleased]` → `### Added`, append (or create if missing):

```
- Research: <methodology-slug> — agent-integration.md (<lines> lines).
```

Keep it to one line. Don't restructure the file.

## Step 4 — commit in your worktree

```bash
cd <worktree-root>  # your pwd is already the worktree root
git add skills/faion-knowledge/knowledge/<tier>/<group>/<domain>/<methodology>/agent-integration.md CHANGELOG.md
git commit -m "research: <methodology-slug> agent-integration"
```

Commit message format: 50-char title, no body needed, no "Co-Authored-By", no emojis.
Pre-commit hook will run. If it fails, read the error, fix, re-stage, re-commit. Never `--no-verify`.

## Step 5 — merge into main (serialized via file lock)

Merges are serialized across parallel agents via a flock on `.research/merge.lock`:

```bash
WORKTREE=$(pwd)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
MAIN_REPO=/home/nero/workspace/projects/faion-net/faion-network

flock /tmp/faion-research-merge.lock bash -euc "
  cd $MAIN_REPO
  git fetch $WORKTREE $BRANCH:refs/research/$BRANCH
  git merge --ff-only refs/research/$BRANCH || {
    # Main moved; rebase our branch onto main then merge
    cd $WORKTREE
    git fetch $MAIN_REPO main:refs/heads/main-latest
    git rebase refs/heads/main-latest
    cd $MAIN_REPO
    git fetch $WORKTREE $BRANCH:refs/research/$BRANCH
    git merge --ff-only refs/research/$BRANCH
  }
"
```

If the merge step fails despite the rebase, abort: do NOT force-push, do NOT reset main. Return a FAIL status in your summary.

## Step 6 — return summary (one line only)

On success:
`OK <methodology-slug> — agent-integration.md (<lines> lines), merged to main`

On failure at any step:
`FAIL <methodology-slug> — <step-name>: <reason>`

No other output. No recap. No explanation of process.

## Hard rules

- Never force-push, never `--no-verify`, never touch `main` except through the locked ff-only merge above.
- Never edit files outside `<TARGET_PATH>` and `CHANGELOG.md`.
- If pre-commit hook modifies files, re-stage and re-commit (not amend).
- If anything in steps 3–5 fails irrecoverably, leave your worktree as-is and return FAIL. The parent will clean up.
