#!/usr/bin/env python3
"""smoke-check.py — assert what a deployed site actually serves, not merely
that something answered.

The post-deploy check everybody writes is `curl -f https://site/ && echo ok`.
It passes against a build that is stale, half-copied or empty, because all of
those return 200. The real failures look like this: an incremental Gatsby
build leaves the previous route's directory in place, so a removed page keeps
serving last month's HTML; a broken bundle leaves an SPA shell that renders
nothing; an nginx root pointing one directory too high serves an index that is
400 bytes of directory listing.

So a check here carries the assertions nobody thinks to add: `not_contains`
for the string that must have disappeared, and `min_bytes` for the floor a
real page cannot fall below. Those two catch the stale and the empty build
respectively, and status alone catches neither.

It issues GET, and HEAD where a check says so. Nothing else: no POST, no
mutation, no login. A smoke check that can change the server is not a smoke
check.

Input:  --spec a JSON file of checks, optionally --base to point the same spec
        at staging or production
Output: one summary line on stdout; one line per failing check on stderr; the
        full result of every check as JSON under --out.

Exit: 0 every check passed · 1 at least one assertion failed · 2 the tool
      could not run (bad spec, unresolvable host, missing auth value).
Zero model calls. One request per check, plus retries.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

NAME = "smoke-check"
USER_AGENT = "faion-smoke-check/1.0"
# The environment variable holding the value for a check's auth header. Never a
# flag: argv is visible in `ps` and lands in shell history and in transcripts.
AUTH_ENV = "SMOKE_AUTH_VALUE"
MAX_BODY = 4 * 1024 * 1024
RETRY_SLEEP = 1.0
METHODS = ("GET", "HEAD")
BODY_KEYS = ("contains", "not_contains", "min_bytes")

OK_SPEC = json.dumps({
    "base": "https://example.com",
    "checks": [
        {"name": "home", "path": "/", "status": 200, "min_bytes": 2048,
         "contains": ["<main"], "not_contains": ["Gatsby development runtime"],
         "content_type": "text/html", "max_ms": 1500},
        {"path": "/assets/app.js", "method": "HEAD", "content_type": "javascript"},
    ],
})
# The mistake a caller actually makes: body assertions on a HEAD request, which
# can never see a body, and a path with no base to hang it on.
BAD_SPEC = json.dumps({
    "checks": [{"path": "/", "method": "HEAD", "min_bytes": 2048}],
})


def response_fixture(status: int = 200, body: bytes = b"<main>" + b"x" * 4090,
                     content_type: str = "text/html; charset=utf-8",
                     elapsed_ms: float = 120.0) -> dict:
    """A canned response, so the evaluator is testable without a server."""
    return {"status": status, "headers": {"content-type": content_type},
            "body": body, "elapsed_ms": elapsed_ms, "error": None,
            "truncated": False}


def as_list(value) -> list:
    """One string or a list of them, always a list."""
    if value is None:
        return []
    return list(value) if isinstance(value, list) else [value]


def normalise(entry, index: int, base: str, auth_header: str) -> tuple[dict, list[str]]:
    """One spec entry as the evaluator wants it, plus everything wrong with it."""
    errors: list[str] = []
    if not isinstance(entry, dict):
        return {}, [f"check {index}: not a JSON object"]
    method = str(entry.get("method", "GET")).upper()
    if method not in METHODS:
        errors.append(f"check {index}: method {method!r} — only GET and HEAD, a "
                      "smoke check never mutates")
    url = entry.get("url") or ""
    if not url:
        path = entry.get("path")
        if not isinstance(path, str) or not path.startswith("/"):
            errors.append(f"check {index}: needs 'url', or 'path' starting with /")
        elif not base:
            errors.append(f"check {index}: has a path and the spec sets no base")
        else:
            url = base.rstrip("/") + path
    if url and not url.startswith(("http://", "https://")):
        errors.append(f"check {index}: {url!r} is not http or https")
    status = [int(code) for code in as_list(entry.get("status", 200))
              if isinstance(code, int)]
    if not status:
        errors.append(f"check {index}: 'status' must be an integer or a list of them")
    for key in ("min_bytes", "max_ms"):
        if entry.get(key) is not None and not isinstance(entry[key], int):
            errors.append(f"check {index}: {key!r} must be an integer")
    if method == "HEAD":
        for key in BODY_KEYS:
            if entry.get(key) is not None:
                errors.append(f"check {index}: {key!r} on a HEAD request, which "
                              "never sees a body")
    name = str(entry.get("name") or f"{method} {entry.get('path') or url}")
    check = {
        "name": name, "url": url, "method": method, "status": status,
        "contains": [str(s) for s in as_list(entry.get("contains"))],
        "not_contains": [str(s) for s in as_list(entry.get("not_contains"))],
        "min_bytes": entry.get("min_bytes"), "max_ms": entry.get("max_ms"),
        "content_type": entry.get("content_type"),
        "auth_header": entry.get("auth_header") or auth_header,
    }
    return check, errors


def load_spec(text: str, base_override: str) -> tuple[list[dict], list[str]]:
    """The spec file as a list of checks, or every reason it cannot be used."""
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        return [], [f"spec is not JSON: {exc}"]
    if isinstance(raw, list):
        raw = {"checks": raw}
    if not isinstance(raw, dict):
        return [], ["spec must be a JSON object or a list of checks"]
    entries = raw.get("checks")
    if not isinstance(entries, list) or not entries:
        return [], ["spec has no non-empty 'checks' list"]
    base = base_override or str(raw.get("base") or "")
    auth_header = str(raw.get("auth_header") or "")
    checks: list[dict] = []
    errors: list[str] = []
    for index, entry in enumerate(entries, 1):
        check, problems = normalise(entry, index, base, auth_header)
        errors += problems
        if check:
            checks.append(check)
    return checks, errors


def evaluate(check: dict, response: dict) -> list[str]:
    """Every assertion this check makes that the response failed. Pure.

    Ordered so the most explanatory finding comes first: a wrong status
    explains a missing string, never the other way round.
    """
    findings: list[str] = []
    label = check["name"]
    if response["status"] not in check["status"]:
        wanted = "/".join(str(code) for code in check["status"])
        findings.append(f"{label}: status {response['status']}, expected {wanted}")
    body = response["body"]
    text = body.decode("utf-8", "replace")
    for needle in check["contains"]:
        if needle not in text:
            findings.append(f"{label}: body does not contain {needle!r}")
    for needle in check["not_contains"]:
        if needle in text:
            findings.append(f"{label}: body still contains {needle!r} — the build "
                            "serving this path is stale")
    if check["min_bytes"] is not None and len(body) < check["min_bytes"]:
        findings.append(f"{label}: body is {len(body)} bytes, minimum "
                        f"{check['min_bytes']} — a 200 over an empty or "
                        "shell-only build")
    if check["content_type"]:
        served = response["headers"].get("content-type", "")
        if check["content_type"].lower() not in served.lower():
            findings.append(f"{label}: content-type {served or 'absent'!r}, "
                            f"expected {check['content_type']!r}")
    if check["max_ms"] is not None and response["elapsed_ms"] > check["max_ms"]:
        findings.append(f"{label}: {response['elapsed_ms']:.0f} ms, over the "
                        f"{check['max_ms']} ms budget")
    return findings


def fetch(check: dict, timeout: float, auth_value: str) -> dict:
    """One request. The only I/O in the tool, and it is a read."""
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if check["auth_header"] and auth_value:
        headers[check["auth_header"]] = auth_value
    request = urllib.request.Request(check["url"], method=check["method"],
                                     headers=headers)
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = b"" if check["method"] == "HEAD" else response.read(MAX_BODY)
            status, raw = response.status, response.headers
    except urllib.error.HTTPError as exc:
        body = b"" if check["method"] == "HEAD" else exc.read(MAX_BODY)
        status, raw = exc.code, exc.headers
    except urllib.error.URLError as exc:
        kind = "dns" if isinstance(exc.reason, socket.gaierror) else "transport"
        return {"error": kind, "message": str(exc.reason), "status": 0,
                "headers": {}, "body": b"", "truncated": False,
                "elapsed_ms": (time.monotonic() - started) * 1000}
    except (OSError, ValueError) as exc:
        return {"error": "transport", "message": str(exc), "status": 0,
                "headers": {}, "body": b"", "truncated": False,
                "elapsed_ms": (time.monotonic() - started) * 1000}
    return {"error": None, "message": "", "status": status,
            "headers": {key.lower(): value for key, value in raw.items()},
            "body": body, "truncated": len(body) >= MAX_BODY,
            "elapsed_ms": (time.monotonic() - started) * 1000}


def run_check(check: dict, attempts: int, timeout: float,
              auth_value: str) -> tuple[dict, list[str]]:
    """Try a check until it passes or the attempts run out.

    Retrying is the point: a check fired seconds after a restart is racing the
    service, and a single red result there is noise, not a finding.
    """
    response: dict = {}
    findings: list[str] = []
    for attempt in range(1, attempts + 1):
        response = fetch(check, timeout, auth_value)
        if response["error"] == "dns":
            return response, [f"{check['name']}: cannot resolve the host "
                              f"({response['message']})"]
        if response["error"]:
            findings = [f"{check['name']}: no response ({response['message']})"]
        else:
            findings = evaluate(check, response)
        if not findings or attempt == attempts:
            break
        time.sleep(RETRY_SLEEP)
    return response, findings


def report(results: list[dict]) -> str:
    """The full inventory: what every check asked for and what it got."""
    payload = {
        "ok": not any(result["findings"] for result in results),
        "failed": [result["name"] for result in results if result["findings"]],
        "checks": results,
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def self_test() -> list[str]:
    """Exercise the evaluator against canned responses. Opens no socket."""
    failures: list[str] = []
    checks, errors = load_spec(OK_SPEC, "")
    if errors:
        failures.append(f"OK spec rejected: {errors}")
    if len(checks) != 2:
        failures.append(f"OK spec produced {len(checks)} checks, expected 2")
    _, bad_errors = load_spec(BAD_SPEC, "")
    if len(bad_errors) < 2:
        failures.append(f"BAD spec produced {len(bad_errors)} errors, expected "
                        "a HEAD-with-body error and a missing-base error")
    if not load_spec("{not json", "")[1]:
        failures.append("malformed JSON accepted as a spec")

    check = checks[0] if checks else {}
    cases = [
        ("status", response_fixture(), response_fixture(status=502)),
        ("contains", response_fixture(), response_fixture(body=b"<div>" + b"x" * 4090)),
        ("not_contains", response_fixture(),
         response_fixture(body=b"<main>Gatsby development runtime" + b"x" * 4090)),
        ("content_type", response_fixture(),
         response_fixture(content_type="application/json")),
        ("min_bytes", response_fixture(),
         response_fixture(body=b"<main></main>")),
        ("max_ms", response_fixture(), response_fixture(elapsed_ms=9000.0)),
    ]
    for label, passing, failing in cases:
        if evaluate(check, passing):
            failures.append(f"{label}: passing fixture produced "
                            f"{evaluate(check, passing)}")
        found = evaluate(check, failing)
        if not found:
            failures.append(f"{label}: failing fixture produced no finding")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", help="JSON file of checks to assert")
    ap.add_argument("--base", help="origin the spec's paths hang off, "
                                   "overriding the one in the spec")
    ap.add_argument("--timeout", type=float, default=10.0,
                    help="per-request timeout in seconds")
    ap.add_argument("--retries", type=int, default=3,
                    help="attempts per check before it is reported failed")
    ap.add_argument("--out", help="write every check's full result as JSON here")
    ap.add_argument("--json", action="store_true",
                    help="print one JSON object instead of the summary line")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=16 failures={len(failures)}")
        return 1 if failures else 0

    if not args.spec:
        print(f"{NAME}: --spec is required", file=sys.stderr)
        return 2
    try:
        text = Path(args.spec).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"{NAME}: cannot read spec: {exc}", file=sys.stderr)
        return 2
    checks, errors = load_spec(text, args.base or "")
    for error in errors:
        print(f"{NAME}: {error}", file=sys.stderr)
    if errors:
        return 2
    if args.retries < 1 or args.timeout <= 0:
        print(f"{NAME}: --retries must be at least 1 and --timeout positive",
              file=sys.stderr)
        return 2

    auth_value = os.environ.get(AUTH_ENV, "")
    if any(check["auth_header"] for check in checks) and not auth_value:
        print(f"{NAME}: a check sets an auth header and {AUTH_ENV} is empty",
              file=sys.stderr)
        return 2

    results: list[dict] = []
    failed: list[str] = []
    for check in checks:
        response, findings = run_check(check, args.retries, args.timeout,
                                       auth_value)
        if response.get("error") == "dns":
            for finding in findings:
                print(f"{NAME}: {finding}", file=sys.stderr)
            return 2
        results.append({
            "name": check["name"], "url": check["url"], "method": check["method"],
            "status": response["status"], "bytes": len(response["body"]),
            "ms": round(response["elapsed_ms"]),
            "content_type": response["headers"].get("content-type", ""),
            "truncated": response["truncated"], "findings": findings,
        })
        if findings:
            failed.append(check["name"])

    if args.out:
        try:
            Path(args.out).write_text(report(results), encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write report: {exc}", file=sys.stderr)
            return 2

    if args.json:
        print(json.dumps({"ok": not failed, "failed": failed}, sort_keys=True))
        return 1 if failed else 0
    for result in results:
        for finding in result["findings"]:
            print(f"{NAME}: {finding}", file=sys.stderr)
    slowest = max((result["ms"] for result in results), default=0)
    print(f"{NAME}: checks={len(results)} failed={len(failed)} "
          f"slowest={slowest}ms -> {args.out or 'stderr'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
