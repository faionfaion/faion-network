---
id: prompt-techniques
name: "Advanced Prompt Techniques"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: prompt-engineering
---

# Advanced Prompt Techniques

Advanced prompting patterns, testing, and management strategies.

## Delimiting and Formatting

```python
def format_with_delimiters(
    instruction: str,
    content: str,
    delimiter: str = "```"
) -> str:
    """Format prompt with clear delimiters."""
    return f"""{instruction}

{delimiter}
{content}
{delimiter}"""

def format_with_xml_tags(
    instruction: str,
    **sections
) -> str:
    """Format prompt with XML-style tags."""
    prompt = instruction + "\n\n"

    for tag, content in sections.items():
        prompt += f"<{tag}>\n{content}\n</{tag}>\n\n"

    return prompt

# Example
prompt = format_with_xml_tags(
    "Summarize the document and answer the question.",
    document="This is a long document about AI...",
    question="What are the main benefits of AI?",
    format="Provide a 2-3 sentence summary followed by a direct answer."
)
```

## Meta-Prompting

```python
def generate_prompt(
    task_description: str,
    client,  # OpenAI client
    model: str = "gpt-4o"
) -> str:
    """Use LLM to generate an effective prompt."""
    meta_prompt = """You are a prompt engineering expert. Create an effective prompt for the following task.

The prompt should:
1. Be clear and specific
2. Include relevant context
3. Specify output format
4. Include examples if helpful
5. Handle edge cases

Task: {task}

Generate only the prompt, no explanation."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": meta_prompt.format(task=task_description)}
        ]
    )

    return response.choices[0].message.content

def optimize_prompt(
    original_prompt: str,
    failure_cases: List[Dict],
    client,
    model: str = "gpt-4o"
) -> str:
    """Improve prompt based on failure cases."""
    meta_prompt = f"""Analyze this prompt and its failure cases, then create an improved version.

Original prompt:
{original_prompt}

Failure cases:
{json.dumps(failure_cases, indent=2)}

Create an improved prompt that addresses these failures while maintaining the original intent."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": meta_prompt}]
    )

    return response.choices[0].message.content
```

## Prompt Chaining

```python
from typing import List, Callable

class PromptChain:
    """Chain multiple prompts together."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model
        self.steps: List[Callable] = []

    def add_step(self, prompt_func: Callable):
        """Add a step to the chain."""
        self.steps.append(prompt_func)
        return self

    def run(self, initial_input: str) -> Dict:
        """Execute the chain."""
        current_input = initial_input
        results = {"steps": []}

        for i, step_func in enumerate(self.steps):
            prompt = step_func(current_input)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )

            output = response.choices[0].message.content

            results["steps"].append({
                "step": i + 1,
                "input": current_input[:100],
                "output": output
            })

            current_input = output

        results["final_output"] = current_input
        return results

# Usage
def step1_extract(text):
    return f"Extract the main entities from this text: {text}"

def step2_categorize(entities):
    return f"Categorize these entities by type: {entities}"

def step3_summarize(categories):
    return f"Create a brief summary of these categorized entities: {categories}"

chain = PromptChain(client, "gpt-4o")
chain.add_step(step1_extract)
chain.add_step(step2_categorize)
chain.add_step(step3_summarize)

result = chain.run("Apple announced a new iPhone with advanced AI features...")
```

## Prompt Library

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional

class PromptCategory(Enum):
    CLASSIFICATION = "classification"
    GENERATION = "generation"
    EXTRACTION = "extraction"
    TRANSFORMATION = "transformation"
    ANALYSIS = "analysis"

@dataclass
class ManagedPrompt:
    name: str
    category: PromptCategory
    system: str
    template: str
    examples: Optional[List[Dict]] = None
    version: str = "1.0"
    description: str = ""

class PromptLibrary:
    """Centralized prompt management."""

    def __init__(self):
        self.prompts: Dict[str, ManagedPrompt] = {}

    def register(self, prompt: ManagedPrompt):
        """Register a prompt."""
        self.prompts[prompt.name] = prompt

    def get(self, name: str) -> ManagedPrompt:
        """Retrieve a prompt."""
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' not found")
        return self.prompts[name]

    def format(self, name: str, **kwargs) -> List[Dict]:
        """Format a prompt with variables."""
        prompt = self.get(name)
        messages = [{"role": "system", "content": prompt.system}]

        if prompt.examples:
            for ex in prompt.examples:
                messages.append({"role": "user", "content": ex["input"]})
                messages.append({"role": "assistant", "content": ex["output"]})

        messages.append({
            "role": "user",
            "content": prompt.template.format(**kwargs)
        })

        return messages

# Initialize library
library = PromptLibrary()

# Register prompts
library.register(ManagedPrompt(
    name="sentiment_analysis",
    category=PromptCategory.CLASSIFICATION,
    system="You are a sentiment analysis expert. Respond with only: positive, negative, or neutral.",
    template="Analyze the sentiment: {text}",
    examples=[
        {"input": "Analyze the sentiment: I love it!", "output": "positive"},
        {"input": "Analyze the sentiment: This is awful.", "output": "negative"}
    ],
    version="1.2",
    description="Classify text sentiment into three categories"
))

# Usage
messages = library.format("sentiment_analysis", text="The product works as expected.")
```

## Prompt Testing

```python
from typing import List, Dict, Callable
import json

class PromptTester:
    """Test prompts against expected outputs."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def test_prompt(
        self,
        prompt_messages: List[Dict],
        test_cases: List[Dict],
        evaluator: Callable[[str, str], bool] = None
    ) -> Dict:
        """Test a prompt against multiple cases."""
        results = {
            "passed": 0,
            "failed": 0,
            "cases": []
        }

        for case in test_cases:
            # Build messages with test input
            messages = prompt_messages.copy()
            messages[-1]["content"] = messages[-1]["content"].format(**case["input"])

            # Get response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            actual = response.choices[0].message.content

            # Evaluate
            expected = case["expected"]
            if evaluator:
                passed = evaluator(actual, expected)
            else:
                passed = expected.lower() in actual.lower()

            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1

            results["cases"].append({
                "input": case["input"],
                "expected": expected,
                "actual": actual,
                "passed": passed
            })

        results["accuracy"] = results["passed"] / len(test_cases)
        return results

# Usage
tester = PromptTester(client)
messages = library.format("sentiment_analysis", text="{text}")

test_cases = [
    {"input": {"text": "I absolutely love this!"}, "expected": "positive"},
    {"input": {"text": "This is the worst."}, "expected": "negative"},
    {"input": {"text": "It arrived on Tuesday."}, "expected": "neutral"},
]

results = tester.test_prompt(messages, test_cases)
print(f"Accuracy: {results['accuracy']:.2%}")
```

## Advanced Techniques

### Prompt Versioning

```python
@dataclass
class VersionedPrompt:
    """Prompt with version control."""
    name: str
    version: str
    prompt: str
    changelog: List[str]
    created_at: datetime
    tested_accuracy: float = 0.0

    def bump_version(self, change_description: str):
        """Increment version and log change."""
        major, minor, patch = map(int, self.version.split('.'))
        self.version = f"{major}.{minor}.{patch + 1}"
        self.changelog.append(f"v{self.version}: {change_description}")
```

### Prompt A/B Testing

```python
class PromptABTest:
    """Compare two prompt variants."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def compare(
        self,
        prompt_a: List[Dict],
        prompt_b: List[Dict],
        test_cases: List[Dict],
        evaluator: Callable
    ) -> Dict:
        """Compare two prompts."""
        results_a = self.test_prompt(prompt_a, test_cases, evaluator)
        results_b = self.test_prompt(prompt_b, test_cases, evaluator)

        return {
            "prompt_a": {
                "accuracy": results_a["accuracy"],
                "passed": results_a["passed"]
            },
            "prompt_b": {
                "accuracy": results_b["accuracy"],
                "passed": results_b["passed"]
            },
            "winner": "a" if results_a["accuracy"] > results_b["accuracy"] else "b"
        }
```

## References

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- See also: [prompt-basics.md](prompt-basics.md)
