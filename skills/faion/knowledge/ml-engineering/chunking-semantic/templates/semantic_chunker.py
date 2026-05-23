# purpose: semantic chunker using cosine similarity between sentence embeddings
# consumes: text, embedding_func, similarity_threshold, max/min size, version
# produces: list[dict] of semantic chunks per templates/semantic-chunk-schema.json
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: medium (one embed call per sentence at index time)
"""SemanticChunker — adjacent-sentence cosine boundary detector with size guards."""
from __future__ import annotations

import hashlib
from typing import Callable

import nltk
import numpy as np


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


class SemanticChunker:
    def __init__(
        self,
        embedding_func: Callable[[str], list[float]],
        embedding_model: str,
        similarity_threshold: float = 0.75,
        max_chunk_size: int = 1000,
        min_chunk_size: int = 100,
        version: str = "1.0.0",
    ) -> None:
        if not 0.6 <= similarity_threshold <= 0.85:
            raise ValueError("similarity_threshold must be in [0.6, 0.85]")
        self.embed = embedding_func
        self.model = embedding_model
        self.th = similarity_threshold
        self.max = max_chunk_size
        self.min = min_chunk_size
        self.version = version

    def chunk(self, text: str, source: str) -> list[dict]:
        sentences = [s for s in nltk.sent_tokenize(text) if s.strip()]
        if len(sentences) <= 1:
            if not sentences:
                return []
            return [self._record(source, 0, sentences, 1)]
        embeddings = [np.array(self.embed(s)) for s in sentences]
        boundaries = [i + 1 for i in range(len(embeddings) - 1) if _cosine(embeddings[i], embeddings[i + 1]) < self.th]
        groups: list[list[str]] = []
        start = 0
        for b in boundaries:
            groups.append(sentences[start:b])
            start = b
        groups.append(sentences[start:])
        chunks: list[dict] = []
        for idx, grp in enumerate(groups):
            chunks.append(self._record(source, idx, grp, len(grp)))
        return self._apply_size_guards(chunks)

    def _record(self, source: str, idx: int, sentences: list[str], sentence_count: int) -> dict:
        body = " ".join(sentences)
        key = f"{source}|{idx}|semantic@{self.version}"
        return {
            "id": hashlib.md5(key.encode("utf-8")).hexdigest(),
            "text": body,
            "embedding_model": self.model,
            "similarity_threshold": self.th,
            "token_count": len(body.split()),
            "source": source,
            "strategy": "semantic",
            "version": self.version,
            "sentence_count": sentence_count,
        }

    def _apply_size_guards(self, chunks: list[dict]) -> list[dict]:
        out: list[dict] = []
        for c in chunks:
            if c["token_count"] > self.max:
                words = c["text"].split()
                for j in range(0, len(words), self.max):
                    sub = dict(c)
                    sub["text"] = " ".join(words[j:j + self.max])
                    sub["token_count"] = len(sub["text"].split())
                    out.append(sub)
            elif out and c["token_count"] < self.min:
                out[-1]["text"] += " " + c["text"]
                out[-1]["token_count"] += c["token_count"]
            else:
                out.append(c)
        return out
