# purpose: Chunker — multi-strategy text splitter with token-based sizing + overlap.
# consumes: chunking-config.json + tokenizer
# produces: list[{id, text, parent_doc_id, token_count}]
# depends-on: content/01-core-rules.xml r1, r2, r3, r5
# token-budget-impact: 0 LLM tokens; tokenization only
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ChunkingConfig:
    strategy: str = "recursive"
    size_unit: str = "tokens"
    chunk_size: int = 512
    overlap_tokens: int = 64
    min_tokens: int = 60
    max_tokens: int = 1024


@dataclass
class Chunker:
    config: ChunkingConfig
    tokenize: Callable[[str], list[str]]
    detokenize: Callable[[list[str]], str]

    def __post_init__(self) -> None:
        if self.config.size_unit != "tokens":
            raise ValueError("size_unit must be tokens (rule r1)")
        if self.config.min_tokens < 50:
            raise ValueError("min_tokens must be >=50 (rule r5)")
        if self.config.overlap_tokens > self.config.chunk_size // 2:
            raise ValueError("overlap_tokens must be <= chunk_size/2")

    def _fixed_token_chunks(self, tokens: list[str]) -> list[list[str]]:
        out: list[list[str]] = []
        step = max(1, self.config.chunk_size - self.config.overlap_tokens)
        for start in range(0, len(tokens), step):
            chunk = tokens[start : start + self.config.chunk_size]
            if len(chunk) < self.config.min_tokens and out:
                break
            out.append(chunk)
        return out

    def _recursive_chunks(self, text: str) -> list[str]:
        # split on paragraphs, then sentences, then tokens
        paras = re.split(r"\n{2,}", text)
        result: list[str] = []
        buffer: list[str] = []
        token_count = 0
        for para in paras:
            ptoks = self.tokenize(para)
            if token_count + len(ptoks) <= self.config.chunk_size:
                buffer.append(para)
                token_count += len(ptoks)
            else:
                if buffer:
                    result.append("\n\n".join(buffer))
                # overlap tail
                tail_tokens = self.tokenize("\n\n".join(buffer))[-self.config.overlap_tokens :] if buffer else []
                buffer = [self.detokenize(tail_tokens), para] if tail_tokens else [para]
                token_count = len(tail_tokens) + len(ptoks)
        if buffer:
            result.append("\n\n".join(buffer))
        return result

    def split(self, doc: dict[str, Any]) -> list[dict[str, Any]]:
        text = doc["text"]
        doc_id = doc["id"]
        if self.config.strategy == "fixed_token":
            chunks = [self.detokenize(c) for c in self._fixed_token_chunks(self.tokenize(text))]
        else:
            chunks = self._recursive_chunks(text)
        return [
            {
                "id": f"{doc_id}::{i}",
                "parent_doc_id": doc_id,
                "text": ch,
                "token_count": len(self.tokenize(ch)),
            }
            for i, ch in enumerate(chunks)
        ]
