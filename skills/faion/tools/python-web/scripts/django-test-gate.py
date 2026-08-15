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
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

NAME = "django-test-gate"
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


def summarise(out: str, returncode: int) -> tuple[bool, int, list[str], str | None]:
    """The verdict, from the runner's captured output alone.

    Pure — no process, no filesystem — because this is the half that can be
    wrong in a way the caller never sees: an exit code derived from a misread
    summary line is a green gate over a red suite. The execution half is
    `subprocess.run` in main; splitting them is what makes this testable
    without a Django project on disk.

    Returns (ok, ran, failures, error); a non-None `error` means the harness
    never got a verdict at all, which is neither green nor red.
    """
    match = RAN_RE.search(out)
    ran = int(match.group(1)) if match else 0
    failures = [f.strip() for f in FAIL_RE.findall(out)]

    if match is None:
        # The runner never reached the summary line: import error, bad label,
        # missing settings. That is a harness failure, not a red suite.
        tail = "; ".join(out.strip().splitlines()[-3:]) or "no output"
        return False, 0, failures, f"suite did not run (rc={returncode}): {tail}"

    ok = returncode == 0 and not failures
    if not ok and not failures:
        count = COUNT_RE.search(out)
        failures = [f"FAILED ({count.group(1)})"] if count else [f"exit {returncode}"]
    return ok, ran, failures, None


def exit_code(ok: bool, error: str | None) -> int:
    """0 green · 1 red · 2 the harness could not run the suite."""
    if error:
        return 2
    return 0 if ok else 1


# Canned runs: a completed subprocess reduced to the only two fields the
# parser reads, plus what each one must be turned into. Real Django output,
# trimmed. These are the whole point of splitting summarise() out — the gate's
# verdict logic is now provable without a project, a venv or a child process.
CANNED_RUNS = (
    ("green", "Creating test database...\nRan 12 tests in 3.204s\n\nOK\n", 0,
     (True, 12, [], None), 0),
    ("green singular", "Ran 1 test in 0.010s\n\nOK\n", 0, (True, 1, [], None), 0),
    ("green with skips", "Ran 9 tests in 1.0s\n\nOK (skipped=2)\n", 0,
     (True, 9, [], None), 0),
    ("red, named failures",
     "FAIL: test_totals (billing.tests.LedgerTest)\n"
     "ERROR: test_import (billing.tests.ImportTest)\n"
     "Ran 12 tests in 3.204s\n\nFAILED (failures=1, errors=1)\n", 1,
     (False, 12, ["test_totals (billing.tests.LedgerTest)",
                  "test_import (billing.tests.ImportTest)"], None), 1),
    ("red, count line only",
     "Ran 12 tests in 3.204s\n\nFAILED (failures=2)\n", 1,
     (False, 12, ["FAILED (failures=2)"], None), 1),
    ("red, no summary of any kind", "Ran 12 tests in 3.204s\n\n", 3,
     (False, 12, ["exit 3"], None), 1),
    ("harness: import error",
     "Traceback (most recent call last):\n"
     "  File \"manage.py\", line 9\n"
     "ImportError: cannot import name 'settings'\n", 1,
     (False, 0, [], "suite did not run (rc=1): Traceback (most recent call "
      "last):;   File \"manage.py\", line 9; ImportError: cannot import name "
      "'settings'"), 2),
    ("harness: no output at all", "", 2,
     (False, 0, [], "suite did not run (rc=2): no output"), 2),
)


def self_test() -> list[str]:
    """Prove the verdict shaper, the exit mapping, the env parser and the venv
    probe against inline fixtures. No Django, no subprocess, no network: every
    path exercised here returns before `subprocess.run` is reached."""
    failures: list[str] = []

    # 1-8: the shaper and the exit mapping, over canned runs.
    for label, out, rc, want, want_exit in CANNED_RUNS:
        got = summarise(out, rc)
        if got != want:
            failures.append(f"{label}: summarise gave {got}, want {want}")
        code = exit_code(got[0], got[3])
        if code != want_exit:
            failures.append(f"{label}: exit {code}, want {want_exit}")

    # 9: a harness failure carries the tail, capped at three lines, so a wall
    # of traceback never lands on the caller's stdout.
    _, _, _, error = summarise("a\nb\nc\nd\ne\n", 1)
    if error is None or "; " not in error or error.count("; ") != 2:
        failures.append(f"the harness tail is not the last three lines: {error!r}")

    # 10-11: the JSON line is exactly one line, and the 'error' key appears
    # only when the harness failed — a caller keys on its presence.
    for label, args, wants_error in (("green", (True, 12, [], None), False),
                                     ("harness", (False, 0, [], "boom"), True)):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            emit(*args)
        text = buffer.getvalue()
        if text.count("\n") != 1:
            failures.append(f"{label}: emit wrote {text.count(chr(10))} lines")
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            failures.append(f"{label}: emit did not write JSON: {exc}")
            continue
        if set(payload) != ({"ok", "ran", "failures", "error"} if wants_error
                            else {"ok", "ran", "failures"}):
            failures.append(f"{label}: emit keys {sorted(payload)}")

    # 12: the env parser. Quoting, an export prefix, comments and a value
    # holding '=' are all things a real .env carries.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env_file = home / ".env"
        env_file.write_text(
            "# comment\n\n"
            "DEBUG=0\n"
            "export SECRET_KEY='x y'\n"
            'ALLOWED_HOSTS="a.example.com,b.example.com"\n'
            "DATABASE_URL=postgres://u:p@h/db?opt=1\n"
            "  SPACED  =  padded  \n"
            "NOEQUALS\n", encoding="utf-8")
        parsed = load_env_file(env_file)
        want_env = {"DEBUG": "0", "SECRET_KEY": "x y",
                    "ALLOWED_HOSTS": "a.example.com,b.example.com",
                    "DATABASE_URL": "postgres://u:p@h/db?opt=1",
                    "SPACED": "padded"}
        if parsed != want_env:
            failures.append(f"load_env_file gave {parsed}, want {want_env}")

        # 13: the interpreter probe, in the order the card documents.
        project = home / "backend"
        (project / "sub").mkdir(parents=True)
        (project / "manage.py").write_text("#\n", encoding="utf-8")
        if find_python(project, None) is not None:
            failures.append("find_python invented an interpreter that is not there")
        root_python = home / ".venv" / "bin" / "python"
        root_python.parent.mkdir(parents=True)
        root_python.write_text("#!/bin/sh\n", encoding="utf-8")
        root_python.chmod(0o644)
        if find_python(project, None) is not None:
            failures.append("a non-executable interpreter was accepted")
        root_python.chmod(0o755)
        if find_python(project, None) != root_python:
            failures.append("the repo-root venv beside the project was not found")

        # 14: <project>/.venv wins over the repo root, and --venv wins outright.
        project_python = project / ".venv" / "bin" / "python"
        project_python.parent.mkdir(parents=True)
        project_python.write_text("#!/bin/sh\n", encoding="utf-8")
        project_python.chmod(0o755)
        if find_python(project, None) != project_python:
            failures.append("the project venv did not take precedence")
        explicit = home / "other"
        (explicit / "bin").mkdir(parents=True)
        (explicit / "bin" / "python").write_text("#!/bin/sh\n", encoding="utf-8")
        (explicit / "bin" / "python").chmod(0o755)
        if find_python(project, str(explicit)) != explicit / "bin" / "python":
            failures.append("--venv did not override the probe")
        if find_python(project, str(home / "missing")) is not None:
            failures.append("a bad --venv silently fell back to the probe")

        # 15-17: the harness refusals, end to end. Every one of these returns
        # before `subprocess.run` is reached, so no child process is started
        # and the interpreter planted below is never executed.
        empty = home / "empty"
        (empty / "app").mkdir(parents=True)
        (empty / "app" / "manage.py").write_text("#\n", encoding="utf-8")
        ready = home / "ready" / "app"
        ready.mkdir(parents=True)
        (ready / "manage.py").write_text("#\n", encoding="utf-8")
        (ready / ".venv" / "bin").mkdir(parents=True)
        (ready / ".venv" / "bin" / "python").write_text("#!/bin/sh\n",
                                                        encoding="utf-8")
        (ready / ".venv" / "bin" / "python").chmod(0o755)
        for label, argv in (
                ("no --project", []),
                ("no manage.py", ["--project", str(empty)]),
                ("no interpreter", ["--project", str(empty / "app")]),
                ("missing --env-file", ["--project", str(ready),
                                        "--env-file", str(home / "nope.env")])):
            code, text = run_cli(argv)
            if code != 2:
                failures.append(f"{label}: exit {code}, want 2")
            if label != "no --project" and "error" not in (text or ""):
                failures.append(f"{label}: no JSON error line on stdout")
    return failures


def run_cli(argv: list[str]) -> tuple[int, str]:
    """main() over a fixed argv, returning its exit code and its stdout. Used
    only by --self-test, and only on paths that refuse before running a suite."""
    saved = sys.argv
    sys.argv = [NAME] + argv
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer), \
                contextlib.redirect_stderr(io.StringIO()):
            return main(), buffer.getvalue()
    finally:
        sys.argv = saved


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", help="directory containing manage.py")
    ap.add_argument("--venv", help="venv dir; default <project>/.venv then <project>/../.venv")
    ap.add_argument("--label", action="append", default=[], help="test label (repeatable)")
    ap.add_argument("--tag", action="append", default=[], help="--tag passed to manage.py test")
    ap.add_argument("--exclude-tag", action="append", default=[], help="--exclude-tag passed through")
    ap.add_argument("--settings", help="DJANGO_SETTINGS_MODULE override")
    ap.add_argument("--env-file", help="KEY=VALUE file sourced into the child env")
    ap.add_argument("--keepdb", action="store_true", help="pass --keepdb")
    ap.add_argument("--timeout", type=int, default=900, help="seconds before abort (default 900)")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=17 failures={len(failures)}")
        return 1 if failures else 0

    # Checked here rather than by argparse's required=True so --self-test
    # needs no other flag.
    if not args.project:
        print(f"{NAME}: the following arguments are required: --project",
              file=sys.stderr)
        return 2

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

    ok, ran, failures, error = summarise(proc.stdout or "", proc.returncode)
    emit(ok, ran, failures, error)
    return exit_code(ok, error)


if __name__ == "__main__":
    sys.exit(main())
