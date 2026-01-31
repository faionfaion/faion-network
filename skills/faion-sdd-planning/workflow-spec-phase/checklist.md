# Workflow Spec Phase Checklist

## Phase 1: Writing Constitutions

### Existing Project Mode (for codebase analysis)

- [ ] Analyze directory structure and detect tech stack
- [ ] Read CLAUDE.md, README.md, package.json, pyproject.toml
- [ ] Review config files (linter, formatter, testing setup)
- [ ] Identify architecture patterns from codebase
- [ ] Extract naming conventions and standards
- [ ] Document findings and present for validation

### New Project Mode (for greenfield projects)

- [ ] Conduct Socratic dialogue: "What problem does this solve?"
- [ ] Apply Five Whys analysis to reach real need
- [ ] Present alternatives for: language, framework, database
- [ ] Show pros/cons for each alternative
- [ ] Discuss architecture: monolith vs microservices, REST vs GraphQL
- [ ] Define standards: linting, formatting, testing, git workflow
- [ ] Draft constitution and gather approval

### Save Constitution

- [ ] Create `.aidocs/constitution.md` at project root
- [ ] Add Vision, Tech Stack, Architecture Patterns, Code Standards, Git Workflow, Structure, Quality Gates, Principles
- [ ] Create CLAUDE.md navigation hub in project folder

## Phase 2: Writing Specifications

### Phase 2.1: Brainstorming

- [ ] Use Five Whys technique to clarify real problem (not symptoms)
- [ ] Generate alternatives for each solution approach
- [ ] Present pros/cons for each alternative
- [ ] Challenge assumptions: "Is this needed for v1?", "What if we don't do this?"
- [ ] Question whether feature already exists in codebase

### Phase 2.2: Research Codebase

- [ ] Search for similar implementations using Glob and Grep
- [ ] Share findings with user: "Found export feature in services.py"
- [ ] Identify existing patterns and reusable components
- [ ] Understand how related features are implemented

### Phase 2.3: Clarify Details

- [ ] Conduct user stories workshop with concrete examples
- [ ] Ask edge case questions: "What if data invalid?", "What if 1000+ records?"
- [ ] Discuss frequency, impact, alternatives
- [ ] Resolve ambiguities through dialogue, not assumptions

### Phase 2.4: Draft Section by Section

- [ ] Write Problem Statement (SMART criteria)
- [ ] Show and validate: "Is this correct?"
- [ ] Write User Stories with AC
- [ ] Show and validate: "Is this complete?"
- [ ] Write Functional Requirements
- [ ] Show and validate: "Anything redundant?"
- [ ] Define Out of Scope
- [ ] Show and validate: "Agree with boundaries?"

### Phase 2.5: Quality Review

- [ ] Verify problem is SMART (specific, measurable, achievable, relevant, time-bound)
- [ ] Check user stories follow INVEST principle
- [ ] Verify requirements are testable
- [ ] Confirm out-of-scope is explicit
- [ ] Call faion-sdd-reviewer-agent (mode: spec)

### Phase 2.6: Save Specification

- [ ] New feature: create `.aidocs/features/backlog/{NN}-{name}/spec.md`
- [ ] Existing feature: update spec.md in existing feature folder
- [ ] Set status to "Draft" or "Approved"

## Phase 3: Backlog Grooming

- [ ] Read roadmap.md and constitution.md
- [ ] List features by status: in-progress, todo, backlog
- [ ] Display status: feature name, summary, priority (P0/P1/P2)
- [ ] Ask user: "What do you want to do?" (review, take feature, add feature, remove, finish)
- [ ] For selected feature: refine spec (if needed), write design (if needed), create tasks (if needed)
- [ ] When all documents complete: move feature from backlog/ to todo/

### Definition of Ready (for moving to todo)

- [ ] Problem/need is clear
- [ ] Acceptance criteria defined
- [ ] Dependencies identified
- [ ] Spec approved
- [ ] Design approved
- [ ] Tasks created
- [ ] No blockers

## Phase 4: Roadmapping

### Phase 4.1: Analyze Progress

- [ ] Count completed features in features/done/
- [ ] Count features in features/backlog/
- [ ] Review milestones and target dates

### Phase 4.2: Review Priorities

- [ ] Ask: "Are priorities current?"
- [ ] Update MoSCoW priorities if needed
- [ ] Discuss any blockers or dependencies

### Phase 4.3: Add New Features

- [ ] For each new idea: discuss scope via Socratic dialogue
- [ ] Create `backlog/{NN}-{name}/spec.md` with problem statement
- [ ] Add feature to roadmap.md

### Phase 4.4: Update Roadmap

- [ ] Now (90% confident): detailed, committed features
- [ ] Next (70% confident): planned, flexible features
- [ ] Later (50% confident): thematic, vision features
- [ ] Done: completed features with highlights
- [ ] Include 20% buffer for unknowns
- [ ] Add risks and mitigation strategies
- [ ] Track success metrics