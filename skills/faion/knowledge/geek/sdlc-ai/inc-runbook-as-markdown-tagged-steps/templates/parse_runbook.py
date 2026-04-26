"""Reference Markdown runbook parser used by the SRE agent loader.

Input:  path to runbook .md file.
Output: ParsedRunbook with diagnose[], auto_remediate[], approval_remediate[],
        escalate[]. Raises RunbookInvalid when the spine or tags are wrong.

The agent MUST refuse to act on a runbook that fails to parse.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_SECTIONS = ("Symptoms", "Diagnose", "Remediate", "Escalate")
TAG_AUTO = "<!-- agent:auto -->"
TAG_APPROVAL = "<!-- agent:approval -->"
SECTION_RE = re.compile(r"^## +(.+?)\s*$")
BULLET_RE = re.compile(r"^- +(.*)$")


class RunbookInvalid(Exception):
    """Spine or step-tag failure; agent must abort."""


@dataclass
class ParsedRunbook:
    path: Path
    symptoms: list[str] = field(default_factory=list)
    diagnose: list[str] = field(default_factory=list)
    auto_remediate: list[str] = field(default_factory=list)
    approval_remediate: list[str] = field(default_factory=list)
    escalate: list[str] = field(default_factory=list)


def parse(path: Path) -> ParsedRunbook:
    text = path.read_text(encoding="utf-8")
    sections: dict[str, list[str]] = {s: [] for s in REQUIRED_SECTIONS}
    current: str | None = None
    for line in text.splitlines():
        m = SECTION_RE.match(line)
        if m:
            current = m.group(1).strip()
            continue
        if current in sections:
            b = BULLET_RE.match(line)
            if b:
                sections[current].append(b.group(1).rstrip())

    for s in REQUIRED_SECTIONS:
        if not sections[s]:
            raise RunbookInvalid(f"missing or empty section: {s}")

    rb = ParsedRunbook(path=path)
    rb.symptoms = sections["Symptoms"]
    rb.diagnose = sections["Diagnose"]
    rb.escalate = sections["Escalate"]
    for step in sections["Remediate"]:
        if step.endswith(TAG_AUTO):
            rb.auto_remediate.append(step[: -len(TAG_AUTO)].rstrip())
        elif step.endswith(TAG_APPROVAL):
            rb.approval_remediate.append(step[: -len(TAG_APPROVAL)].rstrip())
        else:
            raise RunbookInvalid(
                f"remediate step missing agent:auto/agent:approval tag: {step!r}"
            )
    return rb
