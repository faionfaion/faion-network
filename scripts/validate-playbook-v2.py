#!/usr/bin/env python3
"""
Validate playbook v2 manifests (playbook.yaml + body.md) against the canonical
shape defined in `.aidocs/brainstorm-2026-05-17/playbook-template.yaml`.

Usage:
    python3 scripts/validate-playbook-v2.py <path/to/playbook.yaml> [more ...]
    python3 scripts/validate-playbook-v2.py --all       # walk skills/faion/playbooks/
    python3 scripts/validate-playbook-v2.py --self-test # synthetic round-trip

Exit codes:
    0 - all files valid
    1 - one or more files failed validation

Validation rules (F-060):
- YAML well-formed.
- Required keys present at top level:
    slug, title, version, status, last_reviewed, maintainers,
    tier_min, complexity, context, intent, scope, success_criteria,
    stages, token_budget_estimate
- success_criteria: list, >=1 entry.
- stages: list, >=1 entry. Each stage has:
    name, intent, tasks, methodologies, outputs, decision_gate
- For each stages[].methodologies[].path: MUST resolve to an existing dir
  under skills/faion/knowledge/<path> OR the methodology slug MUST appear
  in top-level gaps[] (BLOCK policy from memory `pre-sales-content-completion`).
- If status == "published": gaps[] MUST be empty AND every methodology path
  MUST resolve (no gaps tolerated at publish time).
- content_id: 16-hex string equal to first 16 hex chars of SHA-1(slug+version).
- body.md MUST exist as a sibling of playbook.yaml.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_ROOT = REPO_ROOT / "skills" / "faion" / "knowledge"
PLAYBOOKS_ROOT = REPO_ROOT / "skills" / "faion" / "playbooks"

VALID_STATUS = {"draft", "review", "published", "deprecated"}
VALID_TIER = {"free", "solo", "pro", "geek"}
VALID_COMPLEXITY = {"light", "medium", "deep"}
VALID_CONTEXT = {"solo", "team", "outsource"}

REQUIRED_TOP_KEYS = [
    "slug",
    "title",
    "version",
    "status",
    "last_reviewed",
    "maintainers",
    "tier_min",
    "complexity",
    "context",
    "intent",
    "scope",
    "success_criteria",
    "stages",
    "token_budget_estimate",
]

REQUIRED_STAGE_KEYS = [
    "name",
    "intent",
    "tasks",
    "methodologies",
    "outputs",
    "decision_gate",
]


@dataclass
class Result:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def compute_content_id(slug: str, version: str) -> str:
    """16-hex truncation of SHA-1(slug + version)."""
    h = hashlib.sha1(f"{slug}{version}".encode("utf-8")).hexdigest()
    return h[:16]


def resolve_methodology_path(rel_path: str) -> Path:
    """Resolve a methodology path string against KNOWLEDGE_ROOT.

    Accepts either bare `solo/group/skill/name` or
    `knowledge/solo/...` or `faion/knowledge/solo/...`.
    """
    p = rel_path.strip()
    for prefix in ("skills/", "faion/", "knowledge/"):
        while p.startswith(prefix):
            p = p[len(prefix):]
    return KNOWLEDGE_ROOT / p


def validate_file(path: Path) -> Result:
    res = Result(path=path)

    if not path.exists():
        res.errors.append(f"file missing: {path}")
        return res
    if path.name != "playbook.yaml":
        res.errors.append(f"unexpected filename (expected playbook.yaml): {path.name}")

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        res.errors.append(f"cannot read: {exc}")
        return res

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        res.errors.append(f"yaml parse error: {exc}")
        return res

    if not isinstance(data, dict):
        res.errors.append("yaml root is not a mapping")
        return res

    # Required keys
    missing = [k for k in REQUIRED_TOP_KEYS if k not in data]
    if missing:
        res.errors.append(f"missing required keys: {missing}")

    # Type / value checks
    slug = data.get("slug")
    if slug is not None and not isinstance(slug, str):
        res.errors.append(f"slug must be string, got {type(slug).__name__}")

    version = data.get("version")
    if version is not None and not isinstance(version, str):
        res.errors.append(f"version must be string, got {type(version).__name__}")

    status = data.get("status")
    if status is not None and status not in VALID_STATUS:
        res.errors.append(f"invalid status: {status!r} (allowed: {sorted(VALID_STATUS)})")

    tier_min = data.get("tier_min")
    if tier_min is not None and tier_min not in VALID_TIER:
        res.errors.append(f"invalid tier_min: {tier_min!r}")

    complexity = data.get("complexity")
    if complexity is not None and complexity not in VALID_COMPLEXITY:
        res.errors.append(f"invalid complexity: {complexity!r}")

    context = data.get("context")
    if context is not None:
        if not isinstance(context, list):
            res.errors.append("context must be a list")
        else:
            bad_ctx = [c for c in context if c not in VALID_CONTEXT]
            if bad_ctx:
                res.errors.append(f"invalid context values: {bad_ctx}")

    success_criteria = data.get("success_criteria")
    if success_criteria is not None:
        if not isinstance(success_criteria, list):
            res.errors.append("success_criteria must be a list")
        elif len(success_criteria) < 1:
            res.errors.append("success_criteria must have >=1 entry")

    maintainers = data.get("maintainers")
    if maintainers is not None and not isinstance(maintainers, list):
        res.errors.append("maintainers must be a list")

    # Stages
    stages = data.get("stages")
    gaps = data.get("gaps") or []
    if not isinstance(gaps, list):
        res.errors.append("gaps must be a list (or omitted)")
        gaps = []

    gap_slugs = set()
    for g in gaps:
        if isinstance(g, dict) and "methodology_slug" in g:
            gap_slugs.add(g["methodology_slug"])

    if stages is not None:
        if not isinstance(stages, list):
            res.errors.append("stages must be a list")
        elif len(stages) < 1:
            res.errors.append("stages must have >=1 entry")
        else:
            for i, stage in enumerate(stages, start=1):
                if not isinstance(stage, dict):
                    res.errors.append(f"stage {i}: must be a mapping")
                    continue
                stage_missing = [k for k in REQUIRED_STAGE_KEYS if k not in stage]
                if stage_missing:
                    res.errors.append(
                        f"stage {i} ({stage.get('name', '?')!r}): missing keys {stage_missing}"
                    )
                methodologies = stage.get("methodologies") or []
                if not isinstance(methodologies, list):
                    res.errors.append(f"stage {i}: methodologies must be a list")
                    methodologies = []
                for j, m in enumerate(methodologies, start=1):
                    if not isinstance(m, dict):
                        res.errors.append(f"stage {i} methodology {j}: must be a mapping")
                        continue
                    m_slug = m.get("slug")
                    m_path = m.get("path")
                    if not m_slug:
                        res.errors.append(f"stage {i} methodology {j}: missing slug")
                    if not m_path:
                        res.errors.append(f"stage {i} methodology {j}: missing path")
                        continue
                    resolved = resolve_methodology_path(m_path)
                    if not resolved.is_dir():
                        if m_slug not in gap_slugs:
                            res.errors.append(
                                f"stage {i} methodology {j}: path does not resolve "
                                f"and slug not in gaps[]: {m_path}"
                            )

    # BLOCK policy: published status cannot ship with gaps[] non-empty.
    if status == "published":
        if gaps:
            res.errors.append(
                f"status=published but gaps[] is non-empty ({len(gaps)} entries) "
                f"- BLOCK policy: resolve all gaps before publishing"
            )
        if stages and isinstance(stages, list):
            for i, stage in enumerate(stages, start=1):
                if not isinstance(stage, dict):
                    continue
                for j, m in enumerate(stage.get("methodologies") or [], start=1):
                    if not isinstance(m, dict):
                        continue
                    p = m.get("path")
                    if p and not resolve_methodology_path(p).is_dir():
                        res.errors.append(
                            f"status=published but stage {i} methodology {j} "
                            f"path unresolved: {p}"
                        )

    # content_id check
    if "content_id" in data:
        cid = data["content_id"]
        if not isinstance(cid, str):
            res.errors.append(f"content_id must be string, got {type(cid).__name__}")
        elif len(cid) != 16:
            res.errors.append(f"content_id must be 16 hex chars, got len={len(cid)}")
        elif not all(c in "0123456789abcdef" for c in cid.lower()):
            res.errors.append(f"content_id must be hex: {cid!r}")
        elif slug and version:
            expected = compute_content_id(slug, version)
            if cid.lower() != expected:
                res.errors.append(
                    f"content_id mismatch: have {cid!r}, expected {expected!r} "
                    f"(=SHA-1({slug}+{version})[:16])"
                )

    # body.md sibling
    body = path.parent / "body.md"
    if not body.exists():
        res.errors.append(f"missing sibling body.md at {body}")

    return res


SELF_TEST_VALID_BASE = """\
slug: test-playbook
title: "Test playbook"
version: "0.1.0"
status: draft
last_reviewed: 2026-05-17
maintainers: ["tester"]
tier_min: solo
complexity: light
context: [solo]
intent: |
  Test before-state to test after-state.
scope: |
  Tests scope.
success_criteria:
  - "It works"
stages:
  - name: "Only"
    intent: "Does the thing."
    tasks:
      - "Do the thing"
    methodologies:
      - slug: not-yet-built
        path: solo/research/researcher/not-yet-built
        required: true
        tier_gate: solo
    outputs:
      - "Done"
    decision_gate: "Advance if done."
token_budget_estimate: 1000
gaps:
  - methodology_slug: not-yet-built
    expected_tier: solo
    blocks_stage: 1
    note: "stub"
"""


def self_test() -> int:
    fail = 0
    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        pb_dir = td_p / "playbook-x"
        pb_dir.mkdir()
        yaml_path = pb_dir / "playbook.yaml"
        body_path = pb_dir / "body.md"

        # 1: valid (gap-only methodology) — should PASS
        yaml_path.write_text(SELF_TEST_VALID_BASE)
        body_path.write_text("# body\n")
        res = validate_file(yaml_path)
        if not res.ok:
            print(f"[FAIL] expected pass on gap-only methodology, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] valid playbook with gap-only methodology")

        # 2: missing required key (drop intent) — should FAIL
        broken = SELF_TEST_VALID_BASE.replace("intent: |\n  Test before-state to test after-state.\n", "")
        yaml_path.write_text(broken)
        res = validate_file(yaml_path)
        if not any("missing required keys" in e for e in res.errors):
            print(f"[FAIL] expected missing-keys error, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] caught missing required key")

        # 3: unresolved path + empty gaps[] — should FAIL
        no_gaps = SELF_TEST_VALID_BASE.replace(
            "gaps:\n  - methodology_slug: not-yet-built\n    expected_tier: solo\n    blocks_stage: 1\n    note: \"stub\"\n",
            "gaps: []\n",
        )
        yaml_path.write_text(no_gaps)
        res = validate_file(yaml_path)
        if not any("path does not resolve" in e for e in res.errors):
            print(f"[FAIL] expected unresolved-path error, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] caught unresolved-path without gap")

        # 4: status: published + non-empty gaps[] — should FAIL
        pub = SELF_TEST_VALID_BASE.replace("status: draft", "status: published")
        yaml_path.write_text(pub)
        res = validate_file(yaml_path)
        if not any("status=published" in e and "gaps" in e for e in res.errors):
            print(f"[FAIL] expected published+gaps error, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] caught published-with-gaps")

        # 5: missing body.md — should FAIL
        yaml_path.write_text(SELF_TEST_VALID_BASE)
        body_path.unlink()
        res = validate_file(yaml_path)
        if not any("body.md" in e for e in res.errors):
            print(f"[FAIL] expected missing-body error, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] caught missing body.md")
        body_path.write_text("# body\n")

        # 6: content_id mismatch — should FAIL
        wrong_cid = SELF_TEST_VALID_BASE + "content_id: 0000000000000000\n"
        yaml_path.write_text(wrong_cid)
        res = validate_file(yaml_path)
        if not any("content_id" in e for e in res.errors):
            print(f"[FAIL] expected content_id error, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] caught content_id mismatch")

        # 7: content_id correct — should PASS
        right_cid = compute_content_id("test-playbook", "0.1.0")
        ok_cid = SELF_TEST_VALID_BASE + f"content_id: {right_cid}\n"
        yaml_path.write_text(ok_cid)
        res = validate_file(yaml_path)
        if not res.ok:
            print(f"[FAIL] expected pass with valid content_id, got: {res.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] accepted valid content_id")

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
            sys.stderr.write("playbooks root missing\n")
            return 0
        paths = sorted(PLAYBOOKS_ROOT.rglob("playbook.yaml"))
    else:
        paths = args.paths

    if not paths:
        parser.error("no paths given (use --all or --self-test)")

    fail = 0
    for p in paths:
        r = validate_file(p)
        if r.ok:
            sys.stdout.write(f"PASS {p}\n")
        else:
            fail += 1
            sys.stdout.write(f"FAIL {p}\n")
            for e in r.errors:
                sys.stdout.write(f"  - {e}\n")

    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
