"""
persona_evidence_check.py — fail if any persona claim lacks an evidence ID.

Input: YAML persona file with sections: goals, frustrations, behaviors.
Each item is either a string with [E-###] citations or a dict with evidence_ids list.
Quote section must have source_id set.

Exit 0 if valid, exit 1 with issues printed to stdout.
"""
import yaml, sys, re

REQUIRED = ("goals", "frustrations", "behaviors")


def check(path):
    p = yaml.safe_load(open(path))
    issues = []
    for section in REQUIRED:
        for i, item in enumerate(p.get(section, [])):
            text = item if isinstance(item, str) else item.get("text", "")
            ids = (
                item.get("evidence_ids", [])
                if isinstance(item, dict)
                else re.findall(r"\[E-\d+\]", text)
            )
            if not ids and "[INFERENCE]" not in text:
                issues.append(f"{section}[{i}]: no evidence_id and not marked [INFERENCE]")
    quote = p.get("quote", {})
    if isinstance(quote, dict) and quote.get("source_id") is None:
        issues.append("quote: no source_id — use verbatim participant quote with ID")
    for line in issues:
        print(line)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(check(sys.argv[1]))
