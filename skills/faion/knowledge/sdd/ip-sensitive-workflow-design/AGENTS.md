# IP-Sensitive Workflow Design

## Summary

**One-sentence:** Clean separation (repos, credentials, time-fenced work, IP-attribution log) for outsource specialists building side-SaaS without IP conflict with day-job clients.

**One-paragraph:** IP assignment clauses on day-job contracts vs personal side-SaaS create a hazard: code written 'on hours' or on company gear may belong to the client. A methodology that enforces clean separation is missing. This methodology defines the four-layer separation (physical device, credential store, repo namespace, time fence) plus an IP-attribution log that records when, where, and on whose gear each commit happened. Output is a workflow plan + per-commit attribution evidence that an arbitration board could use.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «ip-sensitive workflow design» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- you have a day-job employment or contractor agreement with an IP-assignment clause.
- you are actively building or maintaining a personal side-SaaS / open-source project.
- the side project is in a domain plausibly adjacent to the day-job client (raising hazard).

## Skip If (ANY kills it)

- your day-job contract carves out personal projects explicitly -- the hazard is already absent.
- the side project is on a publicly published codebase pre-dating the day-job contract.
- the side project is in a regime (jurisdiction / industry) where the IP clause is unenforceable -- consult counsel.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the IP-Sensitive Workflow Design task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/client-conventions-as-code` | day-job engagement conventions live in this file; personal project conventions do not. |
| `pro/sdd/soc2-evidence-generator-cli` | supplies the pattern for per-event evidence logs that the IP attribution log reuses. |

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
| `templates/ip-workflow-plan.md` | Plan skeleton: 4 separation layers + per-commit attribution log columns. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ip-sensitive-workflow-design.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[client-conventions-as-code]]
- [[soc2-evidence-generator-cli]]
- [[dark-knowledge-extraction-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
