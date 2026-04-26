# Agent Integration — Requirements Validation (BA Core)

This is the *ba-core* angle on Requirements Validation: BABOK v3 task fundamentals, the validation-vs-verification distinction, and how an agentic BA pipeline operationalises both. The richer SDD/tooling angle lives in the sibling `business-analyst/requirements-validation/agent-integration.md`; here we stay close to the core practice.

## When to use
- BABOK Task 7.6 trigger: a requirement (or design) is ready to be confirmed against business need before any downstream commitment is made.
- Pairing with Verification (BABOK 7.5) inside a single review pass — verify the artefact is well-formed, validate it represents the right need.
- Before requirements are *baselined* in a Requirements Repository (ba-core "Maintain Requirements" task) — validation is the gate.
- When a stakeholder need is restated by an agent (summary, paraphrase, transcription) — close the loop on representational drift.
- When an existing baselined requirement is challenged by new information (regulation, market signal, data analysis result) and you need a re-validation pass, not a fresh elicitation.
- For a capstone gate before transitioning from "Requirements Analysis & Design Definition" to "Solution Evaluation".

## When NOT to use
- Pre-elicitation: there is nothing to validate yet. Run elicitation-techniques + requirements-documentation first.
- For pure technical-quality concerns (form, style, consistency) — that is *Verification*, not validation. Confusing them is the canonical BA-core mistake.
- Throwaway prototypes meant to provoke a reaction; the prototype itself is the elicitation tool, not a candidate for sign-off.
- Operational/maintenance changes with no new business need (e.g. dependency bumps, refactors).
- After delivery — replace with Solution Evaluation (BABOK ch. 8) and feedback-loop measurement.

## Where it fails / limitations
- **Validation vs Verification confusion.** BAs (and LLMs) routinely run a Verification checklist (well-formed, unambiguous, testable) and call it validation. Validation specifically asks "does this requirement deliver value to the business?" — if the value question is not asked, no validation occurred.
- **No defined value model.** If business value is not explicit (KPIs, OKRs, benefit map), validation devolves into stakeholder opinion. Anchor every validation pass to the *Business Need* and *Solution Scope* that BABOK 5.1 / 6.1 produced.
- **Sign-off without authority.** The named approver lacks decision rights; political validation rather than substantive validation. BA-core fix: trace approver to the RACI built in `ba-planning` / `stakeholder-analysis`.
- **Single technique reliance.** Walkthrough alone misses what a prototype review or simulation would expose, and vice versa. BABOK enumerates 11+ techniques in 10.x; pick by requirement type.
- **Late validation.** Validating only at baseline is too late — defect cost compounds. Validate *as requirements emerge* per BABOK iterative guidance.
- **Confusing validation with UAT.** UAT validates the built solution; requirements validation validates the requirement *before* the build. Different artefact, different audience.
- **Agent-amplified rubber stamping.** Agents writing approve/reject decisions without a real human anchoring the value judgement.

## Agentic workflow

Follow BABOK Task 7.6 inputs/outputs as the contract: inputs are *Requirements (any state)*, *Designs*, and *Business Need / Solution Scope*; output is *Requirements (validated)*. Stage 1: a research agent loads the requirements set + the value reference (Business Need, Goals, KPIs) and emits a per-requirement value-trace (which goal/objective the requirement serves, magnitude of contribution, confidence). Stage 2: an agent classifies each requirement by type (functional, NFR, business, stakeholder, transition) and recommends the BABOK technique most fit for purpose (Reviews, Acceptance and Evaluation Criteria, Item Tracking, Risk Analysis, Prototyping, etc.). Stage 3 is human-led — the agent only facilitates: distributes pre-read, captures decisions verbatim, structures the issue log. Stage 4: a re-validation gate confirms each issue is resolved, deferred (with owner + date), or rejected (with rationale) before the requirement transitions to "validated" in the repository. Inside this repo, plug the gate into `faion-feature-executor` between `todo/ → in-progress/`; the executor refuses to advance any task whose source requirement lacks a `validated: true` flag plus a value-trace.

### Recommended subagents
- `faion-sdd-executor-agent` — enforces the validation gate when moving SDD tasks; reads `validated` flag + value-trace from `spec.md` front-matter.
- `faion-feature-executor` — wires validation as a per-feature gate; refuses promotion without a value-trace and issue-log resolution.
- `faion-brainstorm` — runs an adversarial diverge pass ("how could this requirement still fail to deliver value?") before the human session; converges to a high-signal questions list.
- `faion-improver` — periodic re-validation sweep: scans baselined requirements in `done/` for value drift against current KPIs.
- (Optional, custom) `faion-ba-validator-agent` — Sonnet-tier agent producing the value-trace JSON; cheaper than Opus on a structured task.

### Prompt pattern

Value-trace (Stage 1):
```xml
<role>BA validator (BABOK 7.6). For each requirement, link to the Business Need.</role>
<inputs>
  <business_need>{business_need}</business_need>
  <goals_kpis>{goals_kpis}</goals_kpis>
  <requirements>{requirements_set}</requirements>
</inputs>
<rules>
  Output JSON. Per requirement:
  {req_id, goals_supported[], value_class: enabling|direct|indirect|none,
   contribution: high|medium|low, confidence: high|medium|low,
   evidence_quote, validation_question}
  - validation_question: a single yes/no the human reviewer must answer.
  - If value_class = none: severity = high, recommendation = "remove or re-elicit".
  - No invented req_ids. evidence_quote must come from inputs, not paraphrase.
</rules>
```

Technique selection (Stage 2):
```xml
<task>For each requirement, recommend ONE BABOK validation technique from:
[Reviews, Acceptance and Evaluation Criteria, Prototyping, Item Tracking,
 Risk Analysis and Management, Decision Analysis, Metrics and KPIs].
Output {req_id, technique, rationale, participants_required}.
Rationale must cite requirement type (functional/NFR/business/stakeholder/transition).</task>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vale` | Prose linter for the *Verification* half (style, weasel words) so it does not contaminate the validation pass. | vale.sh |
| `markdownlint-cli2` | Catches malformed traceability tables in `spec.md`. | `npm i -g markdownlint-cli2` |
| `lychee` | Verifies cross-document trace links (req → goal → test) resolve. | `cargo install lychee` |
| `pandoc` | Convert validated requirement set to PDF for stakeholder sign-off (regulated industries). | pandoc.org |
| `mermaid-cli` | Render value-trace diagram (Goal → Requirement → AC) for the validation packet. | `npm i -g @mermaid-js/mermaid-cli` |
| `git log -p spec.md` | Surface what changed since last validation; informs re-validation scope. | builtin git |
| `yq` / `jq` | Extract structured front-matter (`validated`, `value_trace`) for gating. | yq.dev · jqlang.github.io |
| `claude` (CLI) | Drive the value-trace prompt non-interactively from a pre-commit hook. | docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jama Connect | SaaS | Partial (REST) | BABOK-aligned reqs lifecycle, native validation status field, formal sign-off. Heavy for solo. |
| Polarion | SaaS | Partial (REST) | Same audience as Jama; ALM integration. Agents can read/update but UX is human-driven. |
| IBM DOORS Next | SaaS | Partial (OSLC) | Regulated industries; OSLC links carry value-trace cleanly. |
| Jira + Xray | SaaS | Yes (REST) | Pragmatic mid-market trace: Requirement issue type → Test → Validation result; agents transition workflow. |
| Azure DevOps | SaaS | Yes (REST) | Work-item state machine encodes "Proposed → Validated → Approved"; reviewers as fields. |
| Linear | SaaS | Yes (GraphQL) | Lightweight; convention-driven validation tags, value-trace in description. |
| ReqView | Desktop + cloud | Partial | ReqIF interchange; useful as a neutral export target. |
| Confluence / Notion | SaaS | Partial | Pre-read packets, draft minutes; weak on trace — pair with a real reqs tool. |
| Loom / tl;dv / Otter.ai | SaaS | Yes (REST/webhook) | Recorded validation sessions → transcript → minutes agent. |
| GitHub Issues | SaaS | Yes (REST/GraphQL) | OSS/solo: requirement issue type, validation as a labelled review, sign-off via PR merge. |

## Templates & scripts

The README ships review-checklist, session-agenda, and sign-off-form templates — reuse them as-is. The script below is a minimal value-trace gate enforcing BA-core's "validation = right thing" rule by failing when a requirement has no traced value class.

```bash
#!/usr/bin/env bash
# req-value-trace.sh — fail if any requirement in spec.md lacks a value-trace.
# Expects spec.md to carry a YAML block per requirement with:
#   req_id, value_class (enabling|direct|indirect|none), goals_supported (list).
set -euo pipefail
SPEC="${1:?spec.md required}"
[[ -f "$SPEC" ]] || { echo "missing $SPEC" >&2; exit 2; }

mapfile -t REQS < <(grep -oE 'REQ-[A-Z0-9]+-[0-9]+' "$SPEC" | sort -u)
fails=0
for r in "${REQS[@]}"; do
  block=$(awk -v r="$r" '
    $0 ~ "^---$" { in_yaml = !in_yaml; next }
    in_yaml && $0 ~ "req_id:[[:space:]]*"r { found=1 }
    found && $0 ~ "^---$" { exit }
    found { print }
  ' "$SPEC")
  if [[ -z "$block" ]]; then
    echo "FAIL: $r has no YAML value-trace block" >&2; fails=$((fails+1)); continue
  fi
  vc=$(printf '%s\n' "$block" | grep -oE 'value_class:[[:space:]]*[a-z]+' | awk '{print $2}')
  goals=$(printf '%s\n' "$block" | grep -c 'goals_supported:' || true)
  case "$vc" in
    enabling|direct|indirect) : ;;
    none)    echo "FAIL: $r value_class=none — remove or re-elicit" >&2; fails=$((fails+1));;
    *)       echo "FAIL: $r missing/invalid value_class" >&2; fails=$((fails+1));;
  esac
  (( goals > 0 )) || { echo "FAIL: $r no goals_supported" >&2; fails=$((fails+1)); }
done
(( fails == 0 )) || exit 1
echo "OK: ${#REQS[@]} requirements, all value-traced."
```

Wire into the SDD pre-commit hook and `faion-feature-executor` promotion gate.

## Best practices
- **Anchor every validation to a stated business value.** If you cannot name the goal/KPI/outcome a requirement supports, you are verifying, not validating.
- **Verify before you validate.** Run a verification pass first (form, ambiguity, testability) so the validation session debates value, not typos.
- **Match technique to requirement type.** Functional → walkthrough/inspection; NFR → measurement / risk analysis; UI/UX → prototype review; process → simulation; transition → operational walk.
- **Cap session size.** ≤25 requirements per session, ≤90 minutes; multi-pass beats marathon.
- **Severity has a rule, not a vibe.** H = blocks design, M = clarification before implementation, L = wording. Tie to the BABOK Risk Analysis output if available.
- **Two-pass sign-off.** Pass 1 reviews requirements, pass 2 reviews resolved-issue closure. Single-pass approvals quietly leave issues open.
- **Capture conditions explicitly.** "Approved subject to X" without a tracked X = polite rejection. Conditions go on a named owner with status.
- **Validate iteratively.** Per BABOK iterative-development guidance: validate as requirements emerge, not only at baseline.
- **Persist the validated baseline.** Snapshot the validated set (with value-trace) into the SDD `done/` artefact so re-validation has a stable diff target.

## AI-agent gotchas
- **Validation–verification conflation.** LLMs default to "is this well-written?" instead of "does this deliver value?". Force the value question: every prompt names the Business Need.
- **Hallucinated stakeholders.** Models invent SME confirmations. Require an evidence anchor (chat permalink, ticket, signed PDF hash) before any "approved" status.
- **Confirmation bias.** When asked "are these OK?", LLMs trend toward yes. Use adversarial framing: "list 3 ways each requirement could fail to deliver value" before scoring.
- **Severity inflation.** Agents tag everything High to look thorough. Anchor severity to the rule above and reject ungrounded H ratings.
- **Lost provenance.** Agents quote the requirement back to itself instead of the elicitation/business-need source. `evidence_quote` must come from upstream sources.
- **Scope drift.** Agents propose new requirements during validation — that returns to elicitation, not validation.
- **Stakeholder simulation.** Role-playing "as Product Owner" is a dry run, not a sign-off. Sign-offs require a named human.
- **Token cost on large specs.** Cache the Business Need / Goals; batch validation by section. Loading the whole spec per requirement explodes cost.
- **Locale + a11y blind spots.** Agents pass i18n/a11y requirements silently. Add a per-validation locale + a11y matrix.
- **Three mandatory human-in-the-loop checkpoints:** (1) reviewer selection, (2) live decision capture, (3) sign-off. Agents prepare and transcribe; humans decide.

## References
- IIBA, *BABOK Guide v3*, §7.6 "Validate Requirements" (canonical task), §7.5 "Verify Requirements" (sibling task), §10 techniques (Reviews, Acceptance and Evaluation Criteria, Prototyping, Risk Analysis, Item Tracking, Decision Analysis, Metrics and KPIs).
- IIBA, *Agile Extension to the BABOK Guide* — iterative validation guidance.
- Wiegers & Beatty, *Software Requirements*, 3rd ed. (Microsoft Press, 2013) — chapters on validation, verification, inspection, sign-off.
- ISO/IEC/IEEE 29148:2018 — Systems and software engineering: requirements validation criteria.
- Robertson & Robertson, *Mastering the Requirements Process* (Volere) — fit-for-purpose criteria, value model.
- Gilb & Graham, *Software Inspection* (Addison-Wesley, 1993) — formal inspection technique.
- Adzic, *Specification by Example* (Manning, 2011) — living documentation; validation through executable examples.
- Internal: sibling `business-analyst/requirements-validation/agent-integration.md` (richer tooling/SDD angle), `acceptance-criteria/`, `requirements-traceability/`, `requirements-lifecycle/`, `ba-planning/`.
