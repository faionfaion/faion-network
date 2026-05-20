#!/usr/bin/env python3
"""
Validate a workflow folder's AGENTS.md against the v2 envelope schema (F-061).

Usage:
    python3 scripts/validate-workflow-v2.py <path/to/workflow-dir-or-AGENTS.md> [...]
    python3 scripts/validate-workflow-v2.py --all       # walks skills/faion/workflows/
    python3 scripts/validate-workflow-v2.py --self-test # synthetic pass + failure cases

Exit codes:
    0 — every input is valid
    1 — at least one input fails validation

Envelope (v2):
    - AGENTS.md must be ≤80 lines (inclusive of trailing newline).
    - Frontmatter required keys: status, audience, owner, last_verified,
      version, applies_to, content_id (16-hex), success_criteria (list, ≥1).
    - Required H1 + sections: "# <Workflow name>", "## Summary", "## Why",
      "## When To Use", "## When NOT To Use", "## Content".
    - "## Content" must contain a markdown table whose first column lists
      every `content/*.xml` file present on disk under the workflow.
    - Conversely, every `content/*.xml` row in the table must resolve to a
      real file on disk.

Notes:
    - Only files directly under `content/` (non-recursive, .xml suffix) are
      compared. Files like `decisions.xml`, `templates/*` are out of scope.
    - YAML parsing is intentionally minimal so the script has zero deps.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_ROOT = REPO_ROOT / "skills" / "faion" / "workflows"

MAX_LINES = 80

REQUIRED_KEYS = (
    "status",
    "audience",
    "owner",
    "last_verified",
    "version",
    "applies_to",
    "content_id",
    "success_criteria",
)
REQUIRED_SECTIONS = (
    "Summary",
    "Why",
    "When To Use",
    "When NOT To Use",
    "Content",
)

CONTENT_ID_RE = re.compile(r"^[0-9a-f]{16}$")
H1_RE = re.compile(r"^#\s+\S+")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
CONTENT_PATH_RE = re.compile(r"`(content/[^`]+\.xml)`")


@dataclass
class Report:
    path: Path
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def resolve_agents_md(target: Path) -> Path:
    """Accept either workflow dir or AGENTS.md path; return AGENTS.md path."""
    if target.is_dir():
        return target / "AGENTS.md"
    return target


def parse_frontmatter(text: str) -> tuple[dict, list[str]]:
    """Return (frontmatter dict, errors). Minimal YAML — no nested mappings."""
    errors: list[str] = []
    if not text.startswith("---\n"):
        errors.append("missing frontmatter: file must start with '---'")
        return {}, errors
    end = text.find("\n---\n", 4)
    if end == -1:
        errors.append("missing frontmatter close: '---' on its own line")
        return {}, errors
    body = text[4:end]
    fm: dict = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    for raw in body.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        stripped = line.lstrip()
        if stripped.startswith("- "):
            if current_list is None:
                errors.append(f"orphan list item outside a key: {line!r}")
                continue
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ":" not in line:
            errors.append(f"malformed frontmatter line: {line!r}")
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not value:
            # value is a list on following lines
            current_key = key
            current_list = []
            fm[key] = current_list
        else:
            fm[key] = value.strip('"').strip("'")
            current_key = key
            current_list = None
    return fm, errors


def parse_sections(text: str, fm_end_offset: int) -> tuple[list[str], dict[str, str]]:
    """Return (ordered H2 names, name → section body) for body after frontmatter."""
    body = text[fm_end_offset:]
    lines = body.splitlines()
    names: list[str] = []
    bodies: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        m = H2_RE.match(line)
        if m:
            current = m.group(1).strip()
            names.append(current)
            bodies[current] = []
            continue
        if current is not None:
            bodies[current].append(line)
    return names, {k: "\n".join(v) for k, v in bodies.items()}


def extract_content_files_from_table(content_section: str) -> list[str]:
    """Pull every `content/*.xml` filename referenced in the Content section."""
    matches = CONTENT_PATH_RE.findall(content_section)
    return matches


def validate_file(path: Path) -> Report:
    rpt = Report(path=path)
    if not path.is_file():
        rpt.errors.append(f"file not found: {path}")
        return rpt

    text = path.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    if line_count > MAX_LINES:
        rpt.errors.append(
            f"AGENTS.md is {line_count} lines, must be ≤{MAX_LINES}"
        )

    # Frontmatter
    fm, fm_errors = parse_frontmatter(text)
    rpt.errors.extend(fm_errors)
    fm_end = 0
    if text.startswith("---\n"):
        idx = text.find("\n---\n", 4)
        if idx != -1:
            fm_end = idx + len("\n---\n")

    for key in REQUIRED_KEYS:
        if key not in fm:
            rpt.errors.append(f"frontmatter missing required key: {key}")

    content_id = fm.get("content_id")
    if isinstance(content_id, str) and not CONTENT_ID_RE.match(content_id):
        rpt.errors.append(
            f"content_id must be 16-hex lowercase, got {content_id!r}"
        )
    elif isinstance(content_id, list):
        rpt.errors.append("content_id must be a scalar 16-hex string, not a list")

    sc = fm.get("success_criteria")
    if sc is not None:
        if not isinstance(sc, list):
            rpt.errors.append("success_criteria must be a list")
        elif len(sc) < 1:
            rpt.errors.append("success_criteria must have ≥1 entry")
        else:
            for i, item in enumerate(sc):
                if not isinstance(item, str) or not item.strip():
                    rpt.errors.append(
                        f"success_criteria[{i}] must be a non-empty string"
                    )

    # H1
    after_fm = text[fm_end:]
    first_nonempty = next(
        (ln for ln in after_fm.splitlines() if ln.strip()), ""
    )
    if not H1_RE.match(first_nonempty):
        rpt.errors.append(
            "missing H1 header (line after frontmatter must be '# <Workflow name>')"
        )

    # Required H2 sections
    names, bodies = parse_sections(text, fm_end)
    for required in REQUIRED_SECTIONS:
        if required not in names:
            rpt.errors.append(f"missing required section: ## {required}")

    # Content table ↔ filesystem
    content_dir = path.parent / "content"
    on_disk: set[str] = set()
    if content_dir.is_dir():
        on_disk = {
            f"content/{p.name}"
            for p in content_dir.iterdir()
            if p.is_file() and p.suffix == ".xml"
        }
    table_paths: set[str] = set()
    if "Content" in bodies:
        table_paths = set(extract_content_files_from_table(bodies["Content"]))

    missing_on_disk = sorted(table_paths - on_disk)
    missing_in_table = sorted(on_disk - table_paths)
    for p in missing_on_disk:
        rpt.errors.append(
            f"Content table references {p} but the file does not exist"
        )
    for p in missing_in_table:
        rpt.errors.append(
            f"{p} exists on disk but is missing from the Content table"
        )

    return rpt


def collect_targets(paths: list[str], walk_all: bool) -> list[Path]:
    targets: list[Path] = []
    if walk_all:
        if not WORKFLOWS_ROOT.is_dir():
            return []
        for child in sorted(WORKFLOWS_ROOT.iterdir()):
            if not child.is_dir():
                continue
            agents = child / "AGENTS.md"
            content_dir = child / "content"
            # A workflow folder must have BOTH AGENTS.md and content/.
            # Sibling dirs like `adapters/` are not workflows and are skipped.
            if agents.is_file() and content_dir.is_dir():
                targets.append(agents)
        return targets
    for raw in paths:
        targets.append(resolve_agents_md(Path(raw).resolve()))
    return targets


def render_report(rpt: Report) -> str:
    status = "OK " if rpt.ok else "FAIL"
    head = f"[{status}] {rpt.path}"
    if rpt.ok:
        return head
    lines = [head] + [f"    - {e}" for e in rpt.errors]
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    if args.self_test:
        return _self_test()

    targets = collect_targets(args.paths, args.all)
    if not targets:
        sys.stderr.write("no targets provided; pass paths or --all\n")
        return 1

    failures = 0
    for tgt in targets:
        rpt = validate_file(tgt)
        sys.stdout.write(render_report(rpt) + "\n")
        if not rpt.ok:
            failures += 1
    return 1 if failures else 0


def _self_test() -> int:
    """Smoke check: a synthetic minimal-valid file passes, broken ones fail."""
    valid = (
        "---\n"
        "status: active\n"
        "audience: both\n"
        "owner: ruslan\n"
        "last_verified: 2026-05-20\n"
        "version: 2.0.0\n"
        "applies_to: any\n"
        "content_id: 0123456789abcdef\n"
        "success_criteria:\n"
        "  - phase outputs match the contract\n"
        "---\n"
        "\n"
        "# Self Test Workflow\n"
        "\n"
        "## Summary\n\nOne line.\n"
        "## Why\n\nReason.\n"
        "## When To Use\n\n- case.\n"
        "## When NOT To Use\n\n- not.\n"
        "## Content\n\n"
        "| File | What's inside |\n"
        "|------|---------------|\n"
        "| `content/01-overview.xml` | overview |\n"
    )

    failures = 0
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "content").mkdir()
        (root / "content" / "01-overview.xml").write_text(
            "<?xml version='1.0'?>\n<root/>\n", encoding="utf-8"
        )
        agents = root / "AGENTS.md"
        agents.write_text(valid, encoding="utf-8")
        rpt = validate_file(agents)
        if not rpt.ok:
            sys.stderr.write("self-test: VALID case failed:\n")
            sys.stderr.write(render_report(rpt) + "\n")
            failures += 1

        # Bad: missing content_id
        bad = valid.replace("content_id: 0123456789abcdef\n", "")
        agents.write_text(bad, encoding="utf-8")
        rpt = validate_file(agents)
        if rpt.ok or not any("content_id" in e for e in rpt.errors):
            sys.stderr.write("self-test: missing content_id should fail\n")
            failures += 1

        # Bad: oversized (>80 lines)
        agents.write_text(valid + ("padding\n" * 60), encoding="utf-8")
        rpt = validate_file(agents)
        if rpt.ok or not any("lines" in e for e in rpt.errors):
            sys.stderr.write("self-test: oversized file should fail\n")
            failures += 1

        # Bad: drift between disk and table
        (root / "content" / "02-extra.xml").write_text(
            "<?xml version='1.0'?>\n<root/>\n", encoding="utf-8"
        )
        agents.write_text(valid, encoding="utf-8")
        rpt = validate_file(agents)
        if rpt.ok or not any("02-extra.xml" in e for e in rpt.errors):
            sys.stderr.write("self-test: extra disk file should fail\n")
            failures += 1

    sys.stdout.write(
        "self-test: PASS\n" if failures == 0 else f"self-test: FAIL ({failures})\n"
    )
    return 0 if failures == 0 else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("paths", nargs="*", help="workflow dir or AGENTS.md path")
    parser.add_argument(
        "--all",
        action="store_true",
        help=f"validate every workflow under {WORKFLOWS_ROOT.relative_to(REPO_ROOT)}",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run synthetic pass/fail cases (no real files)",
    )
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
