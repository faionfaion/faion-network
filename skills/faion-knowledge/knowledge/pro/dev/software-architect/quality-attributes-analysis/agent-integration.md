# Agent Integration — Quality Attributes Analysis

## When to use
- Pre-architecture phase of a non-trivial system: surface NFRs that will drive structural decisions before code is written.
- Major architectural pivot (monolith → microservices, on-prem → cloud, sync → async) — ATAM-style review surfaces hidden trade-offs.
- Investor / customer due diligence demanding evidence the architecture meets their SLA / compliance / scale promises.
- Performance, security, or availability incident postmortem reveals the original architecture didn't enumerate the relevant quality scenarios.
- Multi-tenant or regulated domain (healthcare, finance, public sector) where ISO/IEC 25010 traceability is required.
- New team onboarding — utility tree + scenarios are the fastest way to align on priorities.

## When NOT to use
- Idea / prototype stage with <5 paying customers — quality attributes are imagined; the bottleneck is product-market fit.
- Tactical sprint planning — utility trees are not a substitute for backlogs.
- Single-developer side project with no SLA — overhead exceeds value.
- Team won't revisit the artifact after the workshop — a one-shot ATAM is theater.
- The quality attributes are obvious and uncontested — don't ceremonialize what one whiteboard fixes.
- The trade-offs being made are political, not technical — no analysis method survives an executive who has already chosen.

## Where it fails / limitations
- **Theatre risk.** Generating a utility tree feels like progress; without scenarios that bind to fitness functions, nothing changes in the system.
- **H/M/L scoring is anchored.** Importance and difficulty are gut feels. Treat them as relative orderings, not absolutes.
- **Stakeholder drift.** Priorities ("availability over performance") shift across quarters. A static utility tree decays in 6 months.
- **Hidden assumptions in scenarios.** "10x traffic spike, p99 < 500ms" — under what mix? cold cache? full DB? Without environment specifics, the scenario is unverifiable.
- **ATAM is heavy.** SEI's full ATAM is a 2-3 day workshop; most teams need a slimmed-down version (utility tree + 5 critical scenarios + targeted analysis).
- **Quality attribute trade-off blindness.** Teams optimize one attribute (availability) by sacrificing another (latency, cost, complexity) without making the trade explicit.
- **Functional bias.** Even after running the analysis, PMs ship feature-only stories; NFRs need owners and a slot in the backlog or they don't happen.
- **Too coarse for vendors.** "We need 99.99% availability" is meaningless to a SaaS vendor without scenario, environment, and measure. Translate to scenario form before negotiating.

## Agentic workflow
Drive QAA as a four-pass pipeline: (1) a discovery agent reads the spec, business model, and competitive context to propose ≥3 candidate scenarios per ISO/IEC 25010 characteristic; (2) a stakeholder-elicitation agent runs structured interviews (or simulated personas) to score importance and propose response measures; (3) a utility-tree agent assembles scenarios into a utility tree with (Importance, Difficulty) priorities and selects the (H,H) drivers; (4) a fitness-function agent emits *executable* tests / monitors per critical scenario (load test, chaos drill, security scan) wired into CI/CD. Agents must always loop a human in for the prioritization step — gut feel about importance is irreducibly human.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — turn each (H,H) scenario into an SDD task with a concrete fitness function as the AC.
- `faion-research-agent` (under `skills/faion-knowledge/knowledge/pro/research/researcher/`) — gather industry SLAs and competitive baselines (e.g., "p99 latency for similar SaaS dashboards"); feeds Step 2.
- A purpose-built **utility-tree builder** (worth creating): given a list of scenarios, output a Mermaid mindmap with (Importance, Difficulty) labels and a sorted "(H,H) drivers" section.
- A purpose-built **scenario linter** (worth creating): rejects scenarios missing any of the 6 parts (source, stimulus, environment, artifact, response, response measure).
- `password-scrubber-agent` — workshop notes leak vendor names, customer SLAs, and incident details; scrub before sharing externally.

### Prompt pattern
Scenario generation:
```
Read <spec>. For each ISO/IEC 25010 characteristic (performance,
reliability, security, maintainability, …), produce ≥3 scenarios
in 6-part form (Source, Stimulus, Environment, Artifact, Response,
Response Measure). Reject scenarios missing any part. Reject
qualitative-only measures ("fast"); require numeric thresholds.
```

Trade-off analysis:
```
Given the architecture in <design.md> and the (H,H) scenarios, list
trade-offs: any time satisfying scenario A makes scenario B harder.
For each pair, propose either (i) an architectural mechanism that
preserves both, or (ii) an explicit prioritization decision with
rationale. Output as a markdown trade-off matrix.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `arch-decision-record` / `adr-tools` | Capture trade-offs and quality decisions in versioned ADRs | https://github.com/npryce/adr-tools |
| `c4-builder` / `structurizr-cli` | Generate C4 architecture diagrams referenced in scenarios | https://structurizr.com |
| `k6` / `locust` / `wrk2` | Performance fitness functions per perf scenario | https://k6.io ; https://locust.io ; https://github.com/giltene/wrk2 |
| `chaos-mesh` / `litmuschaos` / `aws-fis` | Reliability fitness functions: inject the stimulus described in scenarios | https://chaos-mesh.org ; https://litmuschaos.io |
| `zap` / `nuclei` / `trivy` | Security fitness functions (DAST, vuln scanning) | https://www.zaproxy.org ; https://nuclei.projectdiscovery.io ; https://trivy.dev |
| `sonarqube` / `radon` | Maintainability metrics (complexity, duplication) | https://www.sonarsource.com ; https://radon.readthedocs.io |
| `mermaid-cli` | Render utility trees from text | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert utility tree + scenarios → PDF for stakeholders | `apt install pandoc` |
| `claude` (Anthropic CLI) | Run scenario-generation / linter / trade-off passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Structurizr / IcePanel / Lucidscale | SaaS architecture-as-code | API yes | Hold the model; scenarios reference elements/components. |
| Backstage TechDocs | OSS | yes | Living architecture docs + scenarios per service in a service catalog. |
| Datadog / Grafana Cloud / New Relic | SaaS observability | API yes | Where fitness-function dashboards live; bind to scenario response measures. |
| PagerDuty / Opsgenie | SaaS incident mgmt | yes | Scenarios become alert-thresholds + runbooks; closes the loop. |
| Linear / Jira | SaaS issue tracker | yes | (H,H) scenarios become NFR epics with explicit quality acceptance criteria. |
| Confluence / Notion | SaaS docs | yes | Utility tree + scenario catalog + ATAM workshop notes. |
| ArchUnit / import-linter | OSS | yes | Maintainability/architecture rules as fitness functions. |
| OpenSCAP / Vanta / Drata | SaaS / OSS | yes | Security/compliance scenarios mapped to controls. |

## Templates & scripts
The methodology already includes utility-tree and 6-part scenario templates. The high-leverage missing piece is a **scenario linter** so workshop output stays well-formed. Inline drop-in (≤50 lines):

```python
#!/usr/bin/env python3
# scenario_lint.py — fail CI on malformed quality attribute scenarios.
# Usage: python scenario_lint.py docs/quality/scenarios.md
import re, sys, pathlib

REQUIRED = ["source", "stimulus", "environment", "artifact",
            "response", "response measure"]

src = pathlib.Path(sys.argv[1]).read_text().lower()
blocks = re.split(r"^#{2,3}\s+scenario", src, flags=re.M)[1:]
errs = []
for i, b in enumerate(blocks, 1):
    missing = [r for r in REQUIRED if r not in b]
    if missing:
        errs.append(f"scenario {i}: missing {missing}")
    if not re.search(r"\d", b):
        errs.append(f"scenario {i}: no numeric threshold (response measure must be quantitative)")
    if "tbd" in b or "tba" in b:
        errs.append(f"scenario {i}: contains TBD/TBA placeholder")
for e in errs:
    print(e)
sys.exit(1 if errs else 0)
```

Wire into pre-commit on the docs repo or CI on the architecture repo.

## Best practices
- **Scenarios over slogans.** Replace "must be fast" with a 6-part scenario including numeric thresholds and environment.
- **Each (H,H) driver gets a fitness function.** Performance ⇒ k6 test in CI. Availability ⇒ chaos drill in pre-prod. Security ⇒ DAST scan. No fitness function ⇒ the scenario is decorative.
- **Tie scenarios to ADRs.** Every architectural decision references the scenarios it addresses; reverse-traceable when revisiting.
- **Cap the utility tree.** ≤7 quality attributes, ≤3 scenarios per attribute as drivers; everything below is "tracked, not driving."
- **Run a slimmed ATAM, not the full SEI version.** 2-hour workshop with a utility tree, 5 critical scenarios, sensitivity points, trade-offs. Document outcome in 2 pages.
- **Refresh quarterly.** Quality priorities shift with growth stage; what mattered at MVP doesn't at scale.
- **Trade-offs are first-class.** Make explicit which scenario beats which when in conflict; name the loser.
- **Stakeholder mapping.** Every (H,H) scenario has a named owner (engineer + business sponsor) and a review cadence.
- **Distinguish risks from requirements.** Some scenarios capture risks ("under DDoS, …"); their response measure is "degrade gracefully," not "succeed." Don't over-constrain the architecture.

## AI-agent gotchas
- **Hallucinated SLAs.** Agents will invent "industry-standard 99.99% availability for SaaS dashboards" with no citation. Force every numeric measure to cite a source (competitor SLA, internal data, vendor doc).
- **6-part incompleteness.** Agents emit 4-part scenarios (skip environment + artifact). Lint with the script above.
- **Qualitative response measures.** "Acceptable response time" / "good user experience" are banned. Require number + unit.
- **Symmetric-priority tree.** Agents generate utility trees where everything is (H,H). Force quotas: at most 3 (H,H) drivers per tree.
- **Trade-off blindness.** Agents optimize one attribute and ignore the cost. Add a trade-off pass: for each (H,H), name the attribute it costs.
- **ISO/IEC 25010 mismatch.** Agents reference ISO 9126 (the obsolete predecessor) or 25010:2011 instead of 2023. Pin the version in prompts.
- **Scenario inflation.** Agents produce 30 scenarios when 10 are enough. Cap the count and force prioritization.
- **Recency / vendor bias.** Agents over-weight whatever vendor's blog they pulled from web search. Cross-check against multiple sources; require non-vendor academic / standard references for definitions.
- **No human checkpoint on prioritization.** Importance is human business judgment, not LLM inference. Always require human sign-off before the utility tree drives architecture.
- **Ignoring safety / accessibility.** Agents under-produce these scenarios because training data is biased toward perf and security. Require ≥1 scenario per ISO characteristic.

## References
- Bass, Clements, Kazman — "Software Architecture in Practice," 4th ed. Addison-Wesley, 2021.
- SEI Carnegie Mellon — "ATAM: Method for Architecture Evaluation." https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=5177
- ISO/IEC 25010:2023. https://www.iso.org/standard/78176.html
- Kruchten, P. — "The 4+1 View Model of Architecture." https://www.cs.ubc.ca/~gregor/teaching/papers/4+1view-architecture.pdf
- Fowler, M. — "An Appropriate Use of Metrics." https://martinfowler.com/articles/useOfMetrics.html
- ThoughtWorks Tech Radar — "Architectural Fitness Functions." https://www.thoughtworks.com/radar
- Risk-Storming (collab method). https://www.riskstorming.com
- Sibling: `pro/dev/software-architect/reliability-architecture/` (this batch).
- Sibling: `pro/dev/software-architect/observability-architecture/` (this batch) — fitness-function backbone.
