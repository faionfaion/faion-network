# Agent Integration — Implementation Plan Components

## When to use
- As the structural reference when writing or reviewing an `implementation-plan.md` — defines what each section must contain and shows worked examples
- When an agent generates a plan and needs to validate it against the canonical component list before marking it `Draft`
- When adapting the plan template to a specific project type (API-only, frontend-only, full-stack): identify which sections to retain, condense, or omit
- When onboarding an executor agent: the wave analysis and dependency graph sections define the scheduling contract the agent must respect

## When NOT to use
- As a substitute for `writing-implementation-plans/README.md` — that file explains the methodology (100k rule, INVEST, wave algorithm); this file shows the structural components
- When the plan is already written and approved — this is authoring guidance, not execution guidance

## Where it fails / limitations
- The rollout strategy component assumes a production deployment context; for solo dev/staging-only projects, this section becomes overhead that agents dutifully fill with boilerplate
- The wave visualization (ASCII box diagrams) is human-readable but machine-unparseable — agents consuming the plan programmatically need a structured format (table or JSON), not the ASCII diagram
- The contingency buffer ("add 20% to estimates") is a rule-of-thumb, not a calibrated estimate; agents apply it mechanically without understanding which tasks actually carry higher uncertainty
- Testing plan per-phase structure requires knowledge of which tests exist before tasks are written — in practice, test requirements are discovered during implementation, making the pre-plan untestable
- The full template is long (~450 lines with examples); agents filling it for small features produce plans where section overhead exceeds actual task content

## Agentic workflow
The agent reads `design.md` to extract the file change table (CREATE/MODIFY entries), builds the dependency graph (which file depends on which other file existing), applies the wave algorithm, and fills the implementation plan template section by section. Wave analysis is the highest-value section for agent executors because it encodes the scheduling contract. A plan review agent (or human) validates that the critical path is correct and that no circular dependencies exist before marking the plan `Approved`.

### Recommended subagents
- `faion-sdd-executor-agent` — consumes the implementation plan wave by wave; reads the wave analysis table to determine which tasks to run in parallel and in what order

### Prompt pattern
```
Write an implementation plan for feature: <feature-name>.

Read design.md and extract:
1. All file changes (CREATE/MODIFY) from the file structure table
2. All AD-X decisions and their file dependencies

Build:
- Dependency graph (which task must finish before which task can start)
- Wave analysis table (group tasks with no unmet dependencies into same wave)
- Critical path (longest dependency chain by token estimate)

For each task:
- Apply INVEST validation
- Estimate tokens: Context(5-10k) + Files(2-5k each) + Research(10-30k) + Output(5-20k)
- Flag any task >80k for decomposition before the 100k limit

Fill all sections of the implementation plan template.
Status: Draft.
```

```
Validate this implementation plan's wave analysis.
For each wave, verify: all dependencies of tasks in this wave appear in earlier waves.
Check for cycles in the dependency graph.
Output: validation result — OK or list of violations.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| mermaid-cli (`mmdc`) | Renders dependency DAG from Mermaid flowchart syntax to PNG/SVG for plan appendix | `npm install -g @mermaid-js/mermaid-cli` / https://github.com/mermaid-js/mermaid-cli |
| graphviz (`dot`) | Renders DAG from DOT language — more control than Mermaid for complex graphs | `apt install graphviz` / https://graphviz.org |
| tsort | Topological sort of dependency list — validates no cycles | System (GNU coreutils) |
| tokencost | Estimates token count for a set of files — feeds task token estimates | `pip install tokencost` / https://github.com/AgentOps-AI/tokencost |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes — GraphQL API | Import wave structure as cycles; tasks as issues with dependency links |
| GitHub Projects | SaaS | Yes — REST + GraphQL | Wave columns as project board columns; blocked status via custom fields |
| Notion | SaaS | Partial — REST API | Implementation plan as database with dependency relation property |
| Jira | SaaS | Partial — REST API | Story/subtask hierarchy; "blocked by" links map to wave dependencies |

## Templates & scripts
See `README.md` for the complete implementation plan template (all components, full example).

Topological sort validator for dependency list:
```bash
#!/usr/bin/env bash
# usage: ./validate-deps.sh
# Input: tab-separated TASK DEPENDS_ON pairs from stdin (or file)
# Example input line: "TASK-003\tTASK-001"
# Outputs: sorted order or cycle error
tsort 2>&1 | grep -q "loop" && echo "CYCLE DETECTED" || echo "OK: valid DAG"
```

Wave extraction from implementation plan:
```python
#!/usr/bin/env python3
"""Extract wave→tasks mapping from implementation-plan.md wave analysis table."""
import re, sys, json

def extract_waves(path):
    waves = {}
    with open(path) as f:
        in_wave_table = False
        for line in f:
            if '## Wave Analysis' in line:
                in_wave_table = True
                continue
            if in_wave_table and line.startswith('##'):
                break
            if in_wave_table:
                m = re.match(r'\|\s*(\d+)\s*\|\s*([^|]+)', line)
                if m:
                    wave_num = int(m.group(1))
                    tasks = re.findall(r'TASK-\d+', m.group(2))
                    if tasks:
                        waves[wave_num] = tasks
    return waves

if __name__ == '__main__':
    print(json.dumps(extract_waves(sys.argv[1]), indent=2))
```

## Best practices
- Fill the dependency graph before the wave analysis — the graph is the input to wave grouping; inverting this order produces incorrect waves
- The critical path section is only useful if token estimates are accurate; mark all estimates with a confidence level (Low/Medium/High) based on codebase familiarity
- The rollout strategy section should name the specific deployment mechanism (feature flag library, migration script, nginx reload) — generic "deploy code changes" steps provide no value
- Keep per-phase task entries concise: description in 2-3 sentences, acceptance criteria as verifiable conditions, file manifest as the exact paths — agents executing tasks use the manifest as their file list
- Risk assessment impact/likelihood matrix is only useful if mitigations are concrete actions, not vague hedges ("monitor for errors" vs. "alert on error rate > 0.5% for 5 minutes")

## AI-agent gotchas
- Wave visualization (ASCII box diagrams) in the README uses box-drawing characters that agents copy incorrectly, producing malformed diagrams; use simple arrow notation (`TASK-001 → TASK-003`) for agent-generated plans
- Agents tend to assign all tasks to "Wave 1 and Wave 2" because they underestimate the actual depth of the dependency graph; validate wave count against the dependency graph depth
- The `Blocks:` field in each task entry is redundant with the dependency graph but must be kept consistent; agents often update one without updating the other
- Testing plan per-phase tables are filled with "unit tests" for every phase without specifying what unit tests test — require explicit test file names or function names in the acceptance criteria instead
- Human-in-loop checkpoint: implementation plan `Draft → Approved` requires human (or review agent) to validate the critical path and wave analysis before `faion-sdd-executor-agent` begins execution

## References
- https://www.projectmanager.com/guides/critical-path-method (Critical Path Method)
- https://www.projectmanager.com/blog/task-dependencies (FS, SS, FF, SF dependency types)
- https://martinfowler.com/bliki/TestPyramid.html (Testing Pyramid — for testing plan section)
- https://www.pmi.org/learning/library/risk-analysis-project-management-7070 (PMI risk assessment)
- https://arxiv.org/abs/2510.25320 (GAP: Graph-based Agent Planning — parallel execution with dependency awareness)
- `skills/faion-knowledge/knowledge/solo/sdd/sdd/writing-implementation-plans/README.md` — methodology companion to this structural guide
