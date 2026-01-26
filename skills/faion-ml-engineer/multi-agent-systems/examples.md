# Multi-Agent Systems Examples

## 1. Hierarchical Manager-Worker (Vanilla Python)

```python
from dataclasses import dataclass
from typing import List, Dict, Callable
from openai import OpenAI
import json

client = OpenAI()

@dataclass
class AgentConfig:
    name: str
    role: str
    system_prompt: str
    model: str = "gpt-4o"

class Agent:
    """Base agent with LLM capabilities."""

    def __init__(self, config: AgentConfig):
        self.config = config

    def respond(self, message: str) -> str:
        response = client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": self.config.system_prompt},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content

class ManagerAgent(Agent):
    """Manager that delegates tasks to workers."""

    def __init__(self, config: AgentConfig, workers: List[Agent]):
        super().__init__(config)
        self.workers = {w.config.name: w for w in workers}

    def delegate(self, task: str) -> str:
        # Create plan
        plan_prompt = f"""Task: {task}

Available workers:
{chr(10).join([f"- {w.config.name}: {w.config.role}" for w in self.workers.values()])}

Create a plan assigning subtasks to workers.
Return JSON: {{"assignments": [{{"worker": "name", "subtask": "description"}}]}}"""

        response = self.respond(plan_prompt)

        try:
            plan = json.loads(response)
            assignments = plan.get("assignments", [])
        except json.JSONDecodeError:
            return f"Failed to parse plan: {response}"

        # Execute assignments
        results = []
        for assignment in assignments:
            worker_name = assignment["worker"]
            subtask = assignment["subtask"]

            if worker_name in self.workers:
                result = self.workers[worker_name].respond(subtask)
                results.append({
                    "worker": worker_name,
                    "task": subtask,
                    "result": result
                })

        # Synthesize results
        synthesis_prompt = f"""Original task: {task}

Worker results:
{json.dumps(results, indent=2)}

Synthesize these results into a final response."""

        return self.respond(synthesis_prompt)

# Usage
manager = ManagerAgent(
    config=AgentConfig(
        name="ProjectManager",
        role="Project Manager",
        system_prompt="You are a project manager. Decompose tasks and coordinate workers."
    ),
    workers=[
        Agent(AgentConfig(
            name="Developer",
            role="Software Developer",
            system_prompt="You are a developer. Write and review code."
        )),
        Agent(AgentConfig(
            name="Designer",
            role="UI Designer",
            system_prompt="You are a UI designer. Create user interface designs."
        )),
        Agent(AgentConfig(
            name="Tester",
            role="QA Tester",
            system_prompt="You are a QA tester. Create test cases and find bugs."
        ))
    ]
)

result = manager.delegate("Build a simple todo app with tests")
```

## 2. LangGraph Multi-Agent with State

```python
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import operator

# Define state schema
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    task: str
    plan: list[dict]
    results: Annotated[list, operator.add]
    final_output: str

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o")

def planner_node(state: AgentState) -> dict:
    """Create execution plan."""
    messages = [
        {"role": "system", "content": "Create a plan with steps. Return JSON list of steps."},
        {"role": "user", "content": state["task"]}
    ]
    response = llm.invoke(messages)

    import json
    try:
        plan = json.loads(response.content)
    except:
        plan = [{"step": "execute", "description": state["task"]}]

    return {"plan": plan, "messages": [AIMessage(content=f"Plan: {plan}")]}

def executor_node(state: AgentState) -> dict:
    """Execute plan steps."""
    results = []
    for step in state["plan"]:
        messages = [
            {"role": "system", "content": "Execute the given task step."},
            {"role": "user", "content": step.get("description", str(step))}
        ]
        response = llm.invoke(messages)
        results.append({"step": step, "result": response.content})

    return {"results": results}

def synthesizer_node(state: AgentState) -> dict:
    """Synthesize results into final output."""
    results_text = "\n".join([f"- {r['result']}" for r in state["results"]])
    messages = [
        {"role": "system", "content": "Synthesize the results into a coherent response."},
        {"role": "user", "content": f"Task: {state['task']}\n\nResults:\n{results_text}"}
    ]
    response = llm.invoke(messages)

    return {"final_output": response.content}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("synthesizer", synthesizer_node)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "synthesizer")
workflow.add_edge("synthesizer", END)

# Compile with persistence
# Production: use PostgresSaver
# checkpointer = PostgresSaver.from_conn_string("postgresql://...")
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()  # Dev only

app = workflow.compile(checkpointer=checkpointer)

# Run
result = app.invoke(
    {"task": "Create a marketing strategy for a SaaS product", "messages": []},
    config={"configurable": {"thread_id": "1"}}
)
print(result["final_output"])
```

## 3. CrewAI Role-Based Team

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Define tools
search_tool = SerperDevTool()
web_tool = WebsiteSearchTool()

# Define agents with clear roles
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI and data science",
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_tool]
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content about tech advancements",
    backstory="""You are a renowned Content Strategist, known for
    your insightful and engaging articles.""",
    verbose=True,
    allow_delegation=True
)

editor = Agent(
    role="Senior Editor",
    goal="Ensure content quality and accuracy",
    backstory="""You are a meticulous editor with years of experience
    in tech journalism.""",
    verbose=True,
    allow_delegation=False
)

# Define tasks
research_task = Task(
    description="""Conduct comprehensive research on the latest AI
    agent frameworks for 2025. Focus on LangGraph, CrewAI, AutoGen.""",
    expected_output="Detailed research report with key findings",
    agent=researcher
)

writing_task = Task(
    description="""Using the research, write an engaging article
    comparing these frameworks for developers.""",
    expected_output="Well-structured article draft (800-1000 words)",
    agent=writer,
    context=[research_task]  # Depends on research
)

editing_task = Task(
    description="""Review and polish the article. Check for accuracy,
    clarity, and engagement.""",
    expected_output="Final polished article ready for publication",
    agent=editor,
    context=[writing_task]
)

# Create crew
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crew.kickoff()
print(result)
```

## 4. AutoGen Group Chat

```python
from autogen import ConversableAgent, GroupChat, GroupChatManager
import os

config_list = [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}]

# Define specialized agents
coder = ConversableAgent(
    name="Coder",
    system_message="""You are a senior software engineer.
    Write clean, well-documented code.""",
    llm_config={"config_list": config_list}
)

reviewer = ConversableAgent(
    name="Reviewer",
    system_message="""You are a code reviewer.
    Review code for bugs, security issues, and best practices.
    Be constructive but thorough.""",
    llm_config={"config_list": config_list}
)

architect = ConversableAgent(
    name="Architect",
    system_message="""You are a software architect.
    Focus on system design, patterns, and scalability.
    Guide the team on architectural decisions.""",
    llm_config={"config_list": config_list}
)

pm = ConversableAgent(
    name="ProductManager",
    system_message="""You are a product manager.
    Ensure the team stays focused on requirements.
    Say 'TASK_COMPLETE' when the task is done.""",
    llm_config={"config_list": config_list}
)

# Create group chat
group_chat = GroupChat(
    agents=[pm, architect, coder, reviewer],
    messages=[],
    max_round=10,
    speaker_selection_method="auto"  # LLM selects next speaker
)

manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": config_list}
)

# Start conversation
pm.initiate_chat(
    manager,
    message="We need to design and implement a rate limiter for our API. Let's discuss the approach and then implement it."
)
```

## 5. Production Multi-Agent System with Message Bus

```python
from dataclasses import dataclass, field
from typing import Dict, List, Callable, Any
from enum import Enum
import asyncio
import logging
from openai import AsyncOpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    DIRECT = "direct"
    BROADCAST = "broadcast"
    REQUEST = "request"
    RESPONSE = "response"

@dataclass
class Message:
    sender: str
    receiver: str
    content: str
    msg_type: MessageType
    correlation_id: str = ""
    metadata: Dict = field(default_factory=dict)

class MessageBus:
    """Central message bus for agent communication."""

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Message] = []
        self._lock = asyncio.Lock()

    def subscribe(self, agent_name: str, handler: Callable):
        if agent_name not in self.subscribers:
            self.subscribers[agent_name] = []
        self.subscribers[agent_name].append(handler)

    async def publish(self, message: Message):
        async with self._lock:
            self.message_history.append(message)

        if message.msg_type == MessageType.BROADCAST:
            tasks = []
            for name, handlers in self.subscribers.items():
                if name != message.sender:
                    for handler in handlers:
                        tasks.append(handler(message))
            await asyncio.gather(*tasks)
        else:
            if message.receiver in self.subscribers:
                for handler in self.subscribers[message.receiver]:
                    await handler(message)

@dataclass
class ProductionAgentConfig:
    name: str
    role: str
    system_prompt: str
    model: str = "gpt-4o"
    max_retries: int = 3
    timeout: float = 30.0

class ProductionAgent:
    """Production-ready agent with error handling."""

    def __init__(self, config: ProductionAgentConfig, message_bus: MessageBus):
        self.config = config
        self.message_bus = message_bus
        self.client = AsyncOpenAI()
        self._setup_handlers()

    def _setup_handlers(self):
        self.message_bus.subscribe(self.config.name, self._handle_message)

    async def _handle_message(self, message: Message):
        logger.info(f"{self.config.name} received from {message.sender}: {message.content[:100]}...")

        response = await self.respond(message.content)

        if message.msg_type == MessageType.REQUEST:
            await self.message_bus.publish(Message(
                sender=self.config.name,
                receiver=message.sender,
                content=response,
                msg_type=MessageType.RESPONSE,
                correlation_id=message.correlation_id
            ))

        return response

    async def respond(self, message: str) -> str:
        for attempt in range(self.config.max_retries):
            try:
                response = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model=self.config.model,
                        messages=[
                            {"role": "system", "content": self.config.system_prompt},
                            {"role": "user", "content": message}
                        ]
                    ),
                    timeout=self.config.timeout
                )
                return response.choices[0].message.content
            except asyncio.TimeoutError:
                logger.warning(f"{self.config.name}: Timeout on attempt {attempt + 1}")
            except Exception as e:
                logger.error(f"{self.config.name}: Error on attempt {attempt + 1}: {e}")

        return f"Error: Failed after {self.config.max_retries} attempts"

class ProductionOrchestrator:
    """Orchestrator with multiple execution strategies."""

    def __init__(self, agents: List[ProductionAgent], model: str = "gpt-4o"):
        self.agents = {a.config.name: a for a in agents}
        self.model = model
        self.client = AsyncOpenAI()

    async def execute(self, task: str, strategy: str = "hierarchical") -> Dict[str, Any]:
        strategies = {
            "hierarchical": self._hierarchical,
            "parallel": self._parallel,
            "sequential": self._sequential
        }
        return await strategies[strategy](task)

    async def _hierarchical(self, task: str) -> Dict[str, Any]:
        # Create plan
        plan = await self._create_plan(task)

        # Execute assignments
        results = []
        for assignment in plan.get("assignments", []):
            agent_name = assignment["agent"]
            subtask = assignment["task"]

            if agent_name in self.agents:
                result = await self.agents[agent_name].respond(subtask)
                results.append({"agent": agent_name, "task": subtask, "result": result})

        # Synthesize
        return await self._synthesize(task, results)

    async def _parallel(self, task: str) -> Dict[str, Any]:
        plan = await self._create_plan(task)

        async def execute_one(assignment):
            agent_name = assignment["agent"]
            if agent_name in self.agents:
                result = await self.agents[agent_name].respond(assignment["task"])
                return {"agent": agent_name, "result": result}
            return None

        tasks = [execute_one(a) for a in plan.get("assignments", [])]
        results = await asyncio.gather(*tasks)
        results = [r for r in results if r]

        return await self._synthesize(task, results)

    async def _sequential(self, task: str) -> Dict[str, Any]:
        current = task
        results = []

        for name, agent in self.agents.items():
            result = await agent.respond(current)
            results.append({"agent": name, "result": result})
            current = result

        return {"results": results, "final": current}

    async def _create_plan(self, task: str) -> Dict:
        agents_info = "\n".join([f"- {n}: {a.config.role}" for n, a in self.agents.items()])
        prompt = f"""Task: {task}

Available agents:
{agents_info}

Create assignments. Return JSON: {{"assignments": [{{"agent": "name", "task": "description"}}]}}"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        import json
        return json.loads(response.choices[0].message.content)

    async def _synthesize(self, task: str, results: List[Dict]) -> Dict[str, Any]:
        import json
        prompt = f"""Task: {task}

Results:
{json.dumps(results, indent=2)}

Synthesize into a final response."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "individual_results": results,
            "synthesis": response.choices[0].message.content
        }

# Usage
async def main():
    bus = MessageBus()

    agents = [
        ProductionAgent(ProductionAgentConfig(
            name="Researcher",
            role="Research Analyst",
            system_prompt="You research topics thoroughly and provide detailed findings."
        ), bus),
        ProductionAgent(ProductionAgentConfig(
            name="Writer",
            role="Content Writer",
            system_prompt="You write clear, engaging content based on research."
        ), bus),
        ProductionAgent(ProductionAgentConfig(
            name="Editor",
            role="Editor",
            system_prompt="You review and improve content for clarity and accuracy."
        ), bus)
    ]

    orchestrator = ProductionOrchestrator(agents)
    result = await orchestrator.execute(
        "Write a blog post about multi-agent AI systems",
        strategy="hierarchical"
    )
    print(result["synthesis"])

# asyncio.run(main())
```

## 6. Collaborative Agents with Shared Memory

```python
from typing import Dict, List
import json
from openai import OpenAI

client = OpenAI()

class SharedMemory:
    """Shared memory for collaborative agents."""

    def __init__(self):
        self.notes: List[Dict] = []
        self.artifacts: Dict[str, str] = {}
        self.decisions: List[Dict] = []

    def add_note(self, agent: str, content: str):
        self.notes.append({"agent": agent, "content": content})

    def add_artifact(self, name: str, content: str):
        self.artifacts[name] = content

    def add_decision(self, agent: str, decision: str, rationale: str):
        self.decisions.append({
            "agent": agent,
            "decision": decision,
            "rationale": rationale
        })

    def get_context(self) -> str:
        return f"""
Notes: {json.dumps(self.notes[-5:], indent=2)}
Artifacts: {list(self.artifacts.keys())}
Recent decisions: {json.dumps(self.decisions[-3:], indent=2)}
"""

class CollaborativeGroup:
    """Agents that collaborate via shared memory."""

    def __init__(self, agents: List[Agent], memory: SharedMemory):
        self.agents = {a.config.name: a for a in agents}
        self.memory = memory

    def collaborate(self, task: str, rounds: int = 3) -> Dict:
        # Initial ideas
        ideas = {}
        for name, agent in self.agents.items():
            prompt = f"Task: {task}\n\nProvide your initial approach."
            idea = agent.respond(prompt)
            ideas[name] = idea
            self.memory.add_note(name, idea)

        # Iterative refinement
        for round_num in range(rounds):
            for name, agent in self.agents.items():
                context = self.memory.get_context()
                other_ideas = {k: v for k, v in ideas.items() if k != name}

                prompt = f"""Task: {task}

Your current idea: {ideas[name]}

Team context:
{context}

Other ideas:
{json.dumps(other_ideas, indent=2)}

Refine your approach, incorporating good points from others."""

                refined = agent.respond(prompt)
                ideas[name] = refined
                self.memory.add_note(name, f"Round {round_num + 1}: {refined}")

        # Final synthesis
        synthesis_prompt = f"""Task: {task}

Final contributions:
{json.dumps(ideas, indent=2)}

Create a unified solution combining the best elements."""

        final = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": synthesis_prompt}]
        ).choices[0].message.content

        self.memory.add_artifact("final_solution", final)

        return {
            "contributions": ideas,
            "memory": {
                "notes_count": len(self.memory.notes),
                "artifacts": list(self.memory.artifacts.keys()),
                "decisions": len(self.memory.decisions)
            },
            "final": final
        }
```
