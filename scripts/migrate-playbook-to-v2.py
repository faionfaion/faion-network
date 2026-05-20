#!/usr/bin/env python3
"""
Migrate v1 playbook.md files into v2 (playbook.yaml + body.md).

Usage:
    python3 scripts/migrate-playbook-to-v2.py <path/to/playbook.md> [more ...]
    python3 scripts/migrate-playbook-to-v2.py --dry-run <path...>

What it does (per F-060 design):
- Reads v1 front-matter (name, description, tier, group, status, last_verified,
  version, owner) from the leading `---` block.
- Writes a sibling playbook.yaml containing the v2 manifest shape:
    slug         <- name
    title        <- humanized name
    version      <- version (or 0.1.0)
    status       <- always set to "draft" on migration (gaps[] left for fill-in)
    last_reviewed <- last_verified (or today's run date)
    maintainers  <- [owner] if present, else ["unknown"]
    tier_min     <- tier
    complexity   <- "medium" (default, manual reclassification expected)
    context      <- ["solo"] default
    intent       <- description
    scope        <- description repeated (manual rewrite expected)
    success_criteria <- single placeholder pulled from Goal section if present,
                        otherwise generic "Complete all steps".
    stages       <- inferred from H2 sections in body. If a "Steps" section
                    exists and is numerically structured, becomes a single
                    "Default" stage with each numbered step turned into a task.
                    Otherwise: a single "Default" stage with whole-body intent.
    token_budget_estimate <- 8000 default
    gaps         <- []
- Writes a sibling body.md containing the original v1 markdown body (the part
  after the closing `---` of the front-matter). Keeps numbered steps + tables.
- Renames original playbook.md to playbook-v1.md.bak.

Output passes scripts/validate-playbook-v2.py.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class V1Frontmatter:
    name: str = ""
    description: str = ""
    tier: str = "solo"
    group: str = ""
    status: str = "draft"
    owner: str = "unknown"
    last_verified: str = "2026-05-17"
    version: str = "0.1.0"

    @classmethod
    def parse(cls, text: str) -> "V1Frontmatter":
        if not text.startswith("---\n"):
            raise ValueError("missing front-matter")
        end = text.find("\n---\n", 4)
        if end == -1:
            raise ValueError("front-matter not closed")
        block = text[4:end]
        kv: dict = {}
        for line in block.splitlines():
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            k, _, v = line.partition(":")
            kv[k.strip()] = v.strip().strip("'\"")
        fm = cls()
        for f in ("name", "description", "tier", "group", "status",
                  "owner", "last_verified", "version"):
            if f in kv and kv[f]:
                setattr(fm, f, kv[f])
        return fm


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_block, body) — body is everything after closing ---."""
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[: end + 5], text[end + 5:].lstrip("\n")


H2_RE = re.compile(r"^##\s+(.+?)\s*$")
NUMBERED_STEP_RE = re.compile(r"^\s*(\d+)\.\s+(.+)$")


def parse_h2_sections(body: str) -> list[tuple[str, str]]:
    """Return [(heading, content), ...] for `## ` H2 sections in order."""
    sections: list[tuple[str, str]] = []
    cur_name: str | None = None
    cur_buf: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            if cur_name is not None:
                cur_buf.append(line)
            continue
        if not in_fence:
            m = H2_RE.match(line)
            if m:
                if cur_name is not None:
                    sections.append((cur_name, "\n".join(cur_buf).strip()))
                cur_name = m.group(1).strip()
                cur_buf = []
                continue
        if cur_name is not None:
            cur_buf.append(line)
    if cur_name is not None:
        sections.append((cur_name, "\n".join(cur_buf).strip()))
    return sections


def extract_tasks_from_steps(steps_content: str) -> list[str]:
    """Pull numbered steps -> list of one-line task labels."""
    tasks: list[str] = []
    for line in steps_content.splitlines():
        m = NUMBERED_STEP_RE.match(line)
        if m:
            text = m.group(2).strip()
            # Truncate to first sentence / first 120 chars for atomicity.
            first_sentence = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0]
            if len(first_sentence) > 120:
                first_sentence = first_sentence[:117] + "..."
            tasks.append(first_sentence)
    return tasks


def extract_success_criteria(sections: dict[str, str], description: str) -> list[str]:
    """Pull success criteria from Verify section if it has bullet/structured info."""
    crits: list[str] = []
    verify = sections.get("Verify", "").strip()
    if verify:
        for line in verify.splitlines():
            s = line.strip()
            if s.startswith(("-", "*")) and len(s) > 3:
                crits.append(s[1:].strip())
        if not crits and verify:
            # Take first sentence of verify as the single criterion.
            first = re.split(r"(?<=[.!?])\s+", verify, maxsplit=1)[0]
            if first:
                crits.append(first.strip())
    if not crits:
        crits.append(description.strip() or "Complete all playbook steps")
    return crits[:7]


def humanize_title(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").strip().capitalize()


def compute_content_id(slug: str, version: str) -> str:
    h = hashlib.sha1(f"{slug}{version}".encode("utf-8")).hexdigest()
    return h[:16]


def build_v2_manifest(fm: V1Frontmatter, body: str) -> dict:
    sections = parse_h2_sections(body)
    sec_map = {name: content for name, content in sections}

    tier_min = fm.tier if fm.tier in {"free", "solo", "pro", "geek"} else "solo"
    version = fm.version or "0.1.0"
    title = humanize_title(fm.name) if fm.name else "Untitled playbook"

    steps_content = sec_map.get("Steps", "")
    tasks = extract_tasks_from_steps(steps_content)
    if not tasks and steps_content:
        # Fall back: split bulletted list.
        for line in steps_content.splitlines():
            s = line.strip()
            if s.startswith(("-", "*")) and len(s) > 3:
                tasks.append(s[1:].strip())
    if not tasks:
        tasks = ["Follow the body.md sequence end-to-end"]

    decision_gate = (
        sec_map.get("Verify", "").strip().splitlines()[0]
        if sec_map.get("Verify")
        else "Advance when Verify section passes; TBD on rewrite."
    )
    if len(decision_gate) > 200:
        decision_gate = decision_gate[:197] + "..."

    stage_intent = (fm.description or "Default stage").strip()
    next_section = sec_map.get("Next", "").strip()
    outputs = []
    if next_section:
        for line in next_section.splitlines():
            s = line.strip()
            if s.startswith(("-", "*")) and len(s) > 3:
                outputs.append(s[1:].strip())
    if not outputs:
        outputs = ["Artifact described in body.md"]

    stage = {
        "name": "Default",
        "intent": stage_intent,
        "tasks": tasks[:7],
        "methodologies": [],
        "outputs": outputs[:5],
        "decision_gate": decision_gate,
    }

    success_criteria = extract_success_criteria(sec_map, fm.description)

    manifest: dict = {
        "slug": fm.name,
        "title": title,
        "version": version,
        "status": "draft",
        "last_reviewed": fm.last_verified,
        "maintainers": [fm.owner] if fm.owner else ["unknown"],
        "tier_min": tier_min,
        "complexity": "medium",
        "context": ["solo"],
        "intent": fm.description.strip() or "Migrated v1 playbook intent — rewrite required.",
        "scope": fm.description.strip() or "Migrated v1 playbook scope — rewrite required.",
        "success_criteria": success_criteria,
        "stages": [stage],
        "token_budget_estimate": 8000,
        "gaps": [],
        "content_id": compute_content_id(fm.name, version),
    }
    return manifest


def emit_yaml(manifest: dict) -> str:
    return yaml.safe_dump(
        manifest,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
    )


def migrate_one(path: Path, dry_run: bool = False) -> tuple[bool, str]:
    """Returns (ok, message)."""
    if not path.exists():
        return False, f"missing: {path}"
    if path.name != "playbook.md":
        return False, f"not a v1 playbook.md: {path.name}"

    text = path.read_text(encoding="utf-8")
    try:
        fm = V1Frontmatter.parse(text)
    except ValueError as exc:
        return False, f"frontmatter error: {exc}"

    _, body = split_frontmatter(text)
    manifest = build_v2_manifest(fm, body)
    yaml_text = emit_yaml(manifest)

    yaml_path = path.parent / "playbook.yaml"
    body_path = path.parent / "body.md"
    bak_path = path.parent / "playbook-v1.md.bak"

    if dry_run:
        return True, (
            f"DRY-RUN {path}\n"
            f"  -> {yaml_path}\n"
            f"  -> {body_path}\n"
            f"  -> {bak_path}\n"
            f"  manifest preview ({len(yaml_text)} bytes)"
        )

    if yaml_path.exists():
        return False, f"refuse to overwrite existing playbook.yaml at {yaml_path}"
    if body_path.exists():
        return False, f"refuse to overwrite existing body.md at {body_path}"
    if bak_path.exists():
        return False, f"refuse to overwrite existing backup at {bak_path}"

    yaml_path.write_text(yaml_text, encoding="utf-8")
    body_path.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8")
    path.rename(bak_path)

    return True, f"migrated {path} -> {yaml_path.name} + body.md (v1 -> {bak_path.name})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    fail = 0
    for p in args.paths:
        ok, msg = migrate_one(p, dry_run=args.dry_run)
        if ok:
            sys.stdout.write(msg + "\n")
        else:
            fail += 1
            sys.stdout.write(f"FAIL {p}: {msg}\n")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
