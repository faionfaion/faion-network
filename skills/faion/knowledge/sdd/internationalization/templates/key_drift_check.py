# __faion_header_v1__
# purpose: CI check: every key in en.json exists in all locales
# consumes: see content/02-output-contract.xml
# produces: spec; depends-on: content/01-core-rules.xml#icu-messageformat
# faion_header_json: {"__faion_header__":{"purpose":"CI check: every key in en.json exists in all locales","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#icu-messageformat","token_budget_impact":"~150 tokens when loaded"}}
import json
import sys
from pathlib import Path


def main() -> int:
    en = json.loads(Path("locales/en.json").read_text())
    keys = set(en.keys())
    bad = False
    for path in Path("locales").glob("*.json"):
        if path.name == "en.json":
            continue
        other = json.loads(path.read_text())
        missing = keys - set(other.keys())
        if missing:
            sys.stdout.write(f"{path.name} missing: {sorted(missing)}\n")
            bad = True
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
