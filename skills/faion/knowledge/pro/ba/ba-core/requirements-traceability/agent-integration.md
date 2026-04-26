# Agent Integration — Requirements Traceability (BA Core, First Principles)

> Companion to `business-analyst/requirements-traceability/agent-integration.md` (which is tool-heavy). This file focuses on the first-principles core of traceability — the link algebra, the three trace directions, and the minimum-viable matrix an agent can build, verify, and maintain.

## When to use

- A program needs a single, defensible answer to "is everything covered, and why does each thing exist?" — pre-audit, pre-release, before a major refactor.
- BABOK 5.2 "Trace Requirements" is being applied for the first time and the team must learn the link semantics, not the tooling, before adopting Polarion / DOORS / StrictDoc.
- Designing a new RTM schema from scratch: deciding which artifact types are nodes, which link roles are allowed, and what coverage thresholds gate releases.
- Migrating from spreadsheet RTMs to requirements-as-code (frontmatter links): you need first-principles rules to validate the conversion.
- Teaching subagents what "satisfies", "derives", "verifies" actually mean before letting them propose links — the model usually conflates them.
- Lightweight projects where a generated matrix from typed links in markdown is all you need; full RM tooling is overkill.

## When NOT to use

- You only need vendor / tooling guidance — go to `business-analyst/requirements-traceability/agent-integration.md`.
- Discovery / pre-PMF: lock-in of an RTM at this stage encodes premature decisions; opportunity-solution-trees + bare user stories cover it.
- One-shot prototypes, internal scripts, throwaway spikes — overhead exceeds value.
- The team will not enforce link discipline; an out-of-date matrix is worse than none because auditors trust it.
- Pure SLO-driven SRE work where the trace artifact is a dashboard alert rule, not a requirement record.

## Where it fails / limitations

- **Asymmetry of "bidirectional"**: forward (need → test) is mechanical; backward (test → need) breaks the moment a test exists for a non-functional concern with no explicit requirement. Treat the two directions as separate gates with different thresholds.
- **Granularity collapse**: the README warns "too granular" and "too sparse"; the right level is the lowest one at which a defect would be material to a stakeholder. Anything finer is noise.
- **Link-role conflation**: humans and LLMs both confuse `satisfies` (parent → child) with `derives` (peer requirements) with `verifies` (test → req). Without a published vocabulary the matrix becomes lossy.
- **Horizontal trace blindness**: forward and backward are vertical; the horizontal axis (req ↔ req: `derives`, `conflicts`, `duplicates`) is where consistency bugs hide and is rarely matrixed.
- **Coverage-metric gaming**: 100% forward coverage is trivially achieved with one tautological test per requirement; pair with AC-density, mutation testing, or independent reviewer sampling.
- **Stale-by-default**: a hand-edited matrix decays in 2-3 sprints (README mistake #1). Without a generator that derives the matrix from typed links in source artifacts, decay is inevitable.
- **Matrix bloat**: O(n*m) cells across artifact types is unreadable beyond ~50 requirements; switch to a graph view (DAG with role-coloured edges) once n > 50.

## Agentic workflow

The matrix is a generated artifact, not a hand-edited file. Each requirement / design / test stores typed links in its frontmatter (`traces:` block) using the link-role vocabulary below. A deterministic builder aggregates links into the RTM and computes coverage. Subagents do four bounded jobs and never touch the matrix directly: (1) propose typed links when an artifact lands, with quoted evidence and confidence, (2) walk the graph to detect orphans (no parent or no child), (3) walk the graph to detect cycles and conflicts on the horizontal axis, (4) walk the graph for impact analysis on a change request. Agents emit patches to source artifacts only; humans approve the patch before the generator regenerates the matrix. Mandatory human-in-the-loop gates: link confidence < 0.9, any `conflicts` edge, coverage drop > 1pp from last baseline.

### Recommended subagents

- `faion-sdd-executor-agent` — runs link-proposal as an SDD task on each new artifact: read `spec.md`, write a `traces:` block into the related `design.md` and `test-plan.md`. One commit per trace edit, easy to revert.
- A custom `ba-trace-linker-agent` (model: sonnet, per the README "Validate requirement completeness" row) — proposes typed links between two artifacts with a quoted-evidence span and a 0..1 confidence; never auto-merges below 0.9.
- A custom `ba-orphan-detector-agent` (model: haiku, per "Extract requirements from documents" row) — runs the generator, lists orphans up (FR / TC with no parent) and orphans down (BR / SR with no child), opens an issue per cluster.
- A custom `ba-impact-agent` (model: opus, per "Analyze requirement trade-offs" row) — given a CR and the link graph, walks 1-2 hops downstream, fills the README "Impact analysis" table, and drafts the CR impact section.
- `password-scrubber-agent` — RTM aggregation often pastes stakeholder transcripts; scrub before commit.

### Prompt pattern

Two-shot: link proposal then impact walk. Restate the role vocabulary every time — the model does not retain it across turns.

```
You are a requirements trace linker. The five allowed link roles are:
- satisfies: child req fulfils parent need (vertical down)
- derives:   peer req is logically derived from another (horizontal)
- implements:design / code realises a req (vertical down)
- verifies:  test proves a req is satisfied (vertical up from test)
- conflicts: two reqs cannot both hold (horizontal, requires resolution)

SOURCE artifact (id={id}, type={BR|SR|FR|D|TC|M}):
---
{frontmatter + body}
---
CANDIDATES (id, type, abstract): {list}

For each candidate, return strict JSON:
{ "source": "{id}", "links": [
  { "target": "<id>", "role": "<one of the five>",
    "confidence": <float 0..1>,
    "evidence_source": "<verbatim quote from source>",
    "evidence_target": "<verbatim quote from target>",
    "rationale": "<<= 1 sentence>" } ] }

Reject any link where evidence cannot be quoted from BOTH artifacts.
```

```
Given the link graph (JSON) and CR-{n}, list every artifact within 2 hops of the
changed REQ. Group by type. Mark each Update / Review / No-op. Use ONLY the
supplied graph; do not infer artifacts that are not nodes. Output the table from
the README "Impact analysis" example, plus a one-line effort estimate.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `yq` + `jq` | Read `traces:` frontmatter, build the link graph as JSON | `apt install yq jq` |
| `python -m yaml` | Validate frontmatter parses cleanly before commit | stdlib |
| `lychee` | Verify every `[REQ-XXX]` reference in markdown resolves to an existing file | https://github.com/lycheeverse/lychee |
| `mermaid-cli` (`mmdc`) | Render the link graph as a coloured DAG for human review | `npm i -g @mermaid-js/mermaid-cli` |
| `pre-commit` | Wire the generator + orphan check into every commit | https://pre-commit.com |
| `git log --grep='REQ-' --all` | Backward trace: code commits → requirement IDs via Conventional Commits scope | preinstalled |
| `pytest -k 'req_'` + custom marker | Tag tests with REQ IDs (`@pytest.mark.req("REQ-101")`) and emit a coverage report | https://pytest.org |
| `gherkin` `@REQ-101` tags | BDD scenarios double as test-to-req trace; reports pipe straight into the matrix | https://cucumber.io |

For full vendor-tool comparisons (Jama, DOORS, Polarion, StrictDoc, Doorstop, ReqIF tooling) see the sibling business-analyst integration file.

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| StrictDoc | OSS | CLI + plain text | Best fit for a fully agentic, first-principles flow: deterministic, git-native, link-role typed. |
| Doorstop | OSS | CLI + YAML | Markdown + YAML on disk; `doorstop link` / `doorstop publish` produce the RTM. |
| Plain markdown + frontmatter | OSS / DIY | Excellent | Lowest-friction path; pair with the `rtm.py` script below. |
| Jira issue links | SaaS | REST | Cheap baseline if requirements already live there; map "is implemented by" / "verifies" onto the five roles. |
| GitHub Issues + labels | SaaS | REST + GraphQL | Works for solo / small teams; labels carry the role, link via cross-references. |

Heavier RM platforms covered in the sibling file.

## Templates & scripts

The README ships an RTM template (table) and per-requirement upstream/downstream tables. Below is the minimum-viable generator: walks a docs tree, reads `traces:` frontmatter, prints coverage, lists orphans, and exits non-zero on regression — designed to be wired into `pre-commit`.

```python
#!/usr/bin/env python3
"""rtm_min.py - first-principles RTM generator from frontmatter links."""
from __future__ import annotations
import sys, pathlib, collections, yaml

ROLES = {"satisfies", "derives", "implements", "verifies", "conflicts"}
PARENTS  = {"SR": "BR", "FR": "SR", "D": "FR", "M": "D", "TC": "FR"}  # type -> required upstream type

def fm(p: pathlib.Path) -> dict:
    t = p.read_text()
    if not t.startswith("---"): return {}
    return yaml.safe_load(t.split("---", 2)[1]) or {}

def main(root: str = "docs") -> int:
    nodes, edges = {}, []
    for p in pathlib.Path(root).rglob("*.md"):
        d = fm(p)
        nid = d.get("id")
        if not nid: continue
        nodes[nid] = nid.split("-")[0]  # type prefix
        for ln in d.get("traces", []) or []:
            tgt, role = (ln, "satisfies") if isinstance(ln, str) else (ln["to"], ln.get("role", "satisfies"))
            if role not in ROLES:
                print(f"ERR bad role {role} in {nid}"); return 2
            edges.append((nid, tgt, role))
    up = collections.defaultdict(set); down = collections.defaultdict(set)
    for s, t, _ in edges: up[t].add(s); down[s].add(t)
    by_type = collections.Counter(nodes.values())
    print(f"{'Type':<6}{'Total':>6}{'Linked':>8}{'Coverage':>10}")
    rc = 0
    for ty in sorted(by_type):
        total = by_type[ty]
        linked = sum(1 for n, t in nodes.items() if t == ty and (up[n] or down[n]))
        cov = 100 * linked // total
        print(f"{ty:<6}{total:>6}{linked:>8}{cov:>9}%")
        if ty in PARENTS and cov < 95: rc = 1
    orphans_up = [n for n, t in nodes.items() if t in PARENTS and not up[n]]
    if orphans_up: print("\nOrphans (no parent):", ", ".join(orphans_up)); rc = 1
    return rc

if __name__ == "__main__": sys.exit(main(*sys.argv[1:]))
```

Pre-commit hook:

```yaml
- id: rtm-min
  name: RTM coverage and orphan check
  entry: python scripts/rtm_min.py docs/
  language: system
  pass_filenames: false
  files: ^(docs|requirements)/
```

## Best practices

- **Three trace directions, three gates.** Forward (BR → TC): coverage gate, target ≥ 95%. Backward (TC → BR): justification gate, target = 100%. Horizontal (REQ ↔ REQ): consistency gate, target = 0 cycles, 0 unresolved `conflicts`. Track them separately; one number hides the failure mode.
- **One link-role vocabulary, lint-enforced.** Pick five roles (`satisfies`, `derives`, `implements`, `verifies`, `conflicts`). Reject any other string at lint time. Without this, the matrix becomes lossy within a quarter.
- **Generate, never hand-edit.** Typed links live in source artifacts; the matrix is a build product. Hand-edited matrices decay (README mistake #1).
- **Quote evidence on every link.** A link without a quoted span from both artifacts is rejected. Forces real reading; blocks LLM hallucination.
- **Tag a baseline at every release** (`rtm-baseline-2026-Q2`). PRs surface the diff against the baseline; a regression is visible on the PR page.
- **Decide once: tests-without-requirements policy.** Either gold-plating (delete) or implicit NFR (write the requirement). Mixing both rules is fatal.
- **Narrow node set.** Only artifact types where ownership changes hands belong on the matrix (BR, SR, FR, D, TC). UI strings, log lines, helper code are leaves on a TC, not nodes.
- **Switch to a graph at n > 50.** Tables stop being readable; render the link DAG with `mermaid-cli`, colour edges by role.
- **Conventional Commits with REQ scope.** `feat(REQ-045): ...` and `Refs: REQ-046, REQ-047` give a free code → req trace via `git log`.

## AI-agent gotchas

- **Hallucinated links** are the #1 failure. Require quoted evidence from both artifacts; auto-reject < 0.9 confidence; never accept a link the model proposes but cannot quote.
- **Role conflation**: `satisfies` vs `verifies` vs `derives` is the most common LLM error. Restate the vocabulary in the system prompt every turn — do not rely on retention.
- **Forward bias**: agents readily generate forward links (BR → FR) and miss backward (TC → REQ) and horizontal (FR ↔ FR `derives` / `conflicts`). Run three separate passes, one per direction.
- **Bulk operation runaway**: cap any agent run at N (e.g. 20) link edits and require human review on the diff. Cleaning up 500 spurious links is days of work.
- **Discovery vs phrasing**: use deterministic NER / ID-extraction to find candidate IDs; only let the LLM phrase the role + rationale on the candidate pair.
- **Context loading**: at >1000 artifacts, do not load full bodies. Index id + type + title + first 200 chars + frontmatter; load full body on demand for the focal pair.
- **Frontmatter brittleness**: smart quotes, NBSP, BOM bytes silently break YAML parsers. Add a pre-commit hook that rejects non-ASCII keys and BOMs.
- **Diff over rewrite**: agents emit `+ traces: [REQ-101]` as a patch, never a rewritten file. Smaller review surface, preserved history.
- **Mandatory human gates**: (1) confidence < 0.9, (2) `conflicts` edge proposed, (3) coverage drop > 1pp, (4) deletion of an auditor-signed-off link.
- **Stale corpus during long agent runs**: lock the source set with a git SHA at run start; reject the run if the SHA moves before merge — otherwise links point to artifacts that have since changed.

## References

- IIBA BABOK Guide v3, ch. 5.2 "Trace Requirements" — https://www.iiba.org/standards-and-resources/babok/
- ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering — https://www.iso.org/standard/72089.html
- Gotel & Finkelstein, "An Analysis of the Requirements Traceability Problem", 1994 (origin of the forward / backward distinction) — https://ieeexplore.ieee.org/document/292398
- StrictDoc — https://strictdoc.readthedocs.io
- Doorstop — https://doorstop.readthedocs.io
- Sibling, tool-heavy companion: `pro/ba/business-analyst/requirements-traceability/agent-integration.md`
- Related methodologies in this skill: `requirements-lifecycle/`, `requirements-validation/`, `requirements-prioritization/`, `ba-requirements-mgmt/`.
