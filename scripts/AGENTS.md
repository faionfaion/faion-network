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
| `regen-tier-manifest.py [--dry-run]` | Rebuilds `skills/tier-manifest.json` from `meta.json` under `knowledge/`, `playbooks/`, `fragments/<library>/`, `tools/<pack>/` and `lexicon/`. `--dry-run` first, always. Keeps the previous `notes` verbatim behind a `Prior notes, verbatim:` prefix; re-running at the same version leaves `notes` untouched |
| `lib/snapshot.sh` · `lib/integrity-check.sh` | Installer helpers sourced by `update.sh`, not standalone — the caller must already define `log_info` / `log_success` / `log_warning` / `log_error` / `log_file`. Unit-tested by `tests/test_snapshot.sh` |

## Gotchas

- **`build-domain-index-v2.py` is broken — do not run it.** It parses YAML frontmatter that no methodology `AGENTS.md` carries post-F-067, returns 0 entries, and `--write` empties the target `INDEX.xml`. `INDEX.xml` is edited by hand until it is fixed.
- Superseded, kept for history — do not run against the live corpus: `apply-domain-merge.py`, `migrate-f067.py`, `migrate-methodology-to-v2.py`, `migrate-playbook-to-v2.py`, `migrate-playbook-yaml-to-xml.py`, `fix-methodology-phase-d.py`, `build-methodology-index.py`, `build-methodology-index-c.py`, `validate-playbook-v2.py`, `validate-methodology-xml.py`. `slug-rename-map.json` is their input.
- Anything writing `skills/tier-manifest.json` or an `INDEX.xml` mutates 2,637 methodology paths at once. Diff before committing.
- Validators exit 1 on failure and are the gate for corpus work; `f066-validate-all.sh` swallows detail (`tail -3`), so rerun the failing validator directly.
