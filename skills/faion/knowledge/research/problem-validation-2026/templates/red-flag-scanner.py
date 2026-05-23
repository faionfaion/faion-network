#!/usr/bin/env python3
"""
Interview transcript red-flag scanner.
Input: interview transcript file path as first argument.
Output: JSON with per-category red flag matches and total count.
Red flags indicate weak evidence: compliments, hypotheticals, generic statements.
Usage: python3 red-flag-scanner.py interview.txt
"""
import re
import sys
import json

RED_FLAG_PATTERNS = {
    "compliment": [
        r"\b(great idea|love it|love this|brilliant|awesome|fantastic|perfect|amazing)\b",
        r"\b(this is exactly what|this is just what|this is what I was looking for)\b",
    ],
    "hypothetical": [
        r"\b(I would|I'd probably|I might|I could see myself|I'd definitely|I'd likely)\b",
        r"\b(would probably|would definitely|would likely|would use|would pay)\b",
    ],
    "generic": [
        r"\b(everyone|nobody|no one|always|never|all the time|every company)\b",
        r"\b(people always|everyone has|nobody does|everyone needs)\b",
    ],
}

if len(sys.argv) < 2:
    print("Usage: python3 red-flag-scanner.py interview.txt", file=sys.stderr)
    sys.exit(1)

with open(sys.argv[1]) as f:
    text = f.read().lower()

results = {}
total = 0
for category, patterns in RED_FLAG_PATTERNS.items():
    matches = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, text))
    results[category] = {"count": len(matches), "matches": list(set(matches))}
    total += len(matches)

results["total_red_flags"] = total
results["interpretation"] = (
    "High red-flag density — likely compliments/validation-seeking responses. Treat as weak signal."
    if total > 5 else
    "Acceptable red-flag count. Verify specific-past and commitment signals separately."
)

print(json.dumps(results, indent=2))
