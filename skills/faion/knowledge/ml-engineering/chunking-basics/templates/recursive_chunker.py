# purpose: recursive token-accurate chunker for prose RAG corpora
# consumes: raw text, chunk_size + overlap + tiktoken encoding name
# produces: list[dict] of chunk records matching templates/chunk-schema.json
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: small (no LLM calls)
"""Token-accurate recursive splitter with content-based IDs and metadata."""
from __future__ import annotations

import hashlib
from typing import Iterable

import tiktoken


class RecursiveChunker:
    """Splits prose into chunks of ~chunk_size tokens with `overlap` tokens of carry-over."""

    SEPARATORS: tuple[str, ...] = ("\n\n", "\n", ". ", " ", "")

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
        encoding: str = "cl100k_base",
        strategy: str = "recursive",
        version: str = "1.0.0",
    ) -> None:
        if not 0 <= overlap < chunk_size:
            raise ValueError("overlap must be in [0, chunk_size)")
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.enc = tiktoken.get_encoding(encoding)
        self.strategy = strategy
        self.version = version

    def chunk(self, text: str, source: str, page: int | None = None) -> list[dict]:
        token_ids = self.enc.encode(text)
        records: list[dict] = []
        start = 0
        index = 0
        while start < len(token_ids):
            end = min(start + self.chunk_size, len(token_ids))
            window = token_ids[start:end]
            chunk_text = self.enc.decode(window)
            records.append({
                "id": self._cid(source, index),
                "text": chunk_text,
                "token_count": len(window),
                "source": source,
                "page": page,
                "chunk_index": index,
                "strategy": self.strategy,
                "version": self.version,
                "overlap": self.overlap,
            })
            index += 1
            if end == len(token_ids):
                break
            start = end - self.overlap
        return records

    def _cid(self, source: str, index: int) -> str:
        key = f"{source}|{index}|{self.strategy}@{self.version}"
        return hashlib.md5(key.encode("utf-8")).hexdigest()


def chunks_to_jsonl(records: Iterable[dict]) -> str:
    import json
    return "\n".join(json.dumps(r, ensure_ascii=False) for r in records)
