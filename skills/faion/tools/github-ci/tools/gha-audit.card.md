# gha-audit

## Purpose
Static security audit of GitHub Actions workflow YAML: 14 rules, each a real 2025-26 supply-chain incident rather than a style
preference — mutable action tags, a pull-request title interpolated into `run:`, `pull_request_target` checking out the fork's head,
secrets beside `curl`, absent `permissions` or `timeout-minutes`, a deprecated runner. It names the line to change, so it works both
as a pre-merge gate and as the first read of an unfamiliar repository's CI.

## Invoke
```
python3 {script} --dir {.github/workflows} [--format {text|json}] [--severity {low|med|high}] [--fail-on {low|med|high}] [--ignore {rule-id}] [--baseline {report.json}] [--out {file}] [--self-test]
```

## Inputs
- `--dir {path}` — directory of workflow YAML, non-recursive, `.yml` and `.yaml`. Required.
- `--format {text|json}` — report format written to `--out`. Optional, default `text`.
- `--severity {low|med|high}` — lowest severity reported at all. Optional, default `low`.
- `--fail-on {low|med|high}` — lowest severity that fails the run. Optional, default `high`.
- `--ignore {rule-id}` — suppress one rule, e.g. `missing-concurrency`. Optional, repeatable.
- `--baseline {file}` — a JSON report whose findings are accepted, matched on the per-finding fingerprint so accepted debt survives
  reformatting. Optional.
- `--out {file}` — full report destination. Optional, default none.
- `--self-test` — run the built-in fixtures, one per rule, and exit. Optional.

## Outputs
- Files: `{out}` — every finding as `{rule, severity, file, line, evidence, fix, fingerprint}`.
- stdout: `gha-audit: files=N findings=M high=H` — one line, always.
- stderr: one compressed line per finding, capped at 40; JSON lands here when `--format json` is given without `--out`.
- Exit: `0` nothing at or above `--fail-on` · `1` a finding at or above it · `2` the tool could not run — no `--dir`, not a
  directory, no workflow file in it, unreadable baseline or file.

## When NOT to use
- Pinning the tags it reports: that is `gha-pin`, which needs a token. This one never opens a socket.
- Workflows leaning on YAML anchors, aliases, flow mappings or folded scalars — the reader is an indentation-aware mini-lexer, not a
  YAML parser, and those shapes are out of scope.
- Proving a secret is safe. There is no taint tracking, so a secret copied into `env:` and used two steps later is invisible, and
  severity filtering deliberately lets a caller mute a rule.

## Cost
Zero model calls. Zero network calls. One pass per file; milliseconds for a whole `.github/workflows`.
