#!/usr/bin/env python3
"""Apply F-065 phase 1 domain merge.

Walks every `skills/faion/knowledge/**/AGENTS.md`, locates the YAML
frontmatter `domain:` line, and rewrites it to the canonical bucket
per the MERGE map below.

Hard rules:
- Only the `domain:` line is rewritten. Every other byte is preserved.
- Files without a `domain:` line are skipped silently.
- Domains already canonical (or unknown to MERGE) are left untouched.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

MERGE: dict[str, str] = {
    # dev cluster
    "software-developer": "dev",
    "code-quality": "dev",
    "testing-developer": "dev",
    "testing": "dev",
    "qa-engineer": "dev",
    "devtools-developer": "dev",
    # backend cluster
    "backend-systems": "backend",
    "backend-enterprise": "backend",
    "python-developer": "backend",
    "api-developer": "backend",
    "server-craft": "backend",
    "javascript-developer": "backend",
    # frontend cluster
    "frontend-developer": "frontend",
    "ui-designer": "frontend",
    "ux-ui-designer": "frontend",
    # infra cluster
    "infrastructure-engineer": "infra",
    "cicd-engineer": "infra",
    "devops-engineer": "infra",
    # AI split (4 buckets)
    "ai": "ai-core",
    "ml-engineer": "ml-engineering",
    "ml-ops": "ml-engineering",
    "multimodal-ai": "ml-engineering",
    "rag-engineer": "ml-engineering",
    "llm-integration": "ml-engineering",
    "sdd-ai": "sdlc-ai",
    # pm cluster
    "pm-agile": "pm",
    "pm-traditional": "pm",
    "project-manager": "pm",
    "product-manager": "pm",
    "product-operations": "pm",
    "product-planning": "pm",
    # marketing cluster
    "gtm-strategist": "marketing",
    "content-marketer": "marketing",
    "ppc-manager": "marketing",
    "smm-manager": "marketing",
    "seo-manager": "marketing",
    "growth-marketer": "marketing",
    "conversion-optimizer": "marketing",
    # ux cluster
    "ux-researcher": "ux",
    "accessibility-specialist": "ux",
    "user-researcher": "ux",
    # research cluster
    "researcher": "research",
    "market-researcher": "research",
    # ba cluster
    "ba-core": "ba",
    "ba-modeling": "ba",
    "business-analyst": "ba",
    # sdd cluster
    "sdd-planning": "sdd",
    "automation-tooling": "sdd",
    # comms
    "communicator": "comms",
    # architecture (stays)
    "software-architect": "architecture",
    # hr (stays as-is from hr-recruiter)
    "hr-recruiter": "hr",
    # security (stays)
    "sec": "security",
    # claude-code cluster
    "kb-agents-md-context-pyramid": "claude-code",
}

CANONICAL: set[str] = {
    "dev",
    "backend",
    "frontend",
    "infra",
    "ai-agents",
    "sdlc-ai",
    "pm",
    "product",
    "marketing",
    "ux",
    "research",
    "ba",
    "sdd",
    "comms",
    "architecture",
    "hr",
    "security",
    "claude-code",
    "ai-core",
    "ml-engineering",
}

DOMAIN_RE = re.compile(r"^(\s*domain:\s*)(\S.*?)(\s*)$")


def rewrite_file(path: Path, mode: str) -> tuple[str | None, str | None, bool]:
    """Return (old_domain, new_domain, changed)."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Locate frontmatter window.
    if not lines or not lines[0].startswith("---"):
        return None, None, False

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].startswith("---"):
            end_idx = i
            break
    if end_idx is None:
        return None, None, False

    for i in range(1, end_idx):
        m = DOMAIN_RE.match(lines[i].rstrip("\n"))
        if not m:
            continue
        prefix, value, _trail = m.group(1), m.group(2), m.group(3)
        # Strip quotes if present.
        bare = value.strip().strip("'\"")
        old = bare
        new = MERGE.get(bare, bare)
        if new == bare:
            return old, None, False
        # Preserve line ending.
        line = lines[i]
        eol = ""
        if line.endswith("\r\n"):
            eol = "\r\n"
        elif line.endswith("\n"):
            eol = "\n"
        lines[i] = f"{prefix}{new}{eol}"
        if mode == "write":
            path.write_text("".join(lines), encoding="utf-8")
        return old, new, True

    return None, None, False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default="skills/faion/knowledge",
        help="Root dir to walk (relative to repo or absolute).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report only — don't write files.",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_absolute():
        root = Path.cwd() / root
    if not root.exists():
        sys.stderr.write(f"ERROR: root not found: {root}\n")
        return 2

    mode = "report" if args.dry_run else "write"
    mapping_counts: Counter[tuple[str, str]] = Counter()
    canonical_counts: Counter[str] = Counter()
    total = 0
    changed = 0
    no_domain = 0
    unchanged = 0

    for path in sorted(root.rglob("AGENTS.md")):
        total += 1
        old, new, did = rewrite_file(path, mode)
        if old is None and new is None and not did:
            # Either no frontmatter or no domain line.
            no_domain += 1
            continue
        if did and new is not None:
            changed += 1
            mapping_counts[(old, new)] += 1  # type: ignore[arg-type]
            canonical_counts[new] += 1
        else:
            unchanged += 1
            if old is not None:
                canonical_counts[old] += 1

    out = sys.stdout.write
    out(f"Mode: {mode}\n")
    out(f"Root: {root}\n")
    out(f"Total AGENTS.md scanned: {total}\n")
    out(f"  with domain frontmatter: {total - no_domain}\n")
    out(f"  without domain (skipped): {no_domain}\n")
    out(f"  unchanged (already canonical or unknown): {unchanged}\n")
    out(f"  rewritten: {changed}\n")

    if mapping_counts:
        out("\nBy-mapping breakdown (old -> new : count):\n")
        for (old, new), n in sorted(
            mapping_counts.items(), key=lambda kv: (-kv[1], kv[0])
        ):
            out(f"  {old:>32} -> {new:<16} {n}\n")

    out("\nFinal canonical distribution (post-merge):\n")
    stragglers: list[tuple[str, int]] = []
    for d, n in sorted(canonical_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        marker = "" if d in CANONICAL else "  <-- NOT IN CANONICAL-20"
        out(f"  {d:<20} {n}{marker}\n")
        if d not in CANONICAL:
            stragglers.append((d, n))

    out("\n")
    if stragglers:
        out("STRAGGLERS (domain values outside canonical-20):\n")
        for d, n in stragglers:
            out(f"  {d}: {n}\n")
        return 1
    out("OK\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
