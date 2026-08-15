# tpl-params

## Purpose
Lists every parameter a template or block set declares — type, required, default, whether
the store answers it — and in ask mode emits as JSON exactly which are unresolved and the
question to ask for each. It is what an agent reads before it asks the user anything.

## Invoke
```
python3 {script} --blocks {dir} --use header/template-header-block,body/title-h1,./rules.md --ask
python3 {script} --template {file.md} [--project {dir}] [--set name=value] [--unset name] [--json] [--self-test]
```

## Inputs
- `--template {file}` — a single source template. Alternative to `--use`.
- `--blocks {dir}` — block library root holding `{kind}/{name}.md`. Needed only for refs.
- `--use {a,b,c}` — ONE comma-separated ordered list of `kind/name` refs and `.md` paths.
- `--project {dir}` — root holding `.faion/template-params.json`. Optional, default `.`.
- `--set name=value` — write a value to the store; `--unset name` drops one. Repeatable.
- `--ask` — emit the unresolved parameters and their questions as JSON. Optional.
- `--json` — emit the full listing plus the unresolved set as JSON. Optional.
- `--self-test` — run the built-in fixtures and exit. Optional, writes nothing.

## Outputs
- Files: `{project}/.faion/template-params.json`, written only under `--set` / `--unset`;
  a sensitive parameter leaves its placeholder there and never its value.
- stdout: the table, or under `--ask` / `--json` the JSON object and nothing else.
- stderr: one `ask 'name': question` per unresolved parameter, plus the summary line whenever JSON went to stdout.
- Exit: `0` every required parameter resolved · `1` the template is invalid · `2` could not
  run — no source, unreadable file, unusable store · `3` parameters remain unresolved · `4`
  a value refused — sensitive, secret-shaped, undeclared or ill-typed.

## When NOT to use
- Composing a `text` parameter: it reports the question and takes prose back as a value.
- Holding a secret. A sensitive value is refused, and so is any value shaped like a known
  token or key whatever the declaration says — substitute it locally after the build.
- Assembling the document, or remembering an answer a build already resolved: `tpl-build`.

## Cost
Zero model calls. Zero network calls. One read of each source plus the store.
