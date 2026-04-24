# Workflows Checklist

## Phase 1: Select SDD Workflow Phase

- [ ] Determine which phase to execute: Spec, Design, or Execution
- [ ] Read relevant workflow document (workflow-spec-phase.md, workflow-design-phase.md, etc.)
- [ ] Identify prerequisites for this phase
- [ ] Check that prior phases are complete

## Phase 2: Specification Phase Workflow

- [ ] **Writing Constitutions:** Analyze codebase or define project vision (existing vs new project)
- [ ] **Writing Specifications:** Execute Brainstorm → Research → Clarify → Draft → Review → Save
- [ ] **Backlog Grooming:** Review priorities, refine specs, move ready features to todo
- [ ] **Roadmapping:** Analyze progress, add new features, update roadmap.md

## Phase 3: Design Phase Workflow

- [ ] **Read Specification:** Extract requirements, user stories, API contracts
- [ ] **Read Constitution:** Get architecture patterns and code standards
- [ ] **Research Codebase:** Find similar implementations and existing patterns
- [ ] **Make Architecture Decisions:** For each key decision - list options, choose, document rationale
- [ ] **Define Technical Approach:** Break into components, data flows, file changes
- [ ] **Define Testing Strategy:** Unit tests, integration tests, test data
- [ ] **Identify Risks:** Risk description, impact, mitigation strategy
- [ ] **Save design.md:** After approval from stakeholders and agent review

## Phase 4: Implementation Planning Workflow

- [ ] **Load Context:** Read constitution, spec, design
- [ ] **Analyze Complexity:** Estimate tokens for each file to create/modify
- [ ] **Define Work Units:** Group related work into logical blocks
- [ ] **Apply 100k Rule:** Ensure each task < 100k tokens (research + task + impl + buffer)
- [ ] **Map Dependencies:** Create task dependency table and graph
- [ ] **Draft Plan:** Show overview, task list, execution order
- [ ] **Review:** Get stakeholder and agent review
- [ ] **Save implementation-plan.md:** Feature ready for execution

## Phase 5: Task Creation Workflow

- [ ] **Verify Prerequisites:** spec.md and design.md approved
- [ ] **Create or Verify Plan:** implementation-plan.md exists
- [ ] **Load Task Information:** Extract each task from implementation plan
- [ ] **Call Task Creator Agent:** Generate comprehensive TASK_*.md file
- [ ] **Review Tasks:** 4-pass review (completeness, consistency, coverage, executability)
- [ ] **Organize Tasks:** Move to todo/ folder ready for execution

## Phase 6: Execution Phase Workflow

- [ ] **Execute Single Task:** Run one TASK_*.md with agent, capture results
- [ ] **Execute Batch:** Run all tasks in feature with resilience and error handling
- [ ] **Quality Gates:** Verify code, tests, documentation
- [ ] **Confidence Checks:** Validate 90%+ confidence before proceeding
- [ ] **Reflexion Learning:** Update patterns.md and mistakes.md with discoveries

## Phase 7: Key Principles to Apply

- [ ] **100k Token Rule:** Each task must fit within 100k token context window
- [ ] **Quality Gates:** Apply L1-L6 gates (syntax, types, tests, integration, review, acceptance)
- [ ] **Confidence Thresholds:** Proceed >90%, clarify 70-89%, stop <70%
- [ ] **Traceability:** Every task traces to FR/AD, every AC testable
- [ ] **Wave Execution:** Group independent tasks, execute in parallel, checkpoint between waves