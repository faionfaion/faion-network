#!/usr/bin/env python3
"""wrangler-env-lint.py — find the bindings and vars a named Wrangler
environment silently loses because they are non-inheritable.

Cloudflare's own configuration docs say it plainly: bindings and environment
variables are non-inheritable and must be specified per environment. `vars`,
`kv_namespaces`, `d1_databases`, `r2_buckets`, `durable_objects`, `queues`,
`services` and secrets do NOT reach `[env.production]` from the top level,
while `routes` and `workers_dev` do. So a developer reads a top-level binding,
assumes production has it, and the mistake surfaces as `undefined` in
production at request time — never at deploy time, because wrangler deploys a
worker with a missing binding perfectly happily.

This is offline and reads nothing but the config file: no account, no token,
no network. It parses JSONC itself, because `wrangler.jsonc` carries comments
and trailing commas and the standard library has no JSONC parser and a tool
pack ships no dependencies. `wrangler.toml` goes through `tomllib`.

It does NOT judge whether a binding SHOULD exist in an environment. A staging
worker that deliberately has no R2 bucket is a design, not a bug; the tool
reports the delta and the caller decides. Silence is the claim being made.

Input:  --config wrangler.jsonc|wrangler.toml [--envs a,b] [--out report.md]
Output: one summary line on stdout; findings on stderr.

Exit: 0 every named environment redeclares everything - 1 at least one
      finding - 2 the tool could not run: no --config, unreadable file,
      unparseable JSONC or TOML, or an unwritable --out.
Zero model calls.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # python < 3.11 has no toml reader
    tomllib = None

NAME = "wrangler-env-lint"

# Keys Cloudflare documents as NON-inheritable: absent from a named
# environment means absent at runtime, whatever the top level says.
NON_INHERITABLE = (
    "vars", "define", "kv_namespaces", "d1_databases", "r2_buckets",
    "durable_objects", "queues", "services", "analytics_engine_datasets",
    "vectorize", "hyperdrive", "ai", "browser", "mtls_certificates",
    "send_email", "dispatch_namespaces", "version_metadata", "workflows",
    "unsafe",
)
# Keys that DO inherit. Listed so the tool can stay quiet about them and so a
# reader of this file learns the boundary rather than guessing at it.
INHERITABLE = (
    "route", "routes", "workers_dev", "preview_urls", "compatibility_date",
    "compatibility_flags", "main", "account_id", "build", "limits",
    "triggers", "rules", "tsconfig", "logpush", "no_bundle", "minify",
    "usage_model", "placement", "observability", "assets",
)

# OK: every top-level binding is redeclared in the one named environment, and
# the class behind the durable object binding is created by a migration. The
# `//` inside the string literal and the trailing comma are the point of the
# fixture: a naive comment stripper eats the URL, a naive JSON load rejects
# the comma, and either way the tool reports nonsense about a valid config.
OK_FIXTURE = """
{
  // deploy target
  "name": "api",
  "main": "src/index.ts",
  "compatibility_date": "2026-08-01",
  "vars": { "API_BASE": "https://example.com//v1" },
  "kv_namespaces": [{ "binding": "SESSIONS", "id": "abc" }],
  "durable_objects": { "bindings": [{ "name": "ROOM", "class_name": "Room" }] },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["Room"] }],
  "routes": ["api.example.com/*"],
  "env": {
    "production": {
      "vars": { "API_BASE": "https://example.com//v1" },
      "kv_namespaces": [{ "binding": "SESSIONS", "id": "def" }],
      "durable_objects": {
        "bindings": [{ "name": "ROOM", "class_name": "Room" }],
      },
    },
  },
}
"""
# BAD: the mistake a caller actually makes. Production redeclares the KV
# namespace, so it looks tended, but the var and the R2 bucket were never
# copied down, no compatibility_date is set, and the durable object class is
# bound without a migration that creates it.
BAD_FIXTURE = """
{
  "name": "api", /* one worker, two environments */
  "main": "src/index.ts",
  "vars": { "API_BASE": "https://example.com//v1", "FEATURE_X": "on" },
  "kv_namespaces": [{ "binding": "SESSIONS", "id": "abc" }],
  "r2_buckets": [{ "binding": "UPLOADS", "bucket_name": "uploads" }],
  "durable_objects": { "bindings": [{ "name": "ROOM", "class_name": "Room" }] },
  "env": {
    "production": {
      "kv_namespaces": [{ "binding": "SESSIONS", "id": "def" }]
    }
  }
}
"""


def strip_comments(text: str) -> str:
    """Drop `//` and `/* */` comments, leaving string literals untouched.

    A `//` inside a string is not a comment — `https://example.com` is the
    case that breaks every regex-based stripper ever written for this job."""
    out: list[str] = []
    i, n, in_string = 0, len(text), False
    while i < n:
        ch = text[i]
        if in_string:
            if ch == "\\" and i + 1 < n:
                out.append(text[i:i + 2])
                i += 2
                continue
            out.append(ch)
            if ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def drop_trailing_commas(text: str) -> str:
    """Drop a comma whose next non-space character closes an object or array.

    String-aware for the same reason as above: `{"a": "x,}"}` is legal."""
    out: list[str] = []
    i, n, in_string = 0, len(text), False
    while i < n:
        ch = text[i]
        if in_string:
            if ch == "\\" and i + 1 < n:
                out.append(text[i:i + 2])
                i += 2
                continue
            out.append(ch)
            if ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue
        if ch == ",":
            j = i + 1
            while j < n and text[j] in " \t\r\n":
                j += 1
            if j < n and text[j] in "}]":
                i += 1
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def parse_jsonc(text: str) -> dict:
    """JSONC to a dict. Raises ValueError on anything that is not an object."""
    obj = json.loads(drop_trailing_commas(strip_comments(text)))
    if not isinstance(obj, dict):
        raise ValueError("a wrangler config is a JSON object")
    return obj


def parse_config(path: Path) -> dict:
    """Read either dialect. Raises ValueError with a caller-usable message."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".toml":
        if tomllib is None:
            raise ValueError("reading wrangler.toml needs python 3.11 or newer")
        try:
            return tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            raise ValueError(f"toml: {exc}") from exc
    try:
        return parse_jsonc(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"jsonc: {exc}") from exc


def binding_names(key: str, value) -> list[str]:
    """The individual identities inside one config key, sorted.

    Empty means the key has no per-item identity and is compared whole."""
    if key in ("vars", "define") and isinstance(value, dict):
        return sorted(str(k) for k in value)
    if isinstance(value, dict):
        if isinstance(value.get("bindings"), list):
            return sorted(str(b.get("name") or b.get("binding") or "?")
                          for b in value["bindings"] if isinstance(b, dict))
        names: list[str] = []
        for group in ("producers", "consumers"):
            for item in value.get(group) or []:
                if isinstance(item, dict):
                    names.append(str(item.get("binding")
                                     or item.get("queue") or "?"))
        return sorted(names)
    if isinstance(value, list):
        return sorted(str(item.get("binding") or item.get("name") or "?")
                      for item in value if isinstance(item, dict))
    return []


def environments(cfg: dict) -> dict:
    """The named environments, or an empty mapping."""
    env = cfg.get("env")
    return {str(k): v for k, v in env.items()
            if isinstance(v, dict)} if isinstance(env, dict) else {}


def do_classes(scope: dict) -> set[str]:
    """Durable object classes this scope defines itself.

    A binding carrying `script_name` points at a class another worker owns, so
    this worker's migrations say nothing about it."""
    block = scope.get("durable_objects")
    if not isinstance(block, dict):
        return set()
    out = set()
    for item in block.get("bindings") or []:
        if isinstance(item, dict) and not item.get("script_name"):
            name = item.get("class_name")
            if name:
                out.add(str(name))
    return out


def migration_findings(cfg: dict) -> list[str]:
    """Durable object bindings the migration list does not account for."""
    findings: list[str] = []
    created: set[str] = set()
    deleted: set[str] = set()
    tags: list[str] = []
    for step in cfg.get("migrations") or []:
        if not isinstance(step, dict):
            continue
        tags.append(str(step.get("tag") or "?"))
        for field in ("new_classes", "new_sqlite_classes"):
            created.update(str(c) for c in step.get(field) or [])
        for item in step.get("renamed_classes") or []:
            if isinstance(item, dict) and item.get("to"):
                created.add(str(item["to"]))
        deleted.update(str(c) for c in step.get("deleted_classes") or [])

    bound = do_classes(cfg)
    for scope in environments(cfg).values():
        bound |= do_classes(scope)
    for cls in sorted(bound - created):
        findings.append(f"migrations: class {cls} is bound as a durable object "
                        "and no migration creates it")
    for cls in sorted(bound & deleted):
        findings.append(f"migrations: class {cls} is bound and a migration "
                        "deletes it")
    for tag in sorted({t for t in tags if tags.count(t) > 1}):
        findings.append(f"migrations: tag {tag} is used more than once")
    return findings


def check(cfg: dict, wanted: list[str] | None = None) -> list[str]:
    """Every finding, one string each. Pure: no I/O, no exits.

    Three rules. A non-inheritable key or a named binding present at the top
    level and absent from an environment is gone at runtime. A missing
    `compatibility_date` pins the worker to the oldest runtime semantics. A
    durable object class is bound but never created by a migration."""
    findings: list[str] = []
    envs = environments(cfg)
    for name in wanted or []:
        if name not in envs:
            findings.append(f"{name}: --envs names an environment the config "
                            "does not define")
    names = [n for n in sorted(envs) if not wanted or n in wanted]

    if not cfg.get("compatibility_date"):
        missing = [n for n in names if not envs[n].get("compatibility_date")]
        if not names or missing:
            where = ", ".join(missing) if missing else "top level"
            findings.append(f"compatibility_date is unset ({where}); the worker "
                            "runs on the oldest runtime semantics")

    for name in names:
        scope = envs[name]
        for key in NON_INHERITABLE:
            if key not in cfg:
                continue
            top = binding_names(key, cfg[key])
            here = binding_names(key, scope.get(key)) if key in scope else []
            if key not in scope:
                if top:
                    findings.append(
                        f"{name}: {key} {', '.join(top)} declared at the top "
                        "level and absent here — non-inheritable, so undefined "
                        "at runtime")
                else:
                    findings.append(
                        f"{name}: {key} declared at the top level and absent "
                        "here — non-inheritable, so undefined at runtime")
                continue
            for missing in [n for n in top if n not in here]:
                findings.append(
                    f"{name}: {key}.{missing} declared at the top level and "
                    "not redeclared here — non-inheritable, so undefined at "
                    "runtime")
    return findings + migration_findings(cfg)


def report(cfg: dict, names: list[str], findings: list[str]) -> str:
    """The matrix: one row per binding identity, one column per environment.

    This is what --out is for. It is the artefact a caller reads once while
    fixing the config, and exactly the thing that must not be on stdout."""
    envs = environments(cfg)
    head = ["| binding | top level | " + " | ".join(names) + " |",
            "|---|---|" + "---|" * len(names)]
    rows: list[str] = []
    for key in NON_INHERITABLE:
        if key not in cfg:
            continue
        for ident in binding_names(key, cfg[key]) or [""]:
            cells = []
            for name in names:
                scope = envs[name]
                if key not in scope:
                    cells.append("ABSENT")
                elif not ident or ident in binding_names(key, scope[key]):
                    cells.append("declared")
                else:
                    cells.append("ABSENT")
            label = f"{key}.{ident}" if ident else key
            rows.append(f"| {label} | declared | " + " | ".join(cells) + " |")
    lines = [f"# {NAME}", "", f"environments: {', '.join(names) or 'none'}", ""]
    lines += head + (rows or ["| none | | " + " | " * len(names) + "|"])
    lines += ["", f"findings: {len(findings)}", ""]
    lines += [f"- {f}" for f in findings] or ["- none"]
    return "\n".join(lines) + "\n"


def self_test() -> list[str]:
    """Parsing, the string-aware strippers and the three rules. No file read."""
    failures: list[str] = []
    try:
        ok = parse_jsonc(OK_FIXTURE)
        bad = parse_jsonc(BAD_FIXTURE)
    except ValueError as exc:
        return [f"fixture does not parse: {exc}"]

    if ok["vars"]["API_BASE"] != "https://example.com//v1":
        failures.append("a // inside a string literal was eaten as a comment")
    if "production" not in environments(ok):
        failures.append("a trailing comma before } broke the parse")
    if parse_jsonc('{"a": "x,}", "b": [1,],}')["a"] != "x,}":
        failures.append("a comma inside a string literal was dropped")
    if parse_jsonc(r'{"a": "he said \"//\"", "b": 1}')["a"] != 'he said "//"':
        failures.append("an escaped quote desynchronised the string scanner")
    if strip_comments('{"a": 1} /* tail') != '{"a": 1} ':
        failures.append("an unterminated block comment was not consumed")

    if check(ok):
        failures.append(f"OK fixture produced findings: {check(ok)}")
    found = check(bad)
    for want in ("FEATURE_X", "API_BASE", "r2_buckets",
                 "durable_objects", "compatibility_date", "class Room"):
        if not any(want in f for f in found):
            failures.append(f"BAD fixture did not report {want}")
    if any("kv_namespaces" in f for f in found):
        failures.append("a redeclared binding was reported as missing")
    if any("routes" in f for f in found):
        failures.append("an inheritable key was treated as non-inheritable")
    if not check(ok, ["nope"]):
        failures.append("--envs naming an undefined environment was not caught")
    if set(NON_INHERITABLE) & set(INHERITABLE):
        failures.append("a key is listed as both inheritable and not")

    if tomllib is not None:
        toml = tomllib.loads('name = "api"\n[env.production]\n')
        if not check(toml):
            failures.append("the toml path produced no compatibility_date finding")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", help="wrangler.jsonc, wrangler.json or wrangler.toml")
    ap.add_argument("--envs", help="comma-separated environment names to check")
    ap.add_argument("--out", help="write the full inheritance matrix here")
    ap.add_argument("--json", action="store_true",
                    help="emit the summary line as one line of JSON")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=14 failures={len(failures)}")
        return 1 if failures else 0

    if not args.config:
        print(f"{NAME}: --config is required", file=sys.stderr)
        return 2
    try:
        cfg = parse_config(Path(args.config))
    except (OSError, ValueError) as exc:
        print(f"{NAME}: cannot read the config: {exc}", file=sys.stderr)
        return 2

    wanted = [n.strip() for n in args.envs.split(",") if n.strip()] \
        if args.envs else None
    findings = check(cfg, wanted)
    names = [n for n in sorted(environments(cfg)) if not wanted or n in wanted]
    if args.out:
        try:
            Path(args.out).write_text(report(cfg, names, findings),
                                      encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write the matrix: {exc}", file=sys.stderr)
            return 2

    for finding in findings:
        print(f"{NAME}: {finding}", file=sys.stderr)
    if args.json:
        print(json.dumps({"tool": NAME, "config": args.config,
                          "environments": names, "findings": findings},
                         sort_keys=True))
    else:
        print(f"{NAME}: config={args.config} environments={len(names)} "
              f"findings={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
