# tools/

Tool packs: real, reusable scripts an agent runs instead of writing a throwaway one, each with an instruction card. F029 materialises a pack into `~/.faion/tools/<pack>/`.

**Card-first rule.** The card is the contract. An agent must be able to run the tool correctly having read `tools/<name>.card.md` and nothing else — never open the script to work out its arguments, and never re-implement a tool that already has a card. If the card and the script disagree, the card is the bug report.

## Packs

| Pack | Tier | Tools |
|------|------|-------|
| `python-web/` | free | `venv-bootstrap.sh` — idempotent `.venv` create + requirements install + import proof; `django-test-gate.py` — run a Django suite through the project venv, emit one JSON verdict line |
| `game-dev/` | solo | `hmac-rng-golden.py` — emit/verify golden vectors for HMAC-SHA256 rejection-sampling randomness; `deploy-scaffold.py` — systemd unit + nginx vhost + `deploy.sh`, identities namespaced by `--name` |
| `research/` | free | `source-table.py` — claims JSONL → markdown evidence table + gaps report + commercial-lever ledger, fails on an unsourced load-bearing claim or a commercial claim with no lever; `lever-check.py` — ledger × concept verdict → applied/declined counts with every decline printed, fails on a lever the concept never answered |

## Layout

```
INDEX.xml                      # L2 index, generated — never hand-edit
tools/<pack>/
├── meta.json                  # tier gate for the whole pack dir
├── scripts/<name>.py|sh       # the executable
└── tools/<name>.card.md       # the contract, ≤40 lines
```

`INDEX.xml` is what `SKILL.md` routes into and the first place to look before writing a script; regenerate it with `scripts/regen-fragment-index.py`.

## Card shape

Fixed section order, nothing added or dropped: `# <tool-name>` · `## Purpose` · `## Invoke` · `## Inputs` · `## Outputs` · `## When NOT to use` · `## Cost`. Placeholders in `## Invoke` are written `{like-this}`, and the script's own position is written `{script}` — the CLI substitutes the materialised absolute path there (`python3 {script} --in {claims.jsonl}`). A literal `scripts/foo.py` resolves only through a compatibility shim that guesses from the filename; see `.aidocs/crs/done/CR-005-tool-card-invoke-placeholder.md`. `## Outputs` names every file written, the stdout shape, and what each exit code means.

## Script contract

- Dependency-free: `python3` stdlib or POSIX `sh`. No pip installs, no third-party imports.
- Deterministic: same inputs, same bytes out.
- One summary line to stdout; diagnostics to stderr.
- Meaningful exit codes: `0` success, `1` the checked thing is wrong, `2` the tool could not run, further codes documented on the card.
- Never calls a model, never writes outside the paths its card names.

## Validation

`python3 scripts/validate-tools.py` (validator 10) is the enforcement: `meta.json` against [`docs/schemas/tool-pack-meta.schema.json`](../../../docs/schemas/tool-pack-meta.schema.json), the card against [`docs/schemas/card.schema.json`](../../../docs/schemas/card.schema.json), card↔script pairing both ways, the `{script}` placeholder and no literal `scripts/` path, every exit status the script can return explained under `## Outputs`, a shebang plus stdlib-only imports, and — the card-first rule made mechanical — **every long option the script's parser defines must appear in `## Inputs`**, with anything the card names and the script lacks failing the other way.

## Gotchas

- Tier comes from `<pack>/meta.json` — one entry gates every file beneath it. `scripts/regen-tier-manifest.py` walks `skills/faion/tools/<pack>/meta.json` alongside knowledge, playbooks and fragments.
- **Scripts ship.** `vfs-pack` allowlists `.py`/`.sh` from any `scripts/` path segment (`faion-cli/tools/vfs-pack/pack.go:631`, F029-T01) — location is the declaration of intent, so a `.py` anywhere else is authoring scaffolding and stays out. `faion tools sync` materialises a pack to `~/.faion/tools/<pack>/` with the script `0755` and the card `0444`. That directory is **world-readable**: a tool must never cache a credential there.
- Adding a pack means: `meta.json`, a row in the table above, `regen-fragment-index.py --only tools`, `regen-tier-manifest.py`, and a CHANGELOG entry. A pack without `meta.json` inherits the skill-level tier silently, and the missed manifest regen is the one step no validator catches.
- **Do not hand-roll a new tool.** Stamp it: `docs/templates/tool-script.py.template`, `tool-card.md.template`, `tool-pack-meta.json.template` validate clean as substituted. The linear checklist, the failure modes and the `.sh` / network deltas are in [`docs/tool-authoring.md`](../../../docs/tool-authoring.md).
- A shared helper module is currently **impossible**: `validate-tools.py` fails any `.py`/`.sh` in a pack's `scripts/` with no matching card. Duplicate the helper or change the validator first.
