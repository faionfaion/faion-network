# Terraform Modules LLM Prompts

Prompts for AI-assisted module development, review, and troubleshooting.

---

## Module Generation

### Generate Complete Module

```
Create a Terraform module for [RESOURCE_TYPE] with the following requirements:

Resource: [e.g., AWS ECS Fargate service]
Provider: [e.g., AWS]
Features:
- [Feature 1]
- [Feature 2]
- [Feature 3]

Include:
1. main.tf with all resources
2. variables.tf with validations and descriptions
3. outputs.tf with useful exports
4. versions.tf with version constraints
5. README.md with usage example

Follow best practices:
- Single responsibility principle
- Sensible defaults
- Input validation
- Proper tagging
- No hardcoded values
```

### Generate Module from Existing Resources

```
Convert these existing Terraform resources into a reusable module:

[PASTE EXISTING TERRAFORM CODE]

Requirements:
1. Extract configurable values as variables
2. Add variable descriptions and validations
3. Create meaningful outputs
4. Add proper tagging support
5. Maintain all existing functionality
6. Follow module best practices
```

### Generate Child Module

```
Create a child module for [COMPONENT] that will be called by a parent [PARENT_MODULE] module.

Parent module provides:
- [Input 1]
- [Input 2]

Child module should:
- [Responsibility 1]
- [Responsibility 2]

Output values needed by parent:
- [Output 1]
- [Output 2]
```

---

## Module Review

### Security Review

```
Review this Terraform module for security issues:

[PASTE MODULE CODE]

Check for:
1. Hardcoded secrets or credentials
2. Overly permissive IAM policies
3. Missing encryption settings
4. Public network exposure
5. Missing logging/monitoring
6. Security group misconfigurations

Provide:
- List of issues found
- Severity rating for each
- Recommended fixes with code examples
```

### Best Practices Review

```
Review this Terraform module against best practices:

[PASTE MODULE CODE]

Evaluate:
1. Single responsibility principle
2. Variable naming and descriptions
3. Output completeness
4. Validation rules
5. Tagging strategy
6. Documentation quality
7. Version constraints
8. Code organization

Provide:
- Score out of 10 for each category
- Specific improvements with examples
- Priority ranking of changes
```

### Performance Review

```
Review this Terraform module for performance and cost optimization:

[PASTE MODULE CODE]

Analyze:
1. Resource sizing (over/under-provisioned)
2. Cost optimization opportunities
3. State management efficiency
4. Apply/plan performance
5. Resource dependencies

Provide:
- Cost estimation insights
- Optimization recommendations
- Performance improvements
```

---

## Refactoring

### Split Mega-Module

```
This module is too large. Split it into smaller, focused modules:

[PASTE LARGE MODULE CODE]

Requirements:
1. Identify logical boundaries
2. Create separate modules for each concern
3. Define clear interfaces between modules
4. Maintain backward compatibility
5. Minimize cross-module dependencies

Output:
- Recommended module structure
- Interface definitions (inputs/outputs)
- Migration path from current state
```

### Add Validation

```
Add comprehensive validation to this module's variables:

[PASTE VARIABLES.TF]

Add validations for:
1. Format constraints (CIDR, ARN, etc.)
2. Length limits
3. Allowed values
4. Conditional requirements
5. Cross-variable validation

Example output format:
\`\`\`hcl
variable "example" {
  validation {
    condition     = ...
    error_message = "..."
  }
}
\`\`\`
```

### Modernize Module

```
Modernize this Terraform module to use current best practices:

[PASTE LEGACY MODULE CODE]

Updates needed:
1. Replace count with for_each where appropriate
2. Use moved blocks for refactoring
3. Add lifecycle rules
4. Update to latest provider features
5. Add terraform test support
6. Improve error messages

Maintain backward compatibility where possible.
```

---

## Troubleshooting

### Debug Module Error

```
I'm getting this error when using a Terraform module:

Error message:
[PASTE ERROR]

Module code:
[PASTE RELEVANT CODE]

Usage:
[PASTE HOW MODULE IS CALLED]

Please:
1. Explain the error
2. Identify the root cause
3. Provide a fix
4. Suggest prevention strategies
```

### State Issues

```
I have a state-related issue with my module:

Issue: [DESCRIBE ISSUE]
- Resources showing as changed when they shouldn't
- State drift between environments
- Import/migration problems

Current state snippet:
[PASTE RELEVANT STATE]

Module code:
[PASTE CODE]

Help me:
1. Understand what's happening
2. Fix the immediate issue
3. Prevent future occurrences
```

### Dependency Problems

```
I have circular or incorrect dependencies in my modules:

Error/behavior:
[DESCRIBE ISSUE]

Module structure:
[DESCRIBE OR SHOW STRUCTURE]

Please:
1. Identify the dependency problem
2. Suggest restructuring
3. Show how to break circular dependencies
4. Recommend best practices for module dependencies
```

---

## Documentation

### Generate Module Docs

```
Generate comprehensive documentation for this Terraform module:

[PASTE COMPLETE MODULE CODE]

Include:
1. Overview and purpose
2. Architecture diagram (ASCII or description)
3. Prerequisites
4. Usage examples (basic and advanced)
5. Input reference table
6. Output reference table
7. Notes and caveats
8. Changelog template

Format: Markdown compatible with terraform-docs
```

### Generate ADR

```
Create an Architecture Decision Record for this module design:

Module: [MODULE NAME]
Purpose: [PURPOSE]
Key decisions made:
- [Decision 1]
- [Decision 2]

ADR should include:
1. Title
2. Status
3. Context
4. Decision
5. Consequences
6. Alternatives considered
```

---

## Testing

### Generate Tests

```
Generate terraform test files for this module:

[PASTE MODULE CODE]

Create tests for:
1. Basic creation (plan succeeds)
2. All required variables
3. Variable validation rules
4. Expected outputs
5. Idempotency (apply twice = no changes)

Use terraform test (.tftest.hcl) format.
```

### Generate Terratest

```
Generate Terratest (Go) tests for this module:

[PASTE MODULE CODE]

Include:
1. Setup and teardown
2. Basic deployment test
3. Validation of outputs
4. Integration verification
5. Cleanup handling

Provide complete Go test file.
```

---

## Migration

### Migrate from Resources to Module

```
Help me migrate from inline resources to a module:

Current code:
[PASTE CURRENT RESOURCES]

Goals:
1. Create reusable module
2. Migrate state without recreation
3. Maintain all functionality

Provide:
1. New module code
2. State migration commands
3. Root module changes
4. Verification steps
```

### Migrate Module Version

```
Help me migrate from module version X to version Y:

Current usage:
[PASTE CURRENT MODULE CALL]

Changes in new version:
- [BREAKING CHANGE 1]
- [NEW FEATURE 1]
- [DEPRECATION 1]

Provide:
1. Updated module call
2. Required variable changes
3. State migration if needed
4. Testing checklist
```

---

## Composition

### Design Module Architecture

```
Design a module architecture for this infrastructure:

Requirements:
[DESCRIBE INFRASTRUCTURE NEEDS]

Constraints:
- [Constraint 1]
- [Constraint 2]

Provide:
1. Module hierarchy diagram
2. Module responsibilities
3. Interface definitions
4. Dependency graph
5. Recommended file structure
```

### Create Wrapper Module

```
Create a wrapper/facade module that combines these existing modules:

Modules to wrap:
- [Module 1]
- [Module 2]
- [Module 3]

Wrapper should:
1. Simplify common use cases
2. Provide sensible defaults
3. Expose only necessary inputs
4. Aggregate useful outputs

Show complete wrapper module code.
```

---

## Cost Optimization

### Analyze Module Costs

```
Analyze the cost implications of this module:

[PASTE MODULE CODE]

Default configuration:
[PASTE TFVARS OR DEFAULTS]

Provide:
1. Estimated monthly cost breakdown
2. Cost drivers identification
3. Optimization opportunities
4. Cost vs. reliability tradeoffs
5. Recommendations by environment (dev/staging/prod)
```

### Generate Cost-Optimized Variant

```
Create a cost-optimized variant of this module for development environments:

[PASTE PRODUCTION MODULE]

Optimizations to consider:
1. Smaller instance sizes
2. Single AZ deployment
3. Reduced redundancy
4. Spot instances where applicable
5. Shorter retention periods

Maintain functional parity while minimizing costs.
```

---

*Terraform Modules LLM Prompts*
*Part of faion-infrastructure-engineer skill*
