# playwright-scaffold

## Purpose
Emits a determinism-hardened Playwright harness into the caller's own repo, where their venv and
their CI own the ~150 MB dependency. It pins every variable that makes a screenshot differ between
two machines — viewport, device scale factor, motion, clock, timezone, locale, colour scheme, font
hinting, and a navigation that waits for networkidle and then asserts the page settled — and with
`--ci github` pins the Playwright container image, the only way font rasterisation stays stable
across runners. It never launches a browser and never opens a socket.

## Invoke
```
python3 {script} --dir {project} [--lang {py|ts}] [--base-url {url}] [--breakpoints {390,768,1440}] [--baseline-dir {name}] [--ci {github|none}] [--flows {flows.jsonl}] [--force] [--self-test]
```

## Inputs
- `--dir {path}` — project root; the harness lands in `tests/browser`. Required unless self-testing.
- `--lang {py|ts}` — pytest-playwright or @playwright/test. Optional, default `py`.
- `--base-url {url}` — origin the harness navigates against. Optional, default `http://localhost:3000`.
- `--breakpoints {list}` — comma-separated viewport widths, each 200-4000. Optional, default `390,768,1440`.
- `--baseline-dir {name}` — baseline directory, relative to `tests/browser` and refused if it escapes. Optional, default `baseline`.
- `--ci {github|none}` — also emit a workflow pinning the Playwright container image. Optional, default `none`.
- `--flows {file}` — JSONL, one object per line: `name`, `steps` of `{action, selector, value}`, optional `expect` selector. Actions: `goto`, `click`, `fill`, `press`, `wait`, `screenshot`. One spec generated per line. Optional.
- `--force` — overwrite files that already exist. Optional.
- `--self-test` — run the built-in fixtures and exit. Optional.

## Outputs
- Files under `{dir}/tests/browser/`: `README.md`, `determinism.css`, `{baseline-dir}/.gitkeep`, one spec per flow, plus `harness.py` + `conftest.py` + `test_screens.py` for `py`, or `playwright.config.ts` + `determinism.ts` + `screens.spec.ts` for `ts`.
- Files: `{dir}/.github/workflows/browser-visual.yml`, only with `--ci github`.
- stdout: `playwright-scaffold: lang=… files=N breakpoints=… flows=N ci=… image=… -> …/tests/browser`
- Exit: `0` written · `1` refused because output files exist and `--force` was not passed · `2` the tool could not run — missing or non-directory `--dir`, a breakpoint list or `--baseline-dir` it rejects, an unreadable or invalid `--flows` file, an unwritable destination.

## When NOT to use
- Exploratory, one-off browser work. Driving the browser interactively, or through an MCP server, beats a generated harness whenever a model is in the loop and can look at the result. This harness earns its place only where no model is watching: CI, a pre-commit hook, a batch over many URLs.
- Running the tests. It writes files and stops; installing Playwright, downloading the browser and executing the suite are the repo's job.
- Judging a screenshot. Capture and comparison are separate on purpose — the gate is `png-diff`.

## Cost
Zero model calls. Zero network calls. Milliseconds; pure text generation, one write per emitted file.
