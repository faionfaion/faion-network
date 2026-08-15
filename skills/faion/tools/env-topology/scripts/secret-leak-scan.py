#!/usr/bin/env python3
"""secret-leak-scan.py — find committed credentials in a worktree, its CI
config and, on request, its built output, without ever printing one.

Seven rules, each a key that grants real authority and is routinely pasted
into a repository by accident. Supabase reworked its API keys in 2025: the
legacy `anon` / `service_role` JWTs now run in parallel with
`sb_publishable_…` / `sb_secret_…`, and the legacy pair is deprecated at the
end of 2026. A secret key carries BYPASSRLS — every row-level security policy
in the project is off for its bearer — so a `sb_secret_` or a `service_role`
JWT in a client bundle is a full database read. The JWT rule decodes the
payload and reads the `role` claim rather than pattern-matching, because the
publishable half of the legacy pair is the same shape and is meant to ship.
Cloudflare's newer API tokens carry a scannable `cfut_` prefix.

**It never prints a secret.** A finding is `file:line`, the rule, the
severity and at most the first 8 characters. A leak scanner that echoes the
leak into a log, a CI annotation or an agent transcript has not found the
secret, it has copied it somewhere new — and the transcript is the one place
nobody thinks to rotate.

Offline: no network, no credential of its own, no git subprocess. It reads
the worktree as files. It does NOT read git history — see the card. It also
does not decide whether a key is live; rotate on a finding, do not triage it.

Input:  --root . [--include-build dist] [--out report.md]
Output: one summary line on stdout; one redacted line per finding on stderr.

Exit: 0 nothing at or above --fail-on - 1 a finding at or above it - 2 the
      tool could not run: --root is not a directory, or --out is unwritable.
Zero model calls.
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import os
import re
import sys
from pathlib import Path

NAME = "secret-leak-scan"
SEVERITY = {"low": 0, "med": 1, "high": 2}

MAX_BYTES = 2 * 1024 * 1024
PREFIX_CHARS = 8

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".tox",
             ".mypy_cache", ".pytest_cache", "vendor", ".terraform", ".idea",
             ".gradle", ".cache"}
# Build output: excluded by default because it is generated and enormous, and
# included by name with --include-build because a bundler inlining a secret
# key into client JavaScript is exactly the leak worth catching.
BUILD_DIRS = {"dist", "build", "out", ".next", ".nuxt", ".svelte-kit",
              ".output", ".wrangler", "coverage", "target", "public"}
SKIP_NAMES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "go.sum",
              "poetry.lock", "Cargo.lock", "composer.lock", "uv.lock"}
SKIP_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf",
                 ".woff", ".woff2", ".ttf", ".otf", ".zip", ".gz", ".tar",
                 ".mp4", ".mp3", ".wasm", ".map", ".min.js", ".min.css",
                 ".pyc", ".so", ".dylib", ".exe")

JWT = re.compile(r"eyJ[A-Za-z0-9_-]{6,}\.(eyJ[A-Za-z0-9_-]{6,})\.[A-Za-z0-9_-]{4,}")
SUPABASE_SECRET = re.compile(r"sb_secret_[A-Za-z0-9_-]{8,}")
CLOUDFLARE_TOKEN = re.compile(r"cfut_[A-Za-z0-9_-]{16,}")
PRIVATE_KEY = re.compile(
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY(?: BLOCK)?-----")
ASSIGNMENT = re.compile(
    r"""(?ix) \b ([A-Za-z0-9_.\-]* (?: secret | token | passwd | password |
        api[_-]?key | access[_-]?key | private[_-]?key | auth ) [A-Za-z0-9_.\-]*)
        \s* [:=]{1,2} \s* ['"]? ([A-Za-z0-9+/=_\-.~]{20,}) ['"]? """)
ENV_FILE = re.compile(r"(?:^|/)\.env(?:\.[A-Za-z0-9_-]+)?$")
ENV_TEMPLATE = re.compile(r"\.env\.(?:example|sample|template|dist)$")
# Values that look like a key and are not one. Missing one of these costs a
# false positive; a rule with no placeholder list produces nothing but.
PLACEHOLDERS = ("example", "changeme", "change-me", "placeholder", "your-",
                "your_", "yourkey", "xxxx", "dummy", "sample", "redacted",
                "todo", "fake", "insert", "replace", "process.env",
                "os.environ", "os.getenv", "system.getenv", "secrets.",
                "vars.", "env.", "${", "{{", "<", "…", "...", "*****")


def _b64(payload: dict) -> str:
    """Base64url with the padding stripped, as a JWT segment is written."""
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


# A JWT built here, in the open, from a made-up payload and a signature that
# is a sentence. Nothing about it is a real key, and the self-test asserts
# that no finding ever carries more than PREFIX_CHARS characters of it.
FAKE_SERVICE_ROLE_JWT = ".".join([
    _b64({"alg": "HS256", "typ": "JWT"}),
    _b64({"iss": "supabase", "ref": "fixtureproject", "role": "service_role",
          "iat": 1, "exp": 2}),
    "this-signature-is-a-fixture-and-signs-nothing"])
FAKE_ANON_JWT = ".".join([
    _b64({"alg": "HS256", "typ": "JWT"}),
    _b64({"iss": "supabase", "ref": "fixtureproject", "role": "anon",
          "iat": 1, "exp": 2}),
    "this-signature-is-a-fixture-and-signs-nothing"])

# OK: a project that does everything right. The publishable key is meant to
# ship, the secret is read from the environment, and the template file names
# variables without values.
OK_FIXTURE = {
    "src/client.ts": ('const url = "https://example.com";\n'
                      'const key = "sb_publishable_AbCdEf0123456789";\n'
                      'const admin = process.env.SUPABASE_SERVICE_ROLE_KEY;\n'),
    ".env.example": "SUPABASE_SECRET_KEY=your-key-here\nAPI_TOKEN=\n",
    ".github/workflows/deploy.yml":
        "env:\n  CF_API_TOKEN: ${{ secrets.CF_API_TOKEN }}\n",
}
# BAD: the mistake a caller actually makes. A service-role JWT hardcoded in
# client code, a secret key in CI, a private key checked in, and a real .env
# that .gitignore does not cover.
BAD_FIXTURE = {
    "src/admin.ts": f'const admin = "{FAKE_SERVICE_ROLE_JWT}";\n',
    "src/client.ts": f'const anon = "{FAKE_ANON_JWT}";\n',
    ".github/workflows/deploy.yml":
        "env:\n  SUPABASE_SECRET: sb_secret_AbCdEf0123456789xyz\n"
        "  CF_TOKEN: cfut_9pQr7sTuVwXyZ0123456789abcdef\n",
    "deploy/id_ed25519": "-----BEGIN OPENSSH PRIVATE KEY-----\nb3Blbn\n",
    ".env": "DATABASE_PASSWORD=Hn4Kq2Xv9Lm7Rt3Wz8Yb5Cd1Ef6Gh0Jk\n",
}


def preview(value: str) -> str:
    """The most of a secret this tool will ever emit: the first 8 characters."""
    return value[:PREFIX_CHARS]


def entropy(value: str) -> float:
    """Shannon entropy in bits per character."""
    if not value:
        return 0.0
    return -sum((value.count(c) / len(value)) * math.log2(value.count(c) / len(value))
                for c in set(value))


def jwt_role(segment: str) -> str | None:
    """The `role` claim of a JWT payload segment, or None if it is not a JWT.

    Decoding beats pattern-matching here: `anon` and `service_role` are the
    same shape, and only one of them is a catastrophe."""
    padded = segment + "=" * (-len(segment) % 4)
    try:
        claims = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    if not isinstance(claims, dict):
        return None
    return str(claims.get("role") or "")


def looks_placeholder(value: str) -> bool:
    """True when the value is documentation rather than a credential."""
    low = value.lower()
    if any(mark in low for mark in PLACEHOLDERS):
        return True
    return len(set(value)) <= 4 or bool(re.fullmatch(r"[a-z_.\-]+", value))


def scan_text(path: str, text: str) -> list[dict]:
    """Every finding in one file. Pure, and it keeps no line content.

    The redaction is structural, not a formatting choice made at print time:
    nothing but the rule, the location and `preview()` ever leaves here."""
    out: list[dict] = []

    def hit(line: int, rule: str, severity: str, value: str, note: str) -> None:
        out.append({"file": path, "line": line, "rule": rule,
                    "severity": severity, "starts": preview(value),
                    "note": note})

    for number, line in enumerate(text.splitlines(), 1):
        for match in SUPABASE_SECRET.finditer(line):
            hit(number, "supabase-secret-key", "high", match.group(0),
                "BYPASSRLS: every row-level security policy is off for its bearer")
        for match in CLOUDFLARE_TOKEN.finditer(line):
            hit(number, "cloudflare-api-token", "high", match.group(0),
                "scannable cfut_ prefix; rotate in the Cloudflare dashboard")
        if PRIVATE_KEY.search(line):
            hit(number, "private-key-block", "high", "-----BEG",
                "a private key block is committed; rotate the key pair")
        for match in JWT.finditer(line):
            role = jwt_role(match.group(1))
            if role is None:
                continue
            if role == "service_role":
                hit(number, "supabase-service-role-jwt", "high", match.group(0),
                    "legacy service_role JWT: BYPASSRLS, and deprecated end of 2026")
            elif role == "anon":
                hit(number, "supabase-legacy-anon-jwt", "low", match.group(0),
                    "publishable by design, but the legacy pair retires end of "
                    "2026; migrate to sb_publishable_")
            else:
                hit(number, "jwt-literal", "med", match.group(0),
                    f"a bearer token is committed, role claim {role!r}")
        for name, value in ASSIGNMENT.findall(line):
            if looks_placeholder(value) or entropy(value) < 3.6:
                continue
            if SUPABASE_SECRET.match(value) or CLOUDFLARE_TOKEN.match(value) \
                    or JWT.match(value):
                continue
            hit(number, "high-entropy-assignment", "med", value,
                f"{name} is assigned a literal high-entropy value")
    return out


def ignored_by_git(name: str, gitignore: str) -> bool:
    """True when .gitignore plainly covers this path."""
    base = name.rsplit("/", 1)[-1]
    for raw in gitignore.splitlines():
        rule = raw.strip().rstrip("/")
        if not rule or rule.startswith("#"):
            continue
        rule = rule.lstrip("/")
        if rule in (name, base, ".env*", "*.env", ".env.*", "*"):
            return True
    return False


def check(files: dict[str, str], gitignore: str = "") -> list[dict]:
    """Every finding across a mapping of path to text. Pure: no I/O, no exits.

    The .env rule lives here rather than in scan_text because it is about the
    file's existence and .gitignore, not about anything inside it."""
    findings: list[dict] = []
    for path in sorted(files):
        findings += scan_text(path, files[path])
        if ENV_FILE.search(path) and not ENV_TEMPLATE.search(path) \
                and not ignored_by_git(path, gitignore):
            findings.append({
                "file": path, "line": 0, "rule": "env-file-not-ignored",
                "severity": "med", "starts": "",
                "note": "a real .env file that .gitignore does not cover"})
    findings.sort(key=lambda f: (f["file"], f["line"], f["rule"]))
    return findings


def collect(root: Path, include: set[str]) -> tuple[dict[str, str], int]:
    """Read the worktree. Returns the path-to-text mapping and a skipped count."""
    files: dict[str, str] = {}
    skipped = 0
    for folder, dirnames, filenames in os.walk(root):
        here = Path(folder)
        rel_dir = here.relative_to(root).as_posix()
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in SKIP_DIRS
            and (d not in BUILD_DIRS
                 or (f"{rel_dir}/{d}" if rel_dir != "." else d) in include))
        for filename in sorted(filenames):
            target = here / filename
            rel = target.relative_to(root).as_posix()
            if filename in SKIP_NAMES or rel.endswith(SKIP_SUFFIXES):
                continue
            try:
                if target.is_symlink() or target.stat().st_size > MAX_BYTES:
                    skipped += 1
                    continue
                raw = target.read_bytes()
            except OSError:
                skipped += 1
                continue
            if b"\0" in raw[:4096]:
                skipped += 1
                continue
            files[rel] = raw.decode("utf-8", errors="replace")
    return files, skipped


def report(files: dict[str, str], skipped: int, findings: list[dict]) -> str:
    """The full ledger. Redacted the same way stderr is — this file is an
    artefact a caller may well commit, so it must be safe to commit."""
    lines = [f"# {NAME}", "", f"files: {len(files)}  skipped: {skipped}  "
             f"findings: {len(findings)}", "",
             "| file | line | rule | severity | starts | note |",
             "|---|---|---|---|---|---|"]
    for item in findings:
        lines.append(f"| {item['file']} | {item['line']} | {item['rule']} | "
                     f"{item['severity']} | {item['starts']} | {item['note']} |")
    if not findings:
        lines.append("| none | | | | | |")
    return "\n".join(lines) + "\n"


def self_test() -> list[str]:
    """The rules, the placeholder guard and — the one that matters — the proof
    that no finding carries more than 8 characters of the fixture key."""
    failures: list[str] = []
    clean = check(OK_FIXTURE, gitignore=".env\n")
    if clean:
        failures.append(f"OK fixture produced findings: {clean}")

    found = check(BAD_FIXTURE, gitignore="node_modules\n")
    rules = {f["rule"] for f in found}
    for want in ("supabase-service-role-jwt", "supabase-legacy-anon-jwt",
                 "supabase-secret-key", "cloudflare-api-token",
                 "private-key-block", "env-file-not-ignored",
                 "high-entropy-assignment"):
        if want not in rules:
            failures.append(f"BAD fixture did not fire {want}")

    blob = json.dumps(found) + report(BAD_FIXTURE, 0, found)
    for secret in (FAKE_SERVICE_ROLE_JWT, FAKE_ANON_JWT,
                   "sb_secret_AbCdEf0123456789xyz",
                   "cfut_9pQr7sTuVwXyZ0123456789abcdef",
                   "Hn4Kq2Xv9Lm7Rt3Wz8Yb5Cd1Ef6Gh0Jk"):
        for start in range(len(secret) - PREFIX_CHARS):
            if secret[start:start + PREFIX_CHARS + 1] in blob:
                failures.append("a finding carried more than 8 characters of a "
                                "secret — the whole point of this tool")
                break

    if jwt_role(FAKE_SERVICE_ROLE_JWT.split(".")[1]) != "service_role":
        failures.append("the role claim was not decoded from the payload")
    if jwt_role("not-base64-at-all") is not None:
        failures.append("a non-JWT decoded to a role")
    if check({"a.ts": 'const anon = "sb_publishable_AbCdEf0123456789";\n'}):
        failures.append("a publishable key was reported; it is meant to ship")
    if check({"a.ts": 'API_KEY = "your-secret-key-goes-here-ok"\n'}):
        failures.append("a placeholder was reported as a secret")
    if check({".env": "X=1\n"}, gitignore=".env\n"):
        failures.append("an ignored .env was reported")
    if not check({".env.production": "X=1\n"}, gitignore="node_modules\n"):
        failures.append("an unignored .env.production was not reported")
    if check({".env.example": "X=1\n"}, gitignore="node_modules\n"):
        failures.append("a .env template was reported")
    if entropy("aaaaaaaaaaaaaaaaaaaaaa") > 1.0:
        failures.append("entropy scored a constant string as random")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="worktree to scan (default .)")
    ap.add_argument("--include-build", dest="include_build",
                    help="comma-separated build directories to scan too, "
                         "relative to the root, e.g. dist,.wrangler")
    ap.add_argument("--fail-on", dest="fail_on", default="med",
                    choices=("low", "med", "high"),
                    help="lowest severity that exits 1 (default med)")
    ap.add_argument("--out", help="write the full redacted ledger here")
    ap.add_argument("--json", action="store_true",
                    help="emit the summary line as one line of JSON")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=16 failures={len(failures)}")
        return 1 if failures else 0

    root = Path(args.root)
    if not root.is_dir():
        print(f"{NAME}: --root is not a directory: {args.root}", file=sys.stderr)
        return 2
    include = {p.strip().strip("/") for p in (args.include_build or "").split(",")
               if p.strip()}
    files, skipped = collect(root, include)
    gitignore = files.get(".gitignore", "")
    findings = check(files, gitignore)

    if args.out:
        try:
            Path(args.out).write_text(report(files, skipped, findings),
                                      encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write the ledger: {exc}", file=sys.stderr)
            return 2

    for item in findings:
        print(f"{NAME}: {item['severity']:<4} {item['rule']} "
              f"{item['file']}:{item['line']} starts={item['starts']}",
              file=sys.stderr)
    failing = sum(1 for f in findings
                  if SEVERITY[f["severity"]] >= SEVERITY[args.fail_on])
    if args.json:
        print(json.dumps({"tool": NAME, "root": args.root, "files": len(files),
                          "skipped": skipped, "findings": findings,
                          "failing": failing}, sort_keys=True))
    else:
        print(f"{NAME}: files={len(files)} findings={len(findings)} "
              f"at-or-above-{args.fail_on}={failing}")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
