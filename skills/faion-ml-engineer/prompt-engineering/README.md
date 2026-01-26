# Prompt Engineering

Practical guide to designing effective prompts for Large Language Models.

## What is Prompt Engineering?

Prompt engineering is the practice of crafting inputs to LLMs that reliably produce desired outputs. It encompasses:

- **Instruction design** - Structuring tasks clearly
- **Context management** - Providing relevant background
- **Output control** - Specifying format and constraints
- **Evaluation** - Testing and iterating on prompts

## When to Use

| Scenario | Why Prompt Engineering Helps |
|----------|------------------------------|
| Inconsistent outputs | Structured prompts improve reliability |
| Wrong format | Output specifications guide the model |
| Missing context | Background info improves accuracy |
| Complex reasoning | Chain-of-thought enables step-by-step |
| Tool integration | Function calling schemas guide actions |
| Production systems | Tested prompts reduce failures |

## When NOT to Use

| Scenario | Better Alternative |
|----------|-------------------|
| Model lacks capability | Fine-tuning or different model |
| Requires real-time data | RAG with retrieval |
| Domain-specific knowledge | Fine-tuning with domain data |
| Consistent structured output | Structured output mode / JSON schema |
| Complex multi-step workflows | Agent framework (LangChain, etc.) |
| Cost is primary concern | Smaller model + fine-tuning |

## Key Concepts

### Prompt Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **System prompt** | Role, constraints, behavior | "You are a helpful coding assistant..." |
| **Context** | Background information | Document content, conversation history |
| **Task** | What to do | "Summarize the following text" |
| **Examples** | Few-shot learning | Input-output pairs |
| **Output format** | Structure specification | JSON schema, markdown template |
| **Constraints** | Limitations and rules | "Under 100 words", "No speculation" |

### Prompting Techniques

| Technique | Use Case | Complexity |
|-----------|----------|------------|
| **Zero-shot** | Simple, well-defined tasks | Low |
| **Few-shot** | Pattern learning, formatting | Low-Medium |
| **Chain-of-Thought (CoT)** | Complex reasoning, math | Medium |
| **Self-Consistency** | Reliability improvement | Medium |
| **ReAct** | Tool use, information gathering | High |
| **Tree-of-Thought (ToT)** | Exploration, planning | High |
| **Meta-prompting** | Abstract problem solving | High |

### Model-Specific Considerations

| Model | Best Practices |
|-------|---------------|
| **Claude** | XML tags (`<context>`, `<task>`), think step-by-step, explicit instructions |
| **GPT-4** | Hashtags, numbered lists, delimiter-separated sections |
| **Gemini** | Hierarchical structure, outline format, multimodal context |
| **Local (Ollama)** | Shorter prompts, explicit formatting, temperature tuning |

## Terminology

| Term | Definition |
|------|------------|
| **Prompt** | Input text sent to an LLM |
| **System prompt** | Instructions that define model behavior |
| **User prompt** | The actual query or task |
| **Assistant message** | Model's response |
| **Few-shot** | Including examples in the prompt |
| **Zero-shot** | No examples, just instructions |
| **Chain-of-Thought (CoT)** | Encouraging step-by-step reasoning |
| **Prompt injection** | Malicious input that alters behavior |
| **Jailbreak** | Bypassing model safety constraints |
| **Hallucination** | Model generating false information |
| **Grounding** | Anchoring responses to provided facts |
| **Temperature** | Randomness in output (0 = deterministic) |
| **Token** | Unit of text (roughly 4 characters in English) |
| **Context window** | Maximum tokens model can process |

## LLM Usage Tips

### How Claude Can Help with Prompt Engineering

**1. Prompt Analysis and Improvement**
```
Analyze this prompt and suggest improvements:
[paste prompt]

Consider: clarity, specificity, potential edge cases, output format
```

**2. Generating Few-Shot Examples**
```
Create 3 diverse examples for this task:
Task: [description]
Input format: [format]
Output format: [format]

Make examples cover edge cases and different scenarios.
```

**3. Testing Prompt Variations**
```
I have this prompt: [prompt]

Generate 3 variations that might perform better:
1. More specific version
2. With chain-of-thought
3. With explicit constraints
```

**4. Debugging Failures**
```
My prompt produces wrong outputs:

Prompt: [prompt]
Expected: [expected output]
Actual: [actual output]

What's wrong and how to fix it?
```

**5. Converting Tasks to Prompts**
```
Convert this task to an effective prompt:
Task: [describe task]
Input: [describe input]
Output: [describe desired output]
Constraints: [any requirements]
```

### Prompt Engineering Workflow

```
1. Define task clearly
   |
2. Write initial prompt (zero-shot)
   |
3. Test with diverse inputs
   |
4. Identify failure modes
   |
5. Add examples, CoT, or constraints
   |
6. Test again
   |
7. Document final prompt
```

## Security Considerations

### Prompt Injection Prevention

| Risk | Mitigation |
|------|------------|
| Direct injection | Input validation, delimiters |
| Indirect injection | Separate data from instructions |
| Jailbreaking | System prompt hardening |
| Data exfiltration | Output filtering, rate limiting |

### Best Practices

- Clearly separate user input from instructions
- Use XML tags or delimiters to mark boundaries
- Validate and sanitize user inputs
- Implement output filtering for sensitive data
- Monitor for unusual patterns
- Keep humans in the loop for critical actions

## Quality Metrics

| Metric | What It Measures | When to Use |
|--------|------------------|-------------|
| **Task completion** | Did output achieve goal? | All tasks |
| **Accuracy** | Correctness of information | Factual tasks |
| **Relevance** | Output matches request | Open-ended tasks |
| **Format compliance** | Follows specified format | Structured output |
| **Consistency** | Same input = similar output | Production systems |
| **Latency** | Response time | Real-time applications |
| **Token efficiency** | Tokens used for output | Cost optimization |

## External Resources

### Official Documentation

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google AI Prompt Design Guide](https://ai.google.dev/docs/prompt_best_practices)
- [Claude XML Tags Guide](https://docs.anthropic.com/en/docs/use-xml-tags)

### Community Resources

- [Prompt Engineering Guide](https://www.promptingguide.ai/) - Comprehensive techniques reference
- [Lakera Prompt Engineering Guide](https://www.lakera.ai/blog/prompt-engineering-guide) - Security-focused guide
- [LangChain Hub](https://smith.langchain.com/hub) - Community prompt templates
- [Awesome LLM JSON](https://github.com/imaurer/awesome-llm-json) - Structured output resources

### Research Papers

- [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903)
- [Self-Consistency (Wang et al., 2022)](https://arxiv.org/abs/2203.11171)
- [ReAct: Reasoning and Acting (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)
- [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601)

### Security Resources

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [Microsoft Prompt Injection Defense](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks)
- [IBM Prompt Injection Prevention](https://www.ibm.com/think/insights/prevent-prompt-injection)

### Evaluation Tools

- [DeepEval](https://github.com/confident-ai/deepeval) - LLM evaluation framework
- [Confident AI Evaluation Metrics Guide](https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation)
- [Braintrust Evaluation Guide](https://www.braintrust.dev/articles/llm-evaluation-metrics-guide)

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step checklists |
| [examples.md](examples.md) | Real-world examples and patterns |
| [templates.md](templates.md) | Copy-paste prompt templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted work |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-llm-integration](../faion-llm-integration/CLAUDE.md) | API implementation |
| [faion-rag-engineer](../faion-rag-engineer/CLAUDE.md) | RAG prompt patterns |
| [faion-ai-agents](../faion-ai-agents/CLAUDE.md) | Agent prompting |
