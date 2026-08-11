# faion-network

Methodology corpus and Claude Code skill base for the `faion` CLI. Auto-loaded in every session (symlinked as `~/workspace/.claude`), so this file stays inside the 20-80 line budget — deep content lives in `.agents/`.

| Item | Value |
|------|-------|
| Repo | `faionfaion/faion-network` |
| Corpus | 2,637 methodologies over 22 domains, 455 playbooks, 6 workflows, 6 skill dirs |
| Gating | `skills/tier-manifest.json` v11, 3,099 entries — authoritative path-to-tier map |
| Tiers | free / solo / pro / geek (cumulative) |
| Distribution | Read by `faion-cli` at runtime; read by `faion-net-be` on disk via `KNOWLEDGE_ROOT` + `TIER_MANIFEST_PATH`; not bundled into the public `faion` plugin |
| Ecosystem | `../AGENTS.md` — full stack and runtime data flow |

## Layout

| Path | What |
|------|------|
| `skills/faion/knowledge/<domain>/<slug>/` | Methodology: `AGENTS.md` + `meta.json` + `content/*.xml` (+ `templates/`, `scripts/`) |
| `skills/faion/playbooks/by-goal/<goal>/<slug>/` | Playbook: `AGENTS.md` + `content/01-playbook.xml` |
| `skills/faion/workflows/` | 6 orchestration workflows (brainstorm, idea-to-prod, improver, media-ops, poll-agents, sdd-batch-orchestrator) |
| `skills/faion/tools/<pack>/` | Tool pack: `meta.json` + `scripts/<name>.py\|sh` + `tools/<name>.card.md` — runnable tools an agent uses instead of writing a throwaway script |
| `skills/faion/lexicon/` | UA→EN query lexicon: `meta.json` (tier **free**) + `ua-en.tsv` + `ua-stopwords.txt` — a Ukrainian query scores zero against an English corpus without it |
| `skills/tier-manifest.json` | Generated from `meta.json` files — never hand-edit |
| `agents/` · `hooks/` · `rules/` | Subagent definitions · plugin hooks (`hooks.json`) · authoring rules |
| `workflows/` | Runnable Workflow-tool scripts, invoked by name (`article-pipeline`) |
| `scripts/` | Validators and index/manifest generators |
| `docs/` | Corpus specs: `skill-authoring.md`, `directory-structure.md`, `methodology-xml-schema.md` |
| `.aidocs/` | SDD lifecycle docs for this repo |
| `.agents/` | Deep reference — see [.agents/INDEX.md](.agents/INDEX.md) |

## Commands

```bash
bash scripts/f066-validate-all.sh                    # all 7 corpus validators, summary report
python3 scripts/validate-methodology-v2.py <dir>     # one methodology dir
python3 scripts/validate-playbook-v3.py --all        # all playbooks
python3 scripts/validate-domains-index.py            # L1 domains.xml
python3 scripts/validate-lexicon.py                  # UA→EN lexicon shape + provenance
python3 scripts/regen-tier-manifest.py --dry-run     # manifest diff vs meta.json (drop flag to write)
bash tests/test_snapshot.sh                          # installer unit tests
bash init.sh                                         # install skills + agents into ~/.claude
```

## Rules

- **Commits** — `type: short description`, 50-char title, no `Co-Authored-By`, no emojis. Every commit adds an entry under `## [Unreleased]` in `CHANGELOG.md`.
- **Language** — user Ukrainian; docs, code and subagent prompts English.
- **Documentation** — no ASCII art; tables, lists, arrows (`→`) and directory trees are fine.
- **Docs convention** — every source dir carries `CLAUDE.md` (exactly `@AGENTS.md`) + `AGENTS.md` (20-80 lines: purpose, file table, commands, gotchas). Full rules: [.agents/docs-convention.md](.agents/docs-convention.md)
- **SDD** — features `backlog/ → todo/ → in-progress/ → done/`; tasks inside a feature `todo/ → in-progress/ → done/`. Document types and CR/BUG streams: [.agents/sdd-lifecycle.md](.agents/sdd-lifecycle.md)
- **No time estimates** — never state hours, days or dates in SDD docs; use qualitative complexity and token estimates.
- **Linting** — every project must have working pre-commit hooks; on failure fix the cause, never `--no-verify`. Per-project setup: [.agents/linting.md](.agents/linting.md)
- **Skill authoring** — read `rules/skill-authoring.md` before creating or editing anything under `skills/`.
- **Adapters** — packaged for Claude Code and Codex; runtime-specific behavior: [.agents/adapters.md](.agents/adapters.md)

## Gotchas

- `skills/tier-manifest.json` is **generated** from `meta.json` files — regenerate with `regen-tier-manifest.py`; hand-edits get overwritten.
- **`scripts/build-domain-index-v2.py` is BROKEN — never run it.** It reads YAML frontmatter that 0 of 2,637 methodology `AGENTS.md` files carry (F-067 moved that metadata to `meta.json`), so it returns 0 entries for every domain and `--write` silently empties the `INDEX.xml` it targets. Until it is repaired, `INDEX.xml` entries are added **by hand**: one `<methodology slug tier path>` block with a `<summary>`, kept alphabetical, with the `count=` attribute bumped to match.
- The manifest is at `skills/tier-manifest.json`, not the repo root.
- No git hook is installed here — the `CHANGELOG.md` rule is enforced by review, not automatically.
- Methodology and playbook dirs already carry their own `AGENTS.md` envelope fixed by the corpus spec. Do not add repo-style `AGENTS.md` / `CLAUDE.md` pairs anywhere under `skills/faion/knowledge/**` or `skills/faion/playbooks/**`.
- Retrieval is two-level: read `skills/faion/knowledge/domains.xml` (L1), pick at most 3 domains, then their `INDEX.xml` (L2) before opening any leaf. Never enumerate the corpus.
- `docs/catalog.json`, `README.md` and `skills/CLAUDE.md` still quote pre-F-067 counts (52 knowledge bases, 1,300+ methodologies). The manifest is the source of truth.
