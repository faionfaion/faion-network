# Agent Integration — Requirements Validation

## When to use
- Before flipping an SDD feature from `todo/ → in-progress/`: validate that `spec.md` requirements (and AC) actually match what the stakeholder asked for, not what the elicitation agent inferred.
- After a non-trivial elicitation session where an agent transcribed and summarised stakeholder input — validation closes the loop on summarisation drift.
- When a major change is proposed mid-flight (scope edit, regulatory addition) and you need a re-validation pass before resuming `faion-feature-executor`.
- Pre-baseline gate: locking a `spec.md` version before design starts so subsequent code/test work has a stable contract.
- Generating a structured issue log (severity-tagged) that the SDD `mistakes.md` and `patterns.md` memory can ingest.
- Driving a prototype-based check (Storybook/Playwright walkthrough) where users perform tasks and the agent records deviations.

## When NOT to use
- Throwaway spikes / research tasks where the deliverable is a learning, not a baseline. Use a stop condition + brief, not validation.
- Pre-elicitation: validating empty or aspirational requirements is theatre. First elicit, then draft, then validate.
- Pure operational/runbook tweaks (cron edits, nginx vhost changes) — verify with smoke tests, not validation sessions.
- Strictly internal refactors with no behaviour change — validation has no input signal.
- Post-launch: at that point, use measurement (Solution Evaluation) and feedback loops, not validation. Validation is a pre-build artefact.

## Where it fails / limitations
- **Rubber-stamp risk under agent automation.** An agent generating a sign-off form auto-fills "Approved" when the human only skims. Mitigation: require an explicit per-AC `approve|defer|reject` verb from a named human, not a bulk OK.
- **Stakeholder-impedance mismatch.** Validation assumes business stakeholders can read agent-produced Gherkin/AC. They often cannot — translate to plain-language scenarios first.
- **Quality-attribute checks are syntactic, not semantic.** "Unambiguous" passes regex linting yet still hides multiple interpretations. Pair lint with NLI/contradiction checks (LLM-as-judge with a contradiction prompt).
- **Traceability decays.** Once `spec.md` is baselined, subsequent edits skip re-validation; production drifts. Tie validation to a pre-commit hook on `spec.md` changes.
- **Session bloat.** Validating 200 requirements in one walkthrough is the canonical anti-pattern in the README. LLMs amplify this — they will happily emit 200 issues with no severity filter.
- **Hallucinated stakeholders.** Agents fabricate "the Finance SME confirmed X" when no such session occurred. Always require a session-id / chat-log link as evidence.
- **Sign-off authority.** An agent does not have authority to sign off. It can prepare, route, capture, but the signature must be human and auditable.

## Agentic workflow

Run validation as a 4-stage chain inside the SDD lifecycle. Stage 1: a research subagent loads `spec.md`, `design.md`, source elicitation notes, and any related `data-analysis.md` / `interface-analysis.md`, then emits a per-requirement quality scorecard against the 8 attributes (correct, complete, unambiguous, consistent, testable, traceable, feasible, necessary). Stage 2: a session-preparation agent picks the technique (walkthrough vs. inspection vs. prototype review vs. simulation) based on requirement type, drafts agenda + pre-read packet, and assigns reviewers. Stage 3 is human-led — agent only takes minutes, transcribes decisions, and writes a structured issue log. Stage 4: a re-validation gate verifies that every issue is resolved or explicitly deferred before allowing baseline. `faion-feature-executor` should refuse to advance any task whose source AC has unresolved validation issues.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the per-task validation gate; reads issue log, blocks `done/` move if open issues remain.
- `faion-feature-executor` — wires validation as a quality gate between `todo/ → in-progress/` (initial validation) and `in-progress/ → done/` (final sign-off proxy).
- `faion-brainstorm` — diverge phase: enumerate edge cases the requirements may miss (security, locale, error, concurrency); converge phase: keep only items reviewers care about. Use before the human session, not instead of it.
- `faion-improver` — periodic audit: scans `spec.md` files in `done/` for AC that drifted from production, flags re-validation candidates.
- (Optional) a custom `faion-ba-validator-agent` — single-purpose Sonnet agent that emits the quality scorecard JSON; cheaper than running Opus on a checklist task.

### Prompt pattern

Quality scorecard (Stage 1, structured output):
```xml
<role>BA validator. Score each requirement against 8 quality attributes.</role>
<inputs>
  <spec>{spec_md}</spec>
  <design>{design_md}</design>
  <source>{elicitation_notes}</source>
</inputs>
<rules>
  Output JSON array. Per item:
  {req_id, correct, complete, unambiguous, consistent, testable,
   traceable, feasible, necessary, severity, evidence_quote, recommendation}
  - Each attribute: pass|fail|na. severity: high|medium|low.
  - evidence_quote: exact substring from spec/design/source justifying the call.
  - No prose outside JSON. No invented req_ids.
</rules>
```

Session minutes (Stage 3):
```xml
<task>From transcript {transcript_url}, emit a JSON issue log:
{ac_id, issue, severity, root_cause, owner, resolution, resolution_status}.
resolution_status in: open|deferred|resolved.
Refuse to set resolved without an evidence_quote from the transcript.</task>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gherkin-lint` | Lint Gherkin AC for ambiguity / style; cheap pre-validation pass. | `npm i -g gherkin-lint` |
| `vale` | Prose linter with custom styles ("avoid weasel words", "no TBD"). Drives the lexical half of the unambiguity check. | vale.sh |
| `proselint` | English clarity/consistency linter; complements vale on structural prose. | `pip install proselint` |
| `markdownlint-cli2` | Catches malformed tables in `spec.md` (broken traceability matrices). | `npm i -g markdownlint-cli2` |
| `lychee` | Verifies all spec/design hyperlinks resolve — broken trace = broken validation. | `cargo install lychee` |
| `git-blame-someone-else` (or `git log -p spec.md`) | Show who last touched each requirement; informs re-validation scope. | builtin git |
| `pandoc` | Convert `spec.md` to PDF/DOCX for non-engineer reviewers; required for many regulated sign-offs. | pandoc.org |
| `mermaid-cli` | Render trace matrices / decision flows from `spec.md` for the validation packet. | `npm i -g @mermaid-js/mermaid-cli` |
| `Reqnroll` / `Cucumber` | Execute AC as living tests so validation outcomes survive into CI. | reqnroll.net · cucumber.io |
| `aider` / `claude` (CLI) | Drive the quality scorecard prompt against `spec.md` from a pre-commit hook. | aider.chat · docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira + Xray / Zephyr | SaaS | Yes (REST API) | Requirements ↔ test ↔ validation result trace; agents POST issue logs to the requirement ticket. |
| Azure DevOps | SaaS | Yes (REST API) | Native "Acceptance Criteria" + "Reviewers" fields; sign-off captured as work-item state transition. |
| Linear | SaaS | Yes (GraphQL) | Lightweight; AC + issue log live in description; convention-driven validation tags. |
| Polarion / Jama Connect | SaaS | Partial (REST) | Strong reqs lifecycle + formal sign-off, regulated industries (medical/aero). Heavy for solo. |
| ReqView | Desktop + cloud | Partial | ReqIF import/export; agents can transform but UX is human-driven. |
| DocuSign / Adobe Sign | SaaS | Yes (REST) | Auditable sign-off layer over a generated sign-off PDF (pandoc). |
| Loom / tl;dv / Otter.ai | SaaS | Yes (REST/webhook) | Record + transcribe validation sessions; transcript → minutes agent. |
| GitHub Issues + sub-issues | SaaS | Yes (REST/GraphQL) | Issue log as task list; validation closes via PR merge. Works for OSS/solo. |
| Confluence / Notion | SaaS | Partial | Pre-read packets, draft minutes; weak on traceability — pair with a real reqs tool. |
| Storybook + Chromatic | SaaS/OSS | Yes (CLI) | Prototype-review validation: visual diff against approved baseline; agents can flag drift. |
| Playwright `test.step` | OSS | Yes (CLI) | Simulation-style validation: replay user task scripts, capture deviations. |

## Templates & scripts

The methodology files in this folder are stub-only (only `README.md` has content). Reuse the README's three templates (review checklist, session agenda, sign-off form) and add the script below as a CI-friendly pre-validation gate.

```bash
#!/usr/bin/env bash
# req-validate.sh — pre-validation lint over spec.md + traceability sanity.
# Fails on: TBD/TODO, weasel words, AC without IDs, AC IDs without test refs.
set -euo pipefail
DIR="${1:?feature dir required}"
SPEC="$DIR/spec.md"; PLAN="$DIR/test-plan.md"
[[ -f "$SPEC" && -f "$PLAN" ]] || { echo "missing spec.md or test-plan.md" >&2; exit 2; }

fails=0
weasel='\b(fast|slow|user-?friendly|intuitive|reasonable|appropriate|robust|seamless|scalable)\b'
if grep -InE 'TBD|TODO|XXX|\?\?\?'  "$SPEC"; then echo "FAIL: placeholder text in spec" >&2; fails=$((fails+1)); fi
if grep -InEi "$weasel"              "$SPEC"; then echo "FAIL: weasel words in spec"     >&2; fails=$((fails+1)); fi

mapfile -t IDS  < <(grep -oE 'REQ-[A-Z0-9]+-[0-9]+|AC-[A-Z0-9]+-[0-9]+' "$SPEC" | sort -u)
mapfile -t REFS < <(grep -oE 'REQ-[A-Z0-9]+-[0-9]+|AC-[A-Z0-9]+-[0-9]+' "$PLAN" | sort -u)
miss=()
for id in "${IDS[@]}"; do
  printf '%s\n' "${REFS[@]}" | grep -qx "$id" || miss+=("$id")
done
if (( ${#miss[@]} )); then
  printf 'FAIL: %s requirements without test reference:\n' "${#miss[@]}" >&2
  printf '  %s\n' "${miss[@]}" >&2
  fails=$((fails+1))
fi

(( fails == 0 )) || exit 1
echo "OK: ${#IDS[@]} requirements, no placeholders, no weasel words, all traced."
```

Wire as a pre-commit hook on `spec.md`/`test-plan.md` paths and as a gate inside `faion-feature-executor` before the human validation session.

## Best practices
- **Validate small, validate often.** Cap any one session at ~25 requirements; the README anti-pattern of "200 in one go" is the single most common failure mode.
- **Right reviewers, named.** A session without the actual decision-maker is preparation, not validation. Agent-prepared agendas must list specific names + roles, not "Product Owner TBD".
- **Severity discipline.** Every issue gets H/M/L *plus* a root cause class (missing info, ambiguous wording, conflict, infeasible, gold-plating). Drives re-validation scope.
- **Two-pass sign-off.** Pass 1 reviews the requirements; pass 2 reviews the resolved issue log against pass 1. Single-pass sign-off masks unresolved items.
- **Traceability matrix is non-optional.** REQ → source → AC → test ID → review status, in `spec.md` or a generated artefact. Agents enforce this with the script above.
- **Prototype + simulation beat documents for UI/process reqs.** When validating UX or process flows, switch technique — Storybook click-through or BPMN-driven walk beats reading a numbered list.
- **Capture conditions, not just approvals.** "Approved subject to X" without X tracked is the same as "rejected, but politely". Conditions go on a tracked owner with a resolution status.
- **Re-validate on substantive change.** Heuristic: any edit that changes acceptance behaviour, NFRs, or external interfaces re-triggers validation; copy-edits do not.
- **Living docs.** Generate the validated requirements snapshot into the SDD `done/` folder (markdown + signed PDF if regulated); this becomes the auditable baseline.

## AI-agent gotchas
- **Hallucinated approvals.** Models generate "Approved by: Product Owner" when no human approved. Mitigation: require a verifiable evidence anchor (chat permalink, ticket transition, signed PDF hash) before any `resolved`/`approved` state.
- **Confirmation-bias scoring.** When asked "are these requirements OK?", LLMs trend toward yes. Use adversarial framing: "find at least 3 ways each requirement could be misinterpreted" before asking it to grade.
- **Lost source provenance.** Agents quote `spec.md` back to itself instead of the elicitation source. Force `evidence_quote` to come from the source document, not the artefact under review.
- **Severity inflation.** Agents tag every issue High to look thorough. Anchor severity to a concrete rule: H = blocks design, M = needs clarification before implementation, L = wording.
- **Scope drift via "while we're here".** Agents propose new requirements during validation. Validation modifies, it does not extend — extensions return to elicitation.
- **Stakeholder simulation.** Tempting to skip humans by role-playing "as Product Owner". Disallowed for sign-off. Acceptable only as a dry run feeding the agenda.
- **Token-cost trap on large specs.** Loading the full `spec.md` per attribute per requirement explodes cost. Batch by section; cache the design.md / source elicitation packet.
- **Locale and accessibility blindness.** Agents default to English/USD/desktop happy paths and silently pass i18n/a11y reqs. Add a per-validation locale + a11y matrix prompt slot.
- **Human-in-the-loop checkpoints.** Three are mandatory: (1) reviewer selection, (2) decision capture during the session, (3) sign-off. Agents prepare and transcribe; humans decide.
- **Dont conflate validation with verification.** Agents will quietly run tests and call it validation. The README is explicit: validation = right thing; verification = built right. Keep the artefacts and gates separate.

## References
- IIBA, *BABOK v3*, ch. 8 "Requirements Analysis and Design Definition" + ch. 10 technique "Reviews".
- Wiegers & Beatty, *Software Requirements*, 3rd ed. (Microsoft Press, 2013) — chapters on validation, inspection, and sign-off.
- Gilb & Graham, *Software Inspection* (Addison-Wesley, 1993) — formal inspection technique.
- ISO/IEC/IEEE 29148:2018 — Requirements engineering, validation criteria.
- Adzic, *Specification by Example* (Manning, 2011) — living documentation and validation through executable examples.
- Reqnroll docs — reqnroll.net (post-SpecFlow .NET BDD; validation-as-tests).
- Cucumber tag expressions — cucumber.io/docs/cucumber/api/#tag-expressions.
- Internal: `agents/faion-sdd-executor-agent.md`, sibling `acceptance-criteria/agent-integration.md`, repo SDD convention in `AGENTS.md`.
