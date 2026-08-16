# tpl-jinja

## Purpose
Converts one Markdown template into the Jinja form: `{name}.md.j2`, a self-contained
`{name}.html.j2` built from the Markdown structure, and a draft-07 `{name}.vars.schema.json` that
`$ref`s the corpus variable dictionary. It proposes; nothing is touched without `--write`.

## Invoke
```
python3 {script} --template {file.md} [--out-dir {dir}] [--dictionary {file}] [--write] [--json]
```

## Inputs
- `--template {file}` — the Markdown template to convert. Required unless self-testing.
- `--out-dir {dir}` — where the three files go. Optional, default beside the template.
- `--dictionary {file}` — `vars-dictionary.schema.json`; found by walking up. Optional, and absent
  is normal mid-migration: the schema then carries local definitions and an `x-faion-todo`.
- `--write` — write the three files. Optional; without it everything goes to stdout.
- `--json` — the plan as JSON on stdout, the report on stderr. Optional.
- `--self-test` — run the built-in fixtures and exit. Optional, writes nothing.

## Outputs
- Files (only under `--write`): the three above. All are parsed and rendered first — including a
  check that the Markdown renders identically to the pre-Jinja substitution — none written if not.
- stdout: the three files, or the report once writing.
- stderr: one line per placeholder — proposed name and type, or `UNCLEAR: reason` and left alone.
- Exit: `0` every placeholder resolved · `1` placeholders or notes were left for a human, the
  normal outcome · `2` could not run — no template, unreadable file, Jinja not installed, or the
  generated pair failed to verify · `3` refused, the placeholders are already HTML-escaped and
  un-escaping them is a prerequisite · `4` refused, the source declares `sections:`, carries a raw
  Jinja delimiter, or uses a variable with no declaration behind it.

## When NOT to use
- Deciding whether a placeholder IS a variable: prose, per-row table cells and collisions are
  reported for a human, because a wrong declaration makes every later build refuse by name.
- Converting `.json` / `.py` / `.yaml` templates: those stay in their current form by design.
- Rendering a template, or mass-converting a tree — batch conversion is a reviewed queue.

## Cost
Zero model calls. Zero network calls. Needs Jinja (`Jinja2>=3.0`). ~1 s per 30 templates.
