# tpl-render

## Purpose
Renders a converted template pair against a value map: `{name}.md.j2` plus its `{name}.html.j2`
sibling become a Markdown document and a self-contained HTML copy. Sandboxed, autoescaped for HTML,
strict — a missing variable is refused by name, never rendered as an empty string.

## Invoke
```
python3 {script} --template {file.md.j2} --values {values.json} --out {out.md}
python3 {script} --template {file.md.j2} [--set {NAME=VALUE}] [--schema {file}] [--no-html]
```

## Inputs
- `--template {file}` — the `.md.j2` to render. Required unless self-testing. Its `.html.j2` and
  `.vars.schema.json` siblings are derived: the three files are one artefact.
- `--values {file}` — JSON object of variable values. Optional.
- `--set {NAME=VALUE}` — one explicit value, repeatable, beats `--values`. Optional.
- `--schema {file}` — the schema, when it is not the sibling. Optional.
- `--out {path}` — output path; the `.html` sibling is derived. Optional; without it the Markdown
  goes to stdout and nothing is written.
- `--no-html` — render only the Markdown. Optional.
- `--self-test` — run the built-in fixtures and exit. Optional, writes nothing.

## Outputs
- Files (only under `--out`): the Markdown at that path and the HTML beside it.
- stdout: the rendered Markdown when no output path is given, otherwise one summary line.
- stderr: one line per refused value, naming the variable and the question to ask for it.
- Exit: `0` rendered · `1` the template or the schema is invalid · `2` could not run — no template,
  a missing `.html.j2`, or Jinja not installed, which prints the install line · `3` a required
  variable has no value · `4` a value was refused: unknown key, wrong type, outside an `enum`,
  supplied for a sensitive variable, or shaped like a credential.

## When NOT to use
- Rendering a legacy `.md` template: that is `tpl-build`, which reads the old `variables:` header.
- Composing prose for an `x-faion-compose` variable: this renders a value, it never writes one.
- Filling a secret: a sensitive variable renders its placeholder and a supplied value is refused.

## Cost
Zero model calls. Zero network calls. Needs Jinja (`Jinja2>=3.0`). Milliseconds per document.
