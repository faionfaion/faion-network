# secret-leak-scan

## Purpose
Finds committed credentials in a worktree, its CI config and, on request, its built output — and never prints one. Seven rules:
Supabase `sb_secret_` keys and legacy `service_role` JWTs (the payload is decoded and the `role` claim read, because the publishable
half of the legacy pair is the same shape and is meant to ship), Cloudflare `cfut_` tokens, private key blocks, high-entropy
assignments, and a real `.env` that `.gitignore` does not cover. A secret key carries BYPASSRLS: one in a client bundle is the database.

## Invoke
```
python3 {script} [--root {.}] [--include-build {dist}] [--fail-on {low|med|high}] [--out {ledger.md}] [--json] [--self-test]
```

## Inputs
- `--root {dir}` — worktree to scan. Optional, default `.`. Skips `.git`, `node_modules`, virtualenvs, lock files, binaries, symlinks and files over 2 MiB; `.github/workflows` and every other config file is read as ordinary text.
- `--include-build {a,b}` — comma-separated build directories to scan as well, relative to the root, e.g. `dist,.wrangler`. Optional;
  build output is skipped by default because it is generated and large, and included when you want the bundler's inlining caught.
- `--fail-on {low|med|high}` — lowest severity that exits 1. Optional, default `med`. The one `low` rule is a legacy `anon` JWT,
  publishable by design but retiring with the legacy key pair at the end of 2026, so it reports without failing a build.
- `--out {file}` — full redacted ledger, one row per finding. Optional. Redacted identically to stderr, so the ledger is safe to commit.
- `--json` — emit the summary line as one line of JSON, findings included. Optional.
- `--self-test` — run the built-in fixtures and exit. Reads no file. Optional.

## Outputs
- Files: `{out}` — `file | line | rule | severity | starts | note`, nothing more.
- stdout: `secret-leak-scan: files=N findings=M at-or-above-med=F`, or one line of JSON under `--json`.
- stderr: one line per finding: severity, rule, `file:line`, and at most the first `8` characters of the match. Never the line,
  never the value — a scanner that echoes a leak into a log or an agent transcript has moved the secret somewhere new.
- Exit: `0` nothing at or above `--fail-on` · `1` a finding at or above it, or a failed self-test · `2` cannot run: `--root` is not
  a directory, or `--out` is unwritable.

## When NOT to use
- Git history. Worktree only. Reading history without `subprocess` means inflating objects out of `.git` by hand, which works for loose
  objects and silently reads nothing out of a packfile, so the flag was dropped rather than shipped half-working. Assume a pushed leak
  is exposed and rotate it; use a dedicated history scanner if you must prove otherwise.
- Proving a tree is clean. Entropy rules have a placeholder guard and therefore a false-negative floor; a short or word-shaped key passes.
- Triaging. It does not test whether a key is live and does not judge severity beyond the rule. A finding means rotate, not investigate.

## Cost
Zero model calls. Zero network calls. One pass per file, capped at 2 MiB each; well under a second on a typical application repository.
