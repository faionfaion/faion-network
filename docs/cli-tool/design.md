# faion-cli: Technical Design

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        faion-cli                            │
├─────────────────────────────────────────────────────────────┤
│  cmd/faion/          CLI entry point, flag parsing          │
├─────────────────────────────────────────────────────────────┤
│  pkg/                                                       │
│  ├── config/         Configuration loading                  │
│  ├── sdd/            SDD workflow logic                     │
│  │   ├── spec.go     Specification handling                 │
│  │   ├── design.go   Design document handling               │
│  │   ├── plan.go     Implementation plan handling           │
│  │   ├── task.go     Task management                        │
│  │   └── gate.go     Quality gates                          │
│  ├── executor/       Claude Code execution                  │
│  ├── methodology/    Methodology loading & injection        │
│  ├── agent/          Review agents                          │
│  ├── memory/         Pattern/mistake storage                │
│  ├── git/            Git operations                         │
│  ├── progress/       Logging with timestamps                │
│  └── web/            Dashboard, SSE streaming               │
└─────────────────────────────────────────────────────────────┘
```

## Package Design

### pkg/config

```go
package config

type Config struct {
    // Project settings
    ProjectName string
    ProjectType string // web-app, cli, library, etc.

    // Execution
    MaxIterations    int
    IterationDelayMs int
    YoloMode         bool

    // Paths
    AidocsDir    string // default: .aidocs
    MethodsDir   string // faion-network methodologies

    // Claude
    ClaudeCommand string
    ClaudeModel   string

    // Review
    EnableQualityAgent        bool
    EnableTestingAgent        bool
    EnableSimplificationAgent bool
    EnableDocumentationAgent  bool

    // Web
    WebPort int
}

// Load searches: .faion/config → ~/.config/faion/config → embedded
func Load(projectPath string) (*Config, error)
```

### pkg/sdd

Core SDD workflow types:

```go
package sdd

// Feature represents a feature being developed
type Feature struct {
    ID          string    // e.g., "001"
    Name        string    // e.g., "user-authentication"
    Status      Status    // backlog, todo, in-progress, done
    Path        string    // .aidocs/features/{status}/{id}-{name}/
    Spec        *Spec
    Design      *Design
    ImplPlan    *ImplPlan
    Tasks       []*Task
    CreatedAt   time.Time
    CompletedAt *time.Time
}

type Status string

const (
    StatusBacklog    Status = "backlog"
    StatusTodo       Status = "todo"
    StatusInProgress Status = "in-progress"
    StatusDone       Status = "done"
)

// Spec represents a feature specification
type Spec struct {
    Path           string
    Title          string
    Problem        string
    UserNeed       string
    SuccessCriteria []string
    OutOfScope     []string
    GateStatus     GateStatus // L1, L2
}

// Design represents a technical design
type Design struct {
    Path          string
    Architecture  string
    Components    []Component
    APIs          []APIContract
    DataModel     string
    GateStatus    GateStatus // L3
}

// ImplPlan represents implementation plan
type ImplPlan struct {
    Path         string
    Tasks        []TaskDef
    Dependencies map[string][]string
    Complexity   string // low, medium, high
    TokenEstimate int
    GateStatus   GateStatus // L4
}

// Task represents an atomic task
type Task struct {
    ID          string
    Title       string
    Description string
    Checklist   []ChecklistItem
    Status      Status
    FeatureID   string
    GateStatus  GateStatus // L5, L6
}

type ChecklistItem struct {
    Text      string
    Completed bool
}
```

### pkg/methodology

```go
package methodology

// Loader provides access to faion-network methodologies
type Loader struct {
    basePath string // ~/.claude/skills/
}

// Get returns methodology content by skill and name
func (l *Loader) Get(skill, name string) (string, error)

// GetForDomain returns all methodologies for a domain
func (l *Loader) GetForDomain(domain string) ([]Methodology, error)

// InjectPrompt adds relevant methodologies to a prompt
func (l *Loader) InjectPrompt(prompt string, task *sdd.Task) string

type Methodology struct {
    Skill       string // e.g., faion-testing-developer
    Name        string // e.g., test-driven-development
    Path        string
    Content     string
    README      string // README.md content
    Checklist   string // checklist.md content
    Examples    string // examples.md content
    Templates   string // templates.md content
    LLMPrompts  string // llm-prompts.md content
}
```

### pkg/executor

```go
package executor

// Claude executes prompts via Claude Code CLI
type Claude struct {
    command     string // "claude" or custom
    model       string
    methodsDir  string
    methodLoader *methodology.Loader
}

// Config for execution
type Config struct {
    PlanFile     string
    ProgressPath string
    Task         *sdd.Task
    Feature      *sdd.Feature
    Methodologies []string // skills to inject
    Debug        bool
}

// Execute runs Claude with SDD context
func (c *Claude) Execute(ctx context.Context, cfg Config) (*Result, error) {
    prompt := c.buildPrompt(cfg)

    // Add relevant methodologies
    if cfg.Task != nil {
        prompt = c.methodLoader.InjectPrompt(prompt, cfg.Task)
    }

    return c.run(ctx, prompt, cfg.ProgressPath)
}

// Result of execution
type Result struct {
    Success  bool
    Signal   Signal // TASK_DONE, TASK_FAILED, etc.
    Output   string
    Duration time.Duration
}

type Signal string

const (
    SignalTaskDone      Signal = "TASK_DONE"
    SignalTaskFailed    Signal = "TASK_FAILED"
    SignalFeatureDone   Signal = "FEATURE_DONE"
    SignalGatePassed    Signal = "GATE_PASSED"
    SignalGateFailed    Signal = "GATE_FAILED"
    SignalQuestion      Signal = "QUESTION"
    SignalSpecReady     Signal = "SPEC_READY"
    SignalDesignReady   Signal = "DESIGN_READY"
    SignalImplPlanReady Signal = "IMPL_PLAN_READY"
)
```

### pkg/agent

```go
package agent

// Agent performs specialized review
type Agent struct {
    Name        string
    Description string
    PromptPath  string
    Enabled     bool
}

// DefaultAgents returns built-in review agents
func DefaultAgents() []*Agent {
    return []*Agent{
        {Name: "quality", Description: "Bugs, security, race conditions"},
        {Name: "testing", Description: "Coverage, test quality"},
        {Name: "simplification", Description: "Over-engineering detection"},
        {Name: "documentation", Description: "README/CLAUDE.md updates"},
        {Name: "implementation", Description: "Goal achievement verification"},
    }
}

// Runner executes agents in sequence or parallel
type Runner struct {
    agents   []*Agent
    executor *executor.Claude
}

// RunReview executes all enabled agents
func (r *Runner) RunReview(ctx context.Context, changes []string) (*ReviewResult, error)

type ReviewResult struct {
    AgentResults []AgentResult
    PassedAll    bool
    Summary      string
}
```

### pkg/gate

```go
package gate

// Gate represents a quality checkpoint
type Gate struct {
    Level       Level
    Name        string
    Description string
    Checks      []Check
}

type Level int

const (
    L1 Level = iota + 1 // Pre-spec
    L2                  // Post-spec
    L3                  // Post-design
    L4                  // Pre-execute
    L5                  // Post-execute
    L6                  // Pre-merge
)

type Check struct {
    Name     string
    Validate func(context.Context, *sdd.Feature) error
}

// Validator runs gate checks
type Validator struct {
    gates map[Level]*Gate
}

// Validate runs all checks for a gate level
func (v *Validator) Validate(ctx context.Context, level Level, feature *sdd.Feature) (*GateResult, error)

type GateResult struct {
    Level   Level
    Passed  bool
    Results []CheckResult
    Summary string
}
```

### pkg/memory

```go
package memory

// Store manages SDD learning artifacts
type Store struct {
    basePath string // .aidocs/memory/
}

// AddPattern records a learned pattern
func (s *Store) AddPattern(ctx context.Context, p Pattern) error

// AddMistake records an error and solution
func (s *Store) AddMistake(ctx context.Context, m Mistake) error

// AddDecision records a key decision
func (s *Store) AddDecision(ctx context.Context, d Decision) error

// GetRelevant returns patterns/mistakes relevant to a task
func (s *Store) GetRelevant(ctx context.Context, task *sdd.Task) (*Memory, error)

type Pattern struct {
    Date        time.Time
    Context     string
    Pattern     string
    Application string
}

type Mistake struct {
    Date     time.Time
    Error    string
    Solution string
    Lesson   string
}

type Decision struct {
    Date      time.Time
    Context   string
    Decision  string
    Rationale string
}

type Memory struct {
    Patterns  []Pattern
    Mistakes  []Mistake
    Decisions []Decision
}
```

## Command Implementation

### cmd/faion/main.go

```go
package main

type opts struct {
    // Global flags
    Debug   bool `short:"d" long:"debug" description:"enable debug logging"`
    NoColor bool `long:"no-color" description:"disable color output"`
    Version bool `short:"v" long:"version" description:"print version and exit"`

    // Commands
    Init    InitCmd    `command:"init" description:"initialize SDD structure"`
    Feature FeatureCmd `command:"feature" description:"create new feature"`
    Execute ExecuteCmd `command:"execute" description:"execute task(s)"`
    Gate    GateCmd    `command:"gate" description:"run quality gate"`
    Review  ReviewCmd  `command:"review" description:"review changes"`
    Plan    PlanCmd    `command:"plan" description:"create SDD artifacts"`
    Status  StatusCmd  `command:"status" description:"show project status"`
    Tasks   TasksCmd   `command:"tasks" description:"list tasks"`
    Move    MoveCmd    `command:"move" description:"move task between states"`
    Serve   ServeCmd   `command:"serve" description:"start web dashboard"`
    Update  UpdateCmd  `command:"update" description:"update faion-network"`
}
```

### Command: init

```go
type InitCmd struct {
    Force bool `short:"f" long:"force" description:"overwrite existing"`
}

func (c *InitCmd) Execute(args []string) error {
    // 1. Create .aidocs structure
    // 2. Create constitution.md template
    // 3. Create memory/ directory
    // 4. Add .gitignore entries
    // 5. Print success message
}
```

### Command: feature

```go
type FeatureCmd struct {
    Interactive bool `short:"i" long:"interactive" description:"interactive mode"`
    Yolo        bool `long:"yolo" description:"autonomous mode"`
}

func (c *FeatureCmd) Execute(args []string) error {
    // 1. Parse feature description from args
    // 2. Create feature directory in backlog/
    // 3. Run Claude to create spec
    // 4. Wait for SPEC_READY signal
    // 5. Run L2 gate
    // 6. If passed, create design
    // 7. Wait for DESIGN_READY signal
    // 8. Run L3 gate
    // 9. If passed, create impl-plan
    // 10. Wait for IMPL_PLAN_READY signal
    // 11. Run L4 gate
    // 12. Move to todo/
}
```

### Command: execute

```go
type ExecuteCmd struct {
    Yolo        bool `long:"yolo" description:"autonomous mode"`
    MaxTasks    int  `short:"m" long:"max" default:"50" description:"max tasks"`
    Parallel    bool `short:"p" long:"parallel" description:"parallel execution"`
    DryRun      bool `long:"dry-run" description:"show what would be executed"`
}

func (c *ExecuteCmd) Execute(args []string) error {
    // 1. Load task(s) from args or select with fzf
    // 2. Move to in-progress/
    // 3. Execute each task:
    //    a. Build prompt with methodologies
    //    b. Run Claude
    //    c. Parse signal
    //    d. If TASK_DONE, mark complete
    //    e. If TASK_FAILED, stop or retry
    // 4. Run L5 gate after all tasks
    // 5. Run review agents
    // 6. Run L6 gate
    // 7. Move to done/
}
```

## Prompt Templates

### task.txt

```
Read the task file at {{TASK_FILE}}.

Context:
- Feature: {{FEATURE_NAME}}
- Spec: {{SPEC_PATH}}
- Design: {{DESIGN_PATH}}

Available methodologies for this task:
{{METHODOLOGIES}}

Memory (patterns and mistakes from this project):
{{MEMORY}}

STEP 1 - IMPLEMENT:
- Read the spec and design to understand context
- Implement ALL items in the checklist
- Follow patterns from memory
- Avoid mistakes from memory

STEP 2 - VALIDATE:
- Run tests: {{TEST_COMMAND}}
- Run lint: {{LINT_COMMAND}}
- Fix any failures

STEP 3 - COMPLETE:
- Update task file: change [ ] to [x]
- Commit changes
- Output: <<<FAION:TASK_DONE>>>

If failed after attempts, output: <<<FAION:TASK_FAILED>>>
```

### spec.txt

```
Create a specification for the following feature:

Feature: {{DESCRIPTION}}

Use this template:
{{SPEC_TEMPLATE}}

Apply these methodologies:
{{METHODOLOGIES}}

When complete, output: <<<FAION:SPEC_READY>>>
```

## File Locations

| Type | Location |
|------|----------|
| Global config | ~/.config/faion/config |
| Global prompts | ~/.config/faion/prompts/ |
| Project config | .faion/config |
| Project prompts | .faion/prompts/ |
| SDD artifacts | .aidocs/ |
| Progress logs | faion-progress-*.txt |
| Methodologies | ~/.claude/skills/faion-*/ |

## Error Handling

```go
// Errors are wrapped with context
type Error struct {
    Phase   string // init, spec, design, execute, review
    Task    string
    Feature string
    Cause   error
}

// Recoverable errors trigger retry
type RecoverableError struct {
    Error
    RetryCount int
    MaxRetries int
}

// Fatal errors stop execution
type FatalError struct {
    Error
    Suggestion string
}
```

## Metrics & Observability

```go
type Metrics struct {
    FeaturesCreated   int
    TasksExecuted     int
    GatesPassed       int
    GatesFailed       int
    ReviewIssuesFound int
    ExecutionTime     time.Duration
}

// Stored in .aidocs/metrics.json for analysis
```

## Security Considerations

1. **No secrets in prompts** - Never include API keys, passwords
2. **Safe git operations** - No force push, no destructive commands
3. **Sandboxed execution** - Claude runs in restricted mode
4. **Progress file permissions** - 0640, not world-readable
