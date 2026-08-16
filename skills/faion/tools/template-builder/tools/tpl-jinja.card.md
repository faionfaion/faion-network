# tpl-jinja

## Purpose
Converts one Markdown template into `{name}.md.j2`, a self-contained `{name}.html.j2` built from
its structure, and a draft-07 `{name}.vars.schema.json` that `$ref`s the corpus dictionary.

## Invoke
```
python3 {script} --template {file.md} [--out-dir {dir}] [--resolver {file}] [--write] [--json]
```

## Inputs
- `--template {file}` — the Markdown template to convert. Required unless self-testing.
- `--out-dir {dir}` — where the three files go. Optional, default beside the template.
- `--dictionary {file}` — `vars-dictionary.schema.json`; found by walking up. Optional, and absent
  is normal mid-migration: the schema then carries local definitions and an `x-faion-todo`.
- `--resolver {file}` — `vars-resolver.json`, raw-name-plus-context to dictionary-entry rules; found
  beside the dictionary. Optional. Renames `handle` under an owner label to `owner_handle`, and
  leaves local, for review, anything it cannot place with certainty.
- `--no-resolver` — skip those rules; only an exact dictionary-name match `$ref`s. Optional.
- `--write` — write the three files; without it everything goes to stdout. `--json` — the plan as
  JSON on stdout, report on stderr. `--self-test` — run the fixtures and exit. All optional.

## Outputs
- Files (only under `--write`): the three above, each parsed and rendered first — including that
  the Markdown matches the pre-Jinja substitution — none written if not. stdout: the three files,
  or the report once writing. stderr: one line per placeholder — name, type and the resolver rule
  that renamed it, or `UNCLEAR: reason` and left alone.
- Exit: `0` every placeholder resolved · `1` placeholders or notes left for a human, the normal
  outcome · `2` could not run — no template, unreadable file, a broken resolver, Jinja missing, or
  the pair failed to verify · `3` refused, the placeholders are already HTML-escaped, a prerequisite
  · `4` refused, it declares `sections:`, carries a raw Jinja delimiter, or uses an undeclared name.

## When NOT to use
- Deciding whether a placeholder IS a variable: prose, per-row cells and collisions are reported
  for a human, because a wrong declaration makes every later build refuse by name.
  Not for `.json`/`.py`/`.yaml` templates, rendering one, or mass-converting a tree.

## Cost
Zero model calls. Zero network calls. Needs Jinja (`Jinja2>=3.0`). ~1 s per 30 templates.
