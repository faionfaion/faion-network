"""
ci_row.py — strict row shape for cross-session contextual inquiry analysis.

Each observation event during a CI session is one CIRow.
Use this schema to normalize outputs from the observation-tagger LLM agent
before affinity clustering and sequence/flow modeling.

Exit 0 if all rows valid, prints warnings for inferences without quotes.
"""
from dataclasses import dataclass, asdict, field
from typing import Optional
import json, sys


@dataclass
class CIRow:
    session_id: str
    t_seconds: float
    actor: str              # participant id or "researcher"
    action: str             # short verb phrase (observed)
    artifact: Optional[str]
    tool: Optional[str]
    breakdown: bool         # something didn't work as intended
    workaround: bool        # unofficial method substituting for official
    quote_verbatim: Optional[str]  # exact transcript text, not paraphrase
    inference: bool         # True = not directly observed
    tags: list[str] = field(default_factory=list)


def validate(rows: list[CIRow]) -> list[str]:
    warnings = []
    for r in rows:
        if r.inference and not r.quote_verbatim:
            warnings.append(
                f"warn: {r.session_id}@{r.t_seconds} inference without quote — "
                "add supporting quote or mark as observed"
            )
    return warnings


def main():
    raw = json.load(sys.stdin)
    rows = [CIRow(**r) for r in raw]
    for w in validate(rows):
        print(w)
    print(json.dumps([asdict(r) for r in rows], indent=2))


if __name__ == "__main__":
    main()
