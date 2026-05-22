# purpose: code chunker with language dispatch (Python AST / tree-sitter / generic fallback)
# consumes: source text + language + version
# produces: list[dict] of chunk records per templates/code-chunk-schema.json
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: small (no LLM calls)
"""CodeChunker — AST-first dispatch with logged generic fallback."""
from __future__ import annotations

import ast
import hashlib
import logging

logger = logging.getLogger("chunking_code_ast")


class CodeChunker:
    def __init__(self, language: str = "python", version: str = "1.0.0", max_chunk_size: int = 800) -> None:
        self.language = language
        self.version = version
        self.max_chunk_size = max_chunk_size

    def chunk(self, code: str, source: str) -> list[dict]:
        if self.language == "python":
            return self._chunk_python(code, source)
        if self.language in {"javascript", "typescript"}:
            return self._chunk_generic(code, source, reason="tree-sitter-not-wired-in-template")
        return self._chunk_generic(code, source, reason="unsupported-language")

    def _chunk_python(self, code: str, source: str) -> list[dict]:
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            logger.warning("fallback to generic", extra={"file": source, "language": "python", "reason": f"SyntaxError: {exc}"})
            return self._chunk_generic(code, source, reason="syntax-error")
        lines = code.split("\n")
        records: list[dict] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start_line = node.lineno
                end_line = getattr(node, "end_lineno", start_line)
                text = "\n".join(lines[start_line - 1:end_line])
                kind = (
                    "class" if isinstance(node, ast.ClassDef)
                    else "async_function" if isinstance(node, ast.AsyncFunctionDef)
                    else "function"
                )
                records.append({
                    "id": self._cid(source, start_line),
                    "text": text,
                    "type": kind,
                    "name": node.name,
                    "docstring": ast.get_docstring(node) or "",
                    "start_line": start_line,
                    "end_line": end_line,
                    "language": "python",
                    "source": source,
                    "strategy": "ast",
                    "version": self.version,
                    "fallback": False,
                })
        return self._dedup(records)

    def _chunk_generic(self, code: str, source: str, reason: str) -> list[dict]:
        logger.warning("generic fallback", extra={"file": source, "language": self.language, "reason": reason})
        lines = code.split("\n")
        records: list[dict] = []
        buf: list[str] = []
        size = 0
        start_line = 1
        for i, line in enumerate(lines, start=1):
            buf.append(line)
            size += len(line.split())
            if size >= self.max_chunk_size:
                records.append(self._generic_record(source, start_line, i, "\n".join(buf)))
                buf, size, start_line = [], 0, i + 1
        if buf:
            records.append(self._generic_record(source, start_line, len(lines), "\n".join(buf)))
        return records

    def _generic_record(self, source: str, start: int, end: int, text: str) -> dict:
        return {
            "id": self._cid(source, start),
            "text": text, "type": "code_block", "name": "",
            "docstring": "", "start_line": start, "end_line": end,
            "language": "generic", "source": source,
            "strategy": "generic", "version": self.version, "fallback": True,
        }

    def _dedup(self, records: list[dict]) -> list[dict]:
        seen: set[tuple[str, int]] = set()
        keep: list[dict] = []
        # policy A: drop class chunk when its range fully contains other records
        class_records = [r for r in records if r["type"] == "class"]
        contained_lines: set[tuple[str, int]] = set()
        for c in class_records:
            for other in records:
                if other is c:
                    continue
                if other["source"] == c["source"] and c["start_line"] < other["start_line"] <= c["end_line"]:
                    contained_lines.add((c["source"], c["start_line"]))
        for r in records:
            key = (r["source"], r["start_line"])
            if (r["source"], r["start_line"]) in contained_lines:
                continue
            if key in seen:
                continue
            seen.add(key)
            keep.append(r)
        return keep

    def _cid(self, source: str, start_line: int) -> str:
        key = f"{source}|{start_line}|ast@{self.version}"
        return hashlib.md5(key.encode("utf-8")).hexdigest()
