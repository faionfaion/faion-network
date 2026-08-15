#!/usr/bin/env python3
"""gha-pin.py — resolve every `uses: owner/repo@tag` to a 40-char commit SHA.

A tag is a mutable pointer. tj-actions/changed-files was compromised in March
2025 by retagging every version tag at a malicious commit (CVE-2025-30066), so
roughly 23,000 repositories pulled the payload without changing a byte of their
own workflow. A SHA cannot be retagged, which is why GitHub's own hardening
guide says pin third-party actions to a full-length commit SHA. Doing that by
hand across a repo is tedious enough that nobody does it; this does it, and
`--check` keeps it done.

The rewrite is deterministic given the same remote state: `owner/repo@v4`
becomes `owner/repo@<sha> # v4`, the tag surviving as the comment so a human
still reads a version. The one clock-dependent input is `--max-age-days`, which
reports a pin whose commit is older than N days; it never changes the bytes
written.

Credential: GITHUB_TOKEN in the environment, never a flag — argv is visible in
`ps` and lands in shell history and agent transcripts. Public repositories need
no scope at all; the token buys the 5,000/hour rate limit instead of 60.

Input:  --dir a directory of workflow YAML
Output: one summary line on stdout; per-action lines on stderr; ledger to --out.

Exit: 0 every action is pinned · 1 an unpinned or unresolvable ref · 2 the tool
      could not run · 3 GITHUB_TOKEN unset · 4 the token was rejected · 6 the
      GitHub API failed, rate limit included.
Zero model calls.
"""
from __future__ import annotations

import argparse
import datetime
import fnmatch
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import namedtuple
from pathlib import Path

NAME = "gha-pin"
API = "https://api.github.com"
ENV_VAR = "GITHUB_TOKEN"
TIMEOUT = 20

Use = namedtuple("Use", "file line prefix value comment")

USES = re.compile(r"^(\s*(?:-\s+)?uses:\s*)(\S+)(\s+#.*)?\s*$")
SHA = re.compile(r"^[0-9a-f]{40}$")

OK_FIXTURE = """\
jobs:
  build:
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: tj-actions/changed-files@v35
      - uses: ./.github/actions/local
      - uses: docker://alpine:3.20
      - name: run
        uses: goreleaser/goreleaser-action@v6
"""

# A trimmed GET /repos/{o}/{r}/commits/{ref} body. Parsing is what --self-test
# exercises; the network is never touched.
COMMIT_FIXTURE = json.dumps({
    "sha": "11bd71901bbe5b1630ceea73d27597364c9af683",
    "commit": {"committer": {"date": "2025-11-01T09:15:00Z"}},
})


def scan(name: str, text: str) -> list:
    """Every `uses:` line in one file, with the pieces needed to rewrite it."""
    found: list = []
    for lineno, line in enumerate(text.splitlines(), 1):
        match = USES.match(line)
        if match is None:
            continue
        value = match.group(2).strip("\"'")
        found.append(Use(name, lineno, match.group(1), value,
                         (match.group(3) or "").strip()))
    return found


def split_ref(value: str) -> tuple[str, str]:
    """`owner/repo/path@ref` -> ('owner/repo', 'ref'). ('', '') when not one."""
    if "@" not in value:
        return "", ""
    target, ref = value.rsplit("@", 1)
    parts = target.split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        return "", ""
    return "/".join(parts[:2]), ref


def skippable(value: str) -> bool:
    """A local action or a container image has no tag to pin."""
    return value.startswith("./") or value.startswith("docker://")


def allowed(repo: str, patterns: list) -> bool:
    """True when the caller has exempted this owner or repo."""
    return any(fnmatch.fnmatch(repo, p) for p in patterns or [])


def rewrite_line(use: Use, sha: str, ref: str) -> str:
    """The replacement line. Idempotent: re-pinning an already pinned line
    with the same SHA reproduces it byte for byte."""
    target = use.value.rsplit("@", 1)[0]
    return f"{use.prefix}{target}@{sha} # {ref}"


def parse_commit(body: str) -> dict:
    """The two fields a pin needs out of a commits response."""
    try:
        data = json.loads(body)
    except ValueError as exc:
        return {"error": f"unreadable response: {exc}", "exit": 6}
    sha = data.get("sha") or ""
    date = (data.get("commit") or {}).get("committer", {}).get("date") or ""
    if not SHA.match(sha):
        return {"error": "response carried no commit sha", "exit": 6}
    return {"sha": sha, "date": date}


def age_days(iso: str, now: datetime.datetime) -> int:
    """Whole days between a commit date and `now`. -1 when unparseable."""
    try:
        when = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return -1
    return (now - when).days


def api_get(path: str, token: str) -> dict:
    """One GET against the GitHub REST API. Never raises, never logs the token."""
    request = urllib.request.Request(
        f"{API}{path}",
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "User-Agent": NAME})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return parse_commit(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        remaining = exc.headers.get("x-ratelimit-remaining", "")
        if exc.code == 404:
            return {"error": "no such ref", "exit": 0}
        if exc.code == 401:
            return {"error": "token rejected", "exit": 4}
        if exc.code in (403, 429) and remaining == "0":
            reset = exc.headers.get("x-ratelimit-reset", "?")
            return {"error": f"rate limit exhausted, resets at {reset}",
                    "exit": 6}
        if exc.code == 403:
            return {"error": "forbidden — token lacks access", "exit": 4}
        return {"error": f"api returned {exc.code}", "exit": 6}
    except (urllib.error.URLError, OSError, ValueError) as exc:
        return {"error": f"network: {exc}", "exit": 2}


def resolve(repo: str, ref: str, token: str, cache: dict) -> dict:
    """Cached `GET /repos/{o}/{r}/commits/{ref}`. One request per distinct ref."""
    key = f"{repo}@{ref}"
    if key not in cache:
        cache[key] = api_get(f"/repos/{repo}/commits/{ref}", token)
    return cache[key]


def apply_edits(text: str, edits: list) -> str:
    """Replace whole lines by number, keeping every other byte and the file's
    own final newline. Pure, so --self-test covers the writing path too."""
    lines = text.splitlines(keepends=True)
    for lineno, replacement in edits:
        ending = "\n" if lines[lineno - 1].endswith("\n") else ""
        lines[lineno - 1] = replacement + ending
    return "".join(lines)


def ledger(rows: list, findings: list) -> str:
    """The written artefact: one line per action, then the findings."""
    lines = [f"# {NAME}", "", f"actions: {len(rows)}", ""]
    lines += [f"- {r}" for r in rows] or ["- none"]
    lines += ["", "## findings", ""]
    lines += [f"- {f}" for f in findings] or ["- none"]
    return "\n".join(lines) + "\n"


def self_test() -> list:
    """Exercise the scanner, the rewriter, the allow globs and the response
    parser against inline fixtures. Opens no socket and needs no credential."""
    failures: list = []
    uses = scan("w.yml", OK_FIXTURE)
    if len(uses) != 5:
        failures.append(f"scanner found {len(uses)} uses, expected 5")
    if uses and uses[0].line != 4:
        failures.append("scanner line number drifted")
    pinned = [u for u in uses if not skippable(u.value)
              and SHA.match(split_ref(u.value)[1])]
    if len(pinned) != 1:
        failures.append(f"{len(pinned)} pinned refs detected, expected 1")
    if [u.value for u in uses if skippable(u.value)] != \
            ["./.github/actions/local", "docker://alpine:3.20"]:
        failures.append("local or docker action not skipped")
    if split_ref("actions/cache/restore@v4") != ("actions/cache", "v4"):
        failures.append("split_ref mishandled a subdirectory action")
    if split_ref("bare") != ("", ""):
        failures.append("split_ref accepted a ref-less value")

    target = next(u for u in uses if u.value.startswith("tj-actions/"))
    sha = "a" * 40
    once = rewrite_line(target, sha, "v35")
    if once.strip() != f"- uses: tj-actions/changed-files@{sha} # v35":
        failures.append(f"rewrite produced {once!r}")
    again = scan("w.yml", once)
    if not again or rewrite_line(again[0], sha, "v35") != once:
        failures.append("rewrite is not idempotent")

    spliced = apply_edits(OK_FIXTURE, [(target.line, once)])
    if spliced.count("\n") != OK_FIXTURE.count("\n") \
            or once + "\n" not in spliced:
        failures.append("apply_edits did not splice one whole line")
    if apply_edits(OK_FIXTURE, []) != OK_FIXTURE:
        failures.append("apply_edits changed a file with no edits")

    if not allowed("myorg/action", ["myorg/*"]):
        failures.append("allow glob did not match its owner")
    if allowed("other/action", ["myorg/*"]):
        failures.append("allow glob matched a foreign owner")

    parsed = parse_commit(COMMIT_FIXTURE)
    if parsed.get("sha") != "11bd71901bbe5b1630ceea73d27597364c9af683":
        failures.append(f"parse_commit returned {parsed}")
    if parse_commit("{}").get("exit") != 6:
        failures.append("parse_commit accepted a body with no sha")
    now = datetime.datetime(2026, 8, 15, tzinfo=datetime.timezone.utc)
    if age_days(parsed.get("date", ""), now) != 286:
        failures.append(f"age_days returned {age_days(parsed['date'], now)}")
    if age_days("not-a-date", now) != -1:
        failures.append("age_days accepted a malformed date")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", help="directory holding workflow YAML")
    ap.add_argument("--check", action="store_true",
                    help="report drift, write nothing, exit 1 when unpinned")
    ap.add_argument("--write", action="store_true",
                    help="rewrite the workflow files in place")
    ap.add_argument("--allow", action="append", metavar="GLOB",
                    help="owner/repo glob left unpinned; repeatable")
    ap.add_argument("--max-age-days", type=int, default=180,
                    dest="max_age_days",
                    help="report a pin older than N days, 0 disables")
    ap.add_argument("--out", help="ledger destination")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=15 failures={len(failures)}")
        return 1 if failures else 0

    if not args.dir:
        print(f"{NAME}: --dir is required", file=sys.stderr)
        return 2
    if args.check and args.write:
        print(f"{NAME}: --check and --write contradict", file=sys.stderr)
        return 2
    source = Path(args.dir)
    if not source.is_dir():
        print(f"{NAME}: not a directory: {source}", file=sys.stderr)
        return 2
    files = sorted(p for p in source.iterdir()
                   if p.is_file() and p.suffix in (".yml", ".yaml"))
    if not files:
        print(f"{NAME}: no .yml or .yaml under {source}", file=sys.stderr)
        return 2
    token = os.environ.get(ENV_VAR, "").strip()
    if not token:
        print(f"{NAME}: {ENV_VAR} is unset — export a token with no scopes "
              "for public repositories", file=sys.stderr)
        return 3

    now = datetime.datetime.now(datetime.timezone.utc)
    cache: dict = {}
    rows: list = []
    findings: list = []
    plans: dict = {}
    unpinned = stale = 0
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"{NAME}: cannot read {path}: {exc}", file=sys.stderr)
            return 2
        for use in scan(path.name, text):
            if skippable(use.value):
                continue
            repo, ref = split_ref(use.value)
            if not repo:
                findings.append(f"{use.file}:{use.line}: unparseable "
                                f"uses: {use.value}")
                continue
            if allowed(repo, args.allow):
                rows.append(f"{use.file}:{use.line} {repo}@{ref} allowed")
                continue
            pinned_already = bool(SHA.match(ref))
            if pinned_already and args.max_age_days <= 0:
                rows.append(f"{use.file}:{use.line} {repo}@{ref[:12]} pinned")
                continue
            answer = resolve(repo, ref, token, cache)
            code = answer.get("exit")
            if code == 2:
                print(f"{NAME}: {repo}@{ref}: {answer['error']}",
                      file=sys.stderr)
                return 2
            if code == 4:
                print(f"{NAME}: {repo}@{ref}: {answer['error']}",
                      file=sys.stderr)
                return 4
            if code == 6:
                print(f"{NAME}: {repo}@{ref}: {answer['error']}",
                      file=sys.stderr)
                return 6
            if "error" in answer:
                findings.append(f"{use.file}:{use.line}: {repo}@{ref}: "
                                f"{answer['error']}")
                continue
            age = age_days(answer.get("date", ""), now)
            if pinned_already:
                if 0 <= args.max_age_days < age:
                    stale += 1
                    findings.append(f"{use.file}:{use.line}: {repo}@"
                                    f"{ref[:12]}: pin is {age} days old")
                rows.append(f"{use.file}:{use.line} {repo}@{ref[:12]} "
                            f"pinned, {age}d")
                continue
            unpinned += 1
            plans.setdefault(path, []).append(
                (use.line, rewrite_line(use, answer["sha"], ref)))
            rows.append(f"{use.file}:{use.line} {repo}@{ref} -> "
                        f"{answer['sha'][:12]}")
            findings.append(f"{use.file}:{use.line}: {repo}@{ref} is a mutable "
                            f"ref; pin to {answer['sha']}")

    written = 0
    if args.write:
        for path, edits in plans.items():
            body = apply_edits(path.read_text(encoding="utf-8"), edits)
            try:
                path.write_text(body, encoding="utf-8")
            except OSError as exc:
                print(f"{NAME}: cannot write {path}: {exc}", file=sys.stderr)
                return 2
            written += len(edits)

    if args.out:
        try:
            Path(args.out).write_text(ledger(rows, findings), encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write ledger: {exc}", file=sys.stderr)
            return 2
    for item in findings:
        print(f"{NAME}: {item}", file=sys.stderr)
    print(f"{NAME}: files={len(files)} actions={len(rows)} "
          f"unpinned={unpinned} rewritten={written} stale={stale} "
          f"requests={len(cache)}")
    if args.check and unpinned:
        return 1
    if any("unparseable" in f or "no such ref" in f for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
