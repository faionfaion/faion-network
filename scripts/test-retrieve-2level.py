#!/usr/bin/env python3
"""Smoke test for the two-level retrieval prompt.

Verifies that retrieve.py:
  - successfully reads L1 domains.xml + playbook taxonomy.xml,
  - embeds them into the rendered system prompt,
  - emits the four-step two-level retrieval protocol,
  - falls back cleanly when L1 sources are missing.

Does NOT spawn the Claude Agent SDK. Pure XML/Jinja sanity check.

Exit code 0 on all-green, 1 on any assertion failure.
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "skills" / "faion" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Importing retrieve.py may print and exit if SDK deps are missing.
# We swallow that by stubbing the modules before import.

for stub_name in ("claude_agent_sdk", "claude_code_sdk"):
    if stub_name not in sys.modules:
        stub = types.ModuleType(stub_name)
        # Add the names retrieve.py imports from the SDK so `from ... import` works.
        for attr in (
            "AssistantMessage",
            "ClaudeAgentOptions",
            "ToolUseBlock",
            "create_sdk_mcp_server",
            "query",
            "tool",
        ):
            setattr(stub, attr, lambda *a, **kw: None)
        # tool() is used as a decorator with kwargs — return a passthrough decorator.
        stub.tool = lambda **_kw: (lambda fn: fn)  # type: ignore[attr-defined]
        sys.modules[stub_name] = stub

import retrieve  # noqa: E402  (after sys.path/stub setup)


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        print(f"FAIL: {msg}")
        sys.exit(1)
    print(f"  ok: {msg}")


def test_l1_loaders_return_xml() -> None:
    print("\n[1] L1 loaders read real files")
    domains = retrieve.read_domains_l1()
    taxonomy = retrieve.read_taxonomy_l1()
    _expect(domains is not None, "read_domains_l1() returned content")
    _expect(taxonomy is not None, "read_taxonomy_l1() returned content")
    _expect("<domains" in (domains or ""), "domains.xml contains <domains root tag")
    _expect("<taxonomy" in (taxonomy or ""), "taxonomy.xml contains <taxonomy root tag")
    _expect("<domain id=\"ai-agents\"" in (domains or ""), "domains.xml lists ai-agents domain")
    _expect("category id=\"build-ship\"" in (taxonomy or ""), "taxonomy.xml lists build-ship category")


def test_l1_embed_within_budget() -> None:
    print("\n[2] L1 embed stays within word cap")
    domains = retrieve.read_domains_l1()
    taxonomy = retrieve.read_taxonomy_l1()
    d, t, total = retrieve.build_l1_embed(domains, taxonomy)
    _expect(d is not None and t is not None, "build_l1_embed preserves both indexes")
    _expect(total <= retrieve.L1_EMBED_WORD_CAP,
            f"combined L1 words ({total}) <= cap ({retrieve.L1_EMBED_WORD_CAP})")


def test_l1_embed_truncates_when_over_cap() -> None:
    print("\n[3] L1 embed truncates <scope> bodies when over cap")
    # Force the cap so low that truncation MUST trigger.
    orig_cap = retrieve.L1_EMBED_WORD_CAP
    try:
        retrieve.L1_EMBED_WORD_CAP = 50
        domains = retrieve.read_domains_l1()
        taxonomy = retrieve.read_taxonomy_l1()
        d, _t, total = retrieve.build_l1_embed(domains, taxonomy)
        _expect(d is not None, "truncated domains still returned")
        _expect("<scope>" in (d or ""), "<scope> tags preserved after truncation")
        # Original scope sentences had multiple sentences; truncated to first.
        long_sentence = (
            "Production-ready architectures"  # arbitrary substring not in domains.xml
        )
        _expect(long_sentence not in (d or ""),
                "truncation reduced scope bodies (no unexpected long-form text)")
        _expect(total < len((domains or "").split()) + len((taxonomy or "").split()),
                "total word count strictly smaller after truncation")
    finally:
        retrieve.L1_EMBED_WORD_CAP = orig_cap


def test_system_prompt_contains_protocol_and_l1() -> None:
    print("\n[4] System prompt embeds L1 + 4-step protocol")
    domains = retrieve.read_domains_l1()
    taxonomy = retrieve.read_taxonomy_l1()
    d, t, words = retrieve.build_l1_embed(domains, taxonomy)
    prompt = retrieve.render(
        "system_prompt.xml.j2",
        knowledge_root=str(retrieve.KNOWLEDGE_ROOT),
        word_budget=retrieve.WORD_BUDGET,
        two_level_available=True,
        domains_l1_xml=d,
        taxonomy_l1_xml=t,
        l1_word_count=words,
    )
    _expect("<two-level-retrieval-protocol>" in prompt,
            "prompt opens the two-level protocol block")
    _expect("name=\"L1 (already inlined)\"" in prompt,
            "step 1: L1 (already inlined) present")
    _expect("name=\"pick-buckets\"" in prompt,
            "step 2: pick-buckets present")
    _expect("name=\"L2 (read on demand)\"" in prompt,
            "step 3: L2 read present")
    _expect("name=\"leaf\"" in prompt,
            "step 4: leaf read present")
    _expect("≤3 domains" in prompt or "AT MOST 3 candidate methodology domains" in prompt,
            "prompt enforces ≤3 domain picks")
    _expect("≤2 goal categories" in prompt or "AT MOST 2 candidate playbook goal categories" in prompt,
            "prompt enforces ≤2 goal-category picks")
    _expect("<l1-index name=\"domains\">" in prompt,
            "domains L1 inlined under <l1-index name=\"domains\">")
    _expect("<l1-index name=\"playbook-taxonomy\">" in prompt,
            "taxonomy L1 inlined under <l1-index name=\"playbook-taxonomy\">")
    _expect("<domain id=\"ai-agents\"" in prompt,
            "actual domain entry present inside the embed")
    _expect("category id=\"build-ship\"" in prompt,
            "actual goal-category entry present inside the embed")


def test_user_prompt_instructs_bucket_picking() -> None:
    print("\n[5] User prompt instructs bucket-naming before L2 reads")
    prompt = retrieve.render(
        "user_prompt.xml.j2",
        messages=[{"role": "user", "text": "help me build an agent"}],
        two_level_available=True,
    )
    _expect("up to 3 candidate methodology domains" in prompt,
            "user prompt mentions ≤3 candidate domains")
    _expect("up to 2 candidate playbook goal categories" in prompt,
            "user prompt mentions ≤2 candidate goal categories")
    _expect("BEFORE reading any L2 INDEX.xml" in prompt,
            "user prompt orders bucket-naming BEFORE L2 reads")


def test_fallback_when_l1_missing() -> None:
    print("\n[6] Fallback path renders without two-level block when L1 absent")
    prompt = retrieve.render(
        "system_prompt.xml.j2",
        knowledge_root=str(retrieve.KNOWLEDGE_ROOT),
        word_budget=retrieve.WORD_BUDGET,
        two_level_available=False,
        domains_l1_xml=None,
        taxonomy_l1_xml=None,
        l1_word_count=0,
    )
    _expect("<two-level-retrieval-protocol>" not in prompt,
            "no two-level block when fallback engaged")
    _expect("use Glob/Grep to discover candidate methodologies" in prompt,
            "old single-pass step 3 wording restored")


def test_defensive_load_missing_file(tmp_path_factory=None) -> None:
    print("\n[7] _load_l1_file returns None for missing files")
    missing = retrieve.KNOWLEDGE_ROOT / "does-not-exist.xml"
    _expect(retrieve._load_l1_file(missing) is None,
            "_load_l1_file(missing) returns None")


def main() -> None:
    test_l1_loaders_return_xml()
    test_l1_embed_within_budget()
    test_l1_embed_truncates_when_over_cap()
    test_system_prompt_contains_protocol_and_l1()
    test_user_prompt_instructs_bucket_picking()
    test_fallback_when_l1_missing()
    test_defensive_load_missing_file()
    print("\nALL OK")


if __name__ == "__main__":
    main()
