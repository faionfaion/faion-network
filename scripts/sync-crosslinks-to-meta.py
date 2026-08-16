#!/usr/bin/env python3
"""Lift `[[slug]]` cross-links out of leaf AGENTS.md prose into meta.json.

A leaf `AGENTS.md` cross-references sibling methodologies with `[[slug]]` in two
places: the `## Assumes Loaded` table (slug + why) and the `## Related` list
(slug only). Those 8,000-odd links are read by an agent and by nothing else —
no validator resolves them, so a rename breaks them silently, which is exactly
what the F-067 taxonomy change did before `remap-dangling-wikilinks.py` had to
repair it.

This script makes `meta.json` the machine-readable home:

    "assumes_loaded": [{"slug": "api-rest-design", "why": "Endpoint definitions…"}],
    "related": ["api-rest-design", "api-error-handling"]

`meta.json` itself never ships — `packablePath`/`isNonContent` in
`faion-cli/tools/vfs-pack/pack.go` excludes it by basename ahead of every
admission rule. The delivery path is `regen-domains-xml.py`, which reads
meta.json and writes the L2 `INDEX.xml` that does ship. That is an improvement
rather than a detour: a "read this next" pointer is useful while the retriever
is choosing a leaf, and today it is buried in a file you only open after the
choice is made.

Links outside the two sections (prose in `Summary`, `Applies If`, `Skip If`)
are left exactly where they are — they are sentences, not a graph.

Each leaf then says so itself: `--annotate` stamps a `<!-- canonical: … -->`
pointer under both headings, and `--check` is the gate that keeps the pointer
honest. A provenance comment nothing verifies is how the corpus got here.

Usage:
    python3 scripts/sync-crosslinks-to-meta.py             # dry run (default)
    python3 scripts/sync-crosslinks-to-meta.py --report    # per-file detail
    python3 scripts/sync-crosslinks-to-meta.py --check     # drift gate, exit 1
    python3 scripts/sync-crosslinks-to-meta.py --annotate --write
    python3 scripts/sync-crosslinks-to-meta.py --write     # apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "skills" / "faion"
KNOWLEDGE = ROOT / "knowledge"

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
LINK_RE = re.compile(r"\[\[([^\]|]+?)\]\]")
FENCE_RE = re.compile(r"^\s*(```|~~~)")

# Heading vocabulary, lowercased. Mirrors SECTION_ALTERNATES in
# validate-methodology-v2.py — writers use either v2-canonical or v1-legacy names.
ASSUMES_HEADINGS = {"assumes loaded"}
RELATED_HEADINGS = {"related", "see also", "references"}

# `## Prerequisites` is NOT one of them, though the validator lists it beside
# `## Assumes Loaded` as an optional section. On disk it is an input-artefact
# table — `| Input artifact | Format | Source |` — in 2,480 of the 2,497 leaves
# that have it. The 17 exceptions put a wikilink in the *Source* column, naming
# where an input comes from rather than what to load, and this parser reads the
# first column, so none of them was ever lifted. Treating the heading as a
# prerequisite list would put a false "canonical: meta.json" claim on 2,480
# tables that have nothing to do with the cross-link graph.

# Provenance markers written into AGENTS.md by --annotate. Detected by prefix so
# the wording can be revised without orphaning the ones already on disk.
# Kept short deliberately. The marker is a pointer, not an explanation — the
# reasoning lives once in meta-json-spec.md §3.2 rather than 2,520 times on
# disk, and every byte here is paid on every leaf an agent opens, including on
# a customer's machine where meta.json does not ship and the "edit there"
# half would be advice they cannot act on.
MARKER_PREFIX = "<!-- canonical:"
MARKER_ASSUMES = "<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->"
# Deliberately narrower than the assumes marker. `## Related` is not wholly
# derived: 2,168 of its bullets are prose that meta.json does not hold, and 434
# of those name a pre-F-067 path (`pro/…`, `geek/…`) that resolves to nothing.
# Claiming the whole section is generated would be false.
#
# It also must not contain a doubled-bracket example. `extract()` reads this
# same file back, so a literal one in the marker would be lifted as a link to a
# methodology named after the placeholder.
MARKER_RELATED = (
    "<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->"
)


def leaves() -> list[Path]:
    return sorted(d for d in KNOWLEDGE.glob("*/*")
                  if d.is_dir() and (d / "AGENTS.md").exists())


def known_slugs() -> set[str]:
    return {d.name for d in KNOWLEDGE.glob("*/*")
            if d.is_dir() and (d / "AGENTS.md").exists()}


def sections(text: str) -> list[tuple[str, list[str]]]:
    """(lowercased heading, body lines), with fenced code blocks dropped.

    The fence matters: `[[tool.mypy.overrides]]` is TOML and `[[ -f "$f" ]]` is
    bash, and both are indistinguishable from a wikilink to a regex.
    """
    out: list[tuple[str, list[str]]] = []
    current: str | None = None
    buf: list[str] = []
    fenced = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = HEADING_RE.match(line)
        if m:
            if current is not None:
                out.append((current, buf))
            # Headings carry parenthetical qualifiers: "Related (see also)".
            current, buf = m.group(1).strip().lower().split("(")[0].strip(), []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out.append((current, buf))
    return out


def extract(text: str, own_slug: str) -> tuple[list[dict], list[str]]:
    """Pull the two link sets out of an AGENTS.md body.

    Self-references are dropped rather than carried. 43 leaves list themselves
    under `## Related` or `## Assumes Loaded` — harmless while a wikilink was
    an inert string, and an instruction to load the file you are already
    reading once anything resolves it.
    """
    assumes: list[dict] = []
    related: list[str] = []
    for heading, body in sections(text):
        if heading in ASSUMES_HEADINGS:
            for row in body:
                if not row.strip().startswith("|"):
                    continue
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                links = LINK_RE.findall(cells[0]) if cells else []
                if not links:
                    continue  # header row, separator row, or a prose row
                slug = links[0].split("/")[-1].strip()
                if slug == own_slug:
                    continue
                why = cells[1].strip() if len(cells) > 1 else ""
                assumes.append({"slug": slug, "why": why})
        elif heading in RELATED_HEADINGS:
            for row in body:
                for link in LINK_RE.findall(row):
                    slug = link.split("/")[-1].strip()
                    if slug != own_slug and slug not in related:
                        related.append(slug)
    return assumes, related


def rewrite(meta: dict, assumes: list[dict], related: list[str]) -> dict:
    """Return meta with the two keys set (or removed when empty), after `tags`."""
    out: dict = {}
    for key, value in meta.items():
        if key in ("assumes_loaded", "related"):
            continue
        out[key] = value
        if key == "tags":
            if assumes:
                out["assumes_loaded"] = assumes
            if related:
                out["related"] = related
    # `tags` is required by the schema, but do not silently drop data if a file
    # is missing it — append instead of discarding.
    if assumes and "assumes_loaded" not in out:
        out["assumes_loaded"] = assumes
    if related and "related" not in out:
        out["related"] = related
    return out


def annotate(text: str) -> str:
    """Insert the provenance marker under each cross-link heading.

    Idempotent: an existing marker on the line after the heading is replaced,
    so revising the wording does not stack a second one.
    """
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        m = HEADING_RE.match(line.rstrip("\n"))
        if not m:
            continue
        heading = m.group(1).strip().lower().split("(")[0].strip()
        if heading in ASSUMES_HEADINGS:
            marker = MARKER_ASSUMES
        elif heading in RELATED_HEADINGS:
            marker = MARKER_RELATED
        else:
            continue
        # Drop whatever separates the heading from the body, replace any marker
        # already there, and re-emit one canonical blank-marker-blank block.
        # Consuming the trailing blanks too is what makes a second run a no-op
        # rather than a file that grows one blank line per invocation.
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i < len(lines) and lines[i].lstrip().startswith(MARKER_PREFIX):
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
        out.append("\n" + marker + "\n\n")
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true",
                    help="apply changes; without it the script only reports")
    ap.add_argument("--report", action="store_true",
                    help="list every file that would change")
    ap.add_argument("--check", action="store_true",
                    help="drift gate: exit 1 if any meta.json disagrees with its "
                         "AGENTS.md, without writing anything")
    ap.add_argument("--annotate", action="store_true",
                    help="write the 'canonical: meta.json' marker under each "
                         "cross-link heading in AGENTS.md (idempotent)")
    args = ap.parse_args()
    if args.check:
        args.write = False

    slugs = known_slugs()
    stats = Counter()
    unresolved: Counter[str] = Counter()
    unresolved_where: dict[str, str] = {}
    changed: list[tuple[Path, int, int]] = []
    reformat_only: list[Path] = []

    for leaf in leaves():
        meta_path = leaf / "meta.json"
        if not meta_path.exists():
            stats["meta_missing"] += 1
            continue
        original = meta_path.read_text(encoding="utf-8")
        try:
            meta = json.loads(original)
        except json.JSONDecodeError as exc:
            print(f"PARSE {meta_path}: {exc}", file=sys.stderr)
            stats["parse_error"] += 1
            continue

        agents_path = leaf / "AGENTS.md"
        agents_text = agents_path.read_text(encoding="utf-8", errors="replace")
        assumes, related = extract(agents_text, meta.get("slug") or leaf.name)

        if args.annotate:
            annotated = annotate(agents_text)
            if annotated != agents_text:
                stats["annotated"] += 1
                agents_path.write_text(annotated, encoding="utf-8")
        for entry in assumes:
            if entry["slug"] not in slugs:
                unresolved[entry["slug"]] += 1
                unresolved_where.setdefault(entry["slug"], str(leaf.relative_to(ROOT)))
            if not entry["why"]:
                stats["assumes_without_why"] += 1
        for slug in related:
            if slug not in slugs:
                unresolved[slug] += 1
                unresolved_where.setdefault(slug, str(leaf.relative_to(ROOT)))

        stats["assumes_entries"] += len(assumes)
        stats["related_entries"] += len(related)

        updated = json.dumps(rewrite(meta, assumes, related),
                             indent=2, ensure_ascii=False) + "\n"
        if updated == original:
            continue
        if not assumes and not related:
            # No links to lift; any diff here is pure reformatting, so skip the
            # file rather than churn 2,500 blobs for whitespace.
            reformat_only.append(meta_path)
            continue
        changed.append((meta_path, len(assumes), len(related)))
        if args.write:
            meta_path.write_text(updated, encoding="utf-8")

    if args.report:
        for path, a, r in changed:
            print(f"  {path.parent.relative_to(ROOT)}  assumes={a} related={r}")

    print(f"leaves scanned:            {len(leaves())}")
    print(f"files {'written' if args.write else 'to change'}:"
          f"{'':<12}{len(changed)}")
    print(f"assumes_loaded entries:    {stats['assumes_entries']}")
    print(f"related entries:           {stats['related_entries']}")
    print(f"assumes rows without why:  {stats['assumes_without_why']}")
    print(f"skipped (reformat only):   {len(reformat_only)}")
    if args.annotate:
        print(f"AGENTS.md annotated:       {stats['annotated']}")
    if stats["meta_missing"] or stats["parse_error"]:
        print(f"meta.json missing:         {stats['meta_missing']}")
        print(f"meta.json unparseable:     {stats['parse_error']}")

    if args.check and changed:
        print(f"\nDRIFT: {len(changed)} meta.json files disagree with their "
              f"AGENTS.md. Run --write.")
        for path, a, r in changed[:20]:
            print(f"  {path.parent.relative_to(ROOT)}  assumes={a} related={r}")
        return 1

    if unresolved:
        print(f"\nUNRESOLVED slugs: {len(unresolved)} distinct, "
              f"{sum(unresolved.values())} occurrences")
        for slug, count in unresolved.most_common(20):
            print(f"  {slug}  x{count}  (first seen in {unresolved_where[slug]})")
        print("\nRefusing to treat these as a graph. Fix or drop them first.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
