# BRIEF — feature-045 methodology-xml migration

You are a migration agent. You receive a batch of methodology folders. For each one, replace its `*.md` body files (and any existing `content/*.xml`) with a **single `methodology.xml`** in the new schema.

## Your single source of truth

Read these BEFORE touching any file:

1. `docs/methodology-xml-schema.md` — the schema spec (folder layout, root element, mandatory fields, content sections, validation rules, migration mapping tables).
2. `docs/methodology-tag-glossary.xml` — closed tag vocabulary. Unknown tags fail validation.
3. `docs/examples/methodology-reference.xml` — fully migrated reference example.
4. `scripts/validate-methodology-xml.py` — validator. Run after every methodology you touch.

If you skip these you will produce broken output. The validator runs in pre-commit and CI; it WILL reject the commit.

## Your batch input

Each batch line is one absolute methodology folder path:

```
/home/nero/workspace/projects/faion-net/faion-network/skills/faion/knowledge/<tier>/<group>/<domain>/<slug>/
```

Default batch size: 3 folders. Hard cap: 5.

## Per-folder procedure

### Step 1 — read every existing body file

OLD shape (5-file pattern):
- `README.md`, `agent-integration.md`, `checklist.md`, `examples.md`, `llm-prompts.md`, `templates.md`

NEW shape (intermediate):
- `AGENTS.md`, `CLAUDE.md`, `content/*.xml`

Do NOT touch `templates/*` or `scripts/*` files — they stay as-is.

### Step 2 — derive metadata

| Field | Source |
|-------|--------|
| `slug` (root attr) | folder name |
| `<tier>` | first path segment after `knowledge/` |
| `<group>` | second path segment |
| `<domain>` | third path segment |
| `<summary>` (≤200 chars) | first prose paragraph of source, trimmed at word boundary |
| `<created>` | today's ISO date if not derivable from git log |
| `<tags>` | 3-5 keyword tags from filename / H2 list |
| `<category>` (sdlc-ai only) | prefix before first `-` (e.g. `lint-megalinter-polyglot` → `lint`) |
| `<difficulty>` | infer from content; default `intermediate` for geek/pro, `beginner` for free |

### Step 3 — derive content (the agent-facing payload)

Map source markdown sections to schema tags using `docs/methodology-xml-schema.md` § "Migration Mapping". The mandatory order:

1. `<title>` — verbatim H1.
2. `<summary>` — TL;DR (1-3 sentences). Distinct from `<metadata>/<summary>`; can be longer.
3. `<why>` — verbatim "Why" / "Why It Matters" prose. Wrap each paragraph in `<p>`.
4. `<when-to-use>` — `<list>/<item>` per bullet.
5. `<when-not-to-use>` — same format. MUST exist; if missing, infer 1-3 anti-cases from content.
6. Body sections — convert each H2/H3 region to `<section name="...">` with rules, examples, antipatterns inside.
7. `<templates>` / `<scripts>` — auto-generated from existing `templates/` and `scripts/` folder contents.
8. `<see-also>` — collect external URLs and peer references.

### Step 4 — preserve verbatim

**This is the single biggest failure mode.** Do NOT summarize, do NOT rephrase prose to make it shorter. Migration is a format change, not an editorial pass. The validator runs a length-parity check — content text length must be ≥80% of source markdown text length.

Code blocks: keep verbatim, wrap in `<code lang="...">` with `<![CDATA[...]]>`. Do not re-indent.

### Step 5 — write `methodology.xml`

At the methodology folder root. Use exactly this skeleton:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<methodology slug="<folder-name>">
  <metadata>
    <tier>...</tier>
    <group>...</group>
    <domain>...</domain>
    <summary>...</summary>
    <!-- recommended: tags, category, difficulty, created -->
  </metadata>
  <content>
    <title>...</title>
    <summary>...</summary>
    <why>...</why>
    <when-to-use>...</when-to-use>
    <when-not-to-use>...</when-not-to-use>
    <!-- body: sections with rules, examples, antipatterns -->
    <!-- templates/scripts blocks if folder exists -->
    <!-- see-also block if there are cross-references -->
  </content>
</methodology>
```

### Step 6 — delete old body files

After `methodology.xml` is in place and validates:
- Remove `README.md`, `agent-integration.md`, `checklist.md`, `examples.md`, `llm-prompts.md`, `templates.md`.
- Remove `AGENTS.md`, `CLAUDE.md` (from methodology root).
- Remove `content/` folder entirely (its content is inlined into `methodology.xml`).
- KEEP `templates/`, `scripts/`, and any other non-methodology files.

Use `git rm` so the deletions are tracked.

### Step 7 — validate

Run from repo root:

```bash
python3 scripts/validate-methodology-xml.py <abs-path-to-folder>
```

If it fails, read the error code, fix, re-run. Common failures:

| Code | Fix |
|------|-----|
| `XML_PARSE` | Likely an unescaped `<` or `>` in prose — wrap code in CDATA, escape inline `<`/`>`/`&` in element text. |
| `UNKNOWN_TAG` | Tag not in glossary. Either pick an existing tag or — only with strong reason — extend `methodology-tag-glossary.xml` first. |
| `META_*` | Mandatory metadata missing/wrong-valued. |
| `LENGTH_PARITY` | You summarized. Re-add the cut content verbatim. |
| `EMPTY_CONTAINER` | A `<rule>`, `<example>`, etc. has no body. Either fill or remove. |

### Step 8 — commit per methodology folder

ONE commit per methodology, NOT one commit per batch. This keeps `git log` searchable per-slug. Format:

```
chore: migrate <slug> to methodology.xml

Source: <list of removed files>
Closed-shape: methodology.xml validated by scripts/validate-methodology-xml.py
```

Update `CHANGELOG.md` once per BATCH (add one line under `## [Unreleased]`).

## Hard rules

1. NEVER use `--no-verify`. If pre-commit fails, fix the issue.
2. NEVER summarize content during migration. Verbatim or near-verbatim only.
3. NEVER touch `templates/` or `scripts/` file bodies — they are real files.
4. NEVER write absolute paths. All file references inside `methodology.xml` are relative to the methodology folder.
5. NEVER invent tags. Update the glossary first if absolutely needed (rare).
6. NEVER commit without running the validator.

## Worktree merge protocol

Subagents run in isolated worktrees. To merge to main:

```bash
flock /tmp/faion-network-merge.lock bash -c '
  cd /home/nero/workspace/projects/faion-net/faion-network
  git fetch origin main
  git merge --ff-only <worktree-branch> || (git rebase origin/main && git merge --ff-only <worktree-branch>)
  git push origin main
'
```

If the rebase produces conflicts in `CHANGELOG.md`, keep both entries and re-stage.

## Reporting

After the batch, output exactly:

```
batch=<line> done=<N> failed=<M> commits=<sha-list>
```

Nothing else. Parent thread parses this.
