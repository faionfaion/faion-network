#!/usr/bin/env python3
"""unit-lint.py — lint a systemd unit against filesystem reality before it
ever reaches a box.

`systemd-analyze verify` parses a unit and checks its grammar. It cannot tell
you that ExecStart points at a binary the deploy never rsynced, that the
EnvironmentFile holding the database password is mode 0644, that
ProtectHome=true makes the WorkingDirectory unreachable, or that
ProtectSystem=strict leaves the app's own log directory read-only. Each of
those is a green pipeline followed by a unit that dies on first
`systemctl start`, and each is the same twenty-minute loop: edit, rsync,
daemon-reload, start, journalctl, guess again.

The tool reads a unit file and, given --root, the tree that unit will run
against. It starts nothing and writes nothing back — a tool that "fixed" a
unit in place would edit the runtime while the repo stayed wrong, and the repo
is the source.

It deliberately does NOT decide whether the service is correct: no port is
opened, no binary is executed, no sd_notify capability is probed. Type=notify
against an interpreter is reported as a risk, never a verdict, because only
the application knows whether it calls sd_notify.

Input:  --unit the file; optional --root to resolve its paths against;
        optional --installed to check the unit name for a collision
Output: one summary line on stdout; one line per finding on stderr; the full
        parse plus every finding as JSON under --out.

Exit: 0 no findings · 1 at least one finding · 2 the tool could not run.
Zero model calls. Zero network calls. Nothing is executed.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from pathlib import Path

NAME = "unit-lint"

EXEC_KEYS = ("ExecStart", "ExecStartPre", "ExecStartPost", "ExecReload",
             "ExecStop", "ExecStopPost")
# systemd's own ExecStart prefix characters, stripped before the binary path.
EXEC_PREFIX = "-@+!:"
PATH_LIST_KEYS = ("ReadWritePaths", "ReadOnlyPaths", "InaccessiblePaths")
# An absolute argument with one of these suffixes is somewhere the app writes.
WRITE_SUFFIXES = (".sock", ".pid", ".log", ".db", ".sqlite3", ".jsonl")
# Long arguments whose value is a file the app creates.
WRITE_ARGS = ("--log-file", "--logfile", "--error-logfile", "--access-logfile",
              "--pid", "--pidfile", "--pid-file", "--socket", "--unix-socket")
HOME_ROOTS = ("/home", "/root", "/run/user")
HIDDEN_HOME = ("yes", "true", "on", "1", "tmpfs")
ALWAYS_WRITABLE = ("/dev", "/proc", "/sys")
# Interpreters and shells that do not call sd_notify unless the app does.
NEVER_NOTIFY = ("sh", "bash", "dash", "zsh", "env", "python", "python2",
                "python3", "node", "ruby", "perl", "java", "php")
FOREGROUND_FLAGS = ("--foreground", "--no-daemon", "--nodaemon", "daemon off;")
TRUTHY = ("yes", "true", "on", "1")

OK_FIXTURE = """\
[Unit]
Description=example api
After=network.target

[Service]
Type=simple
User=example
Group=example
WorkingDirectory=/opt/example
EnvironmentFile=/opt/example/.env
ExecStart=/opt/example/.venv/bin/gunicorn example.wsgi:application \\
  --bind 127.0.0.1:8000 --workers 4
Restart=on-failure
RestartSec=5
ProtectSystem=full
ProtectHome=true
ReadWritePaths=/var/lib/example

[Install]
WantedBy=multi-user.target
"""

BAD_FIXTURE = """\
[Unit]
Description=broken api

[Service]
Type=notify
WorkingDirectory=srv/broken
EnvironmentFile=/srv/broken/.env
ExecStart=/usr/bin/python3 -m broken.app --log-file /var/log/broken/app.log
ProtectSystem=strict
"""

OK_FACTS = {"probed": True, "collision": None, "paths": {
    "/opt/example": {"exists": True, "is_dir": True, "executable": False,
                     "world_readable": False, "group_readable": False},
    "/opt/example/.env": {"exists": True, "is_dir": False, "executable": False,
                          "world_readable": False, "group_readable": True},
    "/opt/example/.venv/bin/gunicorn": {
        "exists": True, "is_dir": False, "executable": True,
        "world_readable": True, "group_readable": True},
    "/var/lib/example": {"exists": True, "is_dir": True, "executable": False,
                         "world_readable": False, "group_readable": False},
}}

BAD_FACTS = {"probed": True, "collision": None, "paths": {
    "/srv/broken/.env": {"exists": True, "is_dir": False, "executable": False,
                         "world_readable": True, "group_readable": True},
    "/usr/bin/python3": {"exists": True, "is_dir": False, "executable": True,
                         "world_readable": True, "group_readable": True},
}}


def parse_unit(text: str) -> dict[str, dict[str, list[str]]]:
    """A unit file as section -> key -> values, in file order.

    Repeated keys accumulate, because systemd treats several directives as
    lists; an empty assignment resets the list, exactly as systemd does, so a
    drop-in that clears ExecStart is not read as one that keeps it.
    """
    unit: dict[str, dict[str, list[str]]] = {}
    section = ""
    pending = ""
    for raw in text.splitlines():
        line = raw.strip()
        if pending:
            line = pending + " " + line
            pending = ""
        elif not line or line[0] in "#;":
            continue
        if line.endswith("\\"):
            pending = line[:-1].rstrip()
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            unit.setdefault(section, {})
            continue
        key, sep, value = line.partition("=")
        if not sep:
            continue
        bucket = unit.setdefault(section, {}).setdefault(key.strip(), [])
        value = value.strip()
        if value:
            bucket.append(value)
        else:
            bucket.clear()
    return unit


def every(unit: dict, section: str, key: str) -> list[str]:
    """Every value assigned to a key, in file order."""
    return list(unit.get(section, {}).get(key) or [])


def last(unit: dict, section: str, key: str, default: str = "") -> str:
    """The winning value for a single-valued directive: systemd takes the last."""
    values = every(unit, section, key)
    return values[-1] if values else default


def exec_tokens(value: str) -> list[str]:
    """An Exec* line split into argv, with systemd's prefix characters gone."""
    command = value.lstrip(EXEC_PREFIX)
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def under(path: str, root: str) -> bool:
    """True when path is root or lives beneath it."""
    if root == "/":
        return path.startswith("/")
    return path == root or path.startswith(root.rstrip("/") + "/")


def readonly_roots(value: str) -> tuple[str, ...]:
    """What ProtectSystem= makes read-only."""
    setting = value.lower()
    if setting in TRUTHY:
        return ("/usr", "/boot", "/efi")
    if setting == "full":
        return ("/usr", "/boot", "/efi", "/etc")
    if setting == "strict":
        return ("/",)
    return ()


def writable_roots(unit: dict) -> list[str]:
    """Everywhere the sandbox still allows a write."""
    roots: list[str] = list(ALWAYS_WRITABLE)
    for key in ("ReadWritePaths", "ReadWriteDirectories"):
        for value in every(unit, "Service", key):
            roots += [entry.lstrip("-+") for entry in exec_tokens(value)]
    for key, base in (("StateDirectory", "/var/lib"), ("LogsDirectory", "/var/log"),
                      ("CacheDirectory", "/var/cache"), ("RuntimeDirectory", "/run"),
                      ("ConfigurationDirectory", "/etc")):
        for value in every(unit, "Service", key):
            roots += [f"{base}/{entry}" for entry in value.split()]
    if last(unit, "Service", "PrivateTmp").lower() in TRUTHY:
        roots += ["/tmp", "/var/tmp"]
    return roots


def write_candidates(unit: dict) -> dict[str, tuple[str, bool]]:
    """Absolute paths the unit implies the service writes to.

    Value is (which directive named it, certain). WorkingDirectory is not
    certain — plenty of services never write to their cwd — so it only counts
    as a write target under --strict, while being unreachable there is always
    a finding.
    """
    found: dict[str, tuple[str, bool]] = {}

    def add(path: str, why: str, certain: bool = True) -> None:
        if path.startswith("/") and path not in found:
            found[path] = (why, certain)

    workdir = last(unit, "Service", "WorkingDirectory").lstrip("-")
    if workdir:
        add(workdir, "WorkingDirectory", False)
    if last(unit, "Service", "PIDFile"):
        add(last(unit, "Service", "PIDFile"), "PIDFile")
    for key in ("StandardOutput", "StandardError"):
        for value in every(unit, "Service", key):
            for prefix in ("file:", "append:", "truncate:"):
                if value.startswith(prefix):
                    add(value[len(prefix):], key)
    for key in EXEC_KEYS:
        for value in every(unit, "Service", key):
            tokens = exec_tokens(value)
            for index, token in enumerate(tokens):
                if token.startswith("unix:"):
                    add(token[5:], f"{key} socket")
                elif token in WRITE_ARGS and index + 1 < len(tokens):
                    add(tokens[index + 1], f"{key} {token}")
                elif "=" in token and token.split("=", 1)[0] in WRITE_ARGS:
                    add(token.split("=", 1)[1], f"{key} {token.split('=', 1)[0]}")
                elif token.startswith("/") and token.endswith(WRITE_SUFFIXES):
                    add(token, f"{key} argument")
    return found


def check_exec(unit: dict, paths: dict) -> list[str]:
    """ExecStart and friends: absolute, present, executable."""
    findings: list[str] = []
    if "Service" not in unit:
        return ["no [Service] section — this file is not a service unit"]
    if not every(unit, "Service", "ExecStart"):
        findings.append("ExecStart: missing — a service unit with nothing to run")
    for key in EXEC_KEYS:
        for value in every(unit, "Service", key):
            tokens = exec_tokens(value)
            if not tokens:
                findings.append(f"{key}: empty command")
                continue
            binary = tokens[0]
            if not binary.startswith("/"):
                findings.append(
                    f"{key}: {binary!r} is not absolute — systemd does not search "
                    "PATH, so the unit dies at exec with status=203/EXEC")
                continue
            fact = paths.get(binary)
            if fact is None:
                continue
            if not fact["exists"]:
                findings.append(f"{key}: {binary} is not there under the checked "
                                "root — status=203/EXEC on first start")
            elif not fact["executable"]:
                findings.append(f"{key}: {binary} exists and is not executable — "
                                "status=203/EXEC on first start")
    return findings


def check_paths(unit: dict, paths: dict, strict: bool) -> list[str]:
    """WorkingDirectory, EnvironmentFile, and the path-list directives."""
    findings: list[str] = []
    workdir = last(unit, "Service", "WorkingDirectory")
    target = workdir.lstrip("-")
    if target and target != "~" and not target.startswith("/"):
        findings.append(f"WorkingDirectory: {target!r} is relative — systemd "
                        "requires an absolute path and refuses the unit")
    elif target.startswith("/"):
        fact = paths.get(target)
        if fact and not fact["exists"] and not workdir.startswith("-"):
            findings.append(f"WorkingDirectory: {target} does not exist — the "
                            "service fails to chdir with status=200/CHDIR")
        elif fact and fact["exists"] and not fact["is_dir"]:
            findings.append(f"WorkingDirectory: {target} is not a directory")

    for value in every(unit, "Service", "EnvironmentFile"):
        optional = value.startswith("-")
        env = value.lstrip("-")
        if not env.startswith("/"):
            findings.append(f"EnvironmentFile: {env!r} is relative — systemd "
                            "requires an absolute path")
            continue
        fact = paths.get(env)
        if not fact:
            continue
        if not fact["exists"]:
            if not optional:
                findings.append(f"EnvironmentFile: {env} does not exist and is "
                                "not prefixed '-', so the unit refuses to start")
        elif fact["world_readable"]:
            findings.append(f"EnvironmentFile: {env} is world-readable — every "
                            "secret in it is readable by any local account; "
                            "chmod 0600 and chown it to the service user")
        elif fact["group_readable"] and strict:
            findings.append(f"EnvironmentFile: {env} is group-readable")

    for key in PATH_LIST_KEYS:
        for value in every(unit, "Service", key):
            for entry in exec_tokens(value):
                path = entry.lstrip("-+")
                if not path.startswith("/"):
                    findings.append(f"{key}: {path!r} is relative — the sandbox "
                                    "directives take absolute paths only")
                    continue
                fact = paths.get(path)
                if fact and not fact["exists"] and not entry.startswith("-"):
                    findings.append(
                        f"{key}: {path} does not exist — mount namespacing fails "
                        "and the unit dies with status=226/NAMESPACE; prefix it "
                        "'-' or create it with StateDirectory")
    return findings


def check_identity(unit: dict, strict: bool) -> list[str]:
    """Who the service runs as."""
    findings: list[str] = []
    user = last(unit, "Service", "User")
    group = last(unit, "Service", "Group")
    if not user:
        findings.append("User: absent — the service runs as root by omission, "
                        "which is the one privilege decision nobody made on "
                        "purpose; name a system user")
    elif user == "root" and strict:
        findings.append("User: root, stated deliberately — confirm it needs to be")
    if user and user != "root" and not group and strict:
        findings.append(f"Group: absent — the unit falls back to {user}'s primary "
                        "group, which may not be the group owning its files")
    return findings


def check_sandbox(unit: dict, strict: bool) -> list[str]:
    """Whether ReadWritePaths actually covers where the service writes."""
    findings: list[str] = []
    allowed = writable_roots(unit)
    readonly = readonly_roots(last(unit, "Service", "ProtectSystem"))
    home = last(unit, "Service", "ProtectHome").lower()
    for path, (why, certain) in write_candidates(unit).items():
        covered = any(under(path, root) for root in allowed)
        if covered:
            continue
        if home and any(under(path, root) for root in HOME_ROOTS):
            if home in HIDDEN_HOME:
                findings.append(
                    f"{why}: {path} is under ProtectHome={home}, which replaces it "
                    "with an empty tmpfs — the service cannot even read it; list "
                    "it in ReadWritePaths or move it out of the home tree")
                continue
            if home == "read-only" and certain:
                findings.append(f"{why}: {path} is read-only under "
                                "ProtectHome=read-only and the service writes there")
                continue
        if not readonly or (not certain and not strict):
            continue
        if any(under(path, root) for root in readonly):
            findings.append(
                f"{why}: {path} is read-only under ProtectSystem="
                f"{last(unit, 'Service', 'ProtectSystem')} and is not in "
                "ReadWritePaths — the first write fails with EROFS")
    return findings


def check_restart(unit: dict, service_type: str) -> list[str]:
    """Restart policy, skipped for the one type where it is usually wrong."""
    findings: list[str] = []
    if service_type == "oneshot":
        return findings
    restart = last(unit, "Service", "Restart")
    if not restart:
        findings.append("Restart: absent — the default is 'no', so one crash "
                        "leaves the service down until a human notices; "
                        "Restart=on-failure")
    elif restart != "no" and not last(unit, "Service", "RestartSec"):
        findings.append("RestartSec: absent — the 100ms default burns the "
                        "start-limit (5 starts in 10s) in half a second, so a "
                        "crash on boot ends with systemd giving up; RestartSec=5")
    return findings


def check_type(unit: dict, service_type: str, strict: bool) -> list[str]:
    """A Type= that contradicts the shape of its ExecStart."""
    findings: list[str] = []
    restart = last(unit, "Service", "Restart")
    tokens = exec_tokens(last(unit, "Service", "ExecStart"))
    binary = Path(tokens[0]).name if tokens else ""
    if service_type == "oneshot" and restart == "always":
        findings.append("Type=oneshot with Restart=always — systemd rejects the "
                        "combination and the unit never loads")
    if service_type == "forking" and not last(unit, "Service", "PIDFile"):
        findings.append("Type=forking without PIDFile — systemd guesses the main "
                        "process and often tracks the wrong one, so restarts and "
                        "status report a service that is not the one running")
    if service_type == "forking" and any(
            flag in last(unit, "Service", "ExecStart") for flag in FOREGROUND_FLAGS):
        findings.append("Type=forking with a foreground flag on ExecStart — the "
                        "process never forks and start times out")
    if service_type == "dbus" and not last(unit, "Service", "BusName"):
        findings.append("Type=dbus without BusName — systemd has no name to wait "
                        "for and refuses the unit")
    if service_type in ("notify", "notify-reload"):
        if binary in NEVER_NOTIFY:
            findings.append(
                f"Type={service_type} with ExecStart={binary} — a shell or bare "
                "interpreter never calls sd_notify, so start hangs for "
                "TimeoutStartSec (90s default) and then fails; use Type=simple "
                "or make the app notify")
        elif strict:
            findings.append(
                f"Type={service_type}: unverifiable here — if {binary or 'the binary'} "
                "does not call sd_notify, start hangs 90s and fails")
    return findings


def check_install(unit: dict) -> list[str]:
    """Whether the unit can be enabled at all."""
    if every(unit, "Install", "WantedBy") or every(unit, "Install", "RequiredBy") \
            or every(unit, "Install", "Also"):
        return []
    return ["[Install]: no WantedBy — `systemctl enable` has nothing to link, it "
            "reports success, and the service does not come back after a reboot"]


def check(unit: dict, facts: dict, strict: bool = False) -> list[str]:
    """Every finding, one string each. Pure: no I/O, no exits.

    `facts` carries what the filesystem said, gathered by probe(), so this
    function stays testable against fixtures and stays deterministic.
    """
    paths = facts.get("paths") or {}
    findings = check_exec(unit, paths)
    if "Service" not in unit:
        return findings
    service_type = last(unit, "Service", "Type", "simple")
    findings += check_paths(unit, paths, strict)
    findings += check_identity(unit, strict)
    findings += check_sandbox(unit, strict)
    findings += check_restart(unit, service_type)
    findings += check_type(unit, service_type, strict)
    findings += check_install(unit)
    collision = facts.get("collision")
    if collision and not collision["identical"]:
        findings.append(
            f"name: {collision['path']} already exists with different content — "
            "installing this unit replaces a unit somebody else is relying on")
    return findings


def interesting_paths(unit: dict) -> list[str]:
    """Absolute paths worth a stat, in a stable order."""
    wanted: list[str] = []
    for key in EXEC_KEYS:
        for value in every(unit, "Service", key):
            tokens = exec_tokens(value)
            if tokens and tokens[0].startswith("/"):
                wanted.append(tokens[0])
    for key in ("WorkingDirectory", "EnvironmentFile", "PIDFile"):
        for value in every(unit, "Service", key):
            wanted.append(value.lstrip("-"))
    for key in PATH_LIST_KEYS:
        for value in every(unit, "Service", key):
            wanted += [entry.lstrip("-+") for entry in exec_tokens(value)]
    seen: list[str] = []
    for path in wanted:
        if path.startswith("/") and path not in seen:
            seen.append(path)
    return seen


def probe(unit: dict, text: str, root: str | None,
          installed: str | None, unit_name: str) -> dict:
    """The only I/O in the tool: stat what the unit names. Reads, never writes."""
    facts: dict = {"probed": root is not None, "paths": {}, "collision": None}
    if root is not None:
        base = Path(root)
        for path in interesting_paths(unit):
            real = base / path.lstrip("/")
            entry = {"exists": real.exists(), "is_dir": real.is_dir(),
                     "executable": real.is_file() and os.access(real, os.X_OK),
                     "world_readable": False, "group_readable": False}
            try:
                mode = real.stat().st_mode
            except OSError:
                pass
            else:
                entry["world_readable"] = bool(mode & 0o004)
                entry["group_readable"] = bool(mode & 0o040)
            facts["paths"][path] = entry
    if installed:
        candidate = Path(installed) / unit_name
        if candidate.is_file():
            try:
                same = candidate.read_text(encoding="utf-8", errors="replace") == text
            except OSError:
                same = False
            facts["collision"] = {"path": str(candidate), "identical": same}
    return facts


def report(unit_name: str, unit: dict, facts: dict, findings: list[str]) -> str:
    """The full inventory: what was parsed, what was stat-ed, what was found."""
    payload = {
        "unit": unit_name,
        "ok": not findings,
        "probed": bool(facts.get("probed")),
        "sections": {name: {key: values for key, values in sorted(keys.items())}
                     for name, keys in sorted(unit.items())},
        "paths": {path: dict(sorted(fact.items()))
                  for path, fact in sorted((facts.get("paths") or {}).items())},
        "collision": facts.get("collision"),
        "findings": findings,
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def self_test() -> list[str]:
    """Prove the rules still behave against the two fixtures. No filesystem."""
    failures: list[str] = []
    ok_unit = parse_unit(OK_FIXTURE)
    bad_unit = parse_unit(BAD_FIXTURE)

    if last(ok_unit, "Service", "Type") != "simple":
        failures.append("parser lost Type=")
    if "--workers" not in last(ok_unit, "Service", "ExecStart"):
        failures.append("parser dropped an ExecStart line continuation")

    clean = check(ok_unit, OK_FACTS)
    if clean:
        failures.append(f"OK fixture produced findings: {clean}")

    dirty = check(bad_unit, BAD_FACTS)
    if not dirty:
        failures.append("BAD fixture produced no finding")
    for needle, label in (
            ("WorkingDirectory", "relative WorkingDirectory"),
            ("world-readable", "world-readable EnvironmentFile"),
            ("runs as root", "missing User"),
            ("EROFS", "uncovered write path under ProtectSystem=strict"),
            ("Restart", "missing Restart"),
            ("sd_notify", "Type=notify against an interpreter"),
            ("systemctl enable", "missing [Install]")):
        if not any(needle in finding for finding in dirty):
            failures.append(f"BAD fixture missed {label}")

    strict = check(ok_unit, OK_FACTS, strict=True)
    if len(strict) <= len(clean):
        failures.append("--strict added no advisory to the OK fixture")

    hidden = parse_unit("[Service]\nExecStart=/bin/true\nUser=x\nRestart=no\n"
                        "WorkingDirectory=/home/x/app\nProtectHome=yes\n"
                        "[Install]\nWantedBy=multi-user.target\n")
    if not any("ProtectHome" in finding for finding in check(hidden, {})):
        failures.append("ProtectHome=yes over a home WorkingDirectory not caught")

    collision = check(ok_unit, dict(OK_FACTS, collision={
        "path": "/etc/systemd/system/example.service", "identical": False}))
    if not any("already exists" in finding for finding in collision):
        failures.append("unit-name collision not reported")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--unit", help="path to the .service file to lint")
    ap.add_argument("--root", help="filesystem root the unit's absolute paths "
                                   "resolve against; omit to skip every "
                                   "existence check")
    ap.add_argument("--installed", help="directory of already-installed units, "
                                        "checked for a name collision")
    ap.add_argument("--strict", action="store_true",
                    help="report advisories as findings too")
    ap.add_argument("--json", action="store_true",
                    help="print one JSON object instead of the summary line")
    ap.add_argument("--out", help="write the full parse and findings as JSON here")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=14 failures={len(failures)}")
        return 1 if failures else 0

    if not args.unit:
        print(f"{NAME}: --unit is required", file=sys.stderr)
        return 2
    source = Path(args.unit)
    try:
        text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"{NAME}: cannot read unit: {exc}", file=sys.stderr)
        return 2
    if args.root and not Path(args.root).is_dir():
        print(f"{NAME}: --root {args.root} is not a directory", file=sys.stderr)
        return 2
    if args.installed and not Path(args.installed).is_dir():
        print(f"{NAME}: --installed {args.installed} is not a directory",
              file=sys.stderr)
        return 2

    unit = parse_unit(text)
    if not unit:
        print(f"{NAME}: {source.name} holds no [Section] at all — not a unit file",
              file=sys.stderr)
        return 2
    facts = probe(unit, text, args.root, args.installed, source.name)
    findings = check(unit, facts, args.strict)

    if args.out:
        try:
            Path(args.out).write_text(report(source.name, unit, facts, findings),
                                      encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write report: {exc}", file=sys.stderr)
            return 2

    if args.json:
        print(json.dumps({"ok": not findings, "unit": source.name,
                          "findings": findings}, sort_keys=True))
        return 1 if findings else 0
    for finding in findings:
        print(f"{NAME}: {finding}", file=sys.stderr)
    print(f"{NAME}: unit={source.name} findings={len(findings)} "
          f"probed={'yes' if facts['probed'] else 'no'} -> {args.out or 'stderr'}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
