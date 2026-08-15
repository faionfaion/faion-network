#!/usr/bin/env python3
"""api-call.py — one authenticated HTTP transport driven by declarative
per-vendor profiles, returning only the fields the caller selected.

This exists for output compression, not for API access. ClickUp's own MCP
server is capped at 50 calls per 24 hours on the Free plan against roughly
144,000 a day for the REST API, and every call it does answer hands the model
the vendor's whole envelope to pay for token by token. This tool makes the
call, follows the pagination, and returns the three fields `--select` asked
for. A list of 40 issues costs 40 short rows, not 40 vendor objects.

It is deliberately NOT a per-vendor client. A vendor is a JSON-shaped profile
(base URL, auth header shape, pagination strategy, named operations); adding
or repairing one is data, and `--profiles` merges a caller's own file over the
built-ins so a broken operation is fixable without waiting for a release. The
built-ins are embedded here rather than shipped beside this file because a
`.json` never enters the corpus blob and a `.xml` outside `scripts/` is never
materialised by `faion tools sync` — see the pack card for the whole finding.

Input:  --profile and --op, plus --param, --body, --select
Output: one summary line on stdout, selected rows on stdout or --out.

Exit: 0 done - 1 a failed self-test - 2 the tool could not run - 3 the
      credential is absent - 4 the credential was rejected - 5 a mutation
      refused for want of --yes - 6 the vendor API failed, including a 429.
Zero model calls.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

NAME = "api-call"
FALLBACK_ENV = "FAION_TRACKER_TOKEN"
TIMEOUT = 30
RETRIES = 3
RETRY_CAP = 60
STDOUT_ROWS = 20

# Vendors as data. `auth.format` is the exact header value: GitHub takes a
# Bearer prefix, Linear and ClickUp take the raw credential and reject it with
# one. `items` is where the array lives in the response, "" meaning the
# response itself. `mutates` and not the HTTP method is what gates --yes,
# because Linear reads over POST and a method-based gate would demand --yes to
# list issues.
PROFILES: dict = {
    "github": {
        "base": "https://api.github.com",
        "auth": {"header": "Authorization", "format": "Bearer {credential}",
                 "env": "GITHUB_TOKEN"},
        "headers": {"Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"},
        "paginate": "link-header",
        "min_interval": 0.0,
        "ops": {
            "list-issues": {
                "method": "GET", "path": "/repos/{owner}/{repo}/issues",
                "required": ["owner", "repo"],
                "query": {"state": "all", "per_page": "100"},
                "items": "", "mutates": False},
            "get-issue": {
                "method": "GET", "path": "/repos/{owner}/{repo}/issues/{number}",
                "required": ["owner", "repo", "number"],
                "items": None, "paginate": "none", "mutates": False},
            "create-issue": {
                "method": "POST", "path": "/repos/{owner}/{repo}/issues",
                "required": ["owner", "repo"], "body": True,
                "items": None, "paginate": "none", "mutates": True},
            "update-issue": {
                "method": "PATCH", "path": "/repos/{owner}/{repo}/issues/{number}",
                "required": ["owner", "repo", "number"], "body": True,
                "items": None, "paginate": "none", "mutates": True},
        },
    },
    "linear": {
        # One GraphQL endpoint, so one profile covers the whole API and the
        # canned operations below are a convenience over --body, never a limit.
        "base": "https://api.linear.app",
        "auth": {"header": "Authorization", "format": "{credential}",
                 "env": "LINEAR_API_KEY"},
        "headers": {"Content-Type": "application/json"},
        "graphql": True,
        "paginate": "cursor",
        "min_interval": 0.0,
        "ops": {
            "list-issues": {
                "method": "POST", "path": "/graphql", "required": [],
                "graphql": "query($after:String){issues(first:50,after:$after)"
                           "{nodes{id identifier title state{name}}"
                           " pageInfo{hasNextPage endCursor}}}",
                "items": "data.issues.nodes",
                "has_next": "data.issues.pageInfo.hasNextPage",
                "cursor": "data.issues.pageInfo.endCursor",
                "cursor_var": "after", "mutates": False},
            "query": {
                "method": "POST", "path": "/graphql", "required": [],
                "body": True, "items": None, "paginate": "none",
                "mutates": False},
            "create-issue": {
                "method": "POST", "path": "/graphql",
                "required": ["teamId", "title"],
                "graphql": "mutation($teamId:String!,$title:String!,"
                           "$description:String){issueCreate(input:{teamId:$teamId,"
                           "title:$title,description:$description})"
                           "{success issue{id identifier}}}",
                "items": None, "paginate": "none", "mutates": True},
            "update-issue": {
                "method": "POST", "path": "/graphql", "required": ["id"],
                "graphql": "mutation($id:String!,$title:String,$stateId:String)"
                           "{issueUpdate(id:$id,input:{title:$title,"
                           "stateId:$stateId}){success}}",
                "items": None, "paginate": "none", "mutates": True},
        },
    },
    "clickup": {
        # v2 is still the primary API. The credential is a personal token sent
        # as a raw Authorization header with no prefix. 100 requests a minute
        # on Free through Business, hence min_interval. There is no bulk-create
        # endpoint, so a bulk create is N paced POSTs from a JSONL --body.
        "base": "https://api.clickup.com/api/v2",
        "auth": {"header": "Authorization", "format": "{credential}",
                 "env": "CLICKUP_TOKEN"},
        "headers": {"Content-Type": "application/json"},
        "paginate": "page",
        "page_param": "page",
        "page_start": 0,
        "last_page_field": "last_page",
        "min_interval": 0.6,
        "ops": {
            "list-tasks": {
                "method": "GET", "path": "/list/{list_id}/task",
                "required": ["list_id"], "query": {"subtasks": "true"},
                "items": "tasks", "mutates": False},
            "create-task": {
                "method": "POST", "path": "/list/{list_id}/task",
                "required": ["list_id"], "body": True,
                "items": None, "paginate": "none", "mutates": True},
            "update-task": {
                "method": "PUT", "path": "/task/{task_id}",
                "required": ["task_id"], "body": True,
                "items": None, "paginate": "none", "mutates": True},
        },
    },
}

# Fixtures for --self-test. No network, no credential. OK is a GitHub issues
# page as the API returns it; BAD is the mistake a caller actually makes —
# a --param the operation's path needs and the caller did not pass.
OK_FIXTURE = (
    '[{"number": 41, "title": "TASK-049-001 spec deltas", "state": "open",'
    ' "labels": [{"name": "sdd"}]},'
    ' {"number": 42, "title": "TASK-049-002 bdd cli", "state": "closed",'
    ' "labels": []}]'
)
BAD_FIXTURE = '{"owner": "faionfaion"}'


class ApiError(Exception):
    """A failed call, carrying the exit code the caller should return."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


class SameHostRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse a redirect that leaves the API host.

    The request carries the credential in a header and urllib would replay
    that header at whatever host the Location line names."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        here = urllib.parse.urlsplit(req.full_url).hostname
        there = urllib.parse.urlsplit(newurl).hostname
        if here != there:
            return None
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def load_profiles(path: str | None) -> dict:
    """The built-in profiles with a caller's file merged over them, vendor by
    vendor. Raises ValueError on a file that is not an object of profiles."""
    merged = json.loads(json.dumps(PROFILES))
    if not path:
        return merged
    override = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(override, dict):
        raise ValueError("a profiles file is a JSON object of vendor to profile")
    for vendor, profile in override.items():
        if not isinstance(profile, dict):
            raise ValueError(f"profile {vendor!r} is not an object")
        base = merged.get(vendor, {})
        ops = dict(base.get("ops") or {})
        ops.update(profile.get("ops") or {})
        base.update({k: v for k, v in profile.items() if k != "ops"})
        base["ops"] = ops
        merged[vendor] = base
    return merged


def parse_params(pairs: list[str]) -> dict | str:
    """`k=v` strings to a dict, or one error string."""
    out: dict = {}
    for pair in pairs or []:
        if "=" not in pair:
            return f"--param {pair!r} is not k=v"
        key, value = pair.split("=", 1)
        if not key.strip():
            return f"--param {pair!r} has an empty key"
        out[key.strip()] = value
    return out


def resolve_op(profiles: dict, vendor: str, op_name: str) -> tuple[dict, dict]:
    """The profile and the operation, or an ApiError-free ValueError."""
    profile = profiles.get(vendor)
    if not profile:
        raise ValueError(f"no profile {vendor!r}; known: "
                         f"{', '.join(sorted(profiles))}")
    op = (profile.get("ops") or {}).get(op_name)
    if not op:
        raise ValueError(f"profile {vendor!r} has no operation {op_name!r}; "
                         f"known: {', '.join(sorted(profile.get('ops') or {}))}")
    return profile, op


def missing_params(op: dict, params: dict) -> list[str]:
    """Required params the caller did not pass. Pure."""
    return [k for k in op.get("required") or [] if k not in params]


def build_url(profile: dict, op: dict, params: dict) -> str:
    """Path template filled from params, everything left over as query."""
    path = op.get("path", "")
    used = set()
    for key, value in sorted(params.items()):
        token = "{" + key + "}"
        if token in path:
            path = path.replace(token, urllib.parse.quote(str(value), safe=""))
            used.add(key)
    query = dict(op.get("query") or {})
    if not (op.get("graphql") or op.get("body")):
        for key in sorted(set(params) - used):
            query[key] = params[key]
    url = profile.get("base", "") + path
    if query:
        url += "?" + urllib.parse.urlencode(sorted(query.items()))
    return url


def auth_env(profile: dict) -> str:
    """The environment variable this profile reads the credential from."""
    return (profile.get("auth") or {}).get("env") or FALLBACK_ENV


def auth_header(profile: dict, credential: str) -> tuple[str, str]:
    """Header name and value. Linear and ClickUp reject a Bearer prefix."""
    auth = profile.get("auth") or {}
    header = auth.get("header") or "Authorization"
    shape = auth.get("format") or "{credential}"
    return header, shape.replace("{credential}", credential)


def dig(obj, path: str | None):
    """The value at a dotted path. An empty path is the object itself."""
    if not path:
        return obj
    cur = obj
    for seg in path.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(seg)
    return cur


def extract_items(body, items_path: str | None) -> list:
    """The response's item array, whatever shape the vendor wrapped it in."""
    if items_path is None:
        return [body] if body is not None else []
    value = dig(body, items_path)
    if isinstance(value, list):
        return value
    return [] if value is None else [value]


def resolve_multi(root, path: str) -> list:
    """Every value a select path reaches. `[]` explodes a list in place."""
    cursors = [root]
    for seg in path.split("."):
        explode = seg.endswith("[]")
        name = seg[:-2] if explode else seg
        nxt = []
        for cur in cursors:
            value = cur.get(name) if isinstance(cur, dict) else None
            if explode and isinstance(value, list):
                nxt.extend(value)
            else:
                nxt.append(value)
        cursors = nxt
    return cursors


def shape(items: list, expr: str | None) -> list:
    """The rows the caller asked for. No --select keeps the items whole.

    This is the point of the tool: `items[].title,items[].state` turns a
    vendor envelope into two named columns, and nothing else is paid for."""
    if not expr:
        return list(items)
    root = {"items": items}
    columns: list[tuple[str, list]] = []
    seen: set[str] = set()
    for path in [p.strip() for p in expr.split(",") if p.strip()]:
        key = path.split(".")[-1].replace("[]", "") or "items"
        if key in seen:
            key = path.replace("[]", "")
        seen.add(key)
        columns.append((key, resolve_multi(root, path)))
    if not columns:
        return []
    width = max(len(values) for _, values in columns)
    if len(columns) == 1 and width and all(
            isinstance(v, dict) for v in columns[0][1]):
        return list(columns[0][1])
    rows = []
    for index in range(width):
        row = {}
        for key, values in columns:
            if len(values) == width:
                row[key] = values[index]
            else:
                row[key] = values[0] if len(values) == 1 else None
        rows.append(row)
    return rows


def next_link(header: str | None) -> str | None:
    """The `rel="next"` URL of a Link header, or None."""
    for part in (header or "").split(","):
        bits = part.split(";")
        if len(bits) < 2:
            continue
        url = bits[0].strip().strip("<>")
        for attr in bits[1:]:
            if attr.strip().replace(" ", "").replace("'", '"') == 'rel="next"':
                return url
    return None


def retry_after(value: str | None, attempt: int) -> float:
    """Seconds to wait before a retry. Honours Retry-After, caps the wait,
    and falls back to a fixed backoff rather than a random one."""
    if value:
        try:
            return max(0.0, min(float(value.strip()), float(RETRY_CAP)))
        except ValueError:
            pass
    return float(min(2 ** attempt, RETRY_CAP))


def same_host(url: str, base: str) -> bool:
    """A paginated `next` URL must not walk the credential off the host."""
    return urllib.parse.urlsplit(url).hostname == \
        urllib.parse.urlsplit(base).hostname


def graphql_errors(body) -> list[str]:
    """A GraphQL endpoint answers 200 and puts the failure in the body."""
    out = []
    if isinstance(body, dict):
        for item in body.get("errors") or []:
            if isinstance(item, dict):
                out.append(str(item.get("message", ""))[:120])
            else:
                out.append(str(item)[:120])
    return out


def load_payloads(path: str | None) -> list:
    """The --body file as a list of payloads. A JSONL file or a JSON array is
    N payloads, which is how a bulk create happens where no bulk endpoint
    exists. Raises ValueError."""
    if not path:
        return []
    text = Path(path).read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("the body file is empty")
    try:
        whole = json.loads(text)
    except json.JSONDecodeError:
        whole = None
    if isinstance(whole, list):
        return whole
    if isinstance(whole, dict):
        return [whole]
    if whole is not None:
        raise ValueError("a body is a JSON object, or an array of them")
    out = []
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"body line {lineno}: not JSON: {exc}")
    if not out:
        raise ValueError("the body file holds no payload")
    return out


def request_body(op: dict, params: dict, payload) -> bytes | None:
    """The encoded request body: a GraphQL document plus variables, or the
    caller's own payload, or nothing."""
    document = op.get("graphql")
    if document:
        variables = dict(params)
        if isinstance(payload, dict):
            variables.update(payload)
        return json.dumps({"query": document, "variables": variables},
                          sort_keys=True).encode("utf-8")
    if payload is None:
        return None
    return json.dumps(payload, sort_keys=True).encode("utf-8")


def describe(method: str, url: str, body: bytes | None) -> str:
    """The change set line. Never carries the credential — the body is the
    caller's own payload and the header is not printed."""
    shown = "" if body is None else body.decode("utf-8", "replace")[:400]
    return f"{method} {url}" + (f" body={shown}" if shown else "")


def call(url: str, method: str, profile: dict, credential: str,
         body: bytes | None) -> tuple[dict | list | None, dict]:
    """One request, retried on 429. Returns the parsed body and the headers."""
    request = urllib.request.Request(url, data=body, method=method)
    header, value = auth_header(profile, credential)
    request.add_header(header, value)
    request.add_header("Accept", "application/json")
    for key, val in sorted((profile.get("headers") or {}).items()):
        request.add_header(key, val)
    if body is not None:
        request.add_header("Content-Type", "application/json")
    opener = urllib.request.build_opener(SameHostRedirect)
    for attempt in range(RETRIES):
        try:
            with opener.open(request, timeout=TIMEOUT) as response:
                raw = response.read().decode("utf-8")
                headers = {k.lower(): v for k, v in response.headers.items()}
            return (json.loads(raw) if raw.strip() else None), headers
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < RETRIES - 1:
                time.sleep(retry_after(exc.headers.get("Retry-After"), attempt))
                continue
            if exc.code in (401, 403):
                raise ApiError(4, f"credential rejected ({exc.code})")
            raise ApiError(6, f"api {exc.code} on {method} {url}")
        except (urllib.error.URLError, OSError) as exc:
            raise ApiError(2, f"cannot reach the api: {exc}")
        except ValueError:
            raise ApiError(6, f"api returned unparseable json on {url}")
    raise ApiError(6, "rate limited after every retry")


def paginate(url: str, method: str, profile: dict, op: dict, params: dict,
             credential: str, payload, pages: int) -> tuple[list, int]:
    """Follow the profile's pagination strategy. Returns items and requests."""
    strategy = op.get("paginate") or profile.get("paginate") or "none"
    interval = float(profile.get("min_interval") or 0.0)
    items: list = []
    requests = 0
    cursor = None
    page = int(profile.get("page_start", 1))
    while requests < max(1, pages):
        target = url
        body = request_body(op, params, payload)
        if strategy == "cursor" and cursor:
            variables = dict(params)
            variables[op.get("cursor_var") or "after"] = cursor
            body = request_body(op, variables, payload)
        if strategy == "page":
            joiner = "&" if "?" in url else "?"
            target = f"{url}{joiner}{profile.get('page_param', 'page')}={page}"
        if requests and interval:
            time.sleep(interval)
        parsed, headers = call(target, method, profile, credential, body)
        requests += 1
        if op.get("graphql") or profile.get("graphql"):
            problems = graphql_errors(parsed)
            if problems:
                raise ApiError(6, "graphql: " + "; ".join(problems)[:160])
        batch = extract_items(parsed, op.get("items"))
        items += batch
        if strategy == "link-header":
            nxt = next_link(headers.get("link"))
            if not nxt or not same_host(nxt, profile.get("base", "")):
                break
            url = nxt
        elif strategy == "cursor":
            if not dig(parsed, op.get("has_next")):
                break
            cursor = dig(parsed, op.get("cursor"))
            if not cursor:
                break
        elif strategy == "page":
            if not batch or dig(parsed, profile.get("last_page_field")) is True:
                break
            page += 1
        else:
            break
    return items, requests


def self_test() -> list[str]:
    """Prove profile loading, param validation, URL building, the auth header
    shape, pagination parsing and the select expression. No network call."""
    failures: list[str] = []
    profiles = load_profiles(None)
    issues = json.loads(OK_FIXTURE)

    try:
        profile, op = resolve_op(profiles, "github", "list-issues")
    except ValueError as exc:
        return [f"built-in profile does not resolve: {exc}"]
    if missing_params(op, json.loads(BAD_FIXTURE)) != ["repo"]:
        failures.append("a missing required param was not reported")
    if missing_params(op, {"owner": "o", "repo": "r"}):
        failures.append("a complete param set was reported incomplete")

    url = build_url(profile, op, {"owner": "faionfaion", "repo": "faion-net"})
    if "/repos/faionfaion/faion-net/issues" not in url or "state=all" not in url:
        failures.append(f"github url built wrong: {url}")
    if auth_header(profile, "abc") != ("Authorization", "Bearer abc"):
        failures.append("github lost its Bearer prefix")
    for vendor in ("linear", "clickup"):
        if auth_header(profiles[vendor], "abc") != ("Authorization", "abc"):
            failures.append(f"{vendor} must send the credential with no prefix")
    if auth_env(profiles["clickup"]) != "CLICKUP_TOKEN":
        failures.append("clickup reads the wrong environment variable")

    rows = shape(issues, "items[].number,items[].title")
    if rows != [{"number": 41, "title": "TASK-049-001 spec deltas"},
                {"number": 42, "title": "TASK-049-002 bdd cli"}]:
        failures.append(f"select shaped the wrong rows: {rows}")
    if shape(issues, "items[].labels[].name") != [{"name": "sdd"}]:
        failures.append("a nested explode did not flatten")
    if len(shape(issues, None)) != 2:
        failures.append("no select must keep the items whole")

    header = '<https://api.github.com/x?page=2>; rel="next", <https://api.github.com/x?page=9>; rel="last"'
    if next_link(header) != "https://api.github.com/x?page=2":
        failures.append("the next link was not parsed")
    if next_link('<https://api.github.com/x>; rel="last"') is not None:
        failures.append("a header with no next yielded one")
    if not same_host("https://api.github.com/x", "https://api.github.com"):
        failures.append("same-host check rejected its own host")
    if same_host("https://evil.example.com/x", "https://api.github.com"):
        failures.append("pagination would follow a link off the host")

    if retry_after("30", 0) != 30.0 or retry_after(None, 3) != 8.0:
        failures.append("Retry-After was not honoured")
    if retry_after("99999", 0) != float(RETRY_CAP):
        failures.append("Retry-After was not capped")

    linear = profiles["linear"]["ops"]["list-issues"]
    page = {"data": {"issues": {"nodes": [{"id": "1"}], "pageInfo": {
        "hasNextPage": True, "endCursor": "cur"}}}}
    if extract_items(page, linear["items"]) != [{"id": "1"}]:
        failures.append("the graphql item path did not resolve")
    if dig(page, linear["cursor"]) != "cur":
        failures.append("the cursor path did not resolve")
    if not graphql_errors({"errors": [{"message": "bad"}]}):
        failures.append("a 200 graphql error was not detected")

    if profiles["clickup"]["ops"]["create-task"]["mutates"] is not True:
        failures.append("a writing operation is not marked mutating")
    if profiles["linear"]["ops"]["list-issues"]["mutates"] is not False:
        failures.append("a POST read was marked mutating")

    merged = load_profiles(None)
    merged["github"]["ops"]["list-issues"]["query"]["state"] = "open"
    if load_profiles(None)["github"]["ops"]["list-issues"]["query"]["state"] \
            != "all":
        failures.append("load_profiles handed out a shared mutable default")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", help="vendor profile: github, linear, clickup")
    ap.add_argument("--op", help="named operation within the profile")
    ap.add_argument("--param", action="append", default=[],
                    help="k=v, repeatable: path variables and query keys")
    ap.add_argument("--body", help="JSON or JSONL payload file for a write")
    ap.add_argument("--select", help="comma-separated paths, e.g. items[].title")
    ap.add_argument("--out", help="write the selected rows here as JSONL")
    ap.add_argument("--profiles", help="JSON file merged over the built-ins")
    ap.add_argument("--pages", type=int, default=5,
                    help="maximum pages to fetch (default 5)")
    ap.add_argument("--max", type=int, default=25,
                    help="maximum payloads a write may send (default 25)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the request and make no call")
    ap.add_argument("--yes", action="store_true",
                    help="actually perform a mutating operation")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit, offline")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=24 failures={len(failures)}")
        return 1 if failures else 0

    if not args.profile or not args.op:
        print(f"{NAME}: --profile and --op are required", file=sys.stderr)
        return 2
    try:
        profiles = load_profiles(args.profiles)
        profile, op = resolve_op(profiles, args.profile, args.op)
        payloads = load_payloads(args.body)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return 2
    params = parse_params(args.param)
    if isinstance(params, str):
        print(f"{NAME}: {params}", file=sys.stderr)
        return 2
    absent = missing_params(op, params)
    if absent:
        print(f"{NAME}: {args.op} needs --param for: {', '.join(absent)}",
              file=sys.stderr)
        return 2
    if op.get("body") and not payloads:
        print(f"{NAME}: {args.op} needs --body", file=sys.stderr)
        return 2

    method = op.get("method", "GET")
    url = build_url(profile, op, params)
    mutating = bool(op.get("mutates"))
    plan = [describe(method, url, request_body(op, params, p))
            for p in (payloads or [None])]
    if mutating and len(plan) > max(1, args.max):
        print(f"{NAME}: {len(plan)} payloads is over the --max cap of "
              f"{args.max}", file=sys.stderr)
        return 2
    if mutating or args.dry_run:
        for line in plan:
            print(f"{NAME}: would send: {line}", file=sys.stderr)
    if args.dry_run:
        print(f"{NAME}: profile={args.profile} op={args.op} planned="
              f"{len(plan)} requests=0 (dry run)")
        return 0
    if mutating and not args.yes:
        print(f"{NAME}: {args.op} writes to {args.profile} and --yes was not "
              "given", file=sys.stderr)
        return 5

    env_var = auth_env(profile)
    credential = (os.environ.get(env_var)
                  or os.environ.get(FALLBACK_ENV) or "").strip()
    if not credential:
        print(f"{NAME}: neither {env_var} nor {FALLBACK_ENV} is set; the "
              "credential is read from the environment and there is no flag "
              "for it", file=sys.stderr)
        return 3

    items: list = []
    requests = 0
    try:
        if mutating:
            interval = float(profile.get("min_interval") or 0.0)
            for index, payload in enumerate(payloads):
                if index and interval:
                    time.sleep(interval)
                parsed, _ = call(url, method, profile, credential,
                                 request_body(op, params, payload))
                requests += 1
                if op.get("graphql") or profile.get("graphql"):
                    problems = graphql_errors(parsed)
                    if problems:
                        raise ApiError(6, "graphql: " + "; ".join(problems)[:160])
                items += extract_items(parsed, op.get("items"))
        else:
            items, requests = paginate(url, method, profile, op, params,
                                       credential, payloads[0] if payloads
                                       else None, args.pages)
    except ApiError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return exc.code

    rows = shape(items, args.select)
    if args.out:
        try:
            Path(args.out).write_text(
                "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows),
                encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write the rows: {exc}", file=sys.stderr)
            return 2
    elif args.select:
        for row in rows[:STDOUT_ROWS]:
            print(json.dumps(row, sort_keys=True))
        if len(rows) > STDOUT_ROWS:
            print(f"{NAME}: {len(rows) - STDOUT_ROWS} more rows withheld; "
                  "pass --out for all of them", file=sys.stderr)
    print(f"{NAME}: profile={args.profile} op={args.op} requests={requests} "
          f"items={len(items)} rows={len(rows)} -> {args.out or 'stdout'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
