<!-- purpose: Hierarchical WBS outline with PM + all mandatory overhead branches. -->
<!-- consumes: SOW + glossary + (optional) architecture sketch -->
<!-- produces: items[] of the WBS spec; 1:1 conversion to YAML/JSON -->
<!-- depends-on: content/01-core-rules.xml#mandatory-overhead-branches, deliverable-orientation -->
<!-- token-budget-impact: ~170 tokens -->

# WBS — [Project Name]

## 1 Project Management
- 1.1 Planning Documentation
- 1.2 Status Reporting
- 1.3 Risk Management
- 1.4 Change Control

## 2 Requirements
- 2.1 User Research
  - 2.1.1 [Work Package — noun]
  - 2.1.2 [Work Package — noun]
- 2.2 Requirement Documentation
  - 2.2.1 [Work Package — noun]

## 3 [Major Deliverable — noun]
- 3.1 [Sub-deliverable — noun]
- 3.2 [Sub-deliverable — noun]

## 4 Quality Assurance
- 4.1 Unit Test Suite
- 4.2 Integration Test Suite
- 4.3 User Acceptance Test Pack

## 5 Deployment
- 5.1 Environment Setup
- 5.2 Release Package
- 5.3 Monitoring Wiring

## 6 Documentation
- 6.1 User Guide
- 6.2 Admin Guide

## 7 Training
- 7.1 User Training Materials
- 7.2 Admin Training

## 8 Transition
- 8.1 Operations Handover
- 8.2 Documentation Archive

<!--
Rules:
- Every node is a noun phrase (output). No "Build/Design/Test/...".
- All six overhead branches present.
- Append-only IDs; max depth 4; balanced sibling depth.
-->
