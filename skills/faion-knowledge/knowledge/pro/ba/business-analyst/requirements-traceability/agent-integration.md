# Agent Integration — Requirements Traceability

## When to use

- Regulated builds (medical devices ISO 13485 / IEC 62304, automotive ISO 26262, aviation DO-178C, fintech SOX) where auditors demand a complete forward+backward chain from business need → code → test.
- Multi-team programs where a single change request hits 4+ artifacts (BR, SR, FR, design, test, code) and a human cannot mentally fan-out the impact.
- Pairing with `requirements-lifecycle/` and `requirements-validation/` to close the Specify → Verify loop with provable coverage numbers.
- Migrations and re-platforming, where you must prove every legacy capability is preserved or explicitly retired (forward coverage gate).
- AI / LLM features where the prompt, eval set, model version, and acceptance criterion must be linkable so a regression in the eval can be traced back to a requirement and its test.
- Vendor / outsourced delivery: traceability matrix is the contractual deliverable that lets the buyer accept work piecemeal.

## When NOT to use

- Pre-PMF / discovery work — opportunity-solution-trees + lightweight user stories cover it; an RTM ossifies premature decisions.
- Solo developer or 2-person team building a SaaS MVP — `git log --grep` plus issue links already provide enough trace.
- Pure infrastructure / SRE work where requirements are SLOs, not features; SLO dashboards are the trace artifact, not an RTM.
- One-shot internal tools, prototypes, spikes, throwaway scripts.
- When the team will not enforce the maintenance discipline; an outdated RTM is worse than none because it gives false assurance to auditors.

## Where it fails / limitations

- Spreadsheet RTMs go stale within 2-3 sprints — README mistake #1. Without a generator that derives the matrix from typed links in the source artifacts, decay is inevitable.
- "Too granular" trap (README mistake #2): tracing every UI label or log message buries the signal. Pick the lowest level where a defect would be material.
- Bidirectional assumption is asymmetric in practice: forward coverage (need → test) is mechanical; backward (test → need) breaks the moment a developer adds a test for a non-functional concern that has no requirement.
- LLMs hallucinate links. They will confidently associate `REQ-103` with `TC-47` because both contain the word "checkout" — without a deterministic check the matrix poisons itself.
- Tools fragmentation: requirements in Jira, designs in Figma, tests in TestRail, code in GitHub. Each integration is a separate pipeline; a missing webhook silently drops links.
- Coverage metrics are gameable. "100% forward coverage" can be achieved by linking one tautological test per requirement; pair with mutation testing or AC-density to detect gaming.
- ReqIF round-tripping with Polarion / DOORS Next loses custom attributes; never assume export → import → export is identity.

## Agentic workflow

Treat the RTM as a generated artifact, not a hand-edited file. Each artifact (REQ, design, code, test) carries typed links in its frontmatter / docstring / tag (`traces: [BR-05, SR-12]`); a builder script aggregates links into the matrix and computes coverage. Subagents do three jobs: (1) propose links when a new artifact lands, (2) detect orphans and gaps in the generated matrix, (3) walk the graph for impact analysis on a change request. They never write the matrix directly — a deterministic generator owns the canonical state, and agents only emit patches to source artifacts. Human-in-the-loop gates: link approval, gap acceptance, change-request impact sign-off.

### Recommended subagents

- `faion-sdd-executor-agent` — runs link-proposal as an SDD task per artifact: read `spec.md`, emit `traces:` frontmatter into related `design.md` and `test-plan.md`. Each commit is one trace edit, easy to revert.
- `password-scrubber-agent` — sweeps requirement and test docs for leaked credentials before commit; relevant because RTM aggregation tends to copy-paste stakeholder transcripts and ticket comments.
- A custom `ba-trace-linker-agent` (model: sonnet, per README Agent Selection): reads pairs of artifacts and proposes typed links with a confidence score and rationale; never auto-merges below 0.9 confidence.
- A custom `ba-impact-agent` (model: opus): given a change-request and the link graph, walks 1-2 hops downstream, lists every affected artifact, and drafts the impact section of the CR.
- A custom `ba-coverage-auditor-agent` (model: haiku): runs the generator, diff coverage against baseline tag, opens an issue when forward coverage drops below threshold.

### Prompt pattern

Two-shot: link proposal then impact walk.

```
You are the trace linker. Source artifact (id={id}, type={type}) is below.
Candidate targets (with abstracts) follow. For each candidate, decide LINK / NO LINK
and assign confidence in [0,1]. Use ONLY content; do not invent IDs.

Return strict JSON:
{ "source": "{id}", "links": [
  { "target": "<id>", "type": "satisfies|verifies|derives|implements|conflicts",
    "confidence": <float>, "rationale": "<=1 sentence" } ] }

SOURCE:
---
{frontmatter + body}
---
CANDIDATES:
{list}
```

Impact analysis prompt:

```
Given the link graph (JSON below) and CR-{n} description, list every artifact within
2 hops of the changed REQ. Group by type. Mark each as Update / Review / No-op.
Do NOT speculate beyond the supplied graph. Output the table from
requirements-traceability/README.md "Impact analysis" example.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `strictdoc` | OSS requirements-as-code with native traceability, HTML export, link checking | https://strictdoc.readthedocs.io |
| `doorstop` | Git-native RM in Markdown+YAML; built-in `doorstop link` / `doorstop publish` | https://doorstop.readthedocs.io |
| `reqif-tools` | Round-trip ReqIF with Polarion / DOORS Next / Jama | https://github.com/strictdoc-project/reqif |
| `yq` + `jq` | Aggregate `traces:` frontmatter across files into a JSON link graph | `apt install yq jq` |
| `pytest` `--require` plugin (`pytest-reqs`) or custom marker | Tag tests with REQ IDs (`@pytest.mark.req("REQ-101")`) and emit a coverage report | https://pytest.org |
| `gherkin` + Cucumber tags | `@REQ-101` tags on scenarios so BDD reports double as test-to-req trace | https://cucumber.io |
| `git log --grep="REQ-"` | Trace commits to requirements via Conventional Commits scope | preinstalled |
| `gh api graphql` | Pull issue ↔ PR ↔ commit graph for backward trace from code to requirement | https://cli.github.com |
| `mermaid-cli` (`mmdc`) | Render the link graph as a diagram for review | `npm i -g @mermaid-js/mermaid-cli` |
| `lychee` | Validate that every `[REQ-XXX]` link in markdown resolves to an existing file | https://github.com/lycheeverse/lychee |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jama Connect | SaaS | REST + webhooks | First-class Relationships API; agents can fetch impact graphs server-side. OAuth. |
| IBM DOORS Next | SaaS / on-prem | OSLC | Industry standard for safety-critical; OSLC verbose, build adapters once and reuse. |
| Polarion ALM | SaaS / on-prem | REST + WSAPI | Strong work-item linking + LiveDoc; map link roles to its `linkedWorkItems`. |
| Jira (Cloud) + Issue Links | SaaS | REST v3 + JQL | Cheap baseline; "is implemented by" / "verifies" link types cover the basics. Watch rate limits on bulk link creation. |
| Azure DevOps + Test Plans | SaaS | REST + ADO CLI | Native trace from work item → test case → test run; agents drive via `az boards work-item update`. |
| TestRail | SaaS | REST API | Excellent for the test side of the matrix; each case stores `refs:` field for REQ IDs. |
| Xray for Jira | SaaS | REST + GraphQL | Deep BDD + manual + automated test trace into Jira issues. |
| StrictDoc | OSS | CLI + plain text | Best fit for fully agentic flows; deterministic, git-native, ReqIF in/out. |
| ReqView | Desktop / SaaS | ReqIF / JSON | Lightweight RM for small teams; export JSON, agents diff. |
| Modern Requirements (ADO) | SaaS | ADO REST | Adds RTM views on top of Azure DevOps. |
| Codebeamer (PTC) | SaaS / on-prem | REST API | Heavy enterprise; integrated with safety-critical workflows. |
| Helix RM (Perforce) | SaaS / on-prem | REST | Legacy; weaker LLM ecosystem; OK if already in stack. |

## Templates & scripts

The README provides RTM and per-requirement trace templates. Inline below is a Python script that walks a docs tree, reads `traces:` frontmatter, builds the link graph, and prints coverage + orphans matching the README's RTM template.

```python
#!/usr/bin/env python3
"""rtm.py - generate Requirements Traceability Matrix from frontmatter links."""
from __future__ import annotations
import sys, pathlib, collections, yaml

ROLES = {"satisfies","verifies","derives","implements","conflicts"}
TYPES = {"BR","SR","FR","D","TC","M"}  # business, stakeholder, functional, design, test-case, code-module

def load(p: pathlib.Path) -> dict:
    text = p.read_text()
    if not text.startswith("---"): return {}
    fm, _ = text.split("---", 2)[1:]
    return yaml.safe_load(fm) or {}

def main(root: str = "docs") -> int:
    nodes: dict[str, dict] = {}
    edges: list[tuple[str,str,str]] = []
    for p in pathlib.Path(root).rglob("*.md"):
        fm = load(p)
        nid = fm.get("id")
        if not nid: continue
        nodes[nid] = {"path": str(p), "type": nid.split("-")[0], "title": fm.get("title","")}
        for link in fm.get("traces", []) or []:
            if isinstance(link, str): tgt, role = link, "satisfies"
            else: tgt, role = link["to"], link.get("role","satisfies")
            if role not in ROLES: print(f"WARN bad role {role} in {nid}"); continue
            edges.append((nid, tgt, role))
    fwd = collections.defaultdict(set)
    bwd = collections.defaultdict(set)
    for s,t,_ in edges: fwd[s].add(t); bwd[t].add(s)
    orphans_up   = [n for n,m in nodes.items() if m["type"] in {"SR","FR","TC"} and not bwd[n]]
    orphans_down = [n for n,m in nodes.items() if m["type"] in {"BR","SR","FR"} and not fwd[n]]
    by_type = collections.Counter(m["type"] for m in nodes.values())
    print("Type      Total  Linked   Coverage")
    for t in sorted(by_type):
        total = by_type[t]
        linked = sum(1 for n,m in nodes.items() if m["type"]==t and (fwd[n] or bwd[n]))
        print(f"{t:<8} {total:>6} {linked:>7}  {100*linked/total:>5.0f}%")
    if orphans_up:   print("\nOrphans (no upstream):",   ", ".join(orphans_up))
    if orphans_down: print("Orphans (no downstream):", ", ".join(orphans_down))
    return 1 if orphans_up or orphans_down else 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Wire it into pre-commit: any change under `docs/` or `requirements/` triggers `rtm.py` and fails the commit on new orphans.

## Best practices

- Generate the matrix, never hand-maintain it. Store typed links in source artifacts (frontmatter, code annotations, test markers); the matrix is a build product, regenerated on every commit.
- One link role vocabulary across the program: `satisfies` (need → req), `derives` (req → req), `implements` (req → code/design), `verifies` (test → req), `conflicts` (req ↔ req). Reject anything else at lint time.
- Pin coverage thresholds in CI: `forward >= 95%`, `backward == 100%`, `orphans == 0`. Failure blocks the merge.
- Distinguish "linked" from "verified": a link is structural; the verification gate (test pass + reviewer sign-off) is what makes the trace meaningful for audit.
- Use Conventional Commits with REQ scope (`feat(REQ-045): ...`) and `Refs:` footers for multi-req commits — gives a free code-to-req trace via `git log`.
- Tag a baseline (`rtm-baseline-2026-Q2`) at every release; PRs show the diff in coverage so a regression is visible.
- For ML / LLM features, treat the eval dataset row as a test case and link to the REQ; rerun in CI so a model swap that breaks an AC fails the trace gate.
- Keep the matrix narrow but deep: only artifact types that change ownership (BR, FR, design, test) are nodes; UI strings and log lines are leaves on a test case.
- Decide once whether tests-without-requirements are gold-plating (delete) or implicit NFRs (write the requirement). Both are valid; mixing is fatal.

## AI-agent gotchas

- Hallucinated links are the dominant failure: pin every link to evidence (a quoted span from each artifact) and reject low-confidence proposals automatically. README mistake #3 (too sparse) is amplified when reviewers rubber-stamp confident-looking but bogus links.
- Always pass the existing link graph (or the relevant subgraph) into the agent's context for impact analysis. Without it, the model invents downstream nodes.
- LLMs conflate `verifies` with `satisfies`. State the role definitions in the system prompt every time; do not assume the model retained them.
- Bulk operations are dangerous: cap any agent run to N (e.g. 20) link edits, require human review on the diff. A runaway linker that adds 500 spurious links is hard to clean up.
- Use the LLM to phrase the trace, not to discover it: discovery should run a deterministic NER / ID-extraction pass first, then the LLM proposes role + rationale per candidate pair.
- ReqIF imports lose custom link types — never let the agent recreate them from text; carry a YAML mapping file and reapply.
- Token budget at >1000 artifacts: do not load full bodies; index titles + first 200 chars + frontmatter only. Load full body on demand for the focal pair.
- Human-in-the-loop checkpoints (mandatory): (1) link confidence < 0.9, (2) coverage drop > 1pp from baseline, (3) any `conflicts` link, (4) deletion of a link that the auditor previously signed off on.
- Frontmatter parsers fail silently on smart quotes / non-breaking spaces pasted from email; reject non-ASCII keys with a pre-commit hook.
- Always emit a diff (`+ traces: [REQ-101]`), not the rewritten file — review surface is smaller and history is preserved.

## References

- IIBA BABOK Guide v3, ch. 5.2 "Trace Requirements" — https://www.iiba.org/standards-and-resources/babok/
- ISO/IEC/IEEE 29148:2018 Requirements engineering — https://www.iso.org/standard/72089.html
- IEC 62304 (medical software) traceability requirements — https://www.iso.org/standard/38421.html
- DO-178C (avionics software) — https://www.rtca.org
- StrictDoc requirements-as-code — https://strictdoc.readthedocs.io
- Doorstop git-native RM — https://doorstop.readthedocs.io
- ReqIF interchange format — https://www.omg.org/spec/ReqIF/
- Sibling methodologies in this repo: `requirements-lifecycle/`, `requirements-validation/`, `requirements-prioritization/`, `acceptance-criteria/`.
