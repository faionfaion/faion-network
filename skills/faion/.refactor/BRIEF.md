# Subagent Brief — Methodology Refactor (5-file → new shape)

You are a worktree subagent. Refactor the methodology folders in your assigned batch from the OLD 5-file shape (`README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`) to the canonical NEW shape defined in `docs/skill-authoring.md`.

## MANDATORY pre-flight (do this FIRST, before any file write)

Run these reads in parallel:

1. `Read docs/skill-authoring.md` — full structure spec
2. `Read skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml` — closed tag vocabulary for `content/*.xml`
3. `Read skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/AGENTS.md` — the canonical example methodology

Skipping these is the #1 cause of rejected batches. The conventions are non-obvious (semantic XML, role-bearing tags, no `README.md` in subfolders, strict `AGENTS.md` shape).

## Working directory rule

**CRITICAL: write files via worktree-relative paths (`skills/...`), NEVER absolute `/home/...`.** Absolute paths leak into the main repo working tree and bypass worktree isolation.

Always start with `pwd` and confirm you are inside the assigned worktree (its path will look like `.claude/worktrees/<id>/`). All edits use paths relative to that worktree root.

## Per-methodology procedure (run in parallel within the batch when sensible)

For each absolute target path in your TARGETS list:

### 1. Compute the worktree-relative path

The TARGETS are absolute paths under the main repo. Strip the main-repo prefix and prepend your worktree root. Example: `/home/.../faion-network/skills/faion/knowledge/free/dev/python-developer/django-models` → inside the worktree, that's `skills/faion/knowledge/free/dev/python-developer/django-models`.

### 2. Read the source files

Read these five files in parallel:
- `<dir>/README.md`
- `<dir>/checklist.md`
- `<dir>/templates.md`
- `<dir>/examples.md`
- `<dir>/llm-prompts.md`

Also `Read <dir>/agent-integration.md` if it exists (it was added by the earlier research-enrichment pass and contains agent-usage hints).

### 3. Plan the new shape

Produce in your head:
- A single concise `AGENTS.md` (Markdown, target 50-80 lines, hard cap 120) — Summary / Why / When To Use / When NOT To Use / Content / Templates / Scripts (only if scripts/ exists)
- 1-3 `content/NN-<topic>.xml` files (semantic XML using the closed tag glossary, target 30-80 lines each, hard cap 150)
- `templates/` folder ONLY if there is a real reusable artifact extractable from the old `templates.md` content (Pydantic model, JSON, prompt, config snippet — never prose). Native syntax (`.py`, `.json`, `.txt`). One file per artifact, under 80 lines each.
- `scripts/` only if a real verifier/applier/generator script exists.

Map old → new content:
- `README.md` rule + when-to/when-NOT → `AGENTS.md` Summary/Why/When-To/When-NOT
- `README.md` examples → `content/01-<topic>.xml` `<example>` blocks
- `checklist.md` step list → `content/<NN>-checklist.xml` with `<rule>`/`<step>` tags
- `templates.md` code snippets → real files in `templates/` + `<reference path="..."/>` from content
- `examples.md` real cases → `content/<NN>-examples.xml` `<example>`/`<antipattern>` tags
- `llm-prompts.md` prompts → `templates/prompt-*.txt` files + `<reference>` from content

Drop content that is pure filler ("be careful", "follow good practices") — every retained piece must carry information.

### 4. Write the new files

In this order:

1. Write `<dir>/CLAUDE.md` containing exactly one line: `@AGENTS.md`
2. Write `<dir>/AGENTS.md` per the strict shape (`docs/skill-authoring.md` § "AGENTS.md strict shape"). Tables for Content/Templates/Scripts indexes — no separate `README.md` index in subfolders.
3. Write each `<dir>/content/NN-<topic>.xml` using the closed tag vocabulary. Tags describe ROLE (`<rule>`, `<example>`, `<antipattern>`, `<reference>`), never appearance. Source code goes inside `<code lang="..."><![CDATA[ ... ]]></code>`. Cross-reference templates via `<reference path="templates/...">short purpose</reference>`.
4. Write `<dir>/templates/<file>` for each real artifact (omit folder if none).
5. Write `<dir>/scripts/<file>` only if a real script exists.

### 5. Delete the old files

After the new files are in place and pass the quality gates (next step), delete:
- `<dir>/README.md`
- `<dir>/checklist.md`
- `<dir>/templates.md`
- `<dir>/examples.md`
- `<dir>/llm-prompts.md`

Keep `<dir>/agent-integration.md` if present — fold its useful content into `AGENTS.md` and content files where appropriate, but do NOT delete it unless its content is fully absorbed.

### 6. Quality gates (per methodology — REJECT if any fail)

- [ ] `CLAUDE.md` has exactly `@AGENTS.md` (no other text)
- [ ] `AGENTS.md` has ALL six required sections: Summary, Why, When To Use, When NOT To Use, Content, Templates (Templates table can say "none" if folder absent — Scripts section optional)
- [ ] `AGENTS.md` ≤ 120 lines
- [ ] `content/` exists and has ≥ 1 file
- [ ] Every `content/*.xml` parses as valid XML
- [ ] Every `content/*.xml` uses ONLY tags listed in the tag glossary (or root-level common: `<text>`, `<summary>`, `<section>`, `<p>`, `<rule>`, `<statement>`, `<example>`, `<antipattern>`, `<why>`, `<code>`, `<reference>`, etc. — see glossary)
- [ ] No formatting tags (`<bold>`, `<heading>`, `<br>`, `<i>`)
- [ ] Source code wrapped in `<code lang="..."><![CDATA[ ... ]]></code>`
- [ ] No `README.md` inside `content/`, `templates/`, or `scripts/`
- [ ] No empty `templates/` or `scripts/` folder
- [ ] Old 5 files (`README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`) deleted
- [ ] Concrete, testable rule appears in `AGENTS.md` Summary/Why
- [ ] BOTH `When To Use` AND `When NOT To Use` are non-empty

If a methodology fails: roll back its directory to the original state (`git checkout -- <dir>` from the worktree), record `<path>\tFAIL\t<reason>` in your batch report, continue with the rest of the batch. Do NOT abort the batch.

## Commit policy (per batch, not per methodology)

After ALL methodologies in your batch are processed (succeeded or failed):

```bash
cd <worktree-root>
git add -A
# Append to faion-network/CHANGELOG.md under [Unreleased]:
#   - refactor: <N>/8 methodologies migrated to new shape (<batch-id>)
git add CHANGELOG.md
git commit -m "refactor: migrate <N> methodologies to new shape"
# (50-char title, no Co-Authored-By, no emojis)
```

## Merge policy (worktree → main)

This is the trickiest part. Your work lives in an isolated git worktree off `main`. To land it:

```bash
flock /tmp/faion-network-merge.lock bash -c '
  cd /home/nero/workspace/projects/faion-net/faion-network
  git fetch <your-worktree-branch>
  git merge --ff-only <your-worktree-branch>
  git push origin main
'
```

`flock` serializes concurrent merges from sibling worktrees. NEVER force-push. NEVER `--no-verify`.

If `git merge --ff-only` fails because main moved ahead:

```bash
cd <worktree-root>
git fetch origin
git rebase origin/main
# resolve any conflicts (CHANGELOG.md is the most likely conflict — keep both batch entries)
# then retry the flock'd merge above
```

## Return

Print to stdout for the orchestrator to record:

```
BATCH: <batch-id-or-first-target-basename>
ACCEPTED: <count>
REJECTED: <count>
COMMIT: <SHA>
PATHS:
  <abs-path-1>: OK
  <abs-path-2>: FAIL — <reason>
  ...
```

## On quota exhaustion (PARK protocol)

If you see `QUOTA-PARK-SUBAGENT` from the `quota-guard.py` PreToolUse hook (or any tool fails because the hook returns exit 2 with that string), STOP immediately. Do NOT keep trying tools — they will all fail.

In your final response include these markers on their own lines so the orchestrator can record you to `~/.claude/parked-subagents.json`:

```
PARK_REQUEST: <your-agent-id>      (from the hook message, or your worktree dir name `agent-XXX`)
PARENT_PID: <pid>                   (from the hook message; "unknown" is acceptable)
PARENT_SESSION: <uuid>              (from the hook message; "unknown" is acceptable)
BATCH_PATHS:
<each absolute path from your TARGETS list, one per line, indented under this header>
PARTIAL_PATHS:
<each path where files were written but not committed, one per line>
```

Then return your normal `BATCH/ACCEPTED/REJECTED/COMMIT/PATHS` block. The orchestrator parses both blocks: it appends parked entries (keyed by `PARENT_SESSION` so each parent only resumes its own subagents) and either re-dispatches or rolls back partials when the quota recovers.

If the hook error is something OTHER than `QUOTA-PARK-SUBAGENT` (e.g. the hook script went missing entirely), still emit `PARK_REQUEST` with the agent ID — the orchestrator treats that as a generic park signal and will re-dispatch on resume.

## Hard rules (do NOT violate)

- NEVER `--no-verify`. Pre-commit hooks must pass.
- NEVER force-push to main.
- NEVER write to absolute paths under `/home/...` — those leak the worktree.
- NEVER skip the pre-flight Reads. Even if you "remember" the spec.
- NEVER mix Markdown bodies into `content/*.xml`. Only semantic XML.
- NEVER add `<bold>`, `<heading>`, `<br>`, `<i>` or any formatting tag.
- NEVER add `README.md` inside `content/`, `templates/`, or `scripts/`.
- NEVER leave an empty `templates/` or `scripts/` folder.
- NEVER touch methodologies under `geek/ai/ai-agents/` — those 15 are out of scope per the migration note.
- If pre-commit hook fails: read the error, fix the root cause, re-stage, re-commit. Do NOT bypass.
