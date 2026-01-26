# faion-cli: Implementation Plan

## Overview

CLI tool for faion-network SDD workflow automation.

**Repository:** `github.com/faionfaion/faion-cli`

---

## Phase 1: Foundation

### Task 1.1: Project Setup

- [ ] Create repository structure
- [ ] Initialize go.mod with dependencies
- [ ] Create Makefile (build, test, lint, fmt)
- [ ] Setup golangci-lint config
- [ ] Create basic README.md

**Files:**
```
faion-cli/
├── cmd/faion/
│   └── main.go
├── pkg/
│   └── .gitkeep
├── go.mod
├── go.sum
├── Makefile
├── .golangci.yml
├── README.md
└── CLAUDE.md
```

### Task 1.2: CLI Framework

- [ ] Implement main.go with go-flags
- [ ] Add version flag
- [ ] Add debug/no-color global flags
- [ ] Implement help command
- [ ] Add signal handling (SIGINT, SIGTERM)

### Task 1.3: Configuration Package

- [ ] Create pkg/config/config.go with Config struct
- [ ] Implement Load() with precedence: project → global → embedded
- [ ] Create embedded default config
- [ ] Add config validation
- [ ] Write tests

### Task 1.4: Progress Logging

- [ ] Create pkg/progress/logger.go
- [ ] Implement timestamped logging
- [ ] Add color support (with --no-color)
- [ ] Implement file locking (flock)
- [ ] Write tests

---

## Phase 2: Core Commands

### Task 2.1: Init Command

- [ ] Create cmd/faion/init.go
- [ ] Create .aidocs/ directory structure
- [ ] Generate constitution.md template
- [ ] Create memory/ directory
- [ ] Add entries to .gitignore
- [ ] Write tests

### Task 2.2: Status Command

- [ ] Create cmd/faion/status.go
- [ ] Show project name and type
- [ ] Count features by status
- [ ] Count tasks by status
- [ ] Show recent activity
- [ ] Write tests

### Task 2.3: Tasks Command

- [ ] Create cmd/faion/tasks.go
- [ ] List tasks with filters (--todo, --in-progress, --done)
- [ ] Show task details
- [ ] Implement fzf selection
- [ ] Write tests

### Task 2.4: Move Command

- [ ] Create cmd/faion/move.go
- [ ] Move task between status directories
- [ ] Update timestamps
- [ ] Commit changes
- [ ] Write tests

---

## Phase 3: SDD Workflow

### Task 3.1: SDD Package

- [ ] Create pkg/sdd/types.go with Feature, Spec, Design, Task
- [ ] Create pkg/sdd/feature.go for feature management
- [ ] Create pkg/sdd/task.go for task operations
- [ ] Implement status transitions
- [ ] Write tests

### Task 3.2: Methodology Package

- [ ] Create pkg/methodology/loader.go
- [ ] Implement Get() for single methodology
- [ ] Implement GetForDomain() for skill methodologies
- [ ] Implement InjectPrompt() for prompt enrichment
- [ ] Write tests

### Task 3.3: Executor Package

- [ ] Create pkg/executor/claude.go
- [ ] Implement Execute() with streaming output
- [ ] Parse signals from output
- [ ] Handle timeouts and cancellation
- [ ] Write tests with mocks

### Task 3.4: Feature Command

- [ ] Create cmd/faion/feature.go
- [ ] Implement interactive feature creation
- [ ] Generate spec → design → impl-plan
- [ ] Handle signals (SPEC_READY, etc.)
- [ ] Write tests

---

## Phase 4: Execution Engine

### Task 4.1: Execute Command

- [ ] Create cmd/faion/execute.go
- [ ] Load task(s) from args or fzf
- [ ] Execute with methodology injection
- [ ] Handle TASK_DONE/TASK_FAILED signals
- [ ] Update task status
- [ ] Write tests

### Task 4.2: Quality Gates

- [ ] Create pkg/gate/gate.go with Gate types
- [ ] Implement L1-L6 checks
- [ ] Create cmd/faion/gate.go command
- [ ] Integrate gates into feature/execute flow
- [ ] Write tests

### Task 4.3: Memory Package

- [ ] Create pkg/memory/store.go
- [ ] Implement AddPattern/AddMistake/AddDecision
- [ ] Implement GetRelevant for context injection
- [ ] Parse markdown files
- [ ] Write tests

### Task 4.4: Git Operations

- [ ] Create pkg/git/repo.go
- [ ] Implement branch creation
- [ ] Implement commit operations
- [ ] Implement status checking
- [ ] Write tests

---

## Phase 5: Review System

### Task 5.1: Agent Package

- [ ] Create pkg/agent/agent.go
- [ ] Define default agents (quality, testing, etc.)
- [ ] Implement Runner for sequential execution
- [ ] Generate review summary
- [ ] Write tests

### Task 5.2: Review Command

- [ ] Create cmd/faion/review.go
- [ ] Run selected agents on changes
- [ ] Output findings
- [ ] Support --full/--quick modes
- [ ] Write tests

### Task 5.3: Plan Commands

- [ ] Create cmd/faion/plan.go
- [ ] Implement `plan constitution`
- [ ] Implement `plan spec`
- [ ] Implement `plan design`
- [ ] Implement `plan impl`
- [ ] Write tests

---

## Phase 6: Web Dashboard

### Task 6.1: Server Package

- [ ] Create pkg/web/server.go
- [ ] Implement HTTP server
- [ ] Create HTML template
- [ ] Add SSE endpoint for streaming
- [ ] Write tests

### Task 6.2: Serve Command

- [ ] Create cmd/faion/serve.go
- [ ] Start web server
- [ ] Open browser automatically
- [ ] Support --port flag
- [ ] Write tests

### Task 6.3: Session Management

- [ ] Create pkg/web/session.go
- [ ] Implement multi-session support
- [ ] Add file watcher for progress files
- [ ] Broadcast updates via SSE
- [ ] Write tests

---

## Phase 7: Polish

### Task 7.1: Update Command

- [ ] Create cmd/faion/update.go
- [ ] Check faion-network updates
- [ ] Pull latest from git
- [ ] Show changelog
- [ ] Write tests

### Task 7.2: Documentation

- [ ] Write comprehensive README.md
- [ ] Create CLAUDE.md for AI context
- [ ] Write llms.txt for LLM instructions
- [ ] Add usage examples
- [ ] Create man page

### Task 7.3: Release Automation

- [ ] Create .github/workflows/release.yml
- [ ] Build for linux/darwin amd64/arm64
- [ ] Create .deb and .rpm packages
- [ ] Publish to GitHub releases
- [ ] Create Homebrew formula

### Task 7.4: E2E Testing

- [ ] Create test script for full workflow
- [ ] Test init → feature → execute → review
- [ ] Test web dashboard
- [ ] Test signal handling
- [ ] Document test procedures

---

## Dependencies

```go
require (
    github.com/jessevdk/go-flags v1.5.0
    github.com/go-git/go-git/v5 v5.11.0
    gopkg.in/ini.v1 v1.67.0
    github.com/fatih/color v1.16.0
    github.com/stretchr/testify v1.8.4
)
```

---

## Complexity Estimates

| Phase | Complexity | Est. Tokens |
|-------|------------|-------------|
| Phase 1 | Low | ~30k |
| Phase 2 | Low | ~40k |
| Phase 3 | Medium | ~60k |
| Phase 4 | High | ~80k |
| Phase 5 | Medium | ~50k |
| Phase 6 | Medium | ~50k |
| Phase 7 | Low | ~30k |
| **Total** | | **~340k** |

---

## Success Criteria

- [ ] `faion init` creates valid .aidocs structure
- [ ] `faion feature "X"` creates spec/design/impl-plan
- [ ] `faion execute` runs tasks autonomously
- [ ] `faion gate L5` validates quality
- [ ] `faion review` runs all agents
- [ ] `faion serve` shows live dashboard
- [ ] All tests pass with 80%+ coverage
- [ ] Works on Linux and macOS
