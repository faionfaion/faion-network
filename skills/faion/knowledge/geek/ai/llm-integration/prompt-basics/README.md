---
id: prompt-basics
name: "Prompt Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: prompt-engineering
---

# Prompt Basics

Core prompt engineering concepts and patterns.

## When to Use

- Any LLM application
- Before considering fine-tuning
- When outputs are inconsistent
- To improve task accuracy
- To control output format
- To reduce hallucinations

## Key Concepts

### Prompt Components

```
┌─────────────────────────────────────────┐
│           SYSTEM PROMPT                  │
│  - Role definition                       │
│  - Behavioral constraints               │
│  - Output format rules                  │
└─────────────────────────────────────────┘
                   │
┌─────────────────▼───────────────────────┐
│           USER PROMPT                    │
│  - Context/Background                    │
│  - Task description                     │
│  - Examples (few-shot)                  │
│  - Input data                           │
│  - Output instructions                  │
└─────────────────────────────────────────┘
```

### Prompt Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Zero-shot | Simple tasks | "Translate to Spanish: Hello" |
| Few-shot | Pattern learning | Examples + task |
| Chain-of-Thought | Complex reasoning | "Let's think step by step" |
| Self-consistency | Reliability | Multiple samples, vote |
| ReAct | Tool use | Reason + Act pattern |

## Implementation

### Basic Prompting Patterns

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class PromptTemplate:
    """Reusable prompt template."""
    system: str
    user_template: str
    examples: List[Dict] = None

    def format(self, **kwargs) -> List[Dict]:
        """Format prompt with variables."""
        messages = [{"role": "system", "content": self.system}]

        # Add examples if few-shot
        if self.examples:
            for ex in self.examples:
                messages.append({"role": "user", "content": ex["input"]})
                messages.append({"role": "assistant", "content": ex["output"]})

        # Add user message
        messages.append({
            "role": "user",
            "content": self.user_template.format(**kwargs)
        })

        return messages

# Zero-shot template
CLASSIFICATION_PROMPT = PromptTemplate(
    system="""You are a sentiment classifier. Classify text as:
- positive
- negative
- neutral

Respond with only the classification.""",
    user_template="Classify: {text}"
)

# Few-shot template
FEW_SHOT_CLASSIFICATION = PromptTemplate(
    system="You are a sentiment classifier. Respond with only: positive, negative, or neutral.",
    user_template="Classify: {text}",
    examples=[
        {"input": "Classify: I love this product!", "output": "positive"},
        {"input": "Classify: This is terrible.", "output": "negative"},
        {"input": "Classify: The product arrived on time.", "output": "neutral"}
    ]
)

# Usage
messages = FEW_SHOT_CLASSIFICATION.format(text="This exceeded my expectations!")
```

### System Prompt Patterns

```python
SYSTEM_PROMPTS = {
    "assistant": """You are a helpful, harmless, and honest AI assistant.

Guidelines:
- Be concise and direct
- Acknowledge uncertainty
- Ask clarifying questions when needed
- Never make up information""",

    "code_expert": """You are an expert software developer with deep knowledge of:
- Python, JavaScript, TypeScript
- System design and architecture
- Testing and debugging

When writing code:
- Include type hints
- Add docstrings
- Handle errors appropriately
- Follow best practices""",

    "data_analyst": """You are a data analyst expert.

When analyzing data:
- Start with summary statistics
- Identify patterns and anomalies
- Provide actionable insights
- Support claims with data
- Use visualizations when helpful""",

    "editor": """You are a professional editor.

When editing text:
- Fix grammar and spelling
- Improve clarity and flow
- Maintain the author's voice
- Suggest structural improvements
- Be constructive, not critical"""
}

def create_system_prompt(
    role: str,
    constraints: List[str] = None,
    output_format: str = None
) -> str:
    """Create a structured system prompt."""
    prompt_parts = [f"You are {role}."]

    if constraints:
        prompt_parts.append("\nConstraints:")
        for c in constraints:
            prompt_parts.append(f"- {c}")

    if output_format:
        prompt_parts.append(f"\nOutput format:\n{output_format}")

    return "\n".join(prompt_parts)

# Example
system = create_system_prompt(
    role="a helpful customer support agent for TechCorp",
    constraints=[
        "Always be polite and professional",
        "If you don't know, say so",
        "Offer to escalate complex issues",
        "Never share internal information"
    ],
    output_format="Respond in a friendly, concise manner. Include relevant links when available."
)
```

### Role-Based Prompting

```python
def create_expert_prompt(
    expertise: str,
    task: str,
    context: str = ""
) -> List[Dict]:
    """Create a prompt with expert persona."""
    system = f"""You are a world-class expert in {expertise}.

Your expertise includes:
- Deep theoretical knowledge
- Practical experience
- Awareness of common pitfalls
- Knowledge of best practices

Provide thorough, accurate, and actionable advice."""

    user = f"Task: {task}"
    if context:
        user = f"Context: {context}\n\n{user}"

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]

# Usage
messages = create_expert_prompt(
    expertise="Python performance optimization",
    task="Review this code for performance issues and suggest improvements",
    context="This function is called 10,000 times per second in production"
)
```

### Structured Output Prompting

```python
import json
from typing import Type
from pydantic import BaseModel

def create_structured_prompt(
    task: str,
    output_schema: Type[BaseModel],
    examples: List[Dict] = None
) -> str:
    """Create prompt for structured JSON output."""
    schema_str = json.dumps(output_schema.model_json_schema(), indent=2)

    prompt = f"""Task: {task}

Output must be valid JSON matching this schema:
```json
{schema_str}
```
"""

    if examples:
        prompt += "\n\nExamples:\n"
        for ex in examples:
            prompt += f"Input: {ex['input']}\nOutput: {json.dumps(ex['output'])}\n\n"

    return prompt

# Example usage
from pydantic import BaseModel, Field
from typing import List

class ProductReview(BaseModel):
    sentiment: str = Field(..., description="positive, negative, or neutral")
    score: float = Field(..., ge=0, le=1, description="Confidence score")
    key_points: List[str] = Field(..., description="Main points from review")
    summary: str = Field(..., description="One sentence summary")

prompt = create_structured_prompt(
    task="Analyze this product review and extract structured information",
    output_schema=ProductReview,
    examples=[
        {
            "input": "Great product! Fast delivery.",
            "output": {
                "sentiment": "positive",
                "score": 0.95,
                "key_points": ["Product quality", "Fast delivery"],
                "summary": "Customer satisfied with product and delivery speed."
            }
        }
    ]
)
```

## Best Practices

1. **Be Specific**
   - Clear task description
   - Explicit output format
   - Include constraints

2. **Use Examples**
   - Show desired output format
   - Cover edge cases
   - Quality over quantity

3. **Structure Matters**
   - Use delimiters for clarity
   - Separate instruction from content
   - Organize complex prompts

4. **Iterate and Test**
   - Start simple, add complexity
   - Test with diverse inputs
   - Track prompt versions

5. **Manage Prompts**
   - Version control prompts
   - Document purpose and usage
   - Create reusable templates

## Common Pitfalls

1. **Vague Instructions** - Ambiguous tasks lead to inconsistent outputs
2. **No Output Format** - Model guesses desired format
3. **Too Many Examples** - Confuses more than helps
4. **Implicit Assumptions** - Model may not share your assumptions
5. **No Edge Cases** - Fails on unusual inputs
6. **Prompt Injection** - User input manipulates behavior

## References

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- See also: [prompt-techniques.md](prompt-techniques.md)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| System prompt creation | sonnet | Prompt engineering |
| Role definition | haiku | Template application |
| Instruction clarity | sonnet | Writing quality review |
