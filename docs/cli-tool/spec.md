# faion-cli: CLI Tool Specification

## Problem Statement

faion-network is a powerful knowledge framework with 605 methodologies, but:
1. **No standalone CLI** - depends entirely on Claude Code integration
2. **No autonomous execution** - requires user to stay in Claude Code session
3. **No progress visibility** - can't monitor execution from outside
4. **No plan execution engine** - unlike ralphex, can't run plans autonomously

## Philosophy Comparison

| Aspect | ralphex | faion-cli (proposed) |
|--------|---------|---------------------|
| Focus | Plan execution engine | SDD workflow orchestrator |
| Knowledge | Minimal (prompts only) | 605 methodologies |
| Planning | Creates simple task lists | Creates spec → design → impl-plan |
| Execution | Task by task | Feature by feature with quality gates |
| Review | 5 generic agents | Domain-specific agents (testing, quality, etc.) |
| Output | Progress file | SDD artifacts + progress |

## Core Philosophy

**"Specification-Driven Development as a CLI"**

faion-cli brings SDD workflow outside Claude Code:
- Autonomous execution with full methodology access
- Quality gates at each phase
- Domain-specific reviews
- Structured output (.aidocs/)

## Commands

### Primary Commands

```bash
# Initialize SDD structure in project
faion init

# Create feature (spec → design → impl-plan → tasks)
faion feature "user authentication"

# Execute task(s) autonomously
faion execute [task-file|feature-folder]

# Run quality gate
faion gate L1|L2|L3|L4|L5|L6

# Review changes
faion review [--full|--quick]
```

### Planning Commands

```bash
# Create constitution
faion plan constitution

# Create feature spec
faion plan spec "feature description"

# Create design from spec
faion plan design path/to/spec.md

# Create implementation plan from design
faion plan impl path/to/design.md
```

### Utility Commands

```bash
# Show project status
faion status

# List tasks
faion tasks [--todo|--in-progress|--done]

# Move task between states
faion move TASK-001 todo|in-progress|done

# Start web dashboard
faion serve [--port 8080]

# Update faion-network
faion update
```

## Execution Modes

### 1. Interactive Mode (default)
- Asks questions via fzf/terminal
- Shows progress in real-time
- Allows intervention

### 2. YOLO Mode (--yolo)
- Maximum autonomy
- No questions asked
- Full execution until completion or failure

### 3. Dry-run Mode (--dry-run)
- Shows what would be executed
- No actual changes
- Useful for planning review

## Signals

Similar to ralphex, but extended for SDD:

```
<<<FAION:TASK_DONE>>>
<<<FAION:TASK_FAILED>>>
<<<FAION:FEATURE_DONE>>>
<<<FAION:GATE_PASSED:L3>>>
<<<FAION:GATE_FAILED:L3>>>
<<<FAION:QUESTION:{"question":"...", "options":[...]}>>>
<<<FAION:SPEC_READY>>>
<<<FAION:DESIGN_READY>>>
<<<FAION:IMPL_PLAN_READY>>>
```

## Directory Structure

```
project/
├── .aidocs/                    # Created by faion init
│   ├── constitution.md         # Project principles
│   ├── roadmap.md             # Milestones
│   ├── memory/                # Learning storage
│   │   ├── patterns.md
│   │   ├── mistakes.md
│   │   └── decisions.md
│   └── features/
│       ├── backlog/
│       ├── todo/
│       ├── in-progress/
│       └── done/
└── faion-progress-*.txt        # Execution logs (gitignored)
```

## Configuration

### Project Config (.faion/config)

```ini
[project]
name = my-project
type = web-app

[execution]
max_iterations = 50
iteration_delay_ms = 100

[review]
enable_quality_agent = true
enable_testing_agent = true
enable_simplification_agent = true

[claude]
command = claude
model = opus
```

### Global Config (~/.config/faion/config)

```ini
[defaults]
yolo_mode = false
web_dashboard = false
port = 8080

[prompts]
# Override default prompts
task = ~/.config/faion/prompts/task.txt
review = ~/.config/faion/prompts/review.txt
```

## Integration with Claude Code

faion-cli uses Claude Code as execution backend:

```go
// Execute Claude with SDD context
func (e *Executor) RunWithMethodologies(ctx context.Context, task Task) error {
    prompt := e.buildPrompt(task)
    // Inject relevant methodologies from faion-network
    prompt += e.getMethodologies(task.Domain)
    return e.claude.Execute(ctx, prompt)
}
```

## Quality Gates

| Gate | Phase | Checks |
|------|-------|--------|
| L1 | Pre-spec | Problem defined, user need validated |
| L2 | Post-spec | Spec complete, success criteria clear |
| L3 | Post-design | Architecture sound, APIs defined |
| L4 | Pre-execute | Tasks atomic, dependencies clear |
| L5 | Post-execute | Tests pass, code quality OK |
| L6 | Pre-merge | Review complete, docs updated |

## Review Agents

Built-in agents (from faion-network):

| Agent | Focus |
|-------|-------|
| quality | Bugs, security, race conditions |
| testing | Coverage, test quality |
| simplification | Over-engineering detection |
| documentation | README/CLAUDE.md updates |
| implementation | Goal achievement verification |

## Technology Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Go | Fast startup, single binary, ralphex patterns |
| CLI Parser | jessevdk/go-flags | Same as ralphex, proven |
| Git | go-git | Pure Go, no external deps |
| Config | gopkg.in/ini.v1 | Simple, familiar |
| Web | net/http + SSE | Lightweight, no JS framework |

## Implementation Phases

### Phase 1: Core CLI
- init, status, tasks commands
- Basic execution (single task)
- Progress logging

### Phase 2: SDD Workflow
- feature, plan commands
- Quality gates
- Memory storage

### Phase 3: Review System
- Built-in agents
- Multi-phase review
- Web dashboard

### Phase 4: Advanced
- Parallelization
- Remote execution
- Team collaboration

## Success Criteria

1. **Autonomous execution** - Run `faion execute feature-001` and walk away
2. **SDD compliance** - All outputs follow .aidocs structure
3. **Quality enforcement** - Gates prevent bad code from proceeding
4. **Methodology access** - Full 605 methodologies available during execution
5. **Progress visibility** - Web dashboard shows real-time status

## Open Questions

1. Should faion-cli be in faion-network repo or separate?
2. Should we support codex as alternative backend?
3. How to handle rate limits during autonomous execution?
4. Should memory sync across projects?
