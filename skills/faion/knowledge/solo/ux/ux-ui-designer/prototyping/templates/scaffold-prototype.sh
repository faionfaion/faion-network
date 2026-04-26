#!/usr/bin/env bash
# scaffold-prototype.sh — create a minimal HTML click-through prototype
# Usage: bash scaffold-prototype.sh <feature-name> <num-screens>
# Example: bash scaffold-prototype.sh checkout 5
FEATURE="${1:?Usage: $0 <feature-name> <num-screens>}"
NUM="${2:-3}"
mkdir -p "prototype-${FEATURE}"
for i in $(seq 1 "$NUM"); do
  cat > "prototype-${FEATURE}/screen${i}.html" <<HTML
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>${FEATURE} — Screen ${i}</title>
<style>body{font-family:sans-serif;max-width:375px;margin:auto;padding:1rem}</style>
</head>
<body>
<p><strong>Screen ${i}</strong> — replace with design</p>
$([ "$i" -lt "$NUM" ] && echo "<a href='screen$((i+1)).html'>Next &rarr;</a>")
$([ "$i" -gt 1 ] && echo "<a href='screen$((i-1)).html'>&larr; Back</a>")
</body></html>
HTML
done
echo "Prototype scaffolded: prototype-${FEATURE}/ with ${NUM} screens"
echo "Serve with: npx http-server prototype-${FEATURE}/"
