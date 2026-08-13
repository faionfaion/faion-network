#!/usr/bin/env python3
"""Remap or drop dangling [[wikilinks]] in leaf methodology AGENTS.md files.

A leaf `AGENTS.md` cross-references sibling methodologies with `[[slug]]` in its
`## Assumes Loaded` table and `## Related` list. Some of those slugs are stale
references to the pre-F-067 role-based taxonomy: either an old path
(`solo/dev/software-architect/quality-attributes`), an old role or knowledge-base
container name (`project-manager`), or a title-slug that no longer matches the
directory name (`sdd-document-templates` -> `sdd/templates`).

Two actions, decided per slug:

  remap  a successor methodology exists under the current taxonomy; the link is
         rewritten to point at it. Path-style slugs whose basename resolves are
         remapped automatically; everything else needs an entry in REMAP below.
  drop   no successor exists (role containers, domain names, invented slugs);
         the link is removed. Removing a whole `## Related` bullet or a whole
         `## Assumes Loaded` table row when the link is the only thing on it.

Retrieval never navigates by wikilink (it walks domains.xml -> INDEX.xml -> leaf),
so this is hygiene: a dangling `[[link]]` is an inert bracketed string an agent
reads and cannot follow.

Usage:
    python3 scripts/remap-dangling-wikilinks.py --dry-run
    python3 scripts/remap-dangling-wikilinks.py --report   # per-slug decisions
    python3 scripts/remap-dangling-wikilinks.py            # apply
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

KNOWLEDGE = Path(__file__).resolve().parent.parent / "skills" / "faion" / "knowledge"

# Slugs with an explicit successor. Path-style slugs whose basename already
# resolves are handled by the automatic rule and are not listed here.
REMAP = {
    # title-slug drift: the H1 of sdd/templates is "SDD Document Templates"
    "sdd-document-templates": "templates",
    # H1 of infra/docker-compose is "Docker Compose (DevOps)"
    "docker-compose-devops": "docker-compose",
    # H1 of infra/docker-compose-infra is "Docker Compose (Infrastructure)"
    "docker-compose-infrastructure": "docker-compose-infra",
    # double-underscore typo of an existing F-067 suffixed slug
    "linear-issue-tracking__pm-agile": "linear-issue-tracking-pm-agile",
    # qualifier dropped from an existing slug
    "requirements-traceability-full-lifecycle": "requirements-traceability",
    "wcag-22-checklist": "wcag-22-compliance",
    "trunk-based-development": "trunk-based-dev-principles",
    "utm-discipline": "utm-taxonomy-discipline",
    "verb-object-naming": "verb-object-tool-naming",
    "vendor-management": "vendor-management-pm",
    "product-roadmap-design": "roadmap-design",
    "rag-evaluation-frameworks": "rag-evaluation",
    "technical-debt": "technical-debt-management",
    "refactoring": "refactoring-patterns",
    "ai-feature-ux-patterns": "ai-feature-ux-pattern-library",
    "cohort-basics": "cohort-implementation",
    "ml-engineering/eval-set-design": "ai-feature-eval-set-design",
    # sole methodology on the subject under the current taxonomy
    "deploy-blue-green-canary": "release-strategy-canary-blue-green-feature-flag",
    "golden-dataset-construction": "golden-set-curation-and-maintenance",
    "content-moderation": "vision-classification-moderation",
    "claude-code-skills-authoring": "skills",
    "claude-code:skills": "skills",
    # domain annotation leaked into the link target
    "ai-assisted-specification-writing (sdd)": "ai-assisted-specification-writing",
    "ai-assisted-specification-writing (sdd-planning)": "ai-assisted-specification-writing-planning",
    # host methodology is backend/django-*, so the Django variant is the successor
    "service-layer-pattern": "django-service-layer",
    "content-marketing": "growth-content-marketing",
    "django-pytest-setup": "django-pytest",
    "incident-response-playbook": "incident-response-blameless-playbook",
    "architecture-fitness-functions": "evolutionary-architecture-fitness-functions",
    "iac-baseline": "iac-basics",
    "skills-and-plugins": "skills",
}

# Not methodology references. `[[Related]]` is prose pointing at this file's own
# `## Related` section; `[[bin]]` is Cargo-manifest syntax quoted in a table cell.
IGNORE = {"Related", "Assumes Loaded", "bin", "lib"}

FENCE = re.compile(r"^```.*?^```", re.M | re.S)
WIKI = re.compile(r"`?\[\[([^\]|\n]+?)(?:\|[^\]\n]*)?\]\]`?")
BULLET = re.compile(r"^\s*[-*]\s+")
ROW = re.compile(r"^\s*\|\s*")


def load_slugs() -> set[str]:
    return {
        leaf.name
        for domain in KNOWLEDGE.iterdir()
        if domain.is_dir()
        for leaf in domain.iterdir()
        if leaf.is_dir() and (leaf / "AGENTS.md").exists()
    }


def code_spans(text: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in FENCE.finditer(text)]


def in_code(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(a <= pos < b for a, b in spans)


def resolve(slug: str, existing: set[str]) -> str | None:
    """Return the successor slug, or None to drop the link."""
    if slug in existing:
        return slug
    if slug in REMAP:
        return REMAP[slug]
    if "/" in slug:
        base = slug.rsplit("/", 1)[-1]
        if base in existing:
            return base
    return None


def lead_content(line: str) -> int:
    """Offset of the first content character of a bullet or first table cell."""
    for pat in (BULLET, ROW):
        m = pat.match(line)
        if m:
            return m.end()
    return -1


def rewrite_line(line: str, existing: set[str], stats: Counter) -> str | None:
    """Rewrite one line; return None when the whole line should be removed."""
    matches = list(WIKI.finditer(line))
    decisions = []
    for m in matches:
        slug = m.group(1).strip()
        if slug in IGNORE or slug in existing:
            decisions.append((m, slug))
        else:
            decisions.append((m, resolve(slug, existing)))

    drops = [(m, m.group(1).strip()) for m, target in decisions if target is None]
    if not drops:
        out = line
        for m, target in reversed(decisions):
            if target != m.group(1).strip():
                stats["remapped"] += 1
                stats["remap:" + m.group(1).strip()] += 1
                out = out[:m.start()] + m.group(0).replace(m.group(1), target) + out[m.end():]
        return out

    stats["dropped"] += len(drops)
    for _, slug in drops:
        stats["drop:" + slug] += 1

    survivors = [m for m, target in decisions if target is not None]
    lead = lead_content(line)
    if not survivors and lead >= 0 and drops[0][0].start() == lead:
        # the link was the whole bullet / the whole first table cell
        stats["rows_removed" if ROW.match(line) else "bullets_removed"] += 1
        return None

    out = line
    for m, target in reversed(decisions):
        if target is None:
            out = out[:m.start()] + m.group(1).strip() + out[m.end():]
        elif target != m.group(1).strip():
            stats["remapped"] += 1
            stats["remap:" + m.group(1).strip()] += 1
            out = out[:m.start()] + m.group(0).replace(m.group(1), target) + out[m.end():]
    stats["unlinked"] += len(drops)
    return out


def rewrite(text: str, existing: set[str], stats: Counter) -> str:
    spans = code_spans(text)
    out_lines: list[str] = []
    offset = 0
    for line in text.split("\n"):
        start = offset
        offset += len(line) + 1
        if not WIKI.search(line) or in_code(start, spans):
            out_lines.append(line)
            continue
        new = rewrite_line(line, existing, stats)
        if new is not None:
            out_lines.append(new)
    return "\n".join(out_lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    ap.add_argument("--report", action="store_true", help="print the per-slug decision table")
    args = ap.parse_args()

    existing = load_slugs()
    stats: Counter = Counter()
    changed = 0

    for domain in sorted(p for p in KNOWLEDGE.iterdir() if p.is_dir()):
        for leaf in sorted(p for p in domain.iterdir() if p.is_dir()):
            f = leaf / "AGENTS.md"
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8")
            new = rewrite(text, existing, stats)
            if new != text:
                changed += 1
                if not args.dry_run:
                    f.write_text(new, encoding="utf-8")

    print(f"files changed: {changed}")
    print(f"links remapped: {stats['remapped']}")
    print(f"links dropped: {stats['dropped']} "
          f"(bullets removed {stats['bullets_removed']}, rows removed {stats['rows_removed']}, "
          f"unlinked in place {stats['unlinked']})")

    if args.report:
        print("\nslug -> target or DROP (count)")
        rows = []
        for key, n in stats.items():
            if key.startswith("remap:"):
                slug = key[6:]
                rows.append((slug, resolve(slug, existing), n))
            elif key.startswith("drop:"):
                rows.append((key[5:], "DROP", n))
        for slug, target, n in sorted(rows, key=lambda r: (-r[2], r[0])):
            print(f"{n:4d}  {slug}  ->  {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
