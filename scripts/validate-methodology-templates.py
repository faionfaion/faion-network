#!/usr/bin/env python3
"""F-066 B3 validator: methodology templates discipline.

Rules per checklist B3.1..B3.5:
  B3.1 every file listed in AGENTS.md `## Templates` table exists in <dir>/templates/
  B3.2 templates are non-empty (heuristic: >50 bytes, not literal TBD placeholder)
  B3.3 each starts with a 5-line header (purpose / consumes / produces / depends-on / token-budget-impact)
  B3.6 a declared `variables:` block is shape-checked (AD-025 / retrieval-content-contracts.md §2.2):
       name pattern, type enum, required, enum implies options, sensitive implies
       placeholder, description under 240 chars. Absence means a static template
       on the unchanged delivery path, so nothing fires unless an author opted in.
       The block is read from the HEADER region only — the whole file would match
       every GitLab CI, Compose and Ansible template, whose `variables:` is theirs.

Note: this validator only reads the `## Templates` H2 section in the
AGENTS.md body — it never parses meta.json. The body-section check is
independent of the meta.json layout.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "skills" / "faion" / "knowledge"

HEADER_KEYS = ("purpose", "consumes", "produces", "depends-on", "token-budget-impact")

# Files whose syntax has no comment form for headers; we allow a __faion_header__ key inside.
JSON_LIKE = {".json"}


def _templates_listed(agents_md: Path) -> list[str]:
    if not agents_md.exists():
        return []
    text = agents_md.read_text(encoding="utf-8", errors="replace")
    # find ## Templates section, parse the table
    m = re.search(r"(?ms)^## Templates\s*\n(.*?)(?:^## |\Z)", text)
    if not m:
        return []
    body = m.group(1)
    files: list[str] = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if not cols or cols[0].lower() in ("file", "---", ""):
            continue
        cell = cols[0].strip("`")
        if cell and "/" in cell:
            files.append(cell)
    return files


def _has_header(p: Path) -> bool:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False
    head = "\n".join(text.splitlines()[:20]).lower()
    found = sum(1 for k in HEADER_KEYS if k in head)
    if p.suffix in JSON_LIKE:
        return "__faion_header__" in text
    return found >= 3  # tolerant: at least 3/5 keys present somewhere in first 20 lines


VAR_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
VAR_TYPES = {"string", "integer", "boolean", "enum", "path"}


def _header_block(text: str, suffix: str) -> str:
    """The header region only — never the whole file.

    `variables:` extends the header (retrieval-content-contracts.md §2.2), so
    it has to be read from inside it. Scanning the whole file instead would
    flag every GitLab CI, Compose and Ansible template in the corpus, each of
    which has a `variables:` key of its own that means something else entirely.
    """
    if suffix in JSON_LIKE:
        return text if "__faion_header__" in text else ""
    lines = text.splitlines()
    # The header is the leading comment region: everything up to the first line
    # that is neither blank nor comment-like nor inside an open block comment.
    out, in_block = [], False
    for line in lines[:40]:
        s = line.strip()
        if s.startswith("<!--") or s.startswith("/*"):
            in_block = True
        if in_block or s.startswith("#") or s.startswith("//") or not s:
            out.append(line)
            if s.endswith("-->") or s.endswith("*/"):
                in_block = False
            continue
        break
    return "\n".join(out)


def _variable_findings(p: Path, header: str) -> list[str]:
    """Shape-check a declared `variables:` block. Absence means a static
    template on the unchanged delivery path, which is the documented default —
    so nothing here fires unless an author opted in."""
    if not re.search(r"(?im)^\s*\W*\s*variables\s*:", header):
        return []
    errs: list[str] = []
    entries = re.findall(r"(?ms)^\s*\W*\s*-\s+name\s*:\s*(\S+)(.*?)(?=^\s*\W*\s*-\s+name\s*:|\Z)",
                         header)
    if not entries:
        return [f"{p.name}: declares 'variables:' with no '- name:' entry"]
    for name, body in entries:
        name = name.strip().strip("\"'")
        if not VAR_NAME.match(name):
            errs.append(f"{p.name}: variable {name!r} does not match ^[a-z][a-z0-9_]{{0,63}}$")
        def field(key: str) -> str | None:
            m = re.search(rf"(?im)^\s*\W*\s*{key}\s*:\s*(.+)$", body)
            return m.group(1).strip().strip("\"'") if m else None
        vtype, required = field("type"), field("required")
        if vtype is None:
            errs.append(f"{p.name}: variable {name!r} has no 'type'")
        elif vtype not in VAR_TYPES:
            errs.append(f"{p.name}: variable {name!r} type {vtype!r} is not one of "
                        f"{', '.join(sorted(VAR_TYPES))}")
        if required is None:
            errs.append(f"{p.name}: variable {name!r} has no 'required'")
        if vtype == "enum" and field("options") is None:
            errs.append(f"{p.name}: variable {name!r} is an enum with no 'options'")
        if (field("sensitive") or "").lower() == "true" and field("placeholder") is None:
            errs.append(f"{p.name}: variable {name!r} is sensitive with no 'placeholder' — "
                        "a sensitive value never travels, so the server needs something to emit")
        desc = field("description")
        if desc is None:
            errs.append(f"{p.name}: variable {name!r} has no 'description'")
        elif len(desc) > 240:
            errs.append(f"{p.name}: variable {name!r} description is {len(desc)} chars, "
                        "over the 240 cap a human reads under an AskUserQuestion prompt")
    return errs


def validate_dir(dir_path: Path) -> list[str]:
    errs: list[str] = []
    listed = _templates_listed(dir_path / "AGENTS.md")
    if not listed:
        return errs  # nothing declared → nothing to check
    for f in listed:
        # paths in AGENTS.md are written as `templates/foo.ext`
        path = dir_path / f
        if not path.exists():
            errs.append(f"declared template missing: {f}")
            continue
        if path.stat().st_size < 50:
            errs.append(f"template too small (<50 bytes): {f}")
            continue
        if not _has_header(path):
            errs.append(f"template missing 5-line header (purpose/consumes/produces/depends-on/token-budget-impact): {f}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        errs.extend(_variable_findings(path, _header_block(text, path.suffix)))
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    targets: list[Path]
    if args.all:
        targets = [p.parent for p in KNOWLEDGE.rglob("AGENTS.md")]
    else:
        if not args.target:
            ap.error("provide target dir or --all")
        targets = [Path(args.target).resolve()]

    def _display(p: Path) -> str:
        try:
            return str(p.relative_to(REPO_ROOT))
        except ValueError:
            return str(p)

    fail = 0
    for d in targets:
        errs = validate_dir(d)
        if errs:
            fail += 1
            print(f"FAIL {_display(d)}")
            for e in errs:
                print(f"  - {e}")
        elif not args.all:
            print(f"PASS {_display(d)}")
    if args.all:
        print(f"\nsummary: {len(targets)-fail} pass / {fail} fail / {len(targets)} total")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
