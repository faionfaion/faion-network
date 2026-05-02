#!/usr/bin/env python3
"""UserPromptSubmit hook: inject improver suggestion when session is mature.

Fires on every user message. When >25% context used (~200KB transcript),
adds a soft suggestion to ask user about running /faion
at the next logical stopping point.
"""
import json
import os
import sys
from glob import glob
from pathlib import Path


def get_transcript_size_kb() -> float:
    transcript_dirs = glob(os.path.expanduser("~/.claude/projects/*/"))
    if not transcript_dirs:
        return 0
    latest = None
    latest_mtime = 0
    for d in transcript_dirs:
        for f in Path(d).rglob("*.jsonl"):
            mtime = f.stat().st_mtime
            if mtime > latest_mtime:
                latest = f
                latest_mtime = mtime
    if not latest:
        return 0
    return latest.stat().st_size / 1024


def count_subagent_outputs() -> int:
    return len(glob("/tmp/claude-*/*/tasks/*.output"))


def main():
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        pass

    transcript_kb = get_transcript_size_kb()

    if transcript_kb < 200:
        print(json.dumps({}))
        return

    subagent_count = count_subagent_outputs()

    result = {
        "additionalContext": (
            f"<user-prompt-submit-hook>"
            f"[improver session check] "
            f"Session context: ~{transcript_kb:.0f}KB, {subagent_count} subagent outputs. "
            f"Context usage >25%. "
            f"ACTION REQUIRED: If the user's message completes a logical unit of work "
            f"(task done, feature implemented, question answered), you MUST use AskUserQuestion "
            f"to ask: 'Session has significant context (~{transcript_kb:.0f}KB). "
            f"Run /faion to capture patterns and mistakes?' "
            f"If user confirms → use EnterPlanMode, then plan the improvement session "
            f"following the improver skill workflow (Phase 0: Session Review). "
            f"If user declines → continue normally. "
            f"Do NOT ask if you already asked in this conversation. "
            f"Do NOT ask if the user is in the middle of active work."
            f"</user-prompt-submit-hook>"
        ),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
