#!/usr/bin/env python3
"""Faion knowledge retrieval orchestrator.

Spawns a read-only Claude Agent SDK subagent that picks methodology files
relevant to the current Claude Code session. Uses a custom in-process MCP
tool `submit_selection` to force schema-validated structured output.

The tool itself enforces the word budget: if the proposed selection exceeds
the budget, it returns `is_error=True` with per-file breakdown and the agent
retries in the same conversation. No fragile JSON parsing.

Usage:
    retrieve.py [<session-id>]

If session-id is empty or not found, falls back to the most recently
modified session JSONL across all projects.
"""

from __future__ import annotations

import asyncio
import copy
import json
import logging
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

try:
    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        ToolUseBlock,
        create_sdk_mcp_server,
        query,
        tool,
    )
except ImportError:
    print("# faion: claude-agent-sdk not installed. Run: pip install claude-agent-sdk")
    sys.exit(0)

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("# faion: jinja2 not installed. Run: pip install jinja2")
    sys.exit(0)


logger = logging.getLogger("faion.retrieve")


def _patch_sdk_parser() -> None:
    """Make SDK skip unknown message types (e.g. rate_limit_event) instead of crashing."""
    try:
        from claude_code_sdk._internal import client, message_parser  # pyright: ignore[reportPrivateImportUsage, reportMissingImports]
        _original = message_parser.parse_message  # pyright: ignore[reportPrivateImportUsage]

        def _safe_parse(data):
            try:
                return _original(data)
            except Exception:
                return None

        message_parser.parse_message = _safe_parse
        client.parse_message = _safe_parse
    except Exception:
        pass


_patch_sdk_parser()


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"
SKILL_ROOT = SCRIPT_DIR.parent
KNOWLEDGE_ROOT = SKILL_ROOT / "knowledge"
PLAYBOOKS_ROOT = SKILL_ROOT / "playbooks"
DOMAINS_L1_PATH = KNOWLEDGE_ROOT / "domains.xml"
TAXONOMY_L1_PATH = PLAYBOOKS_ROOT / "taxonomy.xml"

WORD_BUDGET = int(os.environ.get("FAION_WORD_BUDGET", "5000"))
MAX_TRANSCRIPT_PAIRS = int(os.environ.get("FAION_TRANSCRIPT_PAIRS", "40"))
MAX_AGENT_TURNS = int(os.environ.get("FAION_MAX_TURNS", "20"))
MODEL = os.environ.get("FAION_MODEL", "claude-sonnet-4-6")
L1_EMBED_WORD_CAP = int(os.environ.get("FAION_L1_WORD_CAP", "1500"))

_jinja = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(default_for_string=False),
    trim_blocks=False,
    lstrip_blocks=False,
    keep_trailing_newline=True,
)


def render(template_name: str, **ctx: Any) -> str:
    return _jinja.get_template(template_name).render(**ctx)


# ---- Methodology metadata (F-067: meta.json is the runtime source of truth) ----

# Keys F-067 promotes from AGENTS.md frontmatter into meta.json. See
# .aidocs/conventions/meta-json-spec.md for the canonical 14-key shape.
_META_KEYS = (
    "slug", "tier", "domain", "group", "version", "status", "last_reviewed",
    "maintainers", "summary", "content_id", "complexity", "produces",
    "est_tokens", "tags",
)


def _parse_agents_md_frontmatter(agents_md: Path) -> dict[str, Any] | None:
    """Best-effort YAML frontmatter parse without a YAML dependency.

    Reads only the leading `---`-delimited block. Handles flat `key: value`
    pairs, inline list syntax `[a, b]`, and bracketed scalars. Returns None
    if the file has no frontmatter or cannot be read.

    # F-067 transitional fallback; remove after T11.
    """
    if not agents_md.exists() or not agents_md.is_file():
        return None
    try:
        text = agents_md.read_text(errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    block = text[3:end].strip("\n")
    out: dict[str, Any] = {}
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        # Strip surrounding quotes on scalars.
        if (len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'")):
            value = value[1:-1]
        # Inline list: [a, b, c]
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            items = [
                item.strip().strip('"').strip("'")
                for item in inner.split(",") if item.strip()
            ] if inner else []
            out[key] = items
        elif value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
            out[key] = int(value)
        else:
            out[key] = value
    return out or None


def read_meta(methodology_dir: Path) -> dict[str, Any] | None:
    """Return methodology metadata as a dict.

    Reads `<methodology-dir>/meta.json` (the F-067 source of truth). If
    meta.json is missing, falls back to parsing YAML frontmatter from
    `<methodology-dir>/AGENTS.md` so the retriever keeps working during the
    F-067 cutover.

    Returns None when neither source yields any metadata.

    # F-067 transitional fallback; remove after T11.
    """
    meta_path = methodology_dir / "meta.json"
    if meta_path.exists() and meta_path.is_file():
        try:
            return json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass  # fall through to frontmatter
    # F-067 transitional fallback; remove after T11.
    return _parse_agents_md_frontmatter(methodology_dir / "AGENTS.md")


# ---- Two-level lookup: L1 index loaders ----

def _truncate_scope_first_sentence(xml_text: str) -> str:
    """Trim every <scope>...</scope> body to its first sentence.

    Used when the L1 embed exceeds the word cap. Conservative — keeps the
    <scope> tag intact, only shortens its inner text up to the first '.'.
    """
    import re

    def _trim(match: "re.Match[str]") -> str:
        body = match.group(1).strip()
        # Take up to and including the first period, then re-wrap.
        dot = body.find(".")
        first = body[: dot + 1].strip() if dot >= 0 else body
        return f"<scope>{first}</scope>"

    return re.sub(r"<scope>(.*?)</scope>", _trim, xml_text, flags=re.DOTALL)


def _load_l1_file(path: Path) -> str | None:
    """Defensive read of an L1 XML index. Returns None if missing or unparseable."""
    if not path.exists() or not path.is_file():
        return None
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return None
    # Sanity check: must contain at least one tag root, otherwise treat as missing.
    if "<" not in text:
        return None
    return text.strip()


def read_domains_l1() -> str | None:
    """Return parsed L1 domains.xml as text snippet for the system prompt.

    Backward-compat: returns None if the file is missing — retriever then
    falls back to the old single-pass behavior (no L1 embed, agent uses
    Glob/Grep from scratch).
    """
    return _load_l1_file(DOMAINS_L1_PATH)


def read_taxonomy_l1() -> str | None:
    """Return parsed L1 playbook taxonomy.xml as text snippet for the system prompt."""
    return _load_l1_file(TAXONOMY_L1_PATH)


def build_l1_embed(domains_xml: str | None, taxonomy_xml: str | None) -> tuple[str | None, str | None, int]:
    """Combine L1 indexes and enforce the word cap.

    Returns (domains_for_prompt, taxonomy_for_prompt, total_words).
    If combined word count exceeds L1_EMBED_WORD_CAP, <scope> bodies in
    domains.xml are truncated to a single sentence (taxonomy already terse).
    Either return value can be None when the source file is absent.
    """
    if domains_xml is None and taxonomy_xml is None:
        return None, None, 0

    def _wc(s: str | None) -> int:
        return len(s.split()) if s else 0

    total = _wc(domains_xml) + _wc(taxonomy_xml)
    if total <= L1_EMBED_WORD_CAP:
        return domains_xml, taxonomy_xml, total

    # Over cap — truncate domain scopes first (highest savings).
    trimmed_domains = (
        _truncate_scope_first_sentence(domains_xml) if domains_xml else None
    )
    total = _wc(trimmed_domains) + _wc(taxonomy_xml)
    return trimmed_domains, taxonomy_xml, total


# ---- Session transcript ----

def find_session_file(session_id: str) -> Path | None:
    base = Path.home() / ".claude" / "projects"
    if not base.exists():
        return None

    if session_id:
        for candidate in base.glob(f"**/{session_id}.jsonl"):
            return candidate

    candidates = [p for p in base.glob("**/*.jsonl") if p.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda f: f.stat().st_mtime)


def extract_transcript(session_file: Path, last_n: int = MAX_TRANSCRIPT_PAIRS) -> list[dict[str, str]]:
    """Return a list of {role, text} dicts — last N user+assistant text messages, no tools/system."""
    messages: list[dict[str, str]] = []
    for raw in session_file.read_text(errors="replace").splitlines():
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            continue

        message_obj = msg.get("message") if isinstance(msg.get("message"), dict) else msg
        actor = message_obj.get("role") or msg.get("type")
        if actor not in ("user", "assistant"):
            continue

        content = message_obj.get("content")
        text_parts: list[str] = []
        if isinstance(content, str):
            text_parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))

        text = "\n".join(p for p in text_parts if p).strip()
        if not text:
            continue
        if text.startswith("<system-reminder>") or text.startswith("<command-"):
            continue
        if len(text) > 3000:
            text = text[:3000] + "\n…[truncated]"
        messages.append({"role": actor, "text": text})

    return messages[-last_n:]


# ---- Word budget validation ----

def count_words(rel_paths: list[str]) -> tuple[int, dict[str, int]]:
    """Count words across selected files. Negative count => path invalid/outside knowledge root."""
    total = 0
    breakdown: dict[str, int] = {}
    for rel in rel_paths:
        full = (KNOWLEDGE_ROOT / rel).resolve()
        try:
            full.relative_to(KNOWLEDGE_ROOT)
        except ValueError:
            breakdown[rel] = -1
            continue
        if not full.exists() or not full.is_file():
            breakdown[rel] = 0
            continue
        words = len(full.read_text(errors="replace").split())
        breakdown[rel] = words
        total += words
    return total, breakdown


# ---- MCP submit_selection tool ----

# Single-call module state — captures the validated selection or clarification request.
_capture: dict[str, Any] = {"selection": None, "clarification": None}


@tool(
    name="submit_selection",
    description=(
        "Submit the final list of methodology files relevant to the user's task. "
        "The orchestrator validates total word count against the budget. "
        "If over budget, this tool returns an error and you must retry with a trimmed list."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "selected_files": {
                "type": "array",
                "description": "Files to include in the bundle. Paths are relative to the knowledge/ root.",
                "items": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path under knowledge/, e.g. 'geek/ai/ai-agents/schema-field-order/AGENTS.md'",
                        },
                        "reason": {
                            "type": "string",
                            "description": "One short line on why this file fits the user's task.",
                        },
                    },
                    "required": ["path"],
                },
            },
        },
        "required": ["selected_files"],
    },
)
async def submit_selection(args: dict[str, Any]) -> dict[str, Any]:
    files = args.get("selected_files") or []
    if not isinstance(files, list):
        return {
            "content": [{"type": "text", "text": "REJECTED: selected_files must be a list."}],
            "is_error": True,
        }

    paths = [f.get("path", "") for f in files if isinstance(f, dict) and f.get("path")]
    if not paths:
        return {
            "content": [{"type": "text", "text": "REJECTED: no valid paths in selection."}],
            "is_error": True,
        }

    total, breakdown = count_words(paths)
    invalid = [p for p, w in breakdown.items() if w == -1]
    missing = [p for p, w in breakdown.items() if w == 0]

    if invalid:
        return {
            "content": [{
                "type": "text",
                "text": (
                    f"REJECTED: paths outside knowledge/: {invalid}. "
                    "All paths must be relative to your cwd (the knowledge/ root)."
                ),
            }],
            "is_error": True,
        }

    if missing:
        return {
            "content": [{
                "type": "text",
                "text": (
                    f"REJECTED: paths do not exist: {missing}. "
                    "Verify each path with Glob/Read before submitting."
                ),
            }],
            "is_error": True,
        }

    if total > WORD_BUDGET:
        breakdown_lines = "\n".join(f"  - {p}: {w} words" for p, w in breakdown.items())
        return {
            "content": [{
                "type": "text",
                "text": (
                    f"REJECTED — over word budget. Total {total} words, budget {WORD_BUDGET}.\n"
                    f"Per-file:\n{breakdown_lines}\n\n"
                    f"Drop the LEAST relevant files until total ≤ {WORD_BUDGET}. "
                    "Keep core routing files (AGENTS.md / SKILL.md) over deep texts when possible. "
                    "Then call submit_selection again with the trimmed list."
                ),
            }],
            "is_error": True,
        }

    _capture["selection"] = files
    return {
        "content": [{
            "type": "text",
            "text": f"Accepted: {len(files)} files, {total} words. You are done — end your turn.",
        }],
    }


@tool(
    name="request_clarification",
    description=(
        "Use INSTEAD OF submit_selection when the user's task is genuinely ambiguous. "
        "Submit 1-3 clarifying questions; the orchestrator will ask the user via AskUserQuestion "
        "and re-invoke faion with the answers in the transcript."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "context": {
                "type": "string",
                "description": "One short paragraph: what's ambiguous and why questions are needed.",
            },
            "questions": {
                "type": "array",
                "minItems": 1,
                "maxItems": 3,
                "items": {
                    "type": "object",
                    "properties": {
                        "header": {
                            "type": "string",
                            "description": "Short header (≤12 chars) for AskUserQuestion UI.",
                        },
                        "question": {
                            "type": "string",
                            "description": "The question itself, in the user's language.",
                        },
                        "multi_select": {
                            "type": "boolean",
                            "description": "True for 'pick all that apply'. Default false.",
                        },
                        "options": {
                            "type": "array",
                            "minItems": 2,
                            "maxItems": 5,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "description": {"type": "string"},
                                },
                                "required": ["label"],
                            },
                        },
                    },
                    "required": ["header", "question", "options"],
                },
            },
        },
        "required": ["context", "questions"],
    },
)
async def request_clarification(args: dict[str, Any]) -> dict[str, Any]:
    questions = args.get("questions") or []
    context = (args.get("context") or "").strip()

    if not isinstance(questions, list) or not questions:
        return {
            "content": [{"type": "text", "text": "REJECTED: questions must be a non-empty list."}],
            "is_error": True,
        }

    normalized: list[dict[str, Any]] = []
    for q in questions:
        if not isinstance(q, dict):
            continue
        opts = q.get("options") or []
        if not isinstance(opts, list) or len(opts) < 2:
            return {
                "content": [{
                    "type": "text",
                    "text": "REJECTED: each question must have at least 2 options.",
                }],
                "is_error": True,
            }
        normalized.append({
            "header": (q.get("header") or "")[:12],
            "question": q.get("question") or "",
            "multi_select": bool(q.get("multi_select", False)),
            "options": [
                {"label": o.get("label", ""), "description": o.get("description", "")}
                for o in opts if isinstance(o, dict) and o.get("label")
            ],
        })

    if not normalized:
        return {
            "content": [{"type": "text", "text": "REJECTED: no valid questions."}],
            "is_error": True,
        }

    _capture["clarification"] = {"context": context, "questions": normalized}
    return {
        "content": [{
            "type": "text",
            "text": f"Clarification request accepted ({len(normalized)} question(s)). End your turn.",
        }],
    }


# ---- Bundle rendering (XML) ----

def render_methodology_xml(path: Path) -> str | None:
    """Parse methodology.xml, strip <metadata>, return <faion-methodology slug="...">...</faion-methodology>.

    Returns None if the file is not a valid methodology document — the caller
    falls back to raw CDATA rendering.
    """
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return None
    root = tree.getroot()
    if root.tag != "methodology":
        return None
    content = root.find("content")
    if content is None:
        return None
    slug = root.get("slug") or path.parent.name
    wrapper = copy.deepcopy(content)
    wrapper.tag = "faion-methodology"
    wrapper.set("slug", slug)
    return ET.tostring(wrapper, encoding="unicode")


def render_bundle(files: list[dict]) -> str:
    documents: list[dict[str, Any]] = []
    total = 0
    for entry in files:
        rel = entry.get("path", "")
        full = (KNOWLEDGE_ROOT / rel).resolve()
        if not full.exists():
            continue

        rendered = full.name == "methodology.xml" and render_methodology_xml(full)
        if rendered:
            content = rendered
            inline = True
        else:
            content = full.read_text(errors="replace")
            inline = False

        words = len(content.split())
        total += words
        documents.append({
            "path": rel,
            "reason": (entry.get("reason") or "").strip(),
            "words": words,
            "content": content,
            "inline": inline,
        })
    return render(
        "bundle.xml.j2",
        files=files,
        total_words=total,
        word_budget=WORD_BUDGET,
        documents=documents,
    )


def render_clarification(payload: dict[str, Any]) -> str:
    return render(
        "clarification.xml.j2",
        context=payload.get("context", ""),
        questions=payload.get("questions", []),
    )


# ---- Subagent run ----

async def run_retrieval(messages: list[dict[str, str]]) -> tuple[str, Any]:
    """Returns (kind, data). kind is one of: 'selection', 'clarification', 'none'."""
    _capture["selection"] = None
    _capture["clarification"] = None

    server = create_sdk_mcp_server(
        name="faion",
        version="1.0.0",
        tools=[submit_selection, request_clarification],
    )

    domains_l1, taxonomy_l1, l1_words = build_l1_embed(
        read_domains_l1(), read_taxonomy_l1()
    )
    two_level_available = domains_l1 is not None or taxonomy_l1 is not None

    system_prompt = render(
        "system_prompt.xml.j2",
        knowledge_root=str(KNOWLEDGE_ROOT),
        word_budget=WORD_BUDGET,
        two_level_available=two_level_available,
        domains_l1_xml=domains_l1,
        taxonomy_l1_xml=taxonomy_l1,
        l1_word_count=l1_words,
    )
    user_prompt = render(
        "user_prompt.xml.j2",
        messages=messages,
        two_level_available=two_level_available,
    )

    options = ClaudeAgentOptions(
        cwd=str(KNOWLEDGE_ROOT),
        mcp_servers={"faion": server},
        allowed_tools=[
            "Read",
            "Grep",
            "Glob",
            "mcp__faion__submit_selection",
            "mcp__faion__request_clarification",
        ],
        disallowed_tools=[
            "Write", "Edit", "Bash", "NotebookEdit", "Task", "WebFetch", "WebSearch",
        ],
        permission_mode="bypassPermissions",
        model=MODEL,
        system_prompt=system_prompt,
        max_turns=MAX_AGENT_TURNS,
    )

    async for msg in query(prompt=user_prompt, options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, ToolUseBlock):
                    if block.name.endswith("submit_selection"):
                        logger.debug(
                            "submit_selection: %d files",
                            len(block.input.get("selected_files", [])),
                        )
                    elif block.name.endswith("request_clarification"):
                        logger.debug(
                            "request_clarification: %d questions",
                            len(block.input.get("questions", [])),
                        )

    if _capture["clarification"]:
        return "clarification", _capture["clarification"]
    if _capture["selection"]:
        return "selection", _capture["selection"]
    return "none", None


# ---- Entry point ----

def main() -> None:
    session_arg = sys.argv[1] if len(sys.argv) > 1 else ""
    session_file = find_session_file(session_arg)
    if not session_file:
        print("<faion_knowledge error=\"no_session_file\"/>")
        return

    messages = extract_transcript(session_file)
    if not messages:
        print("<faion_knowledge error=\"empty_transcript\"/>")
        return

    kind, data = asyncio.run(run_retrieval(messages))
    if kind == "clarification":
        print(render_clarification(data))
        return
    if kind == "selection" and data:
        print(render_bundle(data))
        return
    print("<faion_knowledge error=\"no_selection\"/>")


if __name__ == "__main__":
    main()
