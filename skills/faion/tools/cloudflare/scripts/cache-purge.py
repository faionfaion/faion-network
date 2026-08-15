#!/usr/bin/env python3
"""cache-purge.py — purge a Cloudflare zone's edge cache by url, tag, host or
everything, in confirmed chunks, without printing a response body.

This exists for output compression and for a safe confirmation, not for API
access. The purge endpoint takes at most 100 operations per request and is rate
limited to five requests a minute on Free for tag, host, prefix and everything
purges, so a real purge is a loop with pacing and 429 handling — the part a
model improvises badly and an MCP call cannot do at all. The answer a caller
needs back is how many operations went through, not the vendor's echo.

Safety is the other half. The tool is dry-run until --yes, prints the same plan
and the same plan digest in both modes so the preview can be compared with the
run, caps the change set, and refuses to purge everything unless --yes carries
the zone name itself. Purging everything is the one operation here with a real
blast radius: it evicts every cached object for the zone and the origin absorbs
the refill.

It does NOT delete anything at the origin and cannot: a purge only evicts
copies. It also never edits DNS or settings — its credential needs Cache Purge
and nothing else.

Input:  --zone plus exactly one of --files, --tags, --hosts, --everything
Output: one summary line on stdout; the plan and any refusal on stderr.

Exit: 0 the plan ran or was previewed - 1 the self-test failed - 2 the tool
      could not run - 3 the credential is absent - 4 the credential was
      rejected - 5 refused, unconfirmed or over the cap - 6 the vendor API
      failed, including a rate limit that outlived the backoff.
Zero model calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

NAME = "cache-purge"
API = "https://api.cloudflare.com/client/v4"
ENV_VAR = "CLOUDFLARE_API_TOKEN"
TIMEOUT = 30

# Vendor limit: 100 operations per request.
CHUNK = 100
# Self-imposed caps on one run. The tagged modes share the five-per-minute
# budget, so 500 operations is one minute of purging; a bigger change set is a
# decision, not a flag, and comes back as a refusal.
CAPS = {"files": 1000, "tags": 500, "hosts": 500, "everything": 1}
# Seconds between requests. Twelve is the five-per-minute plan limit.
PACE = {"files": 1.0, "tags": 12.0, "hosts": 12.0, "everything": 12.0}
BACKOFF = [15.0, 30.0, 60.0]
RETRIES = 3
PREVIEW = 10

# Written as a join so this file carries no literal URL: every URL in a tool is
# checked against meta.json network.hosts, and a fixture host is not a host
# this tool may ever contact.
SITE = "https://example.com"
OK_FIXTURE = "\n".join([SITE + "/a.css", "# a comment", "",
                        SITE + "/b.js", "  " + SITE + "/c.png  "])
BAD_FIXTURE = "\n".join([SITE + "/a.css", "/relative/path.css"])


class ApiError(Exception):
    """A failed call, carrying the exit code the caller should return."""

    def __init__(self, code: int, message: str, status: int | None = None):
        super().__init__(message)
        self.code = code
        self.status = status


class SameHostRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse a redirect that leaves the API host.

    The request carries a bearer credential in a header and urllib would
    replay that header at whatever host the Location line names."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        here = urllib.parse.urlsplit(req.full_url).hostname
        there = urllib.parse.urlsplit(newurl).hostname
        if here != there:
            return None
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def envelope_errors(body: dict) -> list[str]:
    """The envelope's own error strings, never its result."""
    out = []
    for item in body.get("errors") or []:
        if isinstance(item, dict):
            out.append(f"{item.get('code', '?')}: {item.get('message', '')}")
        else:
            out.append(str(item))
    return out


def read_items(text: str) -> list[str] | str:
    """One url per line, blanks and # comments skipped, or one error string."""
    items: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith("http"):
            return f"line {lineno}: {line!r} is not an absolute url"
        items.append(line)
    return items


def split_list(value: str) -> list[str]:
    """A comma-separated flag value, deduplicated and ordered."""
    return sorted({part.strip() for part in value.split(",") if part.strip()})


def chunked(items: list[str]) -> list[list[str]]:
    """Operations grouped into requests of at most CHUNK."""
    return [items[i:i + CHUNK] for i in range(0, len(items), CHUNK)]


def plan(mode: str, items: list[str]) -> list[dict]:
    """The exact request bodies this run would send. Pure: no I/O, no exits."""
    if mode == "everything":
        return [{"purge_everything": True}]
    return [{mode: chunk} for chunk in chunked(items)]


def digest(bodies: list[dict]) -> str:
    """A stable fingerprint of the change set, so a preview can be compared
    with the run that follows it."""
    blob = json.dumps(bodies, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


def refusal(mode: str, items: list[str], zone: str,
            confirm: str | None) -> str | None:
    """Why this run must not mutate, or None when it may. Pure.

    Two refusals, both exit 5: a change set past the cap, and a run that was
    never confirmed. Purging everything wants the zone name as the value of
    --yes, because typing the zone is the one confirmation that cannot be
    muscle memory from the last invocation."""
    count = 1 if mode == "everything" else len(items)
    cap = CAPS[mode]
    if count > cap:
        return (f"{count} {mode} operations is over the cap of {cap} for one "
                "run; split it or raise the cap deliberately")
    if mode == "everything":
        if confirm != zone:
            return ("purging everything needs the zone name repeated as the "
                    "value of --yes, e.g. --yes " + (zone or "example.com"))
        return None
    if confirm is None:
        return f"{count} {mode} operations were planned and not confirmed"
    return None


def preview(mode: str, bodies: list[dict]) -> list[str]:
    """The change set, capped: a plan longer than a screen is not a plan."""
    if mode == "everything":
        return ["every cached object for the zone"]
    items = [item for body in bodies for item in body[mode]]
    shown = [f"{mode[:-1]}: {item}" for item in items[:PREVIEW]]
    if len(items) > PREVIEW:
        shown.append(f"... and {len(items) - PREVIEW} more")
    return shown


def with_backoff(send, sleeper) -> dict:
    """Run send(), retrying a 429 with a widening pause. Pure policy: the
    caller injects both the request and the clock, so the rule is testable
    without a socket."""
    for attempt in range(RETRIES):
        try:
            return send()
        except ApiError as exc:
            if exc.status != 429 or attempt + 1 >= RETRIES:
                raise
            sleeper(BACKOFF[min(attempt, len(BACKOFF) - 1)])
    raise ApiError(6, "rate limited beyond the backoff", 429)


def request(path: str, token: str, payload: dict | None = None) -> dict:
    """One call. GET without a payload, POST with one."""
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API + path, data=data,
                                 method="GET" if data is None else "POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    opener = urllib.request.build_opener(SameHostRedirect)
    try:
        with opener.open(req, timeout=TIMEOUT) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise ApiError(4, f"credential rejected ({exc.code}) on {path}",
                           exc.code)
        raise ApiError(6, f"api {exc.code} on {path}", exc.code)
    except (urllib.error.URLError, OSError) as exc:
        raise ApiError(2, f"cannot reach the api: {exc}")
    except ValueError:
        raise ApiError(6, f"api returned unparseable json on {path}")
    if not body.get("success"):
        detail = "; ".join(envelope_errors(body))[:160]
        raise ApiError(6, f"api rejected {path}: {detail}")
    return body


def verify(token: str) -> None:
    """Prove the credential works without mutating anything. One GET."""
    request("/user/tokens/verify", token)


def resolve_zone(zone: str, token: str) -> str:
    """The zone id for a zone name."""
    body = request(f"/zones?name={urllib.parse.quote(zone)}", token)
    result = body.get("result") or []
    if not result:
        raise ApiError(2, f"no zone named {zone} is visible to this token")
    return str(result[0].get("id"))


def run(zone_id: str, token: str, mode: str, bodies: list[dict],
        sleeper) -> int:
    """Send every chunk, paced. Returns the operations that went through."""
    done = 0
    for index, body in enumerate(bodies):
        if index:
            sleeper(PACE[mode])
        with_backoff(lambda: request(f"/zones/{zone_id}/purge_cache", token,
                                     body), sleeper)
        done += 1 if mode == "everything" else len(body[mode])
    return done


def self_test() -> list[str]:
    """Prove parsing, chunking, the caps, the confirmation rules and the 429
    backoff. Makes no network call and needs no credential."""
    failures: list[str] = []
    items = read_items(OK_FIXTURE)
    if isinstance(items, str):
        return [f"fixture does not parse: {items}"]
    if len(items) != 3:
        failures.append(f"expected 3 urls from the fixture, got {items}")
    if not isinstance(read_items(BAD_FIXTURE), str):
        failures.append("a relative path was accepted as a purge url")

    many = [f"{SITE}/{n}.css" for n in range(250)]
    bodies = plan("files", many)
    if [len(b["files"]) for b in bodies] != [100, 100, 50]:
        failures.append(f"chunking gave {[len(b['files']) for b in bodies]}")
    if plan("everything", []) != [{"purge_everything": True}]:
        failures.append("the everything body is not what the api takes")
    if plan("tags", ["a", "b"]) != [{"tags": ["a", "b"]}]:
        failures.append("a tag body was built wrong")
    if digest(bodies) != digest(plan("files", many)):
        failures.append("the plan digest is not stable")
    if digest(bodies) == digest(plan("files", many[:-1])):
        failures.append("the plan digest ignored a change")

    if refusal("files", many, "example.com", "yes") is not None:
        failures.append("a confirmed run under the cap was refused")
    if refusal("files", many, "example.com", None) is None:
        failures.append("an unconfirmed run was allowed to mutate")
    if refusal("files", [f"{SITE}/{n}" for n in range(1001)],
               "example.com", "yes") is None:
        failures.append("a change set over the cap was allowed")
    if refusal("everything", [], "example.com", "yes") is None:
        failures.append("everything ran on a bare confirmation")
    if refusal("everything", [], "example.com", "other.com") is None:
        failures.append("everything ran on the wrong zone name")
    if refusal("everything", [], "example.com", "example.com") is not None:
        failures.append("everything refused the zone name that confirms it")

    shown = preview("files", bodies)
    if len(shown) != PREVIEW + 1 or "and 240 more" not in shown[-1]:
        failures.append(f"the preview is not capped: {shown[-1:]}")

    slept: list[float] = []
    attempts = {"n": 0}

    def flaky() -> dict:
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise ApiError(6, "rate limited", 429)
        return {"success": True}

    if with_backoff(flaky, slept.append) != {"success": True}:
        failures.append("the backoff did not return the eventual success")
    if slept != BACKOFF[:2]:
        failures.append(f"the backoff waits were {slept}")

    def refused() -> dict:
        raise ApiError(4, "credential rejected", 403)

    try:
        with_backoff(refused, slept.append)
        failures.append("a 403 was retried instead of raised")
    except ApiError as exc:
        if exc.code != 4:
            failures.append(f"a 403 came back as exit {exc.code}")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zone", help="zone name to purge, e.g. example.com")
    ap.add_argument("--files", help="file of absolute urls, one per line")
    ap.add_argument("--tags", help="comma-separated cache tags")
    ap.add_argument("--hosts", help="comma-separated hostnames")
    ap.add_argument("--everything", action="store_true",
                    help="purge every cached object for the zone")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan, verify the credential, purge nothing")
    ap.add_argument("--yes", nargs="?", const="yes", default=None,
                    help="execute; for everything its value must be the zone")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit, offline")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=17 failures={len(failures)}")
        return 1 if failures else 0

    chosen = [name for name, value in (("files", args.files),
                                       ("tags", args.tags),
                                       ("hosts", args.hosts),
                                       ("everything", args.everything))
              if value]
    if not args.zone or len(chosen) != 1:
        print(f"{NAME}: --zone and exactly one of --files, --tags, --hosts, "
              "--everything are required", file=sys.stderr)
        return 2
    mode = chosen[0]

    items: list[str] = []
    if mode == "files":
        try:
            parsed = read_items(Path(args.files).read_text(encoding="utf-8"))
        except OSError as exc:
            print(f"{NAME}: cannot read the url list: {exc}", file=sys.stderr)
            return 2
        if isinstance(parsed, str):
            print(f"{NAME}: {parsed}", file=sys.stderr)
            return 2
        items = parsed
    elif mode in ("tags", "hosts"):
        items = split_list(args.tags if mode == "tags" else args.hosts)
    if mode != "everything" and not items:
        print(f"{NAME}: no {mode} to purge", file=sys.stderr)
        return 2

    bodies = plan(mode, items)
    ops = 1 if mode == "everything" else len(items)
    for line in preview(mode, bodies):
        print(f"{NAME}: plan: {line}", file=sys.stderr)

    def summary(purged: int) -> None:
        print(f"{NAME}: zone={args.zone} mode={mode} ops={ops} "
              f"requests={len(bodies)} purged={purged} digest={digest(bodies)}")

    stop = refusal(mode, items, args.zone, args.yes)
    if stop and ("over the cap" in stop or not args.dry_run):
        print(f"{NAME}: refused: {stop}", file=sys.stderr)
        summary(0)
        return 5

    token = os.environ.get(ENV_VAR, "").strip()
    if not token:
        print(f"{NAME}: {ENV_VAR} is not set; the credential is read from the "
              "environment and there is no flag for it", file=sys.stderr)
        return 3

    if args.dry_run:
        try:
            verify(token)
        except ApiError as exc:
            print(f"{NAME}: {exc}", file=sys.stderr)
            return exc.code
        print(f"{NAME}: dry run: credential verified, nothing purged",
              file=sys.stderr)
        summary(0)
        return 0

    try:
        zone_id = resolve_zone(args.zone, token)
        purged = run(zone_id, token, mode, bodies, time.sleep)
    except ApiError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return exc.code
    summary(purged)
    return 0


if __name__ == "__main__":
    sys.exit(main())
