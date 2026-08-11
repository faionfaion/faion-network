#!/usr/bin/env python3
"""django-test-gate.py — run a Django suite through the project's own venv and
report the result as one machine-readable JSON line.

Input:  --project <dir with manage.py> [--venv <dir>] [--label ...]
        [--tag ...] [--exclude-tag ...] [--settings ...] [--env-file ...]
        [--timeout <seconds>] [--keepdb]
Output: one JSON line on stdout:
            {"ok": bool, "ran": int, "failures": [str, ...]}
        On harness failure an "error" key is added and exit code is 2.
Exit:   0 suite green · 1 suite red · 2 harness could not run the suite.

Replaces the ad-hoc "run the tests and eyeball the tail" step: the caller
branches on the exit code, and reads `failures` to know what to fix without
re-reading a wall of output.

Dependency-free (stdlib only). Never calls a model.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

RAN_RE = re.compile(r"^Ran (\d+) tests? in ", re.M)
FAIL_RE = re.compile(r"^(?:FAIL|ERROR): (.+)$", re.M)
COUNT_RE = re.compile(r"^FAILED \((.*)\)$", re.M)


def emit(ok: bool, ran: int, failures: list[str], error: str | None = None) -> None:
    payload: dict = {"ok": ok, "ran": ran, "failures": failures}
    if error:
        payload["error"] = error
    print(json.dumps(payload, ensure_ascii=False, sort_keys=False))


def find_python(project: Path, venv: str | None) -> Path | None:
    """Resolve the interpreter: explicit --venv, then <project>/.venv, then
    <project>/../.venv (the backend/ + repo-root .venv layout)."""
    candidates = []
    if venv:
        candidates.append(Path(venv))
    else:
        candidates.append(project / ".venv")
        candidates.append(project.parent / ".venv")
    for c in candidates:
        py = c / "bin" / "python"
        if py.is_file() and os.access(py, os.X_OK):
            return py
    return None


def load_env_file(path: Path) -> dict[str, str]:
    """Parse a KEY=VALUE .env file. Blank lines and # comments ignored."""
    env: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        k, _, v = line.partition("=")
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        env[k.strip()] = v
    return env


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", required=True, help="directory containing manage.py")
    ap.add_argument("--venv", help="venv dir; default <project>/.venv then <project>/../.venv")
    ap.add_argument("--label", action="append", default=[], help="test label (repeatable)")
    ap.add_argument("--tag", action="append", default=[], help="--tag passed to manage.py test")
    ap.add_argument("--exclude-tag", action="append", default=[], help="--exclude-tag passed through")
    ap.add_argument("--settings", help="DJANGO_SETTINGS_MODULE override")
    ap.add_argument("--env-file", help="KEY=VALUE file sourced into the child env")
    ap.add_argument("--keepdb", action="store_true", help="pass --keepdb")
    ap.add_argument("--timeout", type=int, default=900, help="seconds before abort (default 900)")
    args = ap.parse_args()

    project = Path(args.project).expanduser()
    if not (project / "manage.py").is_file():
        emit(False, 0, [], f"no manage.py in {project}")
        return 2
    project = project.resolve()

    py = find_python(project, args.venv)
    if py is None:
        emit(False, 0, [], f"no venv interpreter for {project} (run venv-bootstrap.sh first)")
        return 2

    env = dict(os.environ)
    if args.env_file:
        ef = Path(args.env_file).expanduser()
        if not ef.is_file():
            emit(False, 0, [], f"env file not found: {ef}")
            return 2
        env.update(load_env_file(ef))
    if args.settings:
        env["DJANGO_SETTINGS_MODULE"] = args.settings
    env.setdefault("PYTHONUNBUFFERED", "1")

    cmd = [str(py), "manage.py", "test", *args.label]
    for t in args.tag:
        cmd += ["--tag", t]
    for t in args.exclude_tag:
        cmd += ["--exclude-tag", t]
    if args.keepdb:
        cmd.append("--keepdb")

    try:
        proc = subprocess.run(
            cmd, cwd=str(project), env=env, timeout=args.timeout,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
    except subprocess.TimeoutExpired:
        emit(False, 0, [], f"timeout after {args.timeout}s")
        return 2
    except OSError as exc:
        emit(False, 0, [], f"cannot execute {py}: {exc}")
        return 2

    out = proc.stdout or ""
    m = RAN_RE.search(out)
    ran = int(m.group(1)) if m else 0
    failures = [f.strip() for f in FAIL_RE.findall(out)]

    if m is None:
        # The runner never reached the summary line: import error, bad label,
        # missing settings. That is a harness failure, not a red suite.
        tail = "; ".join(out.strip().splitlines()[-3:]) or "no output"
        emit(False, 0, failures, f"suite did not run (rc={proc.returncode}): {tail}")
        return 2

    ok = proc.returncode == 0 and not failures
    if not ok and not failures:
        cm = COUNT_RE.search(out)
        failures = [f"FAILED ({cm.group(1)})"] if cm else [f"exit {proc.returncode}"]
    emit(ok, ran, failures)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
