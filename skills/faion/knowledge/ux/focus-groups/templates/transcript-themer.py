# purpose: Cluster transcripts into candidate themes
# consumes: transcripts JSON across groups
# produces: themes.json
# depends-on: stdlib only
# token-budget-impact: ~300
"""transcript-themer.py — naive keyword-cluster across group transcripts."""
from __future__ import annotations
import collections
import json
import re
import sys
from pathlib import Path

STOP = {"the", "and", "but", "of", "to", "a", "is", "i", "you", "we", "it", "in", "for", "on", "at", "or", "this", "that"}

def tokens(t: str) -> list[str]:
    return [w for w in re.findall(r"[a-zA-Z]{3,}", t.lower()) if w not in STOP]

def main(path: str) -> None:
    transcripts = json.loads(Path(path).read_text())
    counter: dict = collections.Counter()
    for g in transcripts:
        for q in g["quotes"]:
            for w in set(tokens(q)):
                counter[w] += 1
    candidates = [{"keyword": w, "groups_with": c} for w, c in counter.items() if c >= 2]
    print(json.dumps(sorted(candidates, key=lambda x: -x["groups_with"]), indent=2))

if __name__ == "__main__":
    main(sys.argv[1])
