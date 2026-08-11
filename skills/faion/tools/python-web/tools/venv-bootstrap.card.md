# venv-bootstrap

## Purpose
Create or refresh a project `.venv`, install its requirements, and prove it imports — before anything else runs tests.

## Invoke
```
sh scripts/venv-bootstrap.sh --dir {project} [--venv {path}] [--requirements {file}] [--verify-import {mod,mod}] [--python {exe}] [--force]
```

## Inputs
- `--dir {project}` — directory the venv belongs to. Required.
- `--venv {path}` — venv location. Optional, default `{project}/.venv`; relative paths resolve inside `{project}`.
- `--requirements {file}` — pip requirements. Optional, default `{project}/requirements.txt` when it exists.
- `--verify-import {mod,mod}` — comma-separated modules to import as proof. Optional.
- `--python {exe}` — interpreter used to create the venv. Optional, default `python3`.
- `--force` — reinstall even when the requirements checksum is unchanged. Optional.

## Outputs
- Files: `{venv}/` (created if absent), `{venv}/.faion-req-stamp` (requirements checksum).
- stdout: `venv-bootstrap: venv=<path> created=yes|no installed=yes|skipped imports=ok(<count>)`
- stderr: one line naming the failing step (venv creation, pip, or the module that would not import).
- Exit: `0` ready · `1` venv creation, pip install, or import verification failed · `2` usage error, missing `--dir`, missing requirements file, missing interpreter.

## When NOT to use
- Poetry, uv, pipenv or conda projects — it drives `python -m venv` + `pip` only.
- Non-Python projects, or when the runtime is a container image built elsewhere.
- To pin or resolve versions — it installs the requirements file as given, nothing more.

## Cost
Zero model calls. Under a second when idempotent (checksum unchanged); first run costs one `python -m venv` plus one `pip install`, network-bound.
