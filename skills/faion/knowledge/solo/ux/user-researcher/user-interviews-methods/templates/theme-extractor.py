# theme_extractor.py — count keyword themes across transcript files
# Input:  ./transcripts/*.txt  (one file per interview)
# Output: sorted table of theme keyword frequencies
import os
import re
from collections import Counter

THEMES = [
    "frustrating", "hate", "can't figure out", "wish",
    "workaround", "too long", "confusing",
]
folder = "./transcripts"

theme_counts: Counter = Counter()
for fname in os.listdir(folder):
    if fname.endswith(".txt"):
        text = open(os.path.join(folder, fname)).read().lower()
        for theme in THEMES:
            theme_counts[theme] += len(re.findall(re.escape(theme), text))

for theme, count in theme_counts.most_common():
    print(f"{count:3d}  {theme}")
