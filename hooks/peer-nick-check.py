#!/usr/bin/env python3
"""Flag a peer message signed with a nickname nobody recognises.

**The evidence was in the headers all day and nobody read it.** On 2026-08-21 a
tmux rename broke the client author's signature: his script derived the nick from
the session name, so messages arrived correctly routed and signed `[budget/budget]`
instead of `[Diablo/budget]`. Nothing failed — routing holds on the project
suffix, not on the sender — so half a day of messages carried an identity shared
with any session of that name, and the three-bracket-then-two shape sat in every
line of the transcript unread.

His diagnosis, which this file exists to answer: **a signal that exists and is
compared against nothing is not a check, it is a trace.**

And his design note, which is why this is a warning and not a refusal: the errors
are asymmetric. A false alarm costs one line in a delivery note; a silent
acceptance costs a day of attributing one agent's words to another. So an unknown
nick is announced, never blocked — a message from a peer whose name changed for a
good reason must still arrive.

The same rename broke my outbound target resolution too, and that half failed
LOUDLY (`can't find pane`). One breakage, two ends, one alarm — and being told
about the loud end is not evidence the quiet end survived.
"""

import json
import re
import sys

#: Nicks that identify a real correspondent. A message signed with anything else
#: is delivered and flagged, never dropped.
#:
#: `budget` is deliberately ABSENT although it arrived for half a day: it is a
#: session name, shared by every session on that machine, and accepting it is what
#: made two agents one correspondent in the incident this file records.
#: `diablo-budget` is **permanent, and it means "the nick was lost"** — not a
#: transitional entry, which is what this comment said for twenty minutes.
#:
#: The plan it described was a rename of his pane title to `Diablo`. He did
#: something better and the comment outlived it: the root was never *which value*
#: sat in `pane_title`, it was that **one string did two jobs** — the address my
#: sender resolves and the identity he signs with — so a change at either end cut
#: the other. Caught three times in one day. He split them: the signature now
#: comes from `@nick`, a tmux pane option nobody routes on, and `pane_title` stays
#: `diablo-budget` untouched.
#:
#: So the degradation is deliberate: if that pane is ever recreated, `@nick`
#: vanishes and the signature falls back to the pane title — landing on exactly
#: this entry. Keeping it means the loss announces itself instead of being
#: assumed.
#:
#: Listed rather than left to fire, because a check that flags every correct
#: message from the one peer it watches is a check somebody removes before the
#: first real substitution — his correction to the asymmetry rule an hour earlier:
#: the cost of a false alarm is bounded per event and **unbounded in aggregate**.
KNOWN = {"diablo", "diablo-budget", "nero", "ruslan"}

#: `[Diablo/budget]`, `[Nero/etns]` — nick, slash, project.
SIGNATURE = re.compile(r"\[([A-Za-zА-Яа-яЇїІіЄєҐґ0-9_.-]+)/([A-Za-z0-9_-]+)\]")
#: Only the leading header is inspected; a quoted `[x/y]` deep in a message body is
#: somebody discussing the format, not signing with it.
HEAD = 400


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    prompt = event.get("prompt") or ""
    found = SIGNATURE.findall(prompt[:HEAD])
    if not found:
        # Not peer traffic at all — the owner typing. Silence is correct here, and
        # a hook that comments on ordinary messages is a hook that gets removed.
        return 0

    # **The LAST group, not every group.** A peer line carries the routing marker
    # `[diablo-budget/budget]` before the signature `[Diablo/budget]`, and the first
    # version read both — so it fired on perfectly correct traffic on its first
    # run. A gate that shouts at correct work gets deleted, which this project has
    # already paid for once.
    nick = found[-1][0]
    unknown = [] if nick.lower() in KNOWN else [nick]
    if unknown:
        # **stdout, one JSON object — the contract these hooks keep.**
        #
        # The first version wrote to stderr, where a `UserPromptSubmit` hook's
        # output on exit 0 reaches nobody. A check built because *a signal compared
        # against nothing is a trace, not a check* would itself have been a trace:
        # correct logic, right list, invisible result. Found by reading the
        # convention beside it (`hooks/AGENTS.md`) rather than by it firing.
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "UserPromptSubmit",
                        "additionalContext": (
                            "PEER SIGNATURE NOT RECOGNISED: "
                            + ", ".join(unknown)
                            + ". Routing is by project suffix, so this arrived "
                            "regardless of who signed it — confirm the sender "
                            "before attributing anything in this message to them. "
                            "See ~/.claude/hooks/peer-nick-check.py."
                        ),
                    }
                },
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
