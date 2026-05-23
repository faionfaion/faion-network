# Decision Log Reconstruction From Git

## Summary

**One-sentence:** Walks git history + PR comments + ticket links and reconstructs an ADR-shaped decision log for repos that never had one, so a late-joining engineer can answer 'why is it this way' without re-deriving each decision.

**One-paragraph:** When engineers join late or hand off, they reverse-engineer 'why' from git log + PR comments + ticket links. A methodology + AI-agent prompt pack that walks the repo, surfaces ADR-shaped decisions, and writes them up is high-leverage and entirely missing. This methodology defines the walk strategy (commit-message + PR-body + ticket-link triangulation), the decision detector (commits matching the ADR pattern: context -> options -> decision -> consequences), the dedupe + clustering pass (similar decisions across multiple commits), and the owner-signoff gate. Output is a reconstructed `decisions/` folder of ADR-shaped markdown files, each cross-linked to commit SHAs.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «decision log reconstruction from git» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- the repo has >=12 months of history and >=200 commits.
- no existing decision log / ADR folder OR existing one is <30% complete.
- you can identify at least one original-author contact to validate ambiguous decisions.

## Skip If (ANY kills it)

- the repo is < 3 months old -- decisions are still in active memory; write ADRs going forward instead.
- the repo is being sunset -- skip; write a postmortem narrative if anything.
- you lack permission to read PR comments / ticket system -- the triangulation does not work without them.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Decision Log Reconstruction From Git task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/dark-knowledge-extraction-protocol` | complementary methodology: this one extracts what git knows, that one extracts what only the leaver knows. |
| `pro/sdd/sdd-planning/definition-of-ready-template` | consumes 'why was this decided' inputs from this reconstructed log. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-skeleton.md` | Per-ADR skeleton: context / options considered / decision / consequences / commit links / signoff. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-log-reconstruction-from-git.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[dark-knowledge-extraction-protocol]]
- [[agents-md-for-receiving-team]]
- [[client-conventions-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
