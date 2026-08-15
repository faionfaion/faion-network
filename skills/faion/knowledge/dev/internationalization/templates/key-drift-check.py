# __faion_header_v1__
# purpose: CI check — every key in the base locale catalogue exists in every other locale
# consumes: locales/*.json catalogues
# produces: code
# depends-on: content/01-core-rules.xml#r6-key-drift-ci
# token-budget-impact: ~260 tokens when loaded as context
"""Exit 1 and list the gaps when any locale is missing a key the base locale has.

Nested catalogues are flattened to dotted paths so `checkout.title` compares
equal whether the catalogue is flat or nested — the two shapes coexist in most
codebases and comparing raw top-level keys silently passes a nested one.
"""
import json
import sys
from pathlib import Path

BASE = "en.json"
LOCALES = Path("locales")


def flatten(obj, prefix=""):
    out = set()
    for key, value in obj.items():
        path = f"{prefix}{key}"
        if isinstance(value, dict):
            out |= flatten(value, f"{path}.")
        else:
            out.add(path)
    return out


def main() -> int:
    base_keys = flatten(json.loads((LOCALES / BASE).read_text(encoding="utf-8")))
    allowlist = set()
    allow_file = LOCALES / "untranslated-allowlist.txt"
    if allow_file.exists():
        allowlist = {ln.strip() for ln in allow_file.read_text().splitlines() if ln.strip()}
    bad = False
    for path in sorted(LOCALES.glob("*.json")):
        if path.name == BASE:
            continue
        missing = base_keys - flatten(json.loads(path.read_text(encoding="utf-8"))) - allowlist
        if missing:
            sys.stdout.write(f"{path.name} missing {len(missing)}: {sorted(missing)[:20]}\n")
            bad = True
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
