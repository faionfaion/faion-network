# Agent Integration — SDD Workflows

## When to use
- As a navigation hub when an agent or developer needs to orient within the SDD lifecycle and find the right workflow file for their current phase
- When bootstrapping a new project: starting from constitution through to first execution phase
- When switching phases mid-feature (e.g., spec is approved, now starting design phase) and need the authoritative input/output map
- When explaining the SDD system to a new agent or contributor — the three-phase structure (Spec → Design → Execution) and their transition criteria are defined here

## When NOT to use
- As a substitute for the detailed phase-specific workflow files: `workflow-spec-phase.md`, `workflow-design-phase.md`, `workflow-execution-phase.md` — this file is navigation, not instructions
- When you are already in a specific phase and know what you need — go directly to the relevant phase file

## Where it fails / limitations
- This is a hub document, not a workflow in itself — agents that stop here and try to execute from it will find only summaries, not step-by-step procedures
- The input/output tables describe file artifacts, not the quality criteria for those artifacts — a "draft" spec.md that fails the confidence check is not a valid input for the design phase
- The quick reference table ("Goal → Files to Use") can mislead agents into jumping phases: starting "design phase" when a spec has not been approved is a common error this document cannot prevent by itself
- Confidence thresholds (90% to proceed) cannot be self-assessed by the executing agent — an external review agent or human must validate

## Agentic workflow
An agent that receives a vague task like "work on feature X" should start by reading this workflows README to locate the current lifecycle state of the feature, then navigate to the appropriate phase file. The three-phase structure (Spec → Design → Execution) maps directly to `faion-sdd-executor-agent`'s phase logic. Agents should use the workflow inputs/outputs table to verify that required artifacts exist and meet status criteria before advancing to the next phase.

### Recommended subagents
- `faion-sdd-executor-agent` — the primary consumer of this workflow structure; navigates through Spec → Design → Execution phases, checks phase inputs, gates on confidence thresholds

### Prompt pattern
```
You are working on feature: <feature-name>.
Current state: spec.md exists (status: Approved), design.md does not exist.

Read the SDD workflow navigation document to identify the correct next phase.
Then read the workflow-design-phase.md for detailed instructions.
Do not skip the confidence check before starting.
```

```
Check the current lifecycle state of feature <feature-name>:
1. Read .aidocs/<lifecycle-dir>/<feature-dir>/ file listing
2. Check spec.md status field
3. Check design.md status field
4. Check implementation-plan.md existence
5. Report: which SDD phase is active and what is the next required action.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| ripgrep (`rg`) | Find features by lifecycle state: `rg 'Status: Draft' .aidocs/` | System / https://github.com/BurntSushi/ripgrep |
| jq | Parse JSON feature manifests if used for state tracking | System / https://jqlang.github.io/jq/ |
| tree | Visualize the .aidocs/ lifecycle directory structure | `apt install tree` / `brew install tree` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Projects | SaaS | Yes — REST + GraphQL API | Mirror SDD lifecycle (backlog/todo/in-progress/done) as project board columns |
| Linear | SaaS | Yes — REST + GraphQL API | SDD phases map to Linear cycle states; features map to projects |
| Notion | SaaS | Partial — REST API | Database view for lifecycle tracking; custom properties for phase status |

## Templates & scripts
This directory is navigation-only. Phase-specific templates are in:
- `../template-spec/` — spec template
- `../template-design/` — design document template
- `../template-task/` — task file template

Feature lifecycle state checker:
```bash
#!/usr/bin/env bash
# usage: ./sdd-state.sh feature-042-shopping-cart
# Reports current SDD lifecycle state for a feature
set -euo pipefail
FEATURE="$1"
AIDOCS=".aidocs"
for phase in backlog todo in-progress done; do
  if [ -d "$AIDOCS/$phase/$FEATURE" ]; then
    echo "Feature $FEATURE is in: $phase"
    # Check document statuses
    for doc in spec.md design.md implementation-plan.md; do
      FILE="$AIDOCS/$phase/$FEATURE/$doc"
      if [ -f "$FILE" ]; then
        STATUS=$(grep -m1 'Status:' "$FILE" | head -1 | sed 's/.*Status: //')
        echo "  $doc → $STATUS"
      else
        echo "  $doc → NOT FOUND"
      fi
    done
    exit 0
  fi
done
echo "Feature $FEATURE not found in any lifecycle directory"
```

## Best practices
- Always confirm the current lifecycle phase before executing any SDD action — running a design-phase action on a spec-phase feature creates artifacts in the wrong order
- The three confidence thresholds (>=90% proceed, 70-89% clarify, <70% stop) should be applied at every phase transition, not just at execution time
- The Quality Gate levels (L1 Syntax through L6 Acceptance) belong to the execution phase, not design — do not apply them to spec or design documents
- Treat this workflows README as the entry point for any agent that receives an SDD task without explicit phase context
- The input/output tables are contracts: do not advance to the next phase until all outputs from the current phase exist with the correct status

## AI-agent gotchas
- Agents reading only this hub document will understand the structure but lack the procedural details; they must follow the links to phase-specific files before executing
- Phase confusion is the most common agent error: an agent asked to "write a design doc" may start writing implementation tasks if it has not confirmed that spec.md is approved
- The 100k token rule applies to execution-phase tasks, not to spec or design documents — agents sometimes refuse to write a thorough design doc because "it might be too long"
- Human-in-loop checkpoints exist at every phase boundary: spec Draft → Approved (human), design Draft → Approved (human), implementation-plan Draft → Approved (human or review agent)
- Agents without file-system access cannot verify the .aidocs/ directory structure — always provide the file listing as part of the task context

## References
- `skills/faion/knowledge/solo/sdd/sdd-planning/workflow-spec-phase.md` — specification phase detail
- `skills/faion/knowledge/solo/sdd/sdd-planning/workflow-design-phase.md` — design phase detail
- `skills/faion/knowledge/solo/sdd/sdd/sdd-workflow-overview/README.md` — high-level SDD overview
- `agents/faion-sdd-executor-agent.md` — the primary agent that implements this workflow
