# Templates Checklist

## Phase 1: Use Specification Template

- [ ] Copy template-spec.md structure for new specifications
- [ ] Include metadata: Version, Status, Author, Date, Project
- [ ] Add Reference Documents (constitution, related specs)
- [ ] Complete all sections: Problem, Personas, Stories, FR, NFR, AC, Scope
- [ ] Ensure each section follows quality guidelines
- [ ] Save to `.aidocs/features/{backlog|todo}/{NN}-{name}/spec.md`

## Phase 2: Use Design Document Template

- [ ] Copy template-design.md structure for design documents
- [ ] Include metadata and links to spec.md and constitution.md
- [ ] Document Architecture Decisions (AD-X) with context, options, rationale
- [ ] Define Components with purpose, location, dependencies
- [ ] Create Data Flow diagrams showing transformations
- [ ] Define Data Models with field types and constraints
- [ ] Specify API Endpoints (reference contracts.md, don't redefine)
- [ ] List Files to change (CREATE/MODIFY with scope)
- [ ] Define Testing Strategy (unit, integration)
- [ ] Identify Risks with mitigation
- [ ] Create FR/AD Coverage mapping
- [ ] Save to `.aidocs/features/{status}/{feature}/design.md`

## Phase 3: Use Implementation Plan Template

- [ ] Copy structure for implementation plans
- [ ] Add Overview: total tasks, complexity, estimated tokens, critical path
- [ ] Create Task Summary table: Task, Name, Complexity, Tokens, Dependencies
- [ ] Draw Dependency Graph showing relationships
- [ ] Define Execution Waves for parallel execution
- [ ] List Tasks with detailed objectives and files
- [ ] Define Quality Gates at checkpoints
- [ ] Map FR/AD coverage to tasks
- [ ] Identify risks and mitigations
- [ ] Save to `.aidocs/features/{feature}/implementation-plan.md`

## Phase 4: Use Constitution Template

- [ ] Copy structure for new project constitutions
- [ ] Add Vision: 1-2 sentences on project purpose
- [ ] Define Tech Stack: Language, Framework, Database, Hosting with rationale
- [ ] Document Architecture Patterns used in project
- [ ] Define Code Standards: Naming, Formatting, Testing, Coverage
- [ ] Specify Git Workflow: Branch strategy, commit format, PR requirements
- [ ] Show Project Structure with directory descriptions
- [ ] Define Quality Gates: Lint, Types, Tests, Coverage with criteria
- [ ] List Principles guiding decisions
- [ ] Save to `.aidocs/constitution.md`

## Phase 5: Use Roadmap Template

- [ ] Add Vision: where project is going
- [ ] Define Now (90% confident): detailed, committed features
- [ ] Define Next (70% confident): planned, flexible features
- [ ] Define Later (50% confident): thematic, vision features
- [ ] List Done: completed features with key outcomes
- [ ] Include 20% buffer for unknowns
- [ ] Identify Risks and mitigations
- [ ] Track Metrics and targets
- [ ] Save to `.aidocs/roadmap.md`

## Phase 6: Use Task File Template

- [ ] Copy structure for each TASK_{NNN}_{slug}.md file
- [ ] Include Metadata: Complexity, Effort, Priority
- [ ] Add SDD References to spec, design, plan
- [ ] Document Task Dependency Tree
- [ ] Write Objective: single, clear, measurable
- [ ] List Dependencies with reasons
- [ ] Write Acceptance Criteria (AC-1, AC-2, etc.)
- [ ] Define Technical Approach (steps)
- [ ] List Files to change
- [ ] Estimate token budget
- [ ] Save to `.aidocs/features/{feature}/todo/TASK_{NNN}_{slug}.md`

## Phase 7: Use Backlog Item Template

- [ ] Create for each backlog feature
- [ ] Include Priority (P0-P3), Estimate (points or T-shirt)
- [ ] Write Problem statement
- [ ] List Acceptance Criteria
- [ ] Document Dependencies (requires, blocks)
- [ ] Add Notes for context
- [ ] Save to `.aidocs/backlog/{feature}/README.md`

## Phase 8: Use Confidence Check Template

- [ ] Use before each phase transition
- [ ] Rate confidence: Phase completion 0-100%
- [ ] Check quality, completeness, alignment
- [ ] Document Pass/Warn/Fail status
- [ ] List questions to answer first
- [ ] Recommend actions: Proceed, Clarify, or Stop
- [ ] Use to prevent advancing with gaps

## Phase 9: Maintain Token Estimation Guide

- [ ] Use for sizing TASK components
- [ ] Django model (simple): 5-10k
- [ ] Django model (complex): 15-25k
- [ ] Service class: 20-40k
- [ ] React component (simple): 5-10k
- [ ] React component (complex): 15-30k
- [ ] Test file: 20-40k
- [ ] Total task must be <100k

## Phase 10: Use Pattern & Mistake Records

- [ ] Document successful patterns discovered
- [ ] Document mistakes and solutions
- [ ] Use for project learning
- [ ] Update project memory with findings
- [ ] Help future tasks leverage lessons