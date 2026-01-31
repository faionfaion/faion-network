# LLM Prompts

AI prompts for applying this methodology with language models.

## Core Prompts

### Prompt 1: [Purpose]

```
You are an expert in [methodology]. Your task is to [specific goal].

Context:
- [Context point 1]
- [Context point 2]

Requirements:
- [Requirement 1]
- [Requirement 2]

Please provide [expected output].
```

### Prompt 2: [Purpose]

```
[Prompt content]
```

## Specialized Prompts

### Analysis Prompt

```
Analyze the following [artifact] using [methodology]:

[Input placeholder]

Provide:
1. [Analysis aspect 1]
2. [Analysis aspect 2]
3. Recommendations
```

### Validation Prompt

```
Validate this [artifact] against [methodology] criteria:

[Input placeholder]

Check for:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

## Prompt Chains

For complex tasks, chain these prompts:

1. **Step 1**: Use [Prompt X] to [goal]
2. **Step 2**: Feed output to [Prompt Y] for [goal]
3. **Step 3**: Finalize with [Prompt Z]

## Tips

- Adjust specificity based on task complexity
- Include relevant context from project
- Use examples to guide LLM output format
