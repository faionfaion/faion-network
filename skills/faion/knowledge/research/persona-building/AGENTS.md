# Persona Building

## Summary

**One-sentence:** Produces 3 personas (primary + secondary + negative), each backed by >=5 interview citations, JTBD statements, top-3 pains, and a kill-criteria block; refuses single-source personas.

**One-paragraph:** Persona authoring methodology that ships exactly 3 personas (primary, secondary, negative) per product, each grounded in >=5 cited interview quotes, with explicit Jobs-to-Be-Done statements, top-3 pains, and a 'kill criteria' block naming the trait that disqualifies a user from this persona. Refuses single-source / single-interview personas.

**Ефективно для:**

- Pre-MVP: треба зафіксувати ICP перед feature greenlight.
- GTM сегментація для emails / ads / landing pages.
- Onboarding flow design - persona визначає first-run experience.
- Founder говорить про 'наших users' без конкретики - треба primary + secondary.
- Negative persona: окреслити, кого ми НЕ обслуговуємо (зменшує churn).

## Applies If (ALL must hold)

- Pre-MVP ICP lock before feature greenlight.
- GTM segmentation for emails, ads, landing pages.
- Onboarding flow design (persona drives first-run experience).
- Founder talks about 'our users' generically; needs primary + secondary.
- Negative persona work to reduce churn by naming the customer we do NOT serve.

## Skip If (ANY kills it)

- Pre-PMF zero users; do customer-development first, not personas.
- Internal tool with one user type (employees).
- Hardware / regulated medical (use clinical-trial cohorts, not personas).
- B2B enterprise with one buyer per account (build a buying committee map instead).
- Stable mature product where personas have not changed in 24 months.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Interview transcripts | markdown / Otter / Looppanel | user research ops |
| Quantitative segment data | PostHog / Amplitude cohorts | analytics |
| Tag library | JTBD + pain + segment | Dovetail / manual |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[user-research-at-scale]] | supplies the transcript volume and tagging that personas summarise |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cluster-segments` | sonnet | Cluster transcripts into 2-4 candidate segments. |
| `write-persona-cards` | sonnet | Compose persona-lean and persona-full per segment. |
| `negative-persona` | sonnet | Identify the user type the product must reject. |
| `citation-check` | haiku | Mechanical check that every persona has >=5 cited quotes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/persona-lean.md.j2` | Lean persona card (1-page) for ad/landing copy |
| `templates/persona-lean.md` | Lean persona card (1-page) for ad/landing copy Generated from `templates/persona-lean.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/persona-full.md.j2` | Full persona doc with JTBD + pains + day-in-the-life + kill criteria |
| `templates/persona-full.md` | Full persona doc with JTBD + pains + day-in-the-life + kill criteria Generated from `templates/persona-full.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/persona-negative.md.j2` | Negative persona template (who we do not serve) |
| `templates/persona-negative.md` | Negative persona template (who we do not serve) Generated from `templates/persona-negative.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/cluster-personas.py` | Cluster transcripts by JTBD tags; print top-K segments |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-persona-building.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[user-research-at-scale]]
- [[continuous-discovery]]
- [[market-research-tam-sam-som]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cluster-personas.py`

```python
#!/usr/bin/env python3
"""
cluster-personas.py — first-draft persona trait clustering from a directory of interview transcripts.

Usage: python cluster-personas.py .aidocs/research/interviews/ > draft-persona.md

Each .md file in the directory is treated as one interview transcript.
Extracts trait patterns across 4 axes (role, goal, frustration, trigger),
counts citations per value, marks traits with fewer than 3 citations as [WEAK].

Output is a draft Markdown persona that requires human review and citation verification.
"""
import sys
import pathlib
import re
import collections


AXES = {
    "role": re.compile(
        r"(?im)^[^\n]*(?:role|title|job)\s*[:\-]\s*(.+)$"
    ),
    "goal": re.compile(
        r"(?im)^[^\n]*(?:goal|wants?\s+to|trying\s+to)\s*[:\-]\s*(.+)$"
    ),
    "frustration": re.compile(
        r"(?im)^[^\n]*(?:frustration|pain|blocker|stuck|annoyed)\s*[:\-]\s*(.+)$"
    ),
    "trigger": re.compile(
        r"(?im)^[^\n]*(?:buy|signed\s+up|started\s+using|switched)\s+(?:when|after|because)\s+(.+)$"
    ),
}

WEAK_THRESHOLD = 3


def main(interview_dir: str) -> None:
    interviews = sorted(pathlib.Path(interview_dir).glob("*.md"))
    if not interviews:
        print(f"No .md files found in {interview_dir}", file=sys.stderr)
        sys.exit(1)

    traits: dict[tuple[str, str], list[str]] = collections.defaultdict(list)

    for f in interviews:
        text = f.read_text(encoding="utf-8", errors="ignore")
        for axis, rx in AXES.items():
            for m in rx.finditer(text):
                value = m.group(1).strip().lower()[:80]
                line = text[: m.start()].count("\n") + 1
                citation = f"[{f.stem}:L{line}]"
                traits[(axis, value)].append(citation)

    print("# Draft Persona (auto-generated — requires human review)\n")
    print("> WARNING: All traits must be verified against source transcripts.")
    print("> Traits marked [WEAK] have fewer than 3 citations and must not appear in the final persona.\n")

    for axis in ("role", "goal", "frustration", "trigger"):
        print(f"## {axis.title()}\n")
        rows = sorted(
            ((key[1], val) for key, val in traits.items() if key[0] == axis),
            key=lambda r: -len(r[1]),
        )
        if not rows:
            print("*(no patterns found)*\n")
            continue
        for value, cites in rows[:5]:
            flag = " **[WEAK]**" if len(cites) < WEAK_THRESHOLD else ""
            cite_str = " ".join(cites[:5])
            print(f"- {value}{flag} — {len(cites)} mention(s) {cite_str}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <interview-directory>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
```
