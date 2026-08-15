# tpl-migrate

## Purpose
Proposes a `variables:` declaration and a `{{name}}` body for a legacy `<Angle>` / `[bracket]`
template, naming every placeholder it will not declare. Nothing is touched without `--write`.

## Invoke
```
python3 {script} --template {file.md}
python3 {script} --template {file.md} [--out {file.md}] [--write] [--json] [--self-test]
python3 {script} --report [--root {dir}] [--glob {pattern}] [--limit {n}] [--json]
```

## Inputs
- `--template {file}` — the template to migrate. Required unless reporting or self-testing.
- `--out {file}` — write the rewritten template here instead of stdout. Optional.
- `--write` — apply the proposal to the template in place. Optional; nothing is written without it.
- `--report` — survey every template under `--root` instead. `--root {dir}` — where it walks, `.`.
- `--glob {pattern}` — what the survey counts as a template. Default `**/templates/*.md`.
- `--limit {n}` — rows per report table. Optional, default `25`. `--json` — the object on stdout.
- `--self-test` — run the built-in fixtures and exit. Optional, writes nothing.

## Outputs
- Files: `{out}`, or the template under `--write`. Neither is written when the declaration cannot
  be spliced or the rewrite fails to parse back: a partial migration is never applied.
- stdout: the rewritten template; under `--out` / `--write` / `--report` the analysis or survey.
- stderr: one line per placeholder — proposed name and type, or `UNCLEAR: reason` and left alone.
- Exit: `0` every candidate resolved · `1` unresolved placeholders remain (the normal outcome), or
  the header would pass the 40-line window validator 5 reads · `2` could not run — no `--template`,
  unreadable file, a header this parser refuses, a template that already declares `variables:` ·
  `3` two placeholders normalise onto one name; nothing written.

## When NOT to use
- Deciding whether a placeholder IS a parameter: prose, options and format tokens are reported for
  a human, because a declaration for a non-parameter makes `tpl-build` refuse a build by name.
- Migrating a `.py` / `.json` / `.tf` template: it reads Markdown structure — headings, tables, fences.
- Filling or assembling a migrated template: that is `tpl-params` then `tpl-build`.

## Cost
Zero model calls. Zero network calls. One pass per file; ~1 s over 2,900 templates.
