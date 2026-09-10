#!/usr/bin/env python3
"""F-077 — un-inline the templates: the `## Template Contents` region comes out.

P0.4 diagnosed correctly that thousands of `## Templates` rows named files no
interface could fetch, and remedied it by pasting each body into the envelope as
a fenced block. The fix for an unreachable file is to make it reachable:
`packablePath` now admits anything under a `templates/` segment, so the file
ships, and the inlined copy is a second shipment of the same bytes — paid during
*retrieval*, on every search that surfaces the slug.

    --report              divergence report; writes nothing
    --write [--domain D]  remove the region, optionally one domain at a time
    --check               exit 1 if any envelope still inlines a body
    --measure             envelope total and worst case, plus dangling rows

The report is not ceremony. A block edited after inlining is content a blind
delete loses, so every block is classified against the file first, and `--write`
refuses to run until every block the mechanical tests cannot vouch for carries a
recorded reason in `scripts/uninline-resolutions.tsv`. A `--force` flag would
have been cheaper and would have recorded nothing.

Never deletes a file under `templates/`. This un-inlines; it does not delete.
"""
from __future__ import annotations

import argparse
import collections
import glob
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

from envelope_inline import (  # noqa: E402
    classify, inlined_blocks, normalise, strip_section,
    trailing_heading_after_section,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOTS = (
    "skills/faion/knowledge/*/*/AGENTS.md",
    "skills/faion/playbooks/*/*/AGENTS.md",
    "skills/faion/workflows/*/AGENTS.md",
)

LOSSLESS = {
    "faithful-copy",
    "same-data-different-wrapping",
    "same-characters-different-line-breaks",
    "block-kept-the-authored-header",
    "block-is-a-substring-of-the-file",
    "too-short-to-compare",
}

# AC4: a block the mechanical tests cannot vouch for is resolved by reading the
# diff and recording why removing it loses nothing. `--write` consults this file
# rather than taking a `--force` flag, because a flag records nothing.
RESOLUTIONS = os.path.join(REPO_ROOT, "scripts", "uninline-resolutions.tsv")


def resolutions() -> dict[str, str]:
    if not os.path.exists(RESOLUTIONS):
        return {}
    out: dict[str, str] = {}
    for line in open(RESOLUTIONS, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        path, _, reason = line.rstrip("\n").partition("\t")
        out[path] = reason
    return out


def envelopes(domain: str | None = None) -> list[str]:
    found: list[str] = []
    for pattern in ROOTS:
        found.extend(glob.glob(os.path.join(REPO_ROOT, pattern)))
    found = sorted(found)
    if domain:
        needle = f"/{domain}/"
        found = [p for p in found if needle in p]
    return found


def survey(paths: list[str]):
    """Classify every inlined block. Returns (counter, rows, missing_files)."""
    counter: collections.Counter[str] = collections.Counter()
    rows: list[tuple[str, str, str]] = []
    missing: list[tuple[str, str]] = []
    for envelope in paths:
        text = open(envelope, encoding="utf-8", errors="replace").read()
        blocks = list(inlined_blocks(text))
        if not blocks:
            continue
        envelope_norm = normalise(text)
        slug_dir = os.path.dirname(envelope)
        for rel, block in blocks:
            path = os.path.join(slug_dir, rel)
            if not os.path.exists(path):
                missing.append((envelope, rel))
                counter["names-a-file-that-does-not-exist"] += 1
                rows.append((envelope, rel, "names-a-file-that-does-not-exist"))
                continue
            verdict = classify(
                block, open(path, encoding="utf-8", errors="replace").read(),
                rel, envelope_norm)
            counter[verdict] += 1
            rows.append((envelope, rel, verdict))
    return counter, rows, missing


def rel(path: str) -> str:
    return os.path.relpath(path, REPO_ROOT)


def cmd_report(args) -> int:
    paths = envelopes(args.domain)
    counter, rows, _missing = survey(paths)
    total = sum(counter.values())
    print(f"envelopes scanned:  {len(paths)}")
    print(f"inlined blocks:     {total}")
    for verdict, count in counter.most_common():
        mark = " " if verdict in LOSSLESS else "!"
        print(f"  {mark} {count:5}  {verdict}")
    recorded = resolutions()
    unresolved = [r for r in rows if r[2] not in LOSSLESS
                  and f"{rel(os.path.dirname(r[0]))}/{r[1]}" not in recorded]
    resolved = sum(1 for r in rows if r[2] not in LOSSLESS
                   and f"{rel(os.path.dirname(r[0]))}/{r[1]}" in recorded)
    if resolved:
        print(f"\n{resolved} of those carry a recorded resolution in "
              f"{rel(RESOLUTIONS)}")
    if unresolved:
        print(f"\n{len(unresolved)} block(s) need a recorded resolution before --write:")
        for envelope, name, verdict in unresolved:
            print(f"  {verdict}\t{rel(os.path.dirname(envelope))}/{name}")
    if args.list:
        print()
        for envelope, name, verdict in rows:
            print(f"{verdict}\t{rel(os.path.dirname(envelope))}/{name}")
    return 0


def template_hashes() -> dict[str, str]:
    """Path → sha256 for every file under a `templates/` dir. AC3's baseline."""
    out: dict[str, str] = {}
    for base in ("skills/faion/knowledge", "skills/faion/playbooks", "skills/faion/workflows"):
        for dirpath, _dirnames, filenames in os.walk(os.path.join(REPO_ROOT, base)):
            if "templates" not in dirpath.split(os.sep):
                continue
            for name in filenames:
                full = os.path.join(dirpath, name)
                with open(full, "rb") as fh:
                    out[rel(full)] = hashlib.sha256(fh.read()).hexdigest()
    return out


def cmd_write(args) -> int:
    paths = envelopes(args.domain)
    counter, rows, _missing = survey(paths)
    recorded = resolutions()
    unresolved = [r for r in rows if r[2] not in LOSSLESS
                  and f"{rel(os.path.dirname(r[0]))}/{r[1]}" not in recorded]
    if unresolved:
        print(f"refusing to write: {len(unresolved)} block(s) with no recorded "
              f"resolution. Run --report, read each diff, and record the reason in "
              f"{rel(RESOLUTIONS)}.", file=sys.stderr)
        for envelope, name, _verdict in unresolved[:10]:
            print(f"  {rel(os.path.dirname(envelope))}/{name}", file=sys.stderr)
        return 1

    before = template_hashes()
    changed = 0
    for envelope in paths:
        text = open(envelope, encoding="utf-8", errors="replace").read()
        if not list(inlined_blocks(text)):
            continue
        after_heading = trailing_heading_after_section(text)
        if after_heading:
            print(f"refusing {rel(envelope)}: a section follows the inlined region "
                  f"({after_heading}) — cutting to end of file would take it too",
                  file=sys.stderr)
            return 1
        new = strip_section(text)
        if new != text:
            open(envelope, "w", encoding="utf-8").write(new)
            changed += 1

    after = template_hashes()
    if before != after:
        added = sorted(set(after) - set(before))
        removed = sorted(set(before) - set(after))
        modified = sorted(p for p in set(before) & set(after) if before[p] != after[p])
        print("ABORT: templates/ is not byte-identical (AC3)", file=sys.stderr)
        for label, items in (("added", added), ("removed", removed), ("modified", modified)):
            for item in items[:10]:
                print(f"  {label}: {item}", file=sys.stderr)
        return 1

    print(f"un-inlined {sum(counter.values())} block(s) from {changed} envelope(s); "
          f"{len(after)} files under templates/ unchanged")
    return 0


TEMPLATE_ROW = re.compile(r"(?m)^\|\s*`(templates/[^`]+)`\s*\|")


def cmd_measure(args) -> int:
    """AC2 and AC5 in one pass: what the envelopes weigh, and which rows lie.

    The envelope is read during retrieval, so its total is the number the
    reversal is for, and the worst case is what a single unlucky search pays.
    """
    paths = envelopes(args.domain)
    total = 0
    worst = ("", 0)
    dangling: list[str] = []
    for envelope in paths:
        text = open(envelope, encoding="utf-8", errors="replace").read()
        size = len(text.encode("utf-8"))
        total += size
        if size > worst[1]:
            worst = (rel(envelope), size)
        slug_dir = os.path.dirname(envelope)
        for row in TEMPLATE_ROW.findall(text):
            if not os.path.exists(os.path.join(slug_dir, row)):
                dangling.append(f"{rel(slug_dir)}/{row}")
    print(f"envelopes:        {len(paths)}")
    print(f"envelope total:   {total / 1024 / 1024:.2f} MB")
    print(f"worst case:       {worst[1] / 1024:.1f} KB  ({worst[0]})")
    print(f"dangling rows:    {len(dangling)}")
    for row in dangling[:20]:
        print(f"  {row}")
    if len(dangling) > 20:
        print(f"  … and {len(dangling) - 20} more")
    return 0


def cmd_check(args) -> int:
    """AC1 as a permanent gate: no envelope carries the body of its own template."""
    paths = envelopes(args.domain)
    counter, rows, _missing = survey(paths)
    copies = [r for r in rows if r[2] != "names-a-file-that-does-not-exist"]
    if not copies:
        print(f"no inlined template bodies in {len(paths)} envelope(s)")
        return 0
    print(f"{len(copies)} inlined template body/bodies still in the envelopes:",
          file=sys.stderr)
    for envelope, name, _verdict in copies[:20]:
        print(f"  {rel(os.path.dirname(envelope))}/{name}", file=sys.stderr)
    if len(copies) > 20:
        print(f"  … and {len(copies) - 20} more", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--report", action="store_true", help="classify, write nothing")
    mode.add_argument("--write", action="store_true", help="remove the inlined region")
    mode.add_argument("--check", action="store_true", help="exit 1 if any body is inlined")
    mode.add_argument("--measure", action="store_true",
                      help="envelope total, worst case, and `## Templates` rows naming no file")
    ap.add_argument("--domain", help="restrict to one domain directory, for reviewable batches")
    ap.add_argument("--list", action="store_true", help="report: print every block")
    args = ap.parse_args()
    if args.report:
        return cmd_report(args)
    if args.write:
        return cmd_write(args)
    if args.measure:
        return cmd_measure(args)
    return cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
