# Dark Knowledge Extraction Protocol

## Summary

**One-sentence:** Structured interview + repo-walk protocol that surfaces tacit, only-in-my-head context from a leaving senior into a written hand-over pack that survives the rotation.

**One-paragraph:** Living-documentation methodology assumes you already know what to write down. Extracting tacit / only-in-my-head context from a senior who is about to leave is a separate, harder problem and ships zero pages otherwise. This methodology defines the structured-interview protocol (5 themed sessions, 90 minutes each), the repo-walk pairing (interviewer + outgoing engineer review hot files together), the scribe contract (capture decisions, gotchas, war stories, and 'do not let the AI agent do X here'), and the receiving-team validation gate (incoming engineer applies the pack against 3 representative tasks before signoff). Output is a versioned hand-over pack indexed to repo paths and named contacts.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «dark knowledge extraction protocol» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- a senior with >=6 months on the codebase is leaving or rotating off.
- no prior hand-over pack exists OR the existing one is >12 months stale.
- a receiving engineer is identified and available for the validation sessions.

## Skip If (ANY kills it)

- the leaver has <2 months on the codebase -- their tacit knowledge is shallow; standard docs suffice.
- the codebase is being deprecated -- write a postmortem-style sunset note instead.
- the leaver refuses to participate -- this methodology cannot be coerced; escalate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Dark Knowledge Extraction Protocol task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/sdd/agents-md-for-receiving-team` | downstream consumer: pack is one of the inputs to the receiving-team's AGENTS.md. |
| `pro/sdd/decision-log-reconstruction-from-git` | complementary methodology that reconstructs the 'why' from git history alongside this 'how' capture. |

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
| `templates/dark-knowledge-pack.md` | 5-session pack skeleton: architecture / hot files / on-call / contacts / AI rules. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dark-knowledge-extraction-protocol.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[agents-md-for-receiving-team]]
- [[decision-log-reconstruction-from-git]]
- [[client-conventions-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
