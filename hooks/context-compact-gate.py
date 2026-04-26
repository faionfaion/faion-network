#!/usr/bin/env python3
"""UserPromptSubmit gate based on context %.

Reads ctx % from /tmp/claude-ctx-{session_id}.txt (written by statusline).

Behavior:
  ctx > 40%: pass through ONLY prompts whose first word is "compact"/"/compact"
             or contain "КРИТИЧНО" anywhere. Block everything else.
  30 < ctx ≤ 40%: inject a warning + proposal to save important state and run
             /compact. Prompt itself goes through.
  ctx ≤ 30%: pass through silently.
"""
from __future__ import annotations

import json
import re
import sys

CTX_FILE_TEMPLATE = "/tmp/claude-ctx-{sid}.txt"
CTX_FILE_FALLBACK = "/tmp/claude-ctx-latest.txt"

EXEMPT_FIRST_WORDS = {"compact", "/compact", "компакт", "/компакт"}
CRITICAL_PATTERN = re.compile(r"КРИТИЧНО", re.IGNORECASE)


def read_ctx_pct(session_id: str) -> int:
    for path in (CTX_FILE_TEMPLATE.format(sid=session_id), CTX_FILE_FALLBACK):
        try:
            with open(path) as f:
                return int(f.read().strip() or 0)
        except (OSError, ValueError):
            continue
    return 0


def is_exempt(prompt: str) -> bool:
    if CRITICAL_PATTERN.search(prompt):
        return True
    stripped = prompt.lstrip()
    if not stripped:
        return False
    first_word = stripped.split(maxsplit=1)[0].lower()
    return first_word in EXEMPT_FIRST_WORDS


def emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = data.get("prompt", "") or ""
    session_id = data.get("session_id", "default")
    ctx_pct = read_ctx_pct(session_id)
    exempt = is_exempt(prompt)

    if ctx_pct > 40:
        if exempt:
            return
        emit({
            "decision": "block",
            "reason": (
                f"Контекст {ctx_pct}% (>40%) — заблоковано.\n"
                "Запусти /compact зараз, або:\n"
                "  • почни запит зі слова 'compact'\n"
                "  • додай слово 'КРИТИЧНО' до запиту"
            ),
        })
        return

    if ctx_pct > 30:
        if exempt:
            return
        emit({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    f"<user-prompt-submit-hook>"
                    f"[context-compact-gate] Контекст {ctx_pct}% (зона 30-40%). "
                    f"М'яке попередження: запропонуй користувачу зберегти "
                    f"важливе (memory entries, поточний план, ключові "
                    f"рішення/файли) і запустити /compact. Після цього — "
                    f"виконуй оригінальний запит."
                    f"</user-prompt-submit-hook>"
                ),
            }
        })
        return


if __name__ == "__main__":
    main()
