#!/usr/bin/env python3
"""
Validate tier-playbook markdown files against the spec.

Usage:
    python3 scripts/validate-tier-playbook.py <path1> [<path2> ...]
    python3 scripts/validate-tier-playbook.py --all       # walks skills/faion/playbooks/
    python3 scripts/validate-tier-playbook.py --self-test # synthetic minimal playbook + failure cases

Exit codes:
    0 — all files valid
    1 — one or more files failed validation

Spec: .aidocs/conventions/playbooks/playbook-spec.md (DS1–DS10).
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_ROOT = REPO_ROOT / "skills" / "faion" / "knowledge"
PLAYBOOKS_ROOT = REPO_ROOT / "skills" / "faion" / "playbooks"
TIER_MANIFEST = REPO_ROOT / "skills" / "tier-manifest.json"

TIER_ORDER = {"free": 0, "solo": 1, "pro": 2, "geek": 3}
VALID_STATUS = {"draft", "active", "deprecated"}
REQUIRED_KEYS = {
    "name", "description", "tier", "group",
    "status", "owner", "last_verified", "version",
}
REQUIRED_SECTIONS = [
    "Goal", "Prerequisites", "Steps",
    "Verify", "Troubleshooting", "Next", "References",
]
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{2,40}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[a-z0-9.-]+)?$")
PLACEHOLDER_RE = re.compile(
    r"(?<![a-z])(foo(?:bar)?|example\.com|baz|qux)(?![a-z])"
    r"|\bbar\.(?:py|js|ts|sh|md|html|css|json|yml|yaml)\b"
    r"|\bfoo\.[a-z]+\b",
    re.IGNORECASE,
)
GENERIC_PHRASES = (
    "this methodology explains",
    "covers the basics",
    "introduces the topic",
    "general overview",
    "explains how",
)


@dataclass
class Result:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_frontmatter(text: str) -> dict:
    """Return front-matter dict. Minimal YAML parser."""
    if not text.startswith("---\n"):
        raise ValueError("missing front-matter; file must start with '---'")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("front-matter not closed; expected closing '---'")
    block = text[4:end]
    fm: dict = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid front-matter line: {line!r}")
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip().strip("'\"")
    return fm


def parse_h2_sections(body: str) -> list[tuple[str, str]]:
    """Return list of (heading, content) tuples for `## ` H2 sections in order.

    Skips H2 lines inside fenced code blocks (``` ... ```).
    """
    sections: list[tuple[str, str]] = []
    cur_name = None
    cur_buf: list[str] = []
    in_fence = False
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            if cur_name is not None:
                cur_buf.append(line)
            continue
        if not in_fence and line.startswith("## "):
            if cur_name is not None:
                sections.append((cur_name, "\n".join(cur_buf)))
            cur_name = line[3:].strip()
            cur_buf = []
        else:
            if cur_name is not None:
                cur_buf.append(line)
    if cur_name is not None:
        sections.append((cur_name, "\n".join(cur_buf)))
    return sections


CITATION_LINK_RE = re.compile(
    r"\[(?P<label>[^\]]+)\]\((?P<path>[^)]+)\)\s*[—–-]\s*(?P<rat>.+)"
)
CITATION_TABLE_RE = re.compile(
    r"^\|\s*`?(?P<path>[^`|]+?)`?\s*\|\s*(?P<rat>[^|]+?)\s*\|"
)


def parse_references(content: str) -> list[dict]:
    """Extract citation entries: dicts with `path` and `rationale`."""
    refs: list[dict] = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = CITATION_LINK_RE.search(line)
        if m:
            refs.append({"path": m.group("path").strip(), "rationale": m.group("rat").strip()})
            continue
        if line.startswith("|") and "|" in line[1:]:
            if line.lower().startswith(("|---", "| ---", "|methodology", "| methodology")):
                continue
            m2 = CITATION_TABLE_RE.match(line)
            if m2:
                refs.append({"path": m2.group("path").strip(), "rationale": m2.group("rat").strip()})
    return refs


def normalise_citation_path(raw: str) -> Path:
    """Strip leading ../ + leading 'knowledge/' prefix, resolve under KNOWLEDGE_ROOT."""
    p = raw.split("#", 1)[0].split("?", 1)[0].strip()
    while p.startswith("../"):
        p = p[3:]
    if p.startswith("skills/"):
        p = p[len("skills/"):]
    if p.startswith("faion/"):
        p = p[len("faion/"):]
    if p.startswith("knowledge/"):
        p = p[len("knowledge/"):]
    return KNOWLEDGE_ROOT / p


def citation_tier(raw: str) -> str | None:
    norm = raw
    while norm.startswith("../"):
        norm = norm[3:]
    for prefix in ("skills/", "faion/", "knowledge/"):
        if norm.startswith(prefix):
            norm = norm[len(prefix):]
    parts = norm.split("/")
    if parts and parts[0] in TIER_ORDER:
        return parts[0]
    return None


def is_generic_rationale(rat: str) -> bool:
    low = rat.lower().strip()
    return any(p in low for p in GENERIC_PHRASES)


def validate_file(path: Path) -> Result:
    res = Result(path=path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        res.errors.append(f"cannot read: {exc}")
        return res

    try:
        fm = parse_frontmatter(text)
    except ValueError as exc:
        res.errors.append(f"front-matter: {exc}")
        return res

    missing = REQUIRED_KEYS - set(fm)
    if missing:
        res.errors.append(f"front-matter missing keys: {sorted(missing)}")

    if "tier" in fm and fm["tier"] not in TIER_ORDER:
        res.errors.append(f"invalid tier: {fm['tier']!r}")
    if "status" in fm and fm["status"] not in VALID_STATUS:
        res.errors.append(f"invalid status: {fm['status']!r}")
    if "name" in fm and not SLUG_RE.match(fm["name"]):
        res.errors.append(f"slug regex fail: {fm['name']!r}")
    if "last_verified" in fm and not DATE_RE.match(fm["last_verified"]):
        res.errors.append(f"last_verified not YYYY-MM-DD: {fm['last_verified']!r}")
    if "version" in fm and not SEMVER_RE.match(fm["version"]):
        res.errors.append(f"version not semver: {fm['version']!r}")

    if "name" in fm and path.parent.name != fm["name"]:
        res.errors.append(
            f"folder/slug mismatch: folder={path.parent.name!r} name={fm['name']!r}"
        )
    if "tier" in fm:
        try:
            tier_dir = path.relative_to(PLAYBOOKS_ROOT).parts[0]
            if tier_dir != fm["tier"]:
                res.errors.append(
                    f"path/tier mismatch: path tier={tier_dir!r} fm tier={fm['tier']!r}"
                )
        except ValueError:
            pass

    body = text[text.find("\n---\n", 4) + 5:]
    sections = parse_h2_sections(body)
    section_names = [s[0] for s in sections]
    if section_names != REQUIRED_SECTIONS:
        if set(REQUIRED_SECTIONS) - set(section_names):
            res.errors.append(
                f"missing sections: {sorted(set(REQUIRED_SECTIONS) - set(section_names))}"
            )
        elif section_names != REQUIRED_SECTIONS:
            res.errors.append(
                f"section order/extras differs: got {section_names}"
            )

    sec_map = dict(sections)
    if "Steps" in sec_map and PLACEHOLDER_RE.search(sec_map["Steps"]):
        bad = PLACEHOLDER_RE.findall(sec_map["Steps"])
        res.errors.append(f"placeholder(s) in Steps: {sorted(set(b.lower() for b in bad))}")

    if "References" in sec_map:
        refs = parse_references(sec_map["References"])
        if fm.get("status", "draft") == "active" and not refs:
            res.errors.append("References: ≥1 citation required for status=active")
        playbook_tier = fm.get("tier")
        for ref in refs:
            cite_path = normalise_citation_path(ref["path"])
            if not cite_path.exists():
                res.errors.append(f"citation path missing: {ref['path']}")
            cite_tier = citation_tier(ref["path"])
            if cite_tier and playbook_tier:
                if TIER_ORDER.get(cite_tier, 99) > TIER_ORDER.get(playbook_tier, -1):
                    res.errors.append(
                        f"tier exceeds: citation={cite_tier} playbook={playbook_tier} ({ref['path']})"
                    )
            if len(ref["rationale"]) < 10:
                res.errors.append(f"rationale too short (<10 chars): {ref['path']}")
            if is_generic_rationale(ref["rationale"]):
                res.errors.append(f"generic rationale: {ref['rationale']!r} for {ref['path']}")

    if "Troubleshooting" in sec_map:
        ts = sec_map["Troubleshooting"].strip()
        if fm.get("status", "draft") == "active" and len(ts) < 50:
            res.errors.append("Troubleshooting: ≥1 named pitfall required for status=active")

    return res


def check_cross_tier_dedupe() -> list[str]:
    """Return list of duplicate-slug errors across all tiers."""
    errors: list[str] = []
    if not PLAYBOOKS_ROOT.exists():
        return errors
    seen: dict[str, Path] = {}
    for pb in PLAYBOOKS_ROOT.rglob("playbook.md"):
        slug = pb.parent.name
        if slug in seen:
            errors.append(f"duplicate slug across tiers: {slug} at {seen[slug]} and {pb}")
        else:
            seen[slug] = pb
    return errors


SELF_TEST_VALID = """---
name: hello-world-deploy
description: Deploy a minimal hello-world page to Cloudflare Pages.
tier: free
group: hosting-infra
status: active
owner: tester
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a public hello-world page at https://hello.mydomain.com.

## Prerequisites

- A GitHub account.
- A Cloudflare account.

## Steps

1. Push an `index.html` to a public GitHub repo.
2. Connect the repo to Cloudflare Pages.
3. Click Deploy.

## Verify

`curl https://hello.mydomain.com` returns `<html>...hello world...</html>` with HTTP 200.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| 404 from Pages | Wrong build output dir | Set Pages output to `/` (root) |

## Next

- Add a custom domain.

## References

- [knowledge/free/dev/devtools-developer/dns-fundamentals](../../../knowledge/free/dev/devtools-developer/dns-fundamentals) — clarifies why Cloudflare Pages requires a CNAME record before the custom domain resolves.
"""


def self_test() -> int:
    """Run synthetic playbooks through the validator."""
    fail = 0
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        good = td_path / "playbooks" / "free" / "hosting-infra" / "hello-world-deploy" / "playbook.md"
        good.parent.mkdir(parents=True)
        good.write_text(SELF_TEST_VALID)

        global PLAYBOOKS_ROOT
        old_pb_root = PLAYBOOKS_ROOT
        PLAYBOOKS_ROOT = td_path / "playbooks"

        # We don't have a real KNOWLEDGE_ROOT in tmp, so the citation-path
        # check is the only one that legitimately fails for the synthetic
        # case. Allow exactly that one error.
        res = validate_file(good)
        non_path_errors = [e for e in res.errors if "citation path missing" not in e]
        if non_path_errors:
            print(f"[FAIL] valid playbook unexpectedly errored: {non_path_errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] valid playbook (excluding tmp-citation)")

        bad = good.read_text().replace("tier: free", "tier: solo").replace(
            "name: hello-world-deploy", "name: HelloWorld"
        )
        bad_path = td_path / "playbooks" / "solo" / "hosting-infra" / "HelloWorld" / "playbook.md"
        bad_path.parent.mkdir(parents=True)
        bad_path.write_text(bad)
        res = validate_file(bad_path)
        if not any("slug regex" in e for e in res.errors):
            print(f"[FAIL] expected slug regex error, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] caught slug regex failure")

        no_fm = good.read_text().replace("---\nname:", "name:")
        nofm_path = td_path / "playbooks" / "free" / "hosting-infra" / "no-fm" / "playbook.md"
        nofm_path.parent.mkdir(parents=True)
        nofm_path.write_text(no_fm)
        res = validate_file(nofm_path)
        if not any("front-matter" in e for e in res.errors):
            print(f"[FAIL] expected front-matter error, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] caught missing front-matter")

        broken_section = good.read_text().replace("## Verify", "## verifyy")
        bs_path = td_path / "playbooks" / "free" / "hosting-infra" / "broken-section" / "playbook.md"
        bs_path.parent.mkdir(parents=True)
        bs_path.write_text(broken_section)
        res = validate_file(bs_path)
        if not any("section" in e.lower() for e in res.errors):
            print(f"[FAIL] expected section error, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] caught broken section")

        with_foo = good.read_text().replace("Push an `index.html`", "Push `foo.html`")
        ff_path = td_path / "playbooks" / "free" / "hosting-infra" / "foobar-test" / "playbook.md"
        ff_path.parent.mkdir(parents=True)
        ff_path.write_text(with_foo)
        res = validate_file(ff_path)
        if not any("placeholder" in e for e in res.errors):
            print(f"[FAIL] expected placeholder error, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] caught foo/bar placeholder")

        PLAYBOOKS_ROOT = old_pb_root

    return 1 if fail else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    if args.all:
        if not PLAYBOOKS_ROOT.exists():
            print("playbooks root does not exist yet — nothing to validate", file=sys.stderr)
            return 0
        paths = sorted(PLAYBOOKS_ROOT.rglob("playbook.md"))
    else:
        paths = args.paths
    if not paths:
        parser.error("no paths given (use --all or --self-test)")

    fail = 0
    results: list[Result] = []
    for p in paths:
        r = validate_file(p)
        results.append(r)
        if r.ok:
            print(f"PASS {p}")
        else:
            fail += 1
            print(f"FAIL {p}")
            for e in r.errors:
                print(f"  - {e}")

    dedupe = check_cross_tier_dedupe()
    if dedupe:
        fail += len(dedupe)
        print("FAIL cross-tier dedupe")
        for e in dedupe:
            print(f"  - {e}")

    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
