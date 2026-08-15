# tpl-build

## Purpose
Assembles an ordered list of block refs and literal `.md` files into canonical Markdown plus a self-contained HTML copy.
Parameters resolve explicit, then store, then default, then ask; one left unfilled is refused by name. A build remembers.

## Invoke
```
python3 {script} --blocks {dir} --use header/template-header-block,body/title-h1,./rules.md --set purpose=Runbook --out {out.md}
python3 {script} --template {file.md} --out {out.md} [--values {file.json}] [--project {dir}] [--no-html] [--no-remember] [--self-test]
```

## Inputs
- `--template {file}` — a single source template. Alternative to `--use`.
- `--blocks {dir}` — block library root holding `{kind}/{name}.md`. Needed only for refs.
- `--use {a,b,c}` — ONE comma-separated, ordered list; not repeatable, not space-separated.
  Each entry is a `kind/name` block ref, or an `.md` path for literal passthrough.
- `--set name=value` — an explicit value; repeatable, beats the store, and is remembered.
- `--values {file.json}` — a JSON object of parameter values; `--set` beats it.
- `--project {dir}` — root holding `.faion/template-params.json`. Optional, default `.`.
- `--out {file.md}` — the Markdown destination; the `.html` sibling is derived. Required.
- `--no-remember` — do not write the answers back. Optional; the default IS to write them.
- `--no-html` — emit only the Markdown. `--self-test` — run the fixtures. Both optional.

## Outputs
- Files: `{out}.md` canonical and `{out}.html` self-contained, no external stylesheet or font;
  plus the store unless `--no-remember` — only answers given, never a default nor a sensitive.
- stdout: `tpl-build: source=S vars=N sections=N remembered=N -> path, path`
- stderr: one line per refusal; for an unresolved parameter, its name and its question.
- Exit: `0` built · `1` invalid template — malformed declaration, unsupported construct,
  undeclared placeholder · `2` could not run — no source, no `--out`, unreadable file, no such
  block · `3` required parameters unresolved · `4` a value refused.

## When NOT to use
- Asking the user for the missing values: that is `tpl-params`, whose JSON is the questions.
- Anything past `{{name}}` and `when: var in [literal, ...]`: loops and filters are refused.
- Rendering rich values: in the HTML a value is escaped text, never markup, never Markdown.

## Cost
Zero model calls. Zero network calls. Two passes over the source; milliseconds.
