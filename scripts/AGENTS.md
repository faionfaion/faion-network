# scripts/

Corpus validators and generators. Run from the repo root; every script resolves paths relative to it.

## Current tooling

| Script | Use |
|--------|-----|
| `f066-validate-all.sh [report]` | Runs the 10 corpus validators, writes a pass/fail summary (default `/tmp/f066-validate-report.txt`). ~4 min, ~205 s of it validator 3 |
| `check-validators.sh --fast\|--check-fast\|--check-all\|--write-baseline` | The same validators in gateable form: `FAIL` lines normalised to `<id>\t<path>` and diffed against `validator-baseline.txt`. New line blocks, disappeared line is reported as a fix. What `pre-commit` runs |
| `validator-baseline.txt` | The committed failure SET (21 lines). The gate is the set, never a count — a count waves through a swap. Refresh with `check-validators.sh --write-baseline` |
| `install-hooks.sh [--quiet]` | Points `core.hooksPath` at `.githooks`. Idempotent; refuses to overwrite a foreign `hooksPath`. Called by `init.sh` and by `check-validators.sh` |
| `validate-methodology-v2.py <dir>` | One methodology dir (positional, no `--all`) |
| `validate-methodology-decision-tree.py --all` | Mandatory `06-decision-tree.xml` |
| `validate-methodology-templates.py --all` · `validate-methodology-scripts.py --all` | `templates/` and `scripts/` per methodology |
| `validate-playbook-v3.py --all` | Playbooks (v3 layout); `--self-test` available |
| `validate-domains-index.py` · `validate-domain-index.py --all` | L1 `domains.xml` and L2 `INDEX.xml` |
| `validate-playbook-taxonomy.py` · `validate-workflow-v2.py` | Goal taxonomy, workflow shape |
| `validate-lexicon.py [dir]` | UA→EN lexicon: file hygiene, row shape, byte order, every `en` term attested in the corpus, `src` re-derived and compared to the declared value, the 20% `observed` cap, stopwords disjoint from the prefixes |
| `validate-fragments.py` · `validate-recipes.py` · `validate-tools.py` | Fragments, recipes, tool packs. All three import `schema_check.py` by absolute path and `ImportError` without it |
| `schema_check.py` | Shared JSON-Schema subset checker. Not standalone; deleting it kills three gate validators at import time |
| `regen-tier-manifest.py [--dry-run]` | Rebuilds `skills/tier-manifest.json` from `meta.json` under `knowledge/`, `playbooks/`, `fragments/<library>/`, `tools/<pack>/` and `lexicon/`. `--dry-run` first, always. Keeps the previous `notes` verbatim behind a `Prior notes, verbatim:` prefix; re-running at the same version leaves `notes` untouched |
| `regen-fragment-index.py [--check] [--only tools]` · `regen-playbook-index.py [--check]` | L2 `INDEX.xml` for fragments/recipes/tools, and the 11 playbook goal indexes. Both read `meta.json`; `--check` is the drift gate |
| `regen-domains-xml.py [--write]` | L1 `domains.xml` + L2 knowledge `INDEX.xml` from `meta.json`. Dry-run by default, backs up before writing. **This is how `INDEX.xml` is maintained** — hand-editing was a workaround for the deleted frontmatter builders and let `count=` drift |
| `repair-playbook-bridge.py [--dry-run]` | Repairs playbook→methodology references. Hard-depends on `slug-rename-map.json` and on the `REMAP` dict inside `remap-dangling-wikilinks.py`, both read as data — aborts without either. Has **not** converged: still reports 3 files it would change |
| `test-retrieve-2level.py` | Two-level retrieval smoke test. Wired into nothing, still finds a live regression (L1 embed 2,768 words against a 1,500 cap) |
| `update.sh` · `lib/snapshot.sh` · `lib/integrity-check.sh` | End-user installer update path (`README.md`, copied by `init.sh`). The `lib/` helpers are sourced, not standalone — the caller must already define `log_info` / `log_success` / `log_warning` / `log_error` / `log_file`. Unit-tested by `tests/test_snapshot.sh` |

## Gotchas

- **The do-not-run list is gone because the scripts are gone.** 13 dead files were deleted 2026-08-14: three frontmatter index builders that wrote `count="0"` over live indexes, six finished migration one-shots, and four validators whose target file type no longer exists anywhere in the corpus. Knowledge `INDEX.xml` entries are still added by hand — see `regen-domains-xml.py` above for why its replacement is not yet trusted.
- **`slug-rename-map.json` is not migration residue.** The old list filed it as migrator input; `repair-playbook-bridge.py` reads it at runtime and aborts without it. Same for `remap-dangling-wikilinks.py`, whose `REMAP` literal is parsed as data even though the script itself has converged.
- `validate-domain-index.py` (singular, L2 per-domain) and `validate-domains-index.py` (plural, L1) are **not** a duplicate pair. Both are gate validators; the one-letter difference is the only thing distinguishing them.
- Anything writing `skills/tier-manifest.json` or an `INDEX.xml` mutates thousands of paths at once (manifest v14: 3,067 entries). Diff before committing.
- Validators exit 1 on failure and are the gate for corpus work; `f066-validate-all.sh` swallows detail (`tail -3`), so rerun the failing validator directly.
