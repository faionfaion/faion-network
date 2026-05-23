"""
validate_events.py — CI guard: fail if any tracking call uses an unregistered event name.

Reads events.yml (map of event_name -> [required_props]) from cwd.
Scans all .ts, .tsx, .js, .jsx files under src/ for gtag/plausible/track calls.
Exits 1 with error list if any unregistered event name is found.

Usage: python validate_events.py
"""
import re
import sys
import yaml
import pathlib

REGISTRY_FILE = "events.yml"
SCAN_ROOT = "src"
# Matches: gtag('event', 'name', ...) | plausible('name', ...) | track('name', ...)
PATTERN = re.compile(
    r"""(?:gtag\s*\(\s*['"]event['"]\s*,\s*|plausible\s*\(\s*|track\s*\(\s*)['"](\w+)['"]"""
)


def main() -> None:
    registry = yaml.safe_load(pathlib.Path(REGISTRY_FILE).read_text())
    bad: list[str] = []

    for path in pathlib.Path(SCAN_ROOT).rglob("*"):
        if path.suffix not in {".ts", ".tsx", ".js", ".jsx"}:
            continue
        for match in PATTERN.finditer(path.read_text()):
            name = match.group(1)
            if name not in registry:
                bad.append(f"{path}: unregistered event '{name}'")

    if bad:
        print("\n".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
