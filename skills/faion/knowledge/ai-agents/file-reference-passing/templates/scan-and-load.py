# purpose: two-stage scan + load pattern (Pydantic + path validation)
# consumes: corpus manifest + goal
# produces: dict mapping path -> file contents (after validation)
# depends-on: pydantic v2, pathlib
# token-budget-impact: stage 1 ~200 tokens of manifest, stage 2 only-selected contents
"""Two-stage scan + load pattern.

Stage 1 (cheap model) sees only the manifest and picks refs.
Stage 2 (strong model) sees only the selected file contents.
The 200 corpus bodies (e.g. 80K tokens) never cross the LLM boundary
together; the cheap-model scan stage is fixed-cost on manifest size.
"""

from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel, Field


class ScanResult(BaseModel):
    rationale: str = Field(description="One sentence explaining the selection.")
    relevant_refs: list[str] = Field(
        description="Refs from the provided manifest only. Each ref must match `path:<rel>`."
    )


def validate_refs(refs: list[str], manifest_paths: set[str]) -> list[Path]:
    valid: list[Path] = []
    for r in refs:
        if not r.startswith("path:"):
            continue
        rel = r[len("path:"):]
        if rel in manifest_paths and Path(rel).exists():
            valid.append(Path(rel))
    return valid


def load_selected(refs: list[str], manifest_paths: set[str]) -> dict[Path, str]:
    paths = validate_refs(refs, manifest_paths)
    return {p: p.read_text(encoding="utf-8") for p in paths}
