# M-LLM-001: Prompt Engineering

## Overview

Prompt engineering is the practice of designing effective instructions for Large Language Models to achieve desired outputs. It covers techniques from basic prompting to advanced patterns like Chain-of-Thought, few-shot learning, and meta-prompting.

**When to use:** Every LLM interaction. This is the foundational skill for working with AI models.

## Core Concepts

### 1. Prompt Anatomy

```
[System Message] - Sets behavior, personality, constraints
[Context] - Background information, documents, data
[Instruction] - What you want the model to do
[Examples] - Few-shot demonstrations (optional)
[Output Format] - Expected structure (JSON, markdown, etc.)
```

### 2. The CRISP Framework

| Element | Description | Example |
|---------|-------------|---------|
| **C**ontext | Background information | "You are a senior Python developer" |
| **R**ole | What persona to adopt | "Act as a code reviewer" |
| **I**nstruction | Clear task directive | "Review this function for bugs" |
| **S**pecifics | Details and constraints | "Focus on error handling" |
| **P**urpose | Why this matters | "This is for production deployment" |

### 3. Prompt Types

| Type | Use Case | Complexity |
|------|----------|------------|
| Zero-shot | Simple, well-defined tasks | Low |
| Few-shot | Tasks needing examples | Medium |
| Chain-of-Thought | Complex reasoning | High |
| Tree-of-Thought | Multi-path exploration | Very High |
| ReAct | Tool use with reasoning | High |

## Best Practices

### 1. Be Specific and Explicit

```markdown
# Bad
"Write code for a user system"

# Good
"Write a Python class called UserManager that:
- Stores users in a dictionary by user_id
- Has methods: create_user(name, email), get_user(user_id), delete_user(user_id)
- Validates email format using regex
- Raises ValueError for invalid inputs
- Include docstrings for all methods"
```

### 2. Use Structured Output

```markdown
Respond in this exact JSON format:
{
  "analysis": "Your analysis here",
  "score": <number 1-10>,
  "recommendations": ["rec1", "rec2", "rec3"],
  "confidence": "<high|medium|low>"
}
```

### 3. Chain-of-Thought Prompting

```markdown
Solve this problem step by step:

1. First, identify the key variables
2. Then, determine the relationships between them
3. Next, apply the relevant formula
4. Finally, calculate and verify the result

Show your reasoning at each step.
```

### 4. Few-Shot Learning

```markdown
Classify the sentiment of product reviews:

Review: "This product exceeded my expectations!"
Sentiment: POSITIVE

Review: "Terrible quality, broke after one day"
Sentiment: NEGATIVE

Review: "It works as described, nothing special"
Sentiment: NEUTRAL

Review: "{{user_review}}"
Sentiment:
```

## Common Patterns

### Pattern 1: Role-Playing

```markdown
You are an expert database architect with 20 years of experience.
You specialize in PostgreSQL optimization and have worked with
systems handling billions of records.

When reviewing database designs, you:
- Prioritize query performance
- Consider data integrity constraints
- Plan for horizontal scaling
- Document your reasoning

Now review this schema: [schema]
```

### Pattern 2: Constraint Stacking

```markdown
Generate a product description that:
- Is exactly 3 sentences
- Uses active voice only
- Mentions the key benefit first
- Ends with a call to action
- Contains no superlatives (best, greatest, etc.)
- Reads at an 8th-grade level
```

### Pattern 3: Self-Correction

```markdown
After generating your response:
1. Review it for accuracy
2. Check for logical errors
3. Verify it follows all constraints
4. If issues found, regenerate with corrections

Output your final answer after self-review.
```

### Pattern 4: Meta-Prompting

```markdown
You are a prompt engineer. Your task is to improve this prompt
to get better results from an LLM:

Original prompt: "{{original_prompt}}"

Improve it by:
- Adding clarity and specificity
- Including output format requirements
- Adding relevant constraints
- Providing an example if helpful

Return the improved prompt.
```

## Anti-patterns

| Anti-pattern | Why It Fails | Better Approach |
|--------------|--------------|-----------------|
| Vague instructions | Ambiguous outputs | Be explicit about every requirement |
| No output format | Unparseable responses | Always specify structure |
| Overloading context | Token waste, confusion | Keep context focused and relevant |
| Ignoring model limits | Truncated outputs | Chunk large tasks |
| No examples for complex tasks | Inconsistent results | Provide 2-3 few-shot examples |

## Advanced Techniques

### 1. Constitutional AI Prompting

```markdown
Before responding, check that your answer:
- Does not contain harmful content
- Is factually accurate to the best of your knowledge
- Acknowledges uncertainty when appropriate
- Respects privacy and confidentiality

If any check fails, revise your response.
```

### 2. Decomposition Prompting

```markdown
Break this complex task into subtasks:

Main task: "Build a user authentication system"

For each subtask:
1. Name and describe it
2. List dependencies
3. Estimate complexity (1-5)
4. Identify potential issues

Then solve each subtask sequentially.
```

### 3. Verification Prompting

```markdown
Generate a solution, then:

1. Create test cases to verify it works
2. Run the test cases mentally
3. Identify any edge cases that fail
4. Fix issues and reverify
5. Only output the verified solution
```

## Tools & References

### Related Skills
- faion-openai-api-skill
- faion-claude-api-skill
- faion-langchain-skill

### Related Agents
- faion-prompt-engineer-agent

### External Resources
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Claude Prompt Design](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [LangChain Prompt Templates](https://python.langchain.com/docs/concepts/prompt_templates/)

## Checklist

### Basic Prompting
- [ ] Clear, specific instruction
- [ ] Role/context defined
- [ ] Output format specified
- [ ] Constraints listed

### Advanced Prompting
- [ ] Few-shot examples (if complex task)
- [ ] Chain-of-thought reasoning (if reasoning needed)
- [ ] Self-verification step (if accuracy critical)
- [ ] Error handling instructions

### Quality Assurance
- [ ] Tested with edge cases
- [ ] Output parseable/usable
- [ ] Consistent across runs
- [ ] Cost-efficient (not over-prompting)

---

*Methodology: M-LLM-001 | Category: LLM/Orchestration*
*Related: faion-prompt-engineer-agent, faion-openai-api-skill, faion-claude-api-skill*
