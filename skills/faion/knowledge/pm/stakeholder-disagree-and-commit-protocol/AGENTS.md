# Stakeholder Disagree-and-Commit Protocol

## Summary

**One-sentence:** A documented disagree-and-commit protocol where dissenting stakeholders sign a "commit now, revisit at trigger" line on a prioritisation decision, plus explicit escalation thresholds, so the roadmap stops getting silently unwound by post-decision lobbying.

**One-paragraph:** Generic stakeholder-management methodologies talk about alignment in the abstract but offer no concrete protocol for the moment a prioritisation decision is taken with active disagreement. The result on P6 product teams: a roadmap is approved, then dissenting stakeholders quietly lobby individual engineers, ask for "small additions", or re-litigate at the next review. This methodology codifies the disagree-and-commit moment: name the dissenting stakeholder, capture the grounds, get them to sign one of `commit-with-revisit` or `escalate-now`, set an explicit revisit trigger (metric crosses threshold OR date passes), and route any escalation to a pre-named threshold owner within the same week. The artefact lives in the decision register and becomes the canonical reference if the conflict re-surfaces. Replaces "we discussed it and decided" entries with auditable commitments.

**Ефективно для:**

- Roadmap-рішення приймається з активним dissent з боку стейкхолдера.
- PM веде decision register і потребує auditable commitment, а не "ми обговорили".
- Команда страждає від post-decision lobbying, що тихо розкручує roadmap mid-quarter.

## Applies If (ALL must hold)

- Prioritisation or roadmap decision was taken with at least one stakeholder objecting on the record.
- The PM owns the decision register and roadmap document.
- Project has a pre-named threshold owner (program head, VP product, sponsor) for escalation.
- Decision affects work that will be committed for at least the current quarter.

## Skip If (ANY kills it)

- Unanimous decision — no dissent to capture.
- Pure operational ticket (bug fix, small enhancement) — over-engineered.
- Project does not maintain a roadmap (e.g., pure backlog scheduling) — protocol has no home document.
- No threshold owner is reachable (vacancy, gap) — fix that first; without escalation the protocol is incomplete.

## Prerequisites

- Decision register / roadmap location agreed and writable by the PM.
- Named threshold owner for escalation documented in project charter.
- Metric or date the team agrees to use as a revisit trigger (e.g., "if churn >5% by end Q3").

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/stakeholder-management` | Underlying stakeholder mapping and engagement plan. |
| `pro/ba/decision-rationale-capture` | Format for the written decision artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-if` | sonnet | Decision tree application against typed inputs. |
| `gather-typed-inputs` | haiku | Mechanical fetch + source-pin. |
| `produce-artefact` | sonnet | Per-instance judgment; bounded inputs. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-disagree-and-commit-protocol.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/stakeholder-disagree-and-commit-protocol.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-stakeholder-disagree-and-commit-protocol.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-disagree-and-commit-protocol.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/pm/project-manager/`
- peer: `stakeholder-conflict-facilitation-script`, `escalation-decision-template`, `cross-team-handoff-tracker`
- external: "Disagree and commit" — Amazon Leadership Principles (Bezos 1997 shareholder letter)

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
