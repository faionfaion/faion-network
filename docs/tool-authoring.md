# Authoring a tool

A tool is a real, dependency-free script an agent runs instead of writing a throwaway one, plus
an instruction card that is its whole contract. This file is what you read instead of
reverse-engineering the conventions from the existing packs. Enforcement is
`python3 scripts/validate-tools.py` (validator 10); the spec it enforces is
`skills/faion/tools/AGENTS.md`.

Before anything else: **read `skills/faion/tools/INDEX.xml`.** A duplicate tool is worse than no
tool.

## The one rule everything else serves

The card is the contract. An agent must be able to run the tool having read
`tools/<name>.card.md` and nothing else — never the script. Every mechanical check below is that
rule made checkable. When the card and the script disagree, **the card is the bug report**: fix
the script to match, or fix the card deliberately, never "sync" them without deciding which one
was right.

## Checklist

Follow linearly. A reviewer verifies each line by running the commands in step 12, so nothing
here needs judgement.

1. **Pick the pack.** An existing group or a new directory `skills/faion/tools/<pack>/`. New pack
   → step 2; existing pack → step 4.
2. `cp docs/templates/tool-pack-meta.json.template skills/faion/tools/<pack>/meta.json`,
   substitute `{{pack}}`, set `last_reviewed` to today, write the `summary` last (step 11).
3. **Choose the tier.** `free` if any fragment or recipe will name this tool — `validate-fragments.py`
   fails a free fragment that names a paid tool, matching on the bare tool name anywhere in the
   body. Otherwise `solo`/`pro`/`geek`. This is the only judgement call in the checklist.
   Second-order trap: if the tool's name is a common word already appearing in some free
   fragment's prose, a `solo` pack fails by accident. Pick a name that reads as an identifier
   (`dns-drift`, not `deploy`).
4. `cp docs/templates/tool-script.py.template skills/faion/tools/<pack>/scripts/<name>.py`, then
   `sed -i 's/{{tool-name}}/<name>/g'` it. The name is lowercase, `^[a-z][a-z0-9-]*$`, and
   identical in three places: the script filename, the card filename, and the card's H1.
5. **Write `check()` as a pure function** — no I/O, no exits, returns a list of finding strings.
   Everything else in the template is plumbing you keep.
6. **Write the two fixtures.** `OK_FIXTURE` produces no findings, `BAD_FIXTURE` at least one, and
   BAD should be the mistake a caller will actually make. These are the tool's only regression
   test.
7. **Keep exits in `main` only.** `0` clean · `1` the checked thing is wrong · `2` the tool could
   not run. Further codes are allowed but must be on the card. The validator's exit scan reads
   `return <int>` constants inside a module-level `def main` plus literal `sys.exit(<int>)` — so
   decisions live in pure helpers, exits live in `main`, and `sys.exit(main())` stays invisible to
   it. Do not nest helpers inside `main`; they are walked too.
8. Run `--self-test`. One line out, exit 0.
9. `cp docs/templates/tool-card.md.template skills/faion/tools/<pack>/tools/<name>.card.md`,
   substitute, fill every `{{...}}`. Delete the guidance comments once each section is written —
   they cost lines against the 40-line cap.
10. **Reconcile card against parser.** Every long option the parser defines appears in
    `## Inputs`; nothing appears in `## Inputs` or `## Invoke` that the parser does not define;
    every exit code the script can return is explained in `## Outputs` in backticks.
11. **Write the `meta.json` summary now**, naming each tool and the failure it makes loud. It is
    copied verbatim into `INDEX.xml` and is the only text an agent reads before deciding whether
    your tool already exists.
12. **Validate, regenerate, validate again:**

    ```bash
    python3 scripts/validate-tools.py skills/faion/tools/<pack>   # fast loop
    python3 scripts/regen-fragment-index.py --check --only tools
    python3 scripts/regen-fragment-index.py --only tools
    python3 scripts/regen-tier-manifest.py --dry-run              # new pack only
    python3 scripts/regen-tier-manifest.py                        # new pack only
    python3 scripts/validate-tools.py                             # whole tree
    bash scripts/check-validators.sh --check-fast                 # the commit gate
    ```

13. **Add the row** to the Packs table in `skills/faion/tools/AGENTS.md` (new pack only — that
    file is capped at 80 lines by the pre-commit hook).
14. **CHANGELOG.** Every commit adds an entry under `## [Unreleased]`.

## Failure modes that will actually bite

| You did | You get |
|---|---|
| Wrote `python3 scripts/foo.py` in `## Invoke` | `## Invoke carries a literal scripts/ path, correct only inside this repo` — the CLI substitutes the materialised absolute path into `{script}`; a literal path resolves only through a filename-guessing shim |
| Added a flag to the parser, not to the card | `--strict is defined by <name>.py and is not in ## Inputs` |
| Documented a flag argparse adds for you | `documents --help, which <name>.py does not define`. Never write `--help` on a card |
| Left a stray `return 3` in `main` | `## Outputs does not say what exit 3 means` |
| Kept the guidance comments and wrote long sections | `lines: 54 is above maximum 40` |
| Put a `--flag` or a backticked digit inside a card comment | The scans read comment text too. No double dashes in `## Inputs`/`## Invoke` comments, no backticked integers in `## Outputs` comments |
| Added a shared helper module `scripts/common.py` | `scripts/common.py: no tools/common.card.md` — **shared helper modules are impossible today.** Every `.py`/`.sh` in a pack's `scripts/` needs its own card. Duplicate the helper, or change the validator first |
| Added a seventh `##` section to the card | Schema failure: `card.schema.json` pins exactly six sections, and `faion-cli/internal/tools/card.go` hardcodes the same six headings. Adding one means editing the schema **and** the Go in lockstep |
| Added a field to `meta.json` | Schema failure: `tool-pack-meta.schema.json` is `additionalProperties:false`. No comment fields either |
| Forgot `regen-fragment-index.py` | `INDEX.xml: pack 'x-tools' is on disk and not in the index` — but **only on a full run**. Passing a pack path skips the index check, so a scoped run is never proof |
| Forgot `regen-tier-manifest.py` | Nothing catches it. The pack ships ungated and inherits the skill-level tier silently. The one step with no safety net |

## Writing a `.sh` tool

Only when the job is process orchestration. Five deltas:

- `#!/bin/sh` + `set -eu`; POSIX only, no bashisms.
- Flags are discovered from `case` arms, and **only from arms that are pure long options**:
  `--out)` and `--dry-run|--dry)` are seen; `--out|-o)` is seen as nothing, so a card documenting
  `--out` then fails with "which x.sh does not define". Give a short alias its own arm, or drop it.
- Exit codes are read from lines matching `^\s*exit <n>`; a code returned any other way is
  undocumented-but-invisible, which is worse.
- `.sh` gets **no dependency check at all** — the import ban is AST-walked on `.py` only. Nothing
  stops you calling `curl` or `jq`. Do not: the dependency-free promise is what makes a pack
  materialisable on a stranger's machine.
- `--self-test` still applies: a branch that runs the tool's own logic over an inline heredoc
  fixture.

## Network tools

The script contract says "deterministic: same inputs, same bytes out". An API tool cannot honour
that literally. The amendment:

- Deterministic **given the same remote state**. Never mix in `time.time()`, `random`, or dict
  iteration order.
- `urllib.request` only — stdlib, passes the import ban. Not `requests`.
- **Credentials come from environment variables, never from a flag and never from a file the tool
  reads by convention.** A token in `argv` lands in shell history, in `ps`, and in an agent
  transcript. Name the variables in `## Inputs` as plain backticked names — the flag scan only
  looks for `--` tokens, so `CLOUDFLARE_API_TOKEN` is free text there.
- Never write a credential anywhere, including the tool's own output and `~/.faion/tools/<pack>/`,
  which is world-readable (`0755`).
- Missing credential → exit `3`. Rejected credential → exit `4`. A mutation refused for want of
  `--yes` → exit `5`. Network failure or a non-2xx that is not the answer → exit `2`. "You have no
  token" and "I crashed" are different actions for the calling agent.
- **Read-only by default.** A mutating tool is dry-run unless `--yes`, prints the exact diff in
  both modes, and caps the change set. An irreversible delete does not ship at all.
- `--self-test` **must not touch the network.** It exercises parsing and rules against inline
  fixtures. A self-test that needs a token is a self-test nobody runs.
- `## Cost` states the request count and the rate limit, not milliseconds.

## Reviewing someone else's tool

Run step 12. Then read only the card and answer: could you invoke this correctly without opening
the script? If not, the card is the bug.
