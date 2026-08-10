---
name: faion-net-content
description: Editorial pipeline for the faion.net content surface. Audience-first, subagent-driven, multilingual. Routes content production into discrete stages each owned by an isolated Claude Code subagent so the main thread stays a thin orchestrator. Triggers - new article ideas, brainstorming, "напиши статтю про X" / "write an article about X", longread review or translation, fresh editorial brief, ultimate-guide chapter.
---

# /faion-net-content

Pipeline orchestrator for faion.net ultimate-guide longreads. Each phase delegates to a specialized **Claude Code subagent** via the Task tool. Validation scripts live in the repo at `scripts/check-*.py` and `scripts/verify-ug-article.mjs` — subagents call them via Bash when relevant.

**This is the v4 (Claude-Code-subagent) architecture.** The legacy Python+Agent-SDK pipeline (`scripts/pipeline-run.py`) is retained for compatibility but new work goes through subagents.

## Phase 1 — Idea funnel (unchanged from v3)

Brainstorm and score with parallel subagents. See `prompts/phase1-brainstorm.md` and `prompts/phase1-score.md` for the prompts. Use Task tool with `subagent_type: general-purpose` for these.

## Phase 2 — Per-article workflow (subagent pipeline)

Triggered by user pointing at a backlog item: "напиши цю статтю", "розпиши `<slug>`".

| # | Step | Subagent | Inputs | Output |
|---|------|----------|--------|--------|
| A.1 | Outline | `faion-article-outliner` | seed file path | ArticleOutline JSON |
| A.2 | Write sections | `faion-article-writer` | outline JSON + working dir | N section-NN.md files + "DONE" |
| A.3 | Assemble en.mdx | main thread | section files + outline | `content/ultimate-guide/<slug>/en.mdx` |
| B | English review | `faion-article-reviewer-en` | en.mdx path | edits in place + "DONE" |
| C | Run en gates | main thread (Bash) | en.mdx | verify-ug + structural + ai-tells reports |
| D | QG fix (if needed) | `faion-qg-fixer` | en.mdx + gate findings | edits + "DONE" |
| E | Glossary extract | `faion-glossary-extractor` | en.mdx + existing slugs | candidate `<slug>.mdx` files in tmp |
| E.1 | Glossary copy | main thread | tmp candidates | non-colliding `.mdx` → `content/glossary/` |
| F | Translate × 7 | `faion-translator` ×7 parallel | en.mdx + target-lang | per-lang section files + meta JSON |
| F.1 | Assemble per lang | main thread | section files + meta | `<lang>.mdx` for each of 7 langs |
| G | Translation review × 7 | `faion-translation-reviewer` ×7 parallel | `<lang>.mdx` + en.mdx + language-rules | edits + "DONE" |
| H | Final gates per lang | main thread (Bash) | each `<lang>.mdx` | verify-ug + structural + ai-tells reports |

## Subagent invocation pattern

For each phase, the main thread uses the Task tool. Example for Phase A.1:

```
Task({
  description: "Outline article",
  subagent_type: "faion-article-outliner",
  prompt: "<seed>\n" + Read(seed_path) + "\n</seed>"
})
```

Phase F (parallel translations) — send 7 Task tool uses in ONE message so they run concurrently:

```
[7 parallel Task calls, each with subagent_type: "faion-translator"
 differing only in target-lang and output-directory]
```

## Validation scripts

Located in `<REPO_ROOT>/scripts/`:

| Script | Use after | Purpose |
|--------|-----------|---------|
| `verify-ug-article.mjs <article-dir>` | A.3, F.1 | structural sanity |
| `check-structural.py <file> --lang <lang> --json` | B, D, G, H | structural lint |
| `check-ai-tells.py <file> --lang <lang> --json` | B, D, G, H | banned phrases + em-dash |
| `check-glossary-coverage.py <file>` | B, G | first-mention GlossaryTerm wraps |

When a subagent has Bash tool, it can run these directly. When the main thread runs them, it parses JSON output and either passes findings to `faion-qg-fixer` (Phase D) or accepts the result.

## Per-article runner (headless)

For batch processing one article end-to-end:

```bash
bash scripts/orchestrator/queue-one-headless.sh <seed-path>
```

This invokes `claude -p` with the orchestrator prompt that walks through phases for that seed.

## Languages

en (source), uk, pt, es, fr, de, hi, pl — 8 total. See `config/languages.json` and `config/language-rules/<lang>.md` for per-language guidance passed to translator/reviewer subagents.

## Storage layout

```
~/workspace/projects/faion-net/faion-net-fe/
├── .aidocs/content/ultimate-guide/
│   ├── backlog/<slug>.md
│   ├── briefs/<slug>-{brief,keywords}.md
│   └── reviews/<slug>/
└── content/ultimate-guide/<slug>/
    ├── en.mdx + uk.mdx + pt.mdx + ... + pl.mdx
```

## Hard rules

- **Subagent-only synthesis.** Main thread orchestrates, persists state. Do NOT inline content writing/scoring/reviewing/translating in the main thread.
- **NERO persona** for Ukrainian content. Sharp, ironic, no-fluff.
- **Methodologies CLI-only.** Articles cite methodologies and link to the CLI command (`faion get-content <slug>`), they do NOT inline methodology bodies on the web.
- **Source-of-truth = English.** All translations derive from `en.mdx`.
- **No emojis in articles.**
- **Faion product positioning** per `/home/nero/workspace/projects/faion-net/AGENTS.md` (no token-pricing copy, CLI-first install messaging).
- **Score gate = 7** in Phase 1.

## Entry points

User says "почати pipeline" / "генерація ідей":
→ Phase 1, dispatch parallel general-purpose brainstorm + scoring subagents.

User points at backlog item and says "напиши цю статтю":
→ Phase 2 starting with faion-article-outliner.

User says "перекласти X на Y" (X already final EN):
→ Skip to Phase F (faion-translator) for lang Y, then Phase G.
