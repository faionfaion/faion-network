# AI Agent Prompt Handover

## Summary

**One-sentence:** Hand-over format for the AI-agent prompts, system rules, and guardrails the vendor team built, structured so a different in-house team can read, run, and modify them without rebuild.

**One-paragraph:** When a vendor leaves, the client inherits Copilot / Claude / Cursor prompts and rules the vendor's team built. Nothing tells you how to format, transfer, and document those for a different in-house team. This methodology defines the four required handover artefacts (prompt inventory, parameter map, run-book, validation suite), the round-trip check (incoming team runs the prompts blind against the validation suite), and the version + ownership cap. Output is a single `prompt-handover/` directory committed at engagement close.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «ai agent prompt handover» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- an engagement is closing AND code ownership transfers to a client in-house team.
- the vendor built prompts / system rules / agent skills for the engagement.
- the receiving team has at least one engineer who will own the prompts going forward.

## Skip If (ANY kills it)

- no agent prompts were built (engagement used vanilla off-the-shelf agents) -- there is nothing to hand over.
- the receiving team has formally declined AI-agent inheritance -- ship a 'do not use these' notice.
- the engagement contract owns the prompts as deliverables under a different format -- defer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the AI Agent Prompt Handover task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdlc-ai/ai-agent-guardrails-pack` | guardrails pack is one of the handover artefacts that this methodology references. |
| `pro/sdd/sdd/agents-md-for-receiving-team` | AGENTS.md handover is the sibling for general project context. |

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
| `templates/prompt-inventory.md` | Inventory + parameter map skeleton + validation-suite stub. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-agent-prompt-handover.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[ai-agent-guardrails-pack]]
- [[agents-md-for-receiving-team]]
- [[faion-cli-agent-adapter-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
