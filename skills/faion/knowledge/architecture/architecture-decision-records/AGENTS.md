# Architecture Decision Records (ADRs)

## Summary

**One-sentence:** Captures one architecturally significant decision per ADR with Context, Decision, Consequences, Alternatives. Lock format; CI-enforce; treat as first-class artefacts.

**One-paragraph:** An ADR is a short document — 1-2 pages — capturing one architecturally significant decision, stored in version control next to the code it explains so the choice outlives the team's memory and the same debates stop recurring. Standard format (Nygard or MADR), locked in ADR-0001, enforced by CI. Output is an ADR file in `docs/adr/` plus an updated ADR index, consumed downstream by `design-docs-patterns` and `code-review-cycle`. Status fields (Proposed, Accepted, Deprecated, Superseded) demand periodic review; pair with `adr-staleness-audit` quarterly.

**Ефективно для (додатково):** solo devs and small teams who keep re-debating 'why did we pick Postgres over MongoDB' every six months because nobody wrote it down.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'architecture decision record' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- An architecturally significant decision is being made (database, framework, language, deployment target, pattern, boundary).
- More than one option was considered — ≥2 genuine alternatives, not strawmen.
- The decision will affect future work or be referenced by ≥2 people, and will be revisited or questioned within 18 months.
- The repo has a `docs/adr/` or `.aidocs/decisions/` folder to store it in.

## Skip If (ANY kills it)

- Trivial implementation choice with no cross-cutting impact.
- Operational tweak (CDN cache TTL, log level).
- Decision reversible inside a single sprint, or reversible-without-cost dev-tooling tweak.
- One-person hobby project with no future readership.
- Same decision already documented in an existing ADR.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision context | problem statement | the deciding engineer |
| Alternatives explored | ≥2 options | design discussion |
| ADR-0001 (format lock) | ADR file | repo ADR folder |
| ADR index file | markdown | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/adr-reversibility-tagging` | Optional pairing — tag reversibility on every ADR. |
| `solo/sdd/sdd/design-docs-patterns` | Sibling — ADRs extract from design docs once locked. |
| `solo/sdd/sdd/living-documentation` | Parent — ADRs live in the docs-as-code repo. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip-this-methodology fallback | ~1500 |
| `content/02-output-contract.xml` | essential | JSON Schema + allowed transformations + forbidden patterns + self-check checklist | ~1400 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + detector + root-cause + fix | ~1000 |
| `content/04-procedure.xml` | medium | 5-step procedure: scope → alternatives → draft → review → merge | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-adr` | haiku | Template fill from prerequisites. |
| `synthesize-alternatives` | sonnet | Generate rejected options + reasons. |
| `audit-against-rules` | sonnet | Bounded judgement: do outputs satisfy `01-core-rules.xml`? |
| `audit-adr-portfolio` | opus | Cross-ADR consistency and staleness audit; sign-off before downstream handoff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-nygard.md.j2` | Nygard-format ADR template (Title, Status, Context, Decision, Consequences). |
| `templates/adr-nygard.md` | Nygard-format ADR template (Title, Status, Context, Decision, Consequences). Generated from `templates/adr-nygard.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/adr-madr.md.j2` | MADR-format ADR template (with Considered Options and Pros/Cons of the Decision). |
| `templates/adr-madr.md` | MADR-format ADR template (with Considered Options and Pros/Cons of the Decision). Generated from `templates/adr-madr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/adr-lint.sh` | CI lint script — filename/status/sections/superseded-ref checks across `docs/adr/`. |
| `templates/adr-authoring-template.md.j2` | Fill-in ADR with inline guidance, a "Do nothing" baseline option, and split Positive/Negative/Risks consequences. |
| `templates/adr-authoring-template.md` | Fill-in ADR with inline guidance, a "Do nothing" baseline option, and split Positive/Negative/Risks consequences. Generated from `templates/adr-authoring-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/new-adr.sh` | Scaffold the next-numbered ADR into `docs/adr/` from the authoring template. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architecture-decision-records.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[adr-reversibility-tagging]]
- [[architect-pr-review-checklist]]
- [[decision-tree-architecture-style]]
- [[design-docs-patterns]]
- [[design-docs-big-tech]]
- [[code-review-cycle]]
- [[living-documentation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/adr-lint.sh`

```bash
set -euo pipefail

ADR_DIR="${1:-docs/adr}"
# r4-status-discipline closes the enum at exactly these four. "Draft" and
# "Rejected" were accepted here until the sdd merge surfaced the contradiction
# with the schema in content/02-output-contract.xml.
VALID_STATUSES=("Proposed" "Accepted" "Deprecated" "Superseded")
ERRORS=0
FILES_CHECKED=0

if [[ ! -d "$ADR_DIR" ]]; then
    echo "ERROR: ADR directory '$ADR_DIR' not found"
    exit 1
fi

for file in "$ADR_DIR"/*.md; do
    [[ -f "$file" ]] || continue
    FILES_CHECKED=$((FILES_CHECKED + 1))
    filename=$(basename "$file")
    file_errors=0

    # 1. Filename must match NNNN-kebab-case-title.md
    if ! echo "$filename" | grep -qP '^\d{4}-[a-z0-9-]+\.md$'; then
        echo "FAIL [$filename] Filename must match NNNN-kebab-case-title.md"
        file_errors=$((file_errors + 1))
    fi

    # 2. Status line must be present and valid
    status_line=$(grep -m1 "^\*\*Status:\*\*" "$file" 2>/dev/null || true)
    if [[ -z "$status_line" ]]; then
        echo "FAIL [$filename] Missing **Status:** line"
        file_errors=$((file_errors + 1))
    else
        status_valid=false
        for valid_status in "${VALID_STATUSES[@]}"; do
            if echo "$status_line" | grep -q "$valid_status"; then
                status_valid=true
                break
            fi
        done
        if [[ "$status_valid" == "false" ]]; then
            echo "FAIL [$filename] Invalid status in: $status_line"
            echo "       Valid statuses: ${VALID_STATUSES[*]}"
            file_errors=$((file_errors + 1))
        fi
    fi

    # 3. Nygard sections: Context, Decision, Consequences
    for section in "## Context" "## Decision" "## Consequences"; do
        if ! grep -q "^${section}" "$file"; then
            echo "FAIL [$filename] Missing required section: ${section}"
            file_errors=$((file_errors + 1))
        fi
    done

    # 4. Superseded ADRs must reference the superseding ADR
    if echo "$status_line" | grep -q "Superseded"; then
        if ! grep -q "Superseded by ADR-" "$file"; then
            echo "FAIL [$filename] Status is Superseded but no 'Superseded by ADR-NNNN' reference found"
            file_errors=$((file_errors + 1))
        fi
    fi

    if [[ $file_errors -eq 0 ]]; then
        echo "OK   [$filename]"
    fi

    ERRORS=$((ERRORS + file_errors))
done

echo ""
echo "Checked $FILES_CHECKED ADR file(s). Errors: $ERRORS"

if [[ $ERRORS -gt 0 ]]; then
    exit 1
fi
```
