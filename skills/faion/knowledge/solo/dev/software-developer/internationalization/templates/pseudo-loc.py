# purpose: Pseudo-localization transformer for catalogue values
# consumes: See content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
"""Generate pseudo-localised catalogue to surface truncation in CI.

Usage: python pseudo-loc.py locales/en.json locales/pseudo.json

Pads every string by ~30% with [!!...~~] markers so truncation, overflow,
and hardcoded-string bugs appear in staging before real translators are involved.
"""
import json
import sys
from pathlib import Path


def pseudo(s: str) -> str:
    pad = "~~" * max(1, len(s) // 3)
    return f"[!!{s}{pad}!!]"


def walk(obj: object) -> object:
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items()}
    if isinstance(obj, str):
        return pseudo(obj)
    return obj


if __name__ == "__main__":
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    data = json.loads(src.read_text(encoding="utf-8"))
    dst.write_text(json.dumps(walk(data), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"pseudo-loc: {src} -> {dst}")
