#!/usr/bin/env python3
"""
vui-lint.py — lint a VUI dialogue script for common issues.
Input: dialogue script file where system lines start with "System:"
Output: list of issues with line numbers; exits 1 if issues found.
Usage: python vui-lint.py dialogue.txt
"""
import sys
import re

MAX_WORDS = 25  # spoken prompts should be short; 20 for smart speakers, 25 for screen+voice

ANTI_PATTERNS = [
    (r"I'm sorry\.", "Hollow apology without action — offer resolution instead"),
    (r"Please (hold|wait)\b", "Dead air without context — explain what is happening"),
    (r"\d{4,}", "Long number is hard to hear — spell out or chunk into groups"),
    (r"\.com|\.net|\.org|https?://", "URL in voice prompt is unusable — send to phone/screen instead"),
    (r"\bError\b\.?\s*$", "Bare 'Error' response — add context and recovery guidance"),
]

if len(sys.argv) < 2:
    print("Usage: python vui-lint.py <dialogue-file>")
    sys.exit(2)

with open(sys.argv[1]) as f:
    lines = f.readlines()

issues = []
for i, line in enumerate(lines, 1):
    if not line.startswith("System:"):
        continue
    text = line[7:].strip()
    words = len(text.split())
    if words > MAX_WORDS:
        issues.append(f"Line {i}: too long ({words} words > {MAX_WORDS}): {text[:60]}...")
    for pattern, msg in ANTI_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            issues.append(f"Line {i}: {msg}: {text[:60]}...")

if issues:
    print("\n".join(issues))
    sys.exit(1)
else:
    print("No issues found.")
