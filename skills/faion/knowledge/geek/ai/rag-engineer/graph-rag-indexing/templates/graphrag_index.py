# purpose: Runnable GraphRAG indexing pipeline skeleton
# consumes: inputs declared in AGENTS.md Prerequisites table
# produces: artefact conforming to content/02-output-contract.xml (graph-rag-indexing)
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~150-400 tokens when loaded as context
"""graphrag_index.py — end-to-end GraphRAG indexing pipeline.

Reads a JSONL doc corpus and writes a versioned GraphRAG index
(chunks + entities + graph + communities + summaries).
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Iterator


def chunk_id(doc_id: str, idx: int, content: str) -> str:
    """Deterministic chunk id — survives pipeline reruns."""
    h = hashlib.sha1(
        f"{doc_id}|{idx}|{hashlib.sha1(content.encode()).hexdigest()}".encode()
    ).hexdigest()
    return h[:16]


def iter_chunks(corpus: Path, chunk_size: int = 800) -> Iterator[dict]:
    for line in corpus.open():
        doc = json.loads(line)
        text = doc["text"]
        for i in range(0, len(text), chunk_size):
            seg = text[i:i + chunk_size]
            yield {
                "chunk_id": chunk_id(doc["doc_id"], i, seg),
                "doc_id": doc["doc_id"],
                "text": seg,
            }


def main(corpus_path: str, out_dir: str, version: str) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with (out / f"chunks.{version}.jsonl").open("w") as fh:
        for c in iter_chunks(Path(corpus_path)):
            fh.write(json.dumps(c) + "\n")
    # entity extraction + graph build + community detect + summarize
    # are wired here in the production pipeline.


if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2], sys.argv[3])
