# tpl-jinja

## Purpose
Converts one Markdown template into the source `{name}.md.j2`, a self-contained `{name}.html.j2`, a
draft-07 `{name}.vars.schema.json` and a regenerated `{name}.md` — one pass, so none can drift.

## Invoke
```
python3 {script} --template {file} [--migrate | --check] [--resolver {file}] [--write] [--json]
```

## Inputs
- `--template {file}` — the `.md` to convert; under `--check` the `.md.j2` to verify. Required.
- `--migrate` — the whole per-template operation, all or nothing: the three Jinja files, the `.md`
  regenerated from the new `.md.j2`, and that AGENTS.md's `## Templates` rows plus its inline
  `## Template Contents` body. Needs `--write`. Optional.
- `--check` — re-derive every generated form from a migrated `.md.j2`, report drift, write nothing.
- `--out-dir {dir}` — where the files go; default beside the template, refused under `--migrate`.
- `--dictionary {file}` — `vars-dictionary.schema.json`, found by walking up; absent mid-migration is
  normal and the schema then carries local definitions plus an `x-faion-todo`. Optional.
- `--resolver {file}` — `vars-resolver.json`, raw-name-plus-context to dictionary-entry rules, found
  beside it: `handle` under an owner label becomes `owner_handle`, and anything it cannot place with
  certainty stays local, for review. Optional.
- `--no-resolver` — skip those rules; only an exact dictionary-name match `$ref`s. `--write` — write;
  without it all goes to stdout. `--json` — the plan as JSON. `--self-test` — fixtures. All optional.

## Outputs
- Files (only under `--write`): the four above, plus the AGENTS.md under `--migrate`; all verified
  before any is written, a failure part-way restores every byte. stdout: the files, or the report;
  stderr: one line per placeholder, or per drift. Exit codes below.
- Exit: `0` clean · `1` placeholders or notes left for a human, the normal outcome, or `--check` found
  drift · `2` could not run, or the forms failed to verify · `3` refused, placeholders already
  HTML-escaped · `4` refused: `sections:`, a raw delimiter, an undeclared name · `5` refused, no row.

## When NOT to use
- Deciding whether a placeholder IS a variable: prose, per-row cells and collisions go to a human.
  Not for `.json`/`.py`/`.yaml` templates, rendering one, or mass-converting a tree.

## Cost
Zero model calls. Zero network calls. Needs Jinja (`Jinja2>=3.0`). ~1 s per 30 templates.
