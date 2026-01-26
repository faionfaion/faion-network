# AI Agent Patterns Examples

Code examples for implementing each agent design pattern.

---

## ReAct Pattern

### Basic ReAct Loop (Python)

```python
from typing import Callable

class ReActAgent:
    def __init__(self, llm: Callable, tools: dict, max_iterations: int = 10):
        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations

    def run(self, task: str) -> str:
        history = []

        for i in range(self.max_iterations):
            # Generate thought and action
            prompt = self._build_prompt(task, history)
            response = self.llm(prompt)

            thought, action, action_input = self._parse_response(response)
            history.append(f"Thought: {thought}")
            history.append(f"Action: {action}[{action_input}]")

            # Check for final answer
            if action == "finish":
                return action_input

            # Execute action and observe
            if action in self.tools:
                observation = self.tools[action](action_input)
            else:
                observation = f"Error: Unknown action '{action}'"

            history.append(f"Observation: {observation}")

        return "Max iterations reached without conclusion"

    def _build_prompt(self, task: str, history: list) -> str:
        return f"""Task: {task}

Available actions: {list(self.tools.keys())} + ["finish"]

{chr(10).join(history)}

Respond with:
Thought: <your reasoning>
Action: <action_name>[<input>]"""

    def _parse_response(self, response: str) -> tuple:
        # Parse thought, action, and input from response
        # Implementation depends on output format
        ...
```

### ReAct with LangChain

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

# Define tools
tools = [
    Tool(
        name="search",
        func=lambda q: search_api(q),
        description="Search the web for current information"
    ),
    Tool(
        name="calculate",
        func=lambda expr: eval(expr),  # Use safe evaluator in production
        description="Perform mathematical calculations"
    )
]

# Create agent
llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, tools, prompt_template)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run
result = executor.invoke({"input": "What is the population of Tokyo times 2?"})
```

---

## Chain-of-Thought Pattern

### Zero-Shot CoT

```python
def zero_shot_cot(llm: Callable, question: str) -> str:
    prompt = f"""{question}

Let's think step by step."""

    return llm(prompt)
```

### Few-Shot CoT

```python
def few_shot_cot(llm: Callable, question: str) -> str:
    examples = """
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
Each can has 3 tennis balls. How many tennis balls does he have now?
A: Roger started with 5 balls.
2 cans of 3 tennis balls each is 2 * 3 = 6 tennis balls.
5 + 6 = 11.
The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 to make lunch and
bought 6 more, how many apples do they have?
A: The cafeteria started with 23 apples.
They used 20, so they have 23 - 20 = 3.
They bought 6 more, so they have 3 + 6 = 9.
The answer is 9.
"""

    prompt = f"""{examples}

Q: {question}
A:"""

    return llm(prompt)
```

### Self-Consistency CoT

```python
from collections import Counter

def self_consistency_cot(llm: Callable, question: str, n_samples: int = 5) -> str:
    answers = []

    for _ in range(n_samples):
        response = zero_shot_cot(llm, question)
        answer = extract_final_answer(response)
        answers.append(answer)

    # Return most common answer
    counter = Counter(answers)
    return counter.most_common(1)[0][0]
```

---

## Tool Use Pattern

### OpenAI Function Calling

```python
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and country"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

def run_with_tools(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # Handle tool calls
    if message.tool_calls:
        messages.append(message)

        for tool_call in message.tool_calls:
            result = execute_tool(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

        # Get final response
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

    return response.choices[0].message.content
```

### Claude Tool Use

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_stock_price",
        "description": "Get current stock price for a ticker symbol",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., AAPL)"
                }
            },
            "required": ["ticker"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's Apple's stock price?"}]
)

# Handle tool use in response
for block in response.content:
    if block.type == "tool_use":
        result = execute_tool(block.name, block.input)
        # Continue conversation with tool result
```

---

## Plan-Execute Pattern

### Basic Plan-Execute

```python
class PlanExecuteAgent:
    def __init__(self, planner_llm, executor_llm):
        self.planner = planner_llm
        self.executor = executor_llm

    def run(self, objective: str) -> str:
        # Step 1: Create plan
        plan = self._create_plan(objective)

        # Step 2: Execute each step
        results = []
        for step in plan:
            result = self._execute_step(step, results)
            results.append({"step": step, "result": result})

            # Check if replanning needed
            if self._needs_replan(step, result):
                plan = self._replan(objective, results)

        # Step 3: Synthesize final output
        return self._synthesize(objective, results)

    def _create_plan(self, objective: str) -> list:
        prompt = f"""Create a step-by-step plan to accomplish:
{objective}

Return as numbered list:
1. First step
2. Second step
..."""

        response = self.planner(prompt)
        return self._parse_plan(response)

    def _execute_step(self, step: str, previous_results: list) -> str:
        context = "\n".join([
            f"Step: {r['step']}\nResult: {r['result']}"
            for r in previous_results
        ])

        prompt = f"""Previous work:
{context}

Current step: {step}

Execute this step and provide the result."""

        return self.executor(prompt)
```

### LangGraph Plan-Execute

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated

class PlanExecuteState(TypedDict):
    objective: str
    plan: list[str]
    current_step: int
    results: list[str]
    final_output: str

def create_plan(state: PlanExecuteState) -> PlanExecuteState:
    plan = planner_llm.invoke(state["objective"])
    return {"plan": plan.steps, "current_step": 0, "results": []}

def execute_step(state: PlanExecuteState) -> PlanExecuteState:
    current = state["plan"][state["current_step"]]
    result = executor_llm.invoke(current, context=state["results"])

    return {
        "results": state["results"] + [result],
        "current_step": state["current_step"] + 1
    }

def should_continue(state: PlanExecuteState) -> str:
    if state["current_step"] >= len(state["plan"]):
        return "synthesize"
    return "execute"

# Build graph
workflow = StateGraph(PlanExecuteState)
workflow.add_node("plan", create_plan)
workflow.add_node("execute", execute_step)
workflow.add_node("synthesize", synthesize_output)

workflow.set_entry_point("plan")
workflow.add_edge("plan", "execute")
workflow.add_conditional_edges("execute", should_continue)
workflow.add_edge("synthesize", END)

agent = workflow.compile()
```

---

## Reflection Pattern

### Basic Reflection Loop

```python
class ReflectionAgent:
    def __init__(self, generator_llm, critic_llm, max_cycles: int = 3):
        self.generator = generator_llm
        self.critic = critic_llm
        self.max_cycles = max_cycles

    def run(self, task: str, criteria: list[str]) -> str:
        output = self._generate(task)

        for cycle in range(self.max_cycles):
            critique = self._critique(task, output, criteria)

            if self._is_satisfactory(critique):
                break

            output = self._revise(task, output, critique)

        return output

    def _generate(self, task: str) -> str:
        return self.generator(f"Complete this task:\n{task}")

    def _critique(self, task: str, output: str, criteria: list[str]) -> str:
        criteria_text = "\n".join(f"- {c}" for c in criteria)

        prompt = f"""Task: {task}

Output to evaluate:
{output}

Evaluation criteria:
{criteria_text}

Provide specific critique for each criterion.
If all criteria are met, respond with "SATISFACTORY"."""

        return self.critic(prompt)

    def _is_satisfactory(self, critique: str) -> bool:
        return "SATISFACTORY" in critique.upper()

    def _revise(self, task: str, output: str, critique: str) -> str:
        prompt = f"""Original task: {task}

Previous output:
{output}

Critique:
{critique}

Revise the output to address the critique."""

        return self.generator(prompt)
```

### Reflection for Code

```python
def code_with_reflection(task: str, test_cases: list) -> str:
    code = generate_code(task)

    for attempt in range(3):
        # Run tests
        test_results = run_tests(code, test_cases)

        if all(r["passed"] for r in test_results):
            return code

        # Critique based on failures
        failures = [r for r in test_results if not r["passed"]]
        critique = analyze_failures(code, failures)

        # Revise code
        code = revise_code(code, critique)

    return code  # Best effort after max attempts
```

---

## Tree-of-Thoughts Pattern

### Basic ToT

```python
class TreeOfThoughts:
    def __init__(self, llm, evaluator, breadth: int = 3, depth: int = 3):
        self.llm = llm
        self.evaluator = evaluator
        self.breadth = breadth
        self.depth = depth

    def solve(self, problem: str) -> str:
        root = {"thought": "", "children": [], "score": 0}
        self._expand(root, problem, depth=0)
        return self._get_best_path(root)

    def _expand(self, node: dict, problem: str, depth: int):
        if depth >= self.depth:
            return

        # Generate multiple thoughts
        thoughts = self._generate_thoughts(problem, node["thought"])

        for thought in thoughts[:self.breadth]:
            child = {
                "thought": thought,
                "children": [],
                "score": self._evaluate(problem, thought)
            }
            node["children"].append(child)

            # Only expand promising branches
            if child["score"] > 0.5:
                self._expand(child, problem, depth + 1)

    def _generate_thoughts(self, problem: str, context: str) -> list:
        prompt = f"""Problem: {problem}

Previous thinking: {context}

Generate {self.breadth} different next thoughts or approaches:"""

        response = self.llm(prompt)
        return self._parse_thoughts(response)

    def _evaluate(self, problem: str, thought: str) -> float:
        prompt = f"""Problem: {problem}
Proposed approach: {thought}

Rate this approach from 0 to 1 based on likelihood of success:"""

        return float(self.evaluator(prompt))

    def _get_best_path(self, root: dict) -> str:
        # Traverse tree following highest-scored children
        path = []
        node = root

        while node["children"]:
            best = max(node["children"], key=lambda x: x["score"])
            path.append(best["thought"])
            node = best

        return "\n".join(path)
```

---

## Multi-Agent Pattern

### Sequential Agents

```python
class SequentialAgentPipeline:
    def __init__(self, agents: list):
        self.agents = agents

    def run(self, initial_input: str) -> str:
        result = initial_input

        for agent in self.agents:
            result = agent.process(result)

        return result

# Usage
pipeline = SequentialAgentPipeline([
    ResearchAgent(),
    AnalysisAgent(),
    WriterAgent(),
    EditorAgent()
])

output = pipeline.run("Write a report on AI trends")
```

### Coordinator Pattern

```python
class CoordinatorAgent:
    def __init__(self, coordinator_llm, specialist_agents: dict):
        self.coordinator = coordinator_llm
        self.specialists = specialist_agents

    def run(self, task: str) -> str:
        # Coordinator decides which specialist to use
        while True:
            decision = self._get_routing_decision(task)

            if decision["action"] == "finish":
                return decision["result"]

            specialist = self.specialists[decision["agent"]]
            result = specialist.process(decision["subtask"])

            task = self._update_task(task, result)

    def _get_routing_decision(self, task: str) -> dict:
        prompt = f"""Task: {task}

Available specialists: {list(self.specialists.keys())}

Decide:
1. Which specialist should handle the next subtask?
2. What subtask should they perform?
3. Or should we finish and return the result?

Respond as JSON: {{"action": "delegate|finish", "agent": "...", "subtask": "...", "result": "..."}}"""

        return json.loads(self.coordinator(prompt))
```

### CrewAI Example

```python
from crewai import Agent, Task, Crew

# Define agents
researcher = Agent(
    role="Senior Researcher",
    goal="Find accurate, up-to-date information",
    backstory="Expert at research and fact-finding",
    tools=[search_tool, scrape_tool]
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear, engaging content",
    backstory="Experienced at explaining complex topics"
)

# Define tasks
research_task = Task(
    description="Research the latest AI agent patterns",
    agent=researcher,
    expected_output="Comprehensive research notes"
)

write_task = Task(
    description="Write a blog post based on research",
    agent=writer,
    expected_output="Published-ready blog post",
    context=[research_task]
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)

result = crew.kickoff()
```
