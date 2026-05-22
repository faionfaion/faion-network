# purpose: HTMLChunker using BeautifulSoup for semantic sectioning elements
# consumes: HTML text, max/min chunk sizes, version
# produces: list[dict] of chunks per templates/doc-chunk-schema.json
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: small
"""HTMLChunker — DOM-walk via BeautifulSoup; never regex over HTML."""
from __future__ import annotations

import hashlib

from bs4 import BeautifulSoup


class HTMLChunker:
    SECTION_SELECTORS = ("section", "article", "main")

    def __init__(self, max_chunk_size: int = 1000, min_chunk_size: int = 100, version: str = "1.0.0") -> None:
        self.max = max_chunk_size
        self.min = min_chunk_size
        self.version = version

    def chunk(self, html: str, source: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        sections = []
        for sel in self.SECTION_SELECTORS:
            sections.extend(soup.find_all(sel))
        if not sections:
            sections = [soup]
        chunks: list[dict] = []
        for sec in sections:
            heading = sec.find(["h1", "h2", "h3", "h4"])
            header_path = heading.get_text(strip=True) if heading else ""
            body = sec.get_text("\n", strip=True)
            if not body:
                continue
            if len(body.split()) <= self.max:
                chunks.append(self._record(source, header_path, None, body))
            else:
                parts = self._sub_split(body, self.max)
                for i, p in enumerate(parts):
                    chunks.append(self._record(source, header_path, i, p))
        return chunks

    def _sub_split(self, body: str, size: int) -> list[str]:
        words = body.split()
        return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]

    def _record(self, source: str, header_path: str, part_index: int | None, body: str) -> dict:
        section_id = header_path.lower().replace(" ", "-")
        text = f"{header_path}\n\n{body}" if header_path else body
        key = f"{source}|{section_id}|{part_index}|html@{self.version}"
        return {
            "id": hashlib.md5(key.encode("utf-8")).hexdigest(),
            "text": text,
            "header_path": header_path,
            "section_id": section_id,
            "token_count": len(text.split()),
            "source": source,
            "strategy": "html",
            "version": self.version,
            "part_index": part_index,
        }
