# purpose: ChunkingService orchestration layer with dispatch + fallback + metadata propagation
# consumes: ChunkingConfig + sub-chunkers dict + per-document text + metadata
# produces: envelope dict {requested_strategy, strategy_used, chunk_count, chunks, warnings}
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: small
"""ChunkingService — production wrapper with fail-fast config + logged fallback."""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Callable

logger = logging.getLogger("chunking_service")


class Strategy(str, Enum):
    FIXED = "fixed"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    MARKDOWN = "markdown"
    HTML = "html"
    CODE = "code"


@dataclass
class ChunkingConfig:
    strategy: Strategy = Strategy.RECURSIVE
    chunk_size: int = 500
    overlap: int = 50
    min_chunk_size: int = 100
    embedding_func: Callable[[str], list[float]] | None = None
    version: str = "1.0.0"


class ChunkingService:
    def __init__(self, config: ChunkingConfig, sub_chunkers: dict[Strategy, object]) -> None:
        if not isinstance(config.strategy, Strategy):
            raise ValueError("strategy must be Strategy enum")
        if config.strategy is Strategy.SEMANTIC and config.embedding_func is None:
            raise ValueError("SEMANTIC requires embedding_func at __init__")
        if config.overlap >= config.chunk_size:
            raise ValueError("overlap must be < chunk_size")
        if config.strategy not in sub_chunkers:
            raise ValueError(f"no sub-chunker registered for {config.strategy}")
        self.cfg = config
        self.sub = sub_chunkers

    def chunk(self, text: str, source: str, metadata: dict | None = None) -> dict:
        meta = dict(metadata or {})
        warnings: list[dict] = []
        try:
            chunks = self.sub[self.cfg.strategy].chunk(text, source)
            strategy_used = self.cfg.strategy.value
        except Exception as exc:
            logger.warning(
                "chunker failure -> fallback",
                extra={"source": source, "requested_strategy": self.cfg.strategy.value, "exception": str(exc)},
            )
            chunks = self._word_split(text, source)
            strategy_used = "fallback"
            warnings.append({
                "source": source, "requested_strategy": self.cfg.strategy.value, "exception": str(exc),
            })
        for c in chunks:
            chunk_meta = c.get("metadata") or {}
            chunk_meta.update(meta)
            c["metadata"] = chunk_meta
            c["strategy_used"] = strategy_used
        return {
            "requested_strategy": self.cfg.strategy.value,
            "strategy_used": strategy_used,
            "chunk_count": len(chunks),
            "chunks": chunks,
            "warnings": warnings,
        }

    def _word_split(self, text: str, source: str) -> list[dict]:
        words = text.split()
        records: list[dict] = []
        for i, start in enumerate(range(0, len(words), self.cfg.chunk_size)):
            body = " ".join(words[start:start + self.cfg.chunk_size])
            key = f"{source}|{i}|fallback@{self.cfg.version}"
            records.append({
                "id": hashlib.md5(key.encode("utf-8")).hexdigest(),
                "text": body, "token_count": len(body.split()),
                "source": source, "strategy_used": "fallback",
                "version": self.cfg.version, "metadata": {},
            })
        return records
