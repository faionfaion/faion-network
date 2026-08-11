# django-test-gate

## Purpose
Run a Django suite through the project's own venv and return the verdict as one JSON line, so a caller branches on an exit code instead of eyeballing output.

## Invoke
```
python3 scripts/django-test-gate.py --project {backend-dir} [--venv {dir}] [--label {app.tests}] [--tag {t}] [--exclude-tag {t}] [--settings {module}] [--env-file {path}] [--keepdb] [--timeout {seconds}]
```

## Inputs
- `--project {backend-dir}` — directory containing `manage.py`. Required.
- `--venv {dir}` — venv root. Optional; default probes `{project}/.venv` then `{project}/../.venv`.
- `--label {app.tests}` — test label, repeatable. Optional, default = whole suite.
- `--tag` / `--exclude-tag {t}` — passed through to `manage.py test`, repeatable. Optional.
- `--settings {module}` — sets `DJANGO_SETTINGS_MODULE`. Optional.
- `--env-file {path}` — `KEY=VALUE` file merged into the child environment. Optional.
- `--keepdb` — reuse the test database. Optional.
- `--timeout {seconds}` — abort the run. Optional, default `900`.

## Outputs
- Files: none.
- stdout: exactly one JSON line `{"ok": bool, "ran": int, "failures": [str]}`; an `"error"` key is added only when the harness could not run the suite.
- Exit: `0` suite green · `1` suite red (`failures` names each `FAIL:`/`ERROR:` test) · `2` harness failure — no `manage.py`, no venv interpreter, missing env file, timeout, or the runner never reached its `Ran N tests` line.

## When NOT to use
- pytest-only projects — it parses the `unittest`/Django runner summary.
- Non-Django Python suites, or any suite that must stream progress to a human.
- As a coverage or lint gate; it reports pass/fail and test names, nothing else.

## Cost
Zero model calls. Runtime = the suite's own runtime plus a few milliseconds of parsing.
