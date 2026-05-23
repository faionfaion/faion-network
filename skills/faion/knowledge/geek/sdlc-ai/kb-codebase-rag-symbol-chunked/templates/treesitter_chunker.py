# purpose: reference tree-sitter symbol-boundary chunker for codebase RAG.
# consumes: repo file tree + tree-sitter grammars per language.
# produces: code (chunk-emitting Python module).
# depends-on: content/02-output-contract.xml (chunker-config schema), chunk_schema.json
# token-budget-impact: medium — ~900 tokens if loaded as reference.
"""Reference symbol-boundary chunker.

One chunk per top-level function / class / method. Padded with file path,
enclosing class signature, and preceding doc comment. Dependency:
`pip install tree-sitter-languages`.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from tree_sitter_languages import get_parser

CHUNK_KINDS = {
    "function_definition", "function_declaration",
    "method_definition", "class_definition",
    "class_declaration", "interface_declaration",
}


@dataclass(slots=True)
class Chunk:
    path: str
    symbol: str
    kind: str
    signature: str
    start_line: int
    end_line: int
    sha: str
    body: str
    language: str


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _kind(node_type: str) -> str:
    if "class" in node_type: return "class"
    if "interface" in node_type: return "interface"
    if "method" in node_type: return "method"
    return "function"


def _name(node, src: str) -> str:
    for c in node.children:
        if c.type in {"identifier", "type_identifier", "property_identifier"}:
            return src[c.start_byte:c.end_byte]
    return ""


def chunk_file(path: Path, language: str) -> Iterator[Chunk]:
    parser = get_parser(language)
    src = path.read_bytes()
    tree = parser.parse(src)
    text = src.decode("utf-8", errors="replace")
    lines = text.splitlines(keepends=True)

    def walk(node, enclosing: str = "") -> Iterator[Chunk]:
        if node.type in CHUNK_KINDS:
            sym = _name(node, text) or "<anonymous>"
            qual = f"{enclosing}.{sym}" if enclosing else sym
            s, e = node.start_point[0], node.end_point[0]
            body = "".join(lines[s:e + 1])
            sig = body.splitlines()[0].strip() if body else ""
            padded = f"# file: {path}\n# enclosing: {enclosing or '-'}\n{body}"
            yield Chunk(str(path), qual, _kind(node.type), sig,
                        s + 1, e + 1, _sha(body), padded, language)
        for c in node.children:
            yield from walk(c, enclosing or _name(node, text) or enclosing)

    yield from walk(tree.root_node)
