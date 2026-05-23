# purpose: Cluster transcripts by JTBD tags; print top-K segments
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
#!/usr/bin/env python3
"""
cluster-personas.py — first-draft persona trait clustering from a directory of interview transcripts.

Usage: python cluster-personas.py .aidocs/research/interviews/ > draft-persona.md

Each .md file in the directory is treated as one interview transcript.
Extracts trait patterns across 4 axes (role, goal, frustration, trigger),
counts citations per value, marks traits with fewer than 3 citations as [WEAK].

Output is a draft Markdown persona that requires human review and citation verification.
"""
import sys
import pathlib
import re
import collections


AXES = {
    "role": re.compile(
        r"(?im)^[^\n]*(?:role|title|job)\s*[:\-]\s*(.+)$"
    ),
    "goal": re.compile(
        r"(?im)^[^\n]*(?:goal|wants?\s+to|trying\s+to)\s*[:\-]\s*(.+)$"
    ),
    "frustration": re.compile(
        r"(?im)^[^\n]*(?:frustration|pain|blocker|stuck|annoyed)\s*[:\-]\s*(.+)$"
    ),
    "trigger": re.compile(
        r"(?im)^[^\n]*(?:buy|signed\s+up|started\s+using|switched)\s+(?:when|after|because)\s+(.+)$"
    ),
}

WEAK_THRESHOLD = 3


def main(interview_dir: str) -> None:
    interviews = sorted(pathlib.Path(interview_dir).glob("*.md"))
    if not interviews:
        print(f"No .md files found in {interview_dir}", file=sys.stderr)
        sys.exit(1)

    traits: dict[tuple[str, str], list[str]] = collections.defaultdict(list)

    for f in interviews:
        text = f.read_text(encoding="utf-8", errors="ignore")
        for axis, rx in AXES.items():
            for m in rx.finditer(text):
                value = m.group(1).strip().lower()[:80]
                line = text[: m.start()].count("\n") + 1
                citation = f"[{f.stem}:L{line}]"
                traits[(axis, value)].append(citation)

    print("# Draft Persona (auto-generated — requires human review)\n")
    print("> WARNING: All traits must be verified against source transcripts.")
    print("> Traits marked [WEAK] have fewer than 3 citations and must not appear in the final persona.\n")

    for axis in ("role", "goal", "frustration", "trigger"):
        print(f"## {axis.title()}\n")
        rows = sorted(
            ((key[1], val) for key, val in traits.items() if key[0] == axis),
            key=lambda r: -len(r[1]),
        )
        if not rows:
            print("*(no patterns found)*\n")
            continue
        for value, cites in rows[:5]:
            flag = " **[WEAK]**" if len(cites) < WEAK_THRESHOLD else ""
            cite_str = " ".join(cites[:5])
            print(f"- {value}{flag} — {len(cites)} mention(s) {cite_str}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <interview-directory>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
