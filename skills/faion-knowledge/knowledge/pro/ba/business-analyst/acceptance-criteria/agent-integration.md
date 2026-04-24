# Agent Integration — Acceptance Criteria (BA facilitation angle)

Sibling: `pro/ba/ba-modeling/acceptance-criteria` covers the modeling/notation
mechanics (Given-When-Then grammar, rule-based vs scenario-based shape). This
file focuses on the **business-analyst role**: cross-team AC facilitation,
the BA→QA hand-off, and traceability between PO intent, story AC, and
executable test cases.

## When to use

- Story has more than one stakeholder (PO + Dev + QA + Compliance) and
  agreement on "done" is non-trivial.
- AC will outlive the story: feeds regression suite, audit evidence, or
  vendor sign-off (regulated domains, SOC 2, HIPAA).
- BA owns the requirement and a separate QA team will write the test cases —
  AC is the contract between them.
- Backlog refinement / 3-amigos session: BA facilitates the conversation,
  not just transcribes it.
- API/integration story where developer A's "done" is consumer team B's
  "started" — AC must be machine-checkable.

## When NOT to use

- Spike / research story whose outcome is a recommendation, not behavior.
  Use a Definition of Ready exit-criteria checklist instead.
- One-line typo fix or copy change — the diff is the AC.
- UI exploration where the team is still discovering what "good" looks like
  (use design critique + opportunity-solution-tree, not AC).
- The team already lives in BDD .feature files driven by devs: writing
  Markdown AC duplicates the source-of-truth and goes stale.

## Where it fails / limitations

- AC inflation: PO + BA add criteria after sprint planning, devs do not
  re-estimate, QA finds 6 new scenarios in test design. Treat AC as
  versioned with the story; changes after commit = new story.
- AC theatre: long lists copy-pasted from prior stories that nobody reads.
- BDD scenarios written by BA but never executed — they rot and contradict
  the implementation within 2-3 sprints.
- Cross-team AC for events / async flows often miss the "what if the message
  never arrives?" branch — failure is silent until production.
- Non-functional AC ("must be performant") with no measurement gate is
  worse than no AC.

## Agentic workflow

The BA agent owns AC drafting from elicited requirements; a QA agent
converts each criterion into executable test cases; a reviewer agent
checks AC against the INVEST + testability heuristics before story is
marked Ready. Claude subagents work well here because AC drafting is
template-driven, but stakeholder validation must stay human.

Pipeline: `requirement → BA agent drafts AC → reviewer agent lints →
human PO approves → QA agent generates test stubs → traceability matrix
auto-updated`.

### Recommended subagents

- `faion-sdd-execution` — picks up the story once AC are approved,
  enforces "AC verified" as a quality gate before marking task done.
- `faion-feature-executor` — sequences tasks in the story, validates each
  AC scenario passes before moving on.
- `faion-brainstorm` — diverge/converge round to surface missing
  scenarios (negative paths, boundary conditions, security cases) before
  freezing AC.
- BA-style sub-agent (custom, model: sonnet) — drafts AC in
  Given-When-Then from a user story; cites the requirement source.
- QA-style sub-agent (custom, model: sonnet) — translates each AC into
  pytest / Playwright / Gherkin step skeletons.

### Prompt pattern

Drafting prompt (BA agent):
```
You are a senior business analyst. Given the user story below,
write acceptance criteria covering:
1. Happy path (1-2 scenarios)
2. Alternative paths (valid variations)
3. Boundary conditions (limits, empty, max)
4. Error handling (invalid input, downstream failure)
5. Non-functional gates (perf threshold, security control) IF stated.

Format: Given-When-Then. One scenario per outcome. No implementation
details. Cite the requirement ID for each scenario. Flag any criterion
you cannot make testable.

User story: <story>
Source requirements: <links>
```

Lint prompt (reviewer agent):
```
Review these acceptance criteria. For each, answer Y/N:
- Testable (can a test verify pass/fail without human judgement)?
- Atomic (one observable outcome)?
- Free of implementation detail (no DB names, no class names)?
- Bound to a measurement when non-functional?
Return a table with violations and a suggested rewrite.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `behave` | Python BDD runner; .feature → executable scenarios | `pip install behave` |
| `cucumber` | Reference Gherkin runner (Ruby/JS/Java/.NET) | https://cucumber.io |
| `pytest-bdd` | Gherkin scenarios as pytest tests | `pip install pytest-bdd` |
| `gauge` | Markdown-based spec runner, language-agnostic | https://gauge.org |
| `Playwright` `--grep` | Run only AC-tagged e2e tests | `npx playwright test --grep @AC-123` |
| `gherkin-lint` | Lint .feature files for style/duplication | `npm i -g gherkin-lint` |
| `jira-cli` (`ankitpokhrel/jira-cli`) | Read/write AC field on issues from BA agent | `brew install jira-cli` |
| `gh` | Map AC ↔ PR via "Closes #" + checklist | bundled |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Jira (Atlassian) | SaaS | Yes — REST + jira-cli | Custom field "Acceptance Criteria"; agent writes via `issue edit` |
| Linear | SaaS | Yes — GraphQL API + `linear` CLI | AC live in description; use `--checklist` blocks |
| Azure DevOps | SaaS / on-prem | Yes — `az boards` CLI | Acceptance Criteria field is HTML, sanitize Markdown |
| GitHub Issues / Projects | SaaS | Yes — `gh issue` | Use task-list checkboxes for AC; auto-close on PR merge |
| Xray / Zephyr (Jira test mgmt) | SaaS plugin | Partial — REST only | Link AC ↔ test cases ↔ runs (traceability matrix) |
| Cucumber Studio (HipTest) | SaaS | Yes — REST | Stores Gherkin, syncs to Jira; good BA↔QA bridge |
| Tricentis qTest | SaaS | Partial | Enterprise QA; agent can pull test results, push AC harder |
| ReqView / Polarion | SaaS / on-prem | Limited | Heavy enterprise traceability; agent integrates via OSLC |

## Templates & scripts

Story-level Markdown templates live in `templates.md`. For BA→QA hand-off,
use this small extractor that turns AC checkboxes in a Jira/GitHub issue
description into Gherkin stubs ready for QA:

```python
# ac_to_gherkin.py — extract "- [ ] When X then Y" lines and emit .feature
import re, sys, pathlib

src = pathlib.Path(sys.argv[1]).read_text()
story_id = re.search(r"(STORY|AC|US)-?\d+", src).group(0)
title = re.search(r"^#\s+(.+)$", src, re.M).group(1).strip()

ac_lines = re.findall(r"^- \[[ x]\]\s+(.+)$", src, re.M)
out = [f"Feature: {title}", f"  # source: {story_id}", ""]
for i, ac in enumerate(ac_lines, 1):
    # detect "When X, then Y" or "Given... When... Then..."
    m = re.match(r"(?i)^when\s+(.+?),?\s+then\s+(.+)$", ac)
    if m:
        when, then = m.groups()
        out += [f"  Scenario: AC-{i} {ac[:60]}",
                f"    When {when.strip()}",
                f"    Then {then.strip()}", ""]
    else:
        out += [f"  Scenario: AC-{i} {ac[:60]}",
                f"    # TODO rewrite as Given/When/Then",
                f"    Then {ac}", ""]
pathlib.Path(f"{story_id}.feature").write_text("\n".join(out))
print(f"wrote {story_id}.feature with {len(ac_lines)} scenarios")
```

Run: `python ac_to_gherkin.py story.md` → `STORY-123.feature` for QA to
flesh out step definitions. Pair with `gherkin-lint` in CI to enforce
style.

## Best practices

- **One scenario, one assertion.** If a scenario has two `Then` clauses
  joined by `And` covering unrelated outcomes, split it — failure
  diagnosis becomes ambiguous otherwise.
- **AC are versioned with the story, not the sprint.** Lock at sprint
  commit; new criteria after = new story or explicit re-estimation.
- **Reference the requirement ID inside each scenario** as a comment
  (`# req: REQ-417`). Survives Jira migrations, lets agents rebuild the
  traceability matrix from the .feature files alone.
- **Negative AC are first-class.** "System must NOT charge twice on retry"
  is more valuable than five happy-path criteria.
- **Non-functional AC need a measurement and a gate.** "p95 < 300ms over
  rolling 5-min window" beats "must be fast". The gate goes in the CI
  pipeline, not in the head of the QA lead.
- **3-amigos before refinement, not during.** BA + Dev lead + QA lead
  sketch AC ahead of refinement so the wider team reviews, not invents.
- **Definition of Done references AC as a single line**: "All AC verified
  by automated test or documented manual test." Don't duplicate AC into
  DoD.

## AI-agent gotchas

- LLMs love to invent plausible-but-untestable AC ("system should be
  intuitive"). Always pass the AC through the lint prompt before
  surfacing to humans.
- Agents will happily write AC for pre-existing behavior the team never
  agreed on — anchor every AC to a requirement source (PO note, ticket,
  user research finding).
- Without explicit non-functional bounds in the prompt, agents skip
  performance/security AC entirely. Add a checklist gate in the system
  prompt.
- AC drift: if AC are stored in Jira and Gherkin is stored in repo, the
  agent must pick one source-of-truth. Recommended: Gherkin in repo,
  Jira holds a link + checksum.
- Never let an agent close a story because "AC look met" — gate on the
  test runner exit code, not on LLM judgement. Human-in-the-loop
  checkpoint: PO accepts the demo; QA confirms test report.
- When AC reference UI copy ("see message 'Saved!'"), the agent must
  pull the exact string from the i18n file, not paraphrase. Otherwise
  tests pass against the wrong locale.

## References

- BABOK v3, ch. 7 "Requirements Analysis and Design Definition" — AC
  technique (10.1).
- Mike Cohn, *User Stories Applied*, ch. 9 "Acceptance Testing".
- Gojko Adzic, *Specification by Example* (2011) — BA↔QA collaboration
  patterns, "living documentation".
- Atlassian, "Acceptance criteria for user stories" — practical Jira
  workflow guide.
- ISTQB Foundation Level Syllabus 2018, §3.2 — testability of
  requirements; ties AC to test-design techniques.
