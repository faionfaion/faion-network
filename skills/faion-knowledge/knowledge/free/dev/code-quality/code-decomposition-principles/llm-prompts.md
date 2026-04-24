# LLM Prompts

Prompts for AI-assisted work using this methodology.

## Overview

Effective prompts for Claude, GPT, and other LLMs when applying this methodology.

## Prompt Categories

### Analysis Prompts

```
Analyze this [code/design/architecture] using [methodology name].
Focus on:
- [Key aspect 1]
- [Key aspect 2]
- [Key aspect 3]

Provide specific recommendations for improvement.
```

### Implementation Prompts

```
Implement [feature/component] following [methodology name].

Requirements:
- [Requirement 1]
- [Requirement 2]

Constraints:
- [Constraint 1]
- [Constraint 2]

Follow patterns from [specific section of README].
```

### Review Prompts

```
Review this implementation against [methodology name] principles.

Check for:
- Adherence to key principles
- Common anti-patterns
- Improvement opportunities
- Best practice violations

Provide actionable feedback.
```

### Refactoring Prompts

```
Refactor this code to follow [methodology name].

Current issues:
- [Issue 1]
- [Issue 2]

Target state:
- [Goal 1]
- [Goal 2]

Maintain backward compatibility where possible.
```

### Documentation Prompts

```
Document this [code/design] using [methodology name] standards.

Include:
- Purpose and rationale
- Key design decisions
- Usage examples
- Integration points

Target audience: [developers/architects/stakeholders]
```

## Prompt Engineering Tips

### Be Specific

```
BAD: "Make this better"
GOOD: "Refactor to follow Single Responsibility Principle, extracting order validation logic"
```

### Provide Context

```
Include:
- Current state
- Desired outcome
- Constraints
- Relevant methodology sections
```

### Request Explanations

```
"Explain your reasoning at each step"
"Document trade-offs considered"
"Cite specific methodology principles"
```

### Iterative Refinement

```
1. Start with high-level analysis
2. Drill into specific areas
3. Request alternatives
4. Compare approaches
5. Refine based on feedback
```

## LLM-Specific Notes

### Claude

- Excels at explaining trade-offs
- Good at following structured methodologies
- Request step-by-step reasoning

### GPT-4

- Strong at code generation
- Good at pattern recognition
- Use for template creation

### Specialized Models

- Codex: Code-focused tasks
- Copilot: In-editor assistance
- Context-specific tools as available

## Workflow Integration

### IDE Integration

```
# VS Code with Copilot
1. Write comment describing intent
2. Reference methodology in comment
3. Let AI suggest implementation
4. Review against checklist
```

### Command-Line Workflow

```
# Using Claude Code or similar
faion apply [methodology] [file/directory]
faion review [methodology] [file/directory]
faion explain [methodology] [concept]
```

## Quality Checks

After AI-assisted work:

- [ ] Verify methodology principles followed
- [ ] Check for anti-patterns
- [ ] Validate against examples
- [ ] Review with checklist
- [ ] Test implementation
- [ ] Update documentation

## References

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- Methodology-specific prompting patterns
- Team prompt library (if available)
