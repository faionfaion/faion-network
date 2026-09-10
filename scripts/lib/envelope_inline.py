"""Shared reader for the `## Template Contents` inlined blocks (F-077).

P0.4 pasted every template body into its slug's `AGENTS.md` as a fenced block
under a `## Template Contents` heading. The envelope is read during *retrieval*,
so that body is paid on every search that surfaces the slug — and since
`packablePath` admits anything under a `templates/` segment, the same bytes also
ship as a file. F-077 removes the blocks and leaves the files alone.

The normalisation and header-stripping here replicate
`faion-cli/tools/vfs-pack/doubleship.go` line for line, deliberately: that guard
is what asserts the result, and a second rule of our own would drift from it
silently. Two constants matter — a body under `MIN_NORMALISED_BYTES` is not
evidence of a copy, and the authored header comes off before comparing, which on
the real corpus was the difference between 12 findings and 2,698.
"""
from __future__ import annotations

import json
import os
import re

MIN_NORMALISED_BYTES = 40

HEADER_KEYS = ("purpose", "consumes", "produces", "depends-on", "token-budget-impact")
JSON_HEADER_KEY = "__faion_header__"
COMMENT_PREFIXES = ("<!--", "/*", "//", "#", "--", ";", "%", "*")
TERMINATORS = ("-->", "*/", '"""', "'''")

# The heading that opens the inlined region, and the per-file blocks inside it.
SECTION_HEADING = re.compile(r"(?m)^## Template Contents[ \t]*$")
BLOCK = re.compile(r"(?ms)^### `([^`]+)`\s*\n+```[^\n]*\n(.*?)\n?```")

# The sentence the inliner added to the `## Templates` section to point at the
# region. It stops being true the moment the region is gone.
POINTER = re.compile(
    r"(?m)^Files the packer does not ship standalone have their bodies inlined "
    r"under `## Template Contents` at the end of this file[^\n]*\n+")


def normalise(text: str) -> str:
    """Trim every line, drop the blank ones. A re-indented copy is still a copy."""
    out = []
    for line in text.replace("\r\n", "\n").split("\n"):
        stripped = line.strip()
        if stripped:
            out.append(stripped)
    return "\n".join(out)


def _is_header_line(line: str) -> bool:
    t = line.strip()
    for prefix in COMMENT_PREFIXES:
        if t.startswith(prefix):
            t = t[len(prefix):].strip()
    t = t.lstrip("\"'").strip()
    for key in HEADER_KEYS:
        if len(t) > len(key) and t[:len(key)].lower() == key and t[len(key):].lstrip().startswith(":"):
            return True
    return False


def strip_authored_header(norm: str) -> str:
    """Remove the five-key header from an already-normalised body.

    Both spellings: the leading comment run (below a shebang, which sits above
    the header in every shell and python template), and the JSON member, which
    is removed where it sits rather than from the front.
    """
    if not norm:
        return norm
    lines = norm.split("\n")
    i = 1 if lines[0].startswith("#!") else 0
    while i < len(lines) and _is_header_line(lines[i]):
        i += 1
    while i < len(lines) and lines[i].strip() in TERMINATORS:
        i += 1
    lines = lines[i:]
    for j in range(min(8, len(lines))):
        if JSON_HEADER_KEY not in lines[j]:
            continue
        if lines[j].count("{") == 0:
            del lines[j]
            break
        depth = lines[j].count("{") - lines[j].count("}")
        k = j
        while depth > 0 and k + 1 < len(lines):
            k += 1
            depth += lines[k].count("{") - lines[k].count("}")
        del lines[j:k + 1]
        break
    return "\n".join(lines)


def inlined_blocks(envelope_text: str):
    """Yield `(relative_path, block_body)` for every inlined block, or nothing."""
    match = SECTION_HEADING.search(envelope_text)
    if not match:
        return
    for rel, block in BLOCK.findall(envelope_text[match.end():]):
        yield rel, block


def _squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _drop_json_header(obj):
    if isinstance(obj, dict):
        return {k: _drop_json_header(v) for k, v in obj.items() if k != JSON_HEADER_KEY}
    if isinstance(obj, list):
        return [_drop_json_header(v) for v in obj]
    return obj


def _as_data(text: str, ext: str):
    if ext in (".json", ".webmanifest"):
        return _drop_json_header(json.loads(text))
    if ext == ".jsonl":
        return [_drop_json_header(json.loads(l)) for l in text.splitlines() if l.strip()]
    if ext in (".yaml", ".yml"):
        import yaml  # optional; absence just falls through to the text tests
        return _drop_json_header(yaml.safe_load(text))
    raise ValueError(ext)


def classify(block: str, file_text: str, rel: str, envelope_norm: str) -> str:
    """Why removing this block loses nothing — or `unresolved` if it might.

    The tests run cheapest first and each one names a reason a delete is
    lossless. `unresolved` is not a verdict of loss; it is a case for the eye,
    which is the whole point of running this as a report before a rewrite.
    """
    body = strip_authored_header(normalise(file_text))
    if len(body) < MIN_NORMALISED_BYTES:
        return "too-short-to-compare"
    if body in envelope_norm:
        return "faithful-copy"
    ext = os.path.splitext(rel)[1].lower()
    try:
        if _as_data(file_text, ext) == _as_data(block, ext):
            return "same-data-different-wrapping"
    except Exception:
        pass
    block_norm = normalise(block)
    if _squash(body) == _squash(block_norm):
        return "same-characters-different-line-breaks"
    if _squash(normalise(file_text)) == _squash(block_norm):
        return "block-kept-the-authored-header"
    if _squash(block_norm) in _squash(normalise(file_text)):
        return "block-is-a-substring-of-the-file"
    return "unresolved"


def strip_section(envelope_text: str) -> str:
    """Remove the `## Template Contents` region and the sentence pointing at it.

    The region runs to end of file: the inliner appended it, and no envelope in
    the corpus carries a section after it. Asserted by the caller rather than
    assumed here — `--write` refuses an envelope where a later `## ` heading
    exists, instead of silently deleting whatever followed.
    """
    match = SECTION_HEADING.search(envelope_text)
    if not match:
        return envelope_text
    head = envelope_text[:match.start()].rstrip() + "\n"
    return POINTER.sub("", head)


def trailing_heading_after_section(envelope_text: str) -> str | None:
    """The first `## ` heading below `## Template Contents`, if any."""
    match = SECTION_HEADING.search(envelope_text)
    if not match:
        return None
    for line in envelope_text[match.end():].split("\n"):
        if line.startswith("## "):
            return line.strip()
    return None
