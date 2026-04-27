"""
Scan CSS and component files for hardcoded color and spacing values
that should be token references.
Input: sys.argv[1] = path to token JSON file, sys.argv[2] = directory to scan
Output: JSON list of violations (file, line, type, content)
Usage: python token-violation-scanner.py tokens.json src/
"""
import json
import re
import sys
from pathlib import Path

HARDCODED_COLOR = re.compile(
    r'#[0-9a-fA-F]{3,8}|rgb\(|rgba\(|hsl\(|hsla\('
)
HARDCODED_SPACING = re.compile(
    r'(?<!\w)(padding|margin|gap|width|height|top|right|bottom|left):\s*\d+px'
)
HARDCODED_FONT_SIZE = re.compile(
    r'font-size:\s*\d+(px|rem|em)'
)

EXTENSIONS = {".css", ".scss", ".sass", ".less", ".tsx", ".ts", ".jsx", ".js", ".vue"}


def scan_file(filepath: str) -> list:
    issues = []
    with open(filepath, encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            if HARDCODED_COLOR.search(line):
                issues.append({
                    "file": filepath,
                    "line": i,
                    "type": "hardcoded_color",
                    "content": line.strip()[:120],
                })
            if HARDCODED_SPACING.search(line):
                issues.append({
                    "file": filepath,
                    "line": i,
                    "type": "hardcoded_spacing",
                    "content": line.strip()[:120],
                })
            if HARDCODED_FONT_SIZE.search(line):
                issues.append({
                    "file": filepath,
                    "line": i,
                    "type": "hardcoded_font_size",
                    "content": line.strip()[:120],
                })
    return issues


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python token-violation-scanner.py <tokens.json> <src-dir>")
        sys.exit(1)

    token_file = sys.argv[1]
    src_dir = sys.argv[2]

    with open(token_file) as f:
        tokens = json.load(f)

    all_issues = []
    for path in Path(src_dir).rglob("*"):
        if path.suffix in EXTENSIONS and path.is_file():
            all_issues.extend(scan_file(str(path)))

    print(json.dumps(all_issues[:100], indent=2))
    print(f"\nTotal violations found: {len(all_issues)}")
    if len(all_issues) > 100:
        print("(showing first 100)")
