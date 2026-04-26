# evidence_scorer.py — score validation evidence by hierarchy level
# Input:  list of evidence dicts with type, source, note
# Output: validation score percentage and sorted evidence table

HIERARCHY = {
    "paid": 5,
    "committed": 4,   # LOI, signed up, pre-order
    "engaged": 3,     # used prototype, returned 3x
    "stated": 2,      # expressed interest in interview
    "anecdote": 1,    # single mention, no follow-up
}

evidence = [
    {"type": "stated",   "source": "Interview #1",  "note": "Would pay $50/mo"},
    {"type": "engaged",  "source": "Landing page",  "note": "47% email signup rate"},
    {"type": "stated",   "source": "Reddit",        "note": "Upvoted complaint thread"},
    {"type": "anecdote", "source": "Friend",        "note": 'Said "sounds interesting"'},
]

total = sum(HIERARCHY[e["type"]] for e in evidence)
max_possible = len(evidence) * 5
print(f"Validation score: {total}/{max_possible} ({100 * total // max_possible}%)")
for e in sorted(evidence, key=lambda x: -HIERARCHY[x["type"]]):
    print(f"  [{HIERARCHY[e['type']]}] {e['type']:10} | {e['source']} — {e['note']}")
