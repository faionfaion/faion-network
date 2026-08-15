#!/usr/bin/env python3
"""dns-snapshot.py — snapshot one Cloudflare zone's DNS records into canonical
JSONL and fail when they have drifted from a committed baseline.

This exists for output compression, not for API access. A zone list is
paginated vendor JSON — id, created_on, modified_on, meta, comment and tags on
every record — and asking a model to spot a change in it costs the whole list
twice. This tool fetches the pages, reduces each record to the six fields that
decide anything, orders them deterministically, and prints only the names that
moved. An unchanged zone costs one line.

Records are compared per name and type, not per record id, because the id is
not stable across the operation that matters: in-place DNS type changes were
removed from the API (EOL 2026-06-30), so changing A to CNAME is now a delete
plus a create. Grouping by name and type keeps that legible as one removal and
one addition instead of two unrelated ids.

It does NOT judge whether a record is correct — only whether it is what the
baseline says. Commit the baseline, review the diff.

Input:  --zone, an optional --baseline JSONL to diff against
Output: one summary line on stdout; one line per changed name on stderr.

Exit: 0 no drift - 1 the zone differs from the baseline - 2 the tool could not
      run - 3 the credential is absent - 4 the credential was rejected
      - 6 the vendor API failed, including a rate limit.
Zero model calls.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

NAME = "dns-snapshot"
API = "https://api.cloudflare.com/client/v4"
ENV_VAR = "CLOUDFLARE_API_TOKEN"
TIMEOUT = 30
PER_PAGE = 100
MAX_PAGES = 200

# The only fields that decide anything. Everything else the API returns —
# id, meta, comment, tags, created_on, modified_on — is dropped, which is what
# makes a snapshot diffable and a diff readable.
FIELDS = ("name", "type", "content", "ttl", "proxied", "priority")

# A committed baseline and the same zone after somebody "just fixed one thing":
# the apex A moved, a staging CNAME appeared, the SPF record went away.
OK_FIXTURE = (
    '{"name": "example.com", "type": "A", "content": "203.0.113.10", '
    '"ttl": 1, "proxied": true}\n'
    '{"name": "www.example.com", "type": "CNAME", "content": "example.com", '
    '"ttl": 1, "proxied": true}\n'
    '{"name": "example.com", "type": "TXT", "content": "v=spf1 -all", '
    '"ttl": 3600}\n'
)
BAD_FIXTURE = (
    '{"name": "example.com", "type": "A", "content": "198.51.100.7", '
    '"ttl": 1, "proxied": false}\n'
    '{"name": "www.example.com", "type": "CNAME", "content": "example.com", '
    '"ttl": 1, "proxied": true}\n'
    '{"name": "stage.example.com", "type": "CNAME", '
    '"content": "example.com", "ttl": 1, "proxied": false}\n'
)


class ApiError(Exception):
    """A failed call, carrying the exit code the caller should return."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


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


def canonical(records: list, types: list[str] | None = None) -> list[dict]:
    """Records reduced to FIELDS, filtered, and ordered deterministically."""
    out: list[dict] = []
    for item in records:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("type") or "")
        if types and kind.upper() not in types:
            continue
        out.append({k: item[k] for k in FIELDS
                    if k in item and item[k] is not None})
    return sorted(out, key=lambda r: (str(r.get("name", "")),
                                      str(r.get("type", "")),
                                      str(r.get("content", ""))))


def shape(record: dict) -> str:
    """One comparable, printable string per record."""
    bits = [str(record.get("content", ""))]
    if record.get("priority") is not None:
        bits.append(f"prio={record['priority']}")
    if record.get("ttl") is not None:
        bits.append(f"ttl={record['ttl']}")
    if record.get("proxied") is not None:
        bits.append("proxied" if record["proxied"] else "direct")
    return " ".join(bits)


def group(records: list[dict]) -> dict:
    """{(name, type): [shape, ...]} — the unit a caller reasons about."""
    out: dict = {}
    for record in records:
        key = (str(record.get("name", "")), str(record.get("type", "")))
        out.setdefault(key, []).append(shape(record))
    return {key: sorted(value) for key, value in out.items()}


def diff(baseline: list[dict], current: list[dict]) -> list[str]:
    """One finding per changed name and type. Pure: no I/O, no exits.

    At most one line per changed record set, never the whole zone: a caller
    reading this should see the change and nothing else."""
    was, now = group(baseline), group(current)
    findings: list[str] = []
    for key in sorted(set(was) | set(now)):
        before, after = was.get(key), now.get(key)
        label = f"{key[0]} {key[1]}"
        if before is None:
            findings.append(f"added {label}: {', '.join(after or [])}")
        elif after is None:
            findings.append(f"removed {label}: {', '.join(before)}")
        elif before != after:
            findings.append(f"changed {label}: {', '.join(before)} -> "
                            f"{', '.join(after)}")
    return findings


def read_jsonl(text: str) -> list[dict] | str:
    """Parse a snapshot file, or return one error string."""
    out: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            return f"line {lineno}: not JSON: {exc}"
        if not isinstance(obj, dict):
            return f"line {lineno}: not a JSON object"
        out.append(obj)
    return out


def write_jsonl(records: list[dict]) -> str:
    """Canonical bytes: fixed key order, no whitespace drift, one per line."""
    return "".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n"
                   for r in records)


def pages_needed(info: dict) -> int:
    """total_pages from result_info, floored at one and capped."""
    try:
        total = int(info.get("total_pages") or 1)
    except (TypeError, ValueError):
        total = 1
    return max(1, min(total, MAX_PAGES))


def call(path: str, token: str) -> dict:
    """One GET, returning the parsed envelope."""
    request = urllib.request.Request(API + path, method="GET")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/json")
    opener = urllib.request.build_opener(SameHostRedirect)
    try:
        with opener.open(request, timeout=TIMEOUT) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise ApiError(4, f"credential rejected ({exc.code}) on {path}")
        raise ApiError(6, f"api {exc.code} on {path}")
    except (urllib.error.URLError, OSError) as exc:
        raise ApiError(2, f"cannot reach the api: {exc}")
    except ValueError:
        raise ApiError(6, f"api returned unparseable json on {path}")
    if not body.get("success"):
        detail = "; ".join(envelope_errors(body))[:160]
        raise ApiError(6, f"api rejected {path}: {detail}")
    return body


def resolve_zone(zone: str, token: str) -> str:
    """The zone id for a zone name."""
    body = call(f"/zones?name={urllib.parse.quote(zone)}", token)
    result = body.get("result") or []
    if not result:
        raise ApiError(2, f"no zone named {zone} is visible to this token")
    return str(result[0].get("id"))


def fetch_records(zone_id: str, token: str) -> list:
    """Every page of the record list, following result_info.total_pages."""
    records: list = []
    page, total = 1, 1
    while page <= total:
        body = call(f"/zones/{zone_id}/dns_records?page={page}"
                    f"&per_page={PER_PAGE}&order=name&direction=asc", token)
        records += body.get("result") or []
        total = pages_needed(body.get("result_info") or {})
        page += 1
    return records


def self_test() -> list[str]:
    """Prove parsing, canonical order, the type filter and the diff. Offline."""
    failures: list[str] = []
    base = read_jsonl(OK_FIXTURE)
    live = read_jsonl(BAD_FIXTURE)
    if isinstance(base, str) or isinstance(live, str):
        return [f"fixture does not parse: {base if isinstance(base, str) else live}"]

    if diff(canonical(base), canonical(base)):
        failures.append("an identical zone reported drift")
    found = diff(canonical(base), canonical(live))
    if len(found) != 3:
        failures.append(f"expected 3 findings, got {found}")
    if not any(f.startswith("changed example.com A") for f in found):
        failures.append("a content change was not reported")
    if not any(f.startswith("added stage.example.com") for f in found):
        failures.append("a new record was not reported")
    if not any(f.startswith("removed example.com TXT") for f in found):
        failures.append("a deleted record was not reported")

    filtered = canonical(base, ["CNAME"])
    if len(filtered) != 1 or filtered[0]["type"] != "CNAME":
        failures.append(f"the type filter kept {filtered}")
    if diff(canonical(base, ["CNAME"]), canonical(live, ["CNAME"])) == []:
        failures.append("the type filter hid a real CNAME change")

    noisy = [{"name": "b.example.com", "type": "A", "content": "203.0.113.1",
              "ttl": 1, "proxied": False, "id": "x", "modified_on": "now",
              "meta": {"auto_added": False}},
             {"name": "a.example.com", "type": "A", "content": "203.0.113.2",
              "ttl": 1, "proxied": False}]
    clean = canonical(noisy)
    if any("id" in r or "meta" in r for r in clean):
        failures.append("vendor bookkeeping fields survived canonicalisation")
    if [r["name"] for r in clean] != ["a.example.com", "b.example.com"]:
        failures.append("canonical order is not deterministic")
    if write_jsonl(clean) != write_jsonl(canonical(list(reversed(noisy)))):
        failures.append("input order changed the written bytes")

    if pages_needed({"total_pages": 4}) != 4:
        failures.append("total_pages was not read")
    if pages_needed({}) != 1 or pages_needed({"total_pages": None}) != 1:
        failures.append("a missing total_pages did not floor at one")
    if pages_needed({"total_pages": 10 ** 6}) != MAX_PAGES:
        failures.append("the page cap did not hold")
    if not isinstance(read_jsonl("{oops}"), str):
        failures.append("a malformed baseline line was not rejected")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zone", help="zone name to snapshot, e.g. example.com")
    ap.add_argument("--out", help="write the canonical JSONL snapshot here")
    ap.add_argument("--baseline", help="committed JSONL snapshot to diff against")
    ap.add_argument("--type", help="comma-separated record types to keep")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit, offline")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=14 failures={len(failures)}")
        return 1 if failures else 0

    if not args.zone:
        print(f"{NAME}: --zone is required", file=sys.stderr)
        return 2
    types = [t.strip().upper() for t in (args.type or "").split(",") if t.strip()]

    baseline: list[dict] = []
    if args.baseline:
        try:
            parsed = read_jsonl(Path(args.baseline).read_text(encoding="utf-8"))
        except OSError as exc:
            print(f"{NAME}: cannot read the baseline: {exc}", file=sys.stderr)
            return 2
        if isinstance(parsed, str):
            print(f"{NAME}: baseline: {parsed}", file=sys.stderr)
            return 2
        baseline = canonical(parsed, types)

    token = os.environ.get(ENV_VAR, "").strip()
    if not token:
        print(f"{NAME}: {ENV_VAR} is not set; the credential is read from the "
              "environment and there is no flag for it", file=sys.stderr)
        return 3

    try:
        zone_id = resolve_zone(args.zone, token)
        records = canonical(fetch_records(zone_id, token), types)
    except ApiError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return exc.code

    if args.out:
        try:
            Path(args.out).write_text(write_jsonl(records), encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write the snapshot: {exc}", file=sys.stderr)
            return 2

    findings = diff(baseline, records) if args.baseline else []
    for finding in findings:
        print(f"{NAME}: {finding}", file=sys.stderr)
    print(f"{NAME}: zone={args.zone} records={len(records)} "
          f"drift={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
