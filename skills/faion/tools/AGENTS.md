# tools/

Tool packs: real, reusable scripts an agent runs instead of writing a throwaway one, each with an instruction card. F029 materialises a pack into `~/.faion/tools/<pack>/`.

**Card-first rule.** The card is the contract. An agent must be able to run the tool correctly having read `tools/<name>.card.md` and nothing else — never open the script to work out its arguments, and never re-implement a tool that already has a card. If the card and the script disagree, the card is the bug report.

## Packs

| Pack | Tier | Tools |
|------|------|-------|
| `python-web/` | free | `venv-bootstrap.sh` — idempotent `.venv` create + requirements install + import proof; `django-test-gate.py` — run a Django suite through the project venv, emit one JSON verdict line |
| `game-dev/` | solo | `hmac-rng-golden.py` — emit/verify golden vectors for HMAC-SHA256 rejection-sampling randomness; `deploy-scaffold.py` — systemd unit + nginx vhost + `deploy.sh`, identities namespaced by `--name` |
| `research/` | free | `source-table.py` — claims JSONL → markdown evidence table + gaps report + commercial-lever ledger, fails on an unsourced load-bearing claim or a commercial claim with no lever; `lever-check.py` — ledger × concept verdict → applied/declined counts with every decline printed, fails on a lever the concept never answered |
| `static-web/` | free | `asset-stamp.py` — appends each asset's content hash to the URL the HTML emits so a CDN edge holding an `immutable` copy must refetch, unchanged assets keep their URL, and `--check` fails a build still pointing at stale bytes |
| `browser/` | free | `playwright-scaffold.py` — writes a determinism-hardened Playwright harness into the caller's own repo (pinned container, frozen clock, killed animations, fixed viewport); `png-diff.py` — stdlib PNG codec plus a two-gate verdict, changed-pixel ratio **and** largest connected cluster, so a small structural shift a ratio hides still fails |
| `cloudflare/` | solo | `zone-audit.py` — fans out over the per-setting endpoints that replaced the deprecated batch settings API and exits 1 on a policy violation; `dns-snapshot.py` — canonical JSONL plus baseline diff; `cache-purge.py` — chunked, rate-paced, dry-run until `--yes` |
| `github-ci/` | pro | `gha-audit.py` — 14 static workflow-security rules (unpinned actions, expression injection, `pull_request_target` pwn requests, secrets in argv), no token and no network; `gha-pin.py` — resolves and enforces 40-char SHA pins |
| `web-parse/` | solo | `polite-fetch.py` — robots-aware, rate-limited, resumable cache every other parser reads from; `page-extract.py` — readable text/markdown plus JSON-LD/OpenGraph/microdata in one pass, with the implied-end-tag repair `html.parser` needs to nest correctly |
| `deploy/` | free | `unit-lint.py` — validates a systemd unit against filesystem reality before it touches a box (`Type=notify` on a bare interpreter, `EnvironmentFile` world-readable, a `WorkingDirectory` that `ProtectHome` replaces with an empty tmpfs); `smoke-check.py` — post-deploy assertions where `not_contains` and a minimum body size catch the 200 that serves a stale build |
| `template-builder/` | free | `tpl-build.py` — assembles blocks plus literal `.md` into Markdown and self-contained HTML, refusing a required parameter by name rather than substituting empty; `tpl-params.py` — lists declared parameters and emits the questions to ask, keeping a sensitive value out of the project store; `tpl-migrate.py` — proposes a `variables:` declaration for a legacy `<Angle>` template and names every placeholder it will not declare, writing nothing without `--write` |
| `env-topology/` | solo | `wrangler-env-lint.py` — offline JSONC/TOML lint for the bindings a named wrangler environment silently does **not** inherit; `secret-leak-scan.py` — finds `sb_secret_`, `service_role` JWTs (decoded, not pattern-matched) and `cfut_` tokens in a worktree, build output and CI, reporting location and eight characters, never the secret |
| `hetzner/` | pro | `baseline-audit.py` — 37-item CIS-derived baseline scored from API state plus `sshd -T` / `ss` / `sysctl` output the caller supplies, with expiring waivers because a baseline that cannot be waived gets ignored wholesale; `fw-sync.py` — declarative cloud-firewall convergence that **proves** admin SSH survives before writing, then arms a revert only a second `--commit` cancels |
| `sdd-sync/` | pro | `api-call.py` — the pack's only networking path: env auth, 429 backoff, page/cursor/link pagination and a `--select` shaper so the caller gets three fields instead of a vendor envelope; `sdd-sync.py` — reconciles `.aidocs` task files against a tracker through a hash ledger, so a second run updates instead of duplicating |

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
- **A shared helper goes in `scripts/lib/`, not `scripts/`.** The card rule only reaches the top level — `validate-tools.py` globs `scripts/*` non-recursively — and `faion tools sync` materialises nested `scripts/<sub>/*.py` as pack Helpers (`faion-cli/internal/tools/discover.go:96`), so a helper both validates and reaches the user's disk. A `.py` sitting directly in `scripts/` still needs its own card.
- **Data files do not ship.** `vfs-pack` excludes `.json` deliberately, and while `.xml` enters the blob, `syncPack` materialises only each tool's script, its card and the nested helpers — so a `profiles/*.xml` would be packed and never land on disk. Config a tool needs at runtime must be embedded in the script, with a `--file` flag to override it locally.
