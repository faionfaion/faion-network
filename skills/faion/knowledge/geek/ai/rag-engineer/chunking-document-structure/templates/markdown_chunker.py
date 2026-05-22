# purpose: MarkdownChunker with header_path propagation
# consumes: markdown text, max/min chunk sizes, version
# produces: list[dict] of chunks per templates/doc-chunk-schema.json
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: small
"""MarkdownChunker — header-aware splitter that propagates parent header_path into every chunk."""
from __future__ import annotations

import hashlib
import re

HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$")


class MarkdownChunker:
    def __init__(self, max_chunk_size: int = 1000, min_chunk_size: int = 100, version: str = "1.0.0") -> None:
        self.max = max_chunk_size
        self.min = min_chunk_size
        self.version = version

    def chunk(self, text: str, source: str) -> list[dict]:
        path_stack: list[tuple[int, str]] = []
        sections: list[tuple[str, str]] = []
        buf: list[str] = []
        current_path = ""
        for line in text.splitlines():
            m = HEADER_RE.match(line)
            if m:
                if buf:
                    sections.append((current_path, "\n".join(buf).strip()))
                    buf = []
                depth = len(m.group(1))
                title = m.group(2).strip()
                while path_stack and path_stack[-1][0] >= depth:
                    path_stack.pop()
                path_stack.append((depth, title))
                current_path = " > ".join(t for _, t in path_stack)
            else:
                buf.append(line)
        if buf:
            sections.append((current_path, "\n".join(buf).strip()))

        chunks: list[dict] = []
        for header_path, body in sections:
            if not body:
                continue
            if len(body.split()) <= self.max:
                chunks.append(self._record(source, header_path, None, body))
            else:
                parts = self._sub_split(body, self.max)
                for i, p in enumerate(parts):
                    chunks.append(self._record(source, header_path, i, p))
        return self._merge_below_min(chunks)

    def _sub_split(self, body: str, size: int) -> list[str]:
        words = body.split()
        return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]

    def _record(self, source: str, header_path: str, part_index: int | None, body: str) -> dict:
        section_id = re.sub(r"[^a-z0-9-]", "-", header_path.lower())
        text = f"{header_path}\n\n{body}" if header_path else body
        key = f"{source}|{section_id}|{part_index}|markdown@{self.version}"
        return {
            "id": hashlib.md5(key.encode("utf-8")).hexdigest(),
            "text": text,
            "header_path": header_path,
            "section_id": section_id,
            "token_count": len(text.split()),
            "source": source,
            "strategy": "markdown",
            "version": self.version,
            "part_index": part_index,
        }

    def _merge_below_min(self, chunks: list[dict]) -> list[dict]:
        out: list[dict] = []
        for c in chunks:
            if out and c["token_count"] < self.min and out[-1]["header_path"] == c["header_path"]:
                out[-1]["text"] += "\n\n" + c["text"].split("\n\n", 1)[-1]
                out[-1]["token_count"] += c["token_count"]
            else:
                out.append(c)
        return out
