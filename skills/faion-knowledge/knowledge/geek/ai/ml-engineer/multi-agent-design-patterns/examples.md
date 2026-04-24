# Multi-Agent Design Patterns: Code Examples

Practical implementation examples for each pattern across popular frameworks.

## Supervisor Pattern Examples

### LangGraph Implementation

```python
from typing import Literal, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# State definition
class AgentState(TypedDict):
    messages: list
    next_agent: str
    final_response: str

# Supervisor logic
def supervisor_node(state: AgentState) -> AgentState:
    """Route request to appropriate worker."""
    llm = ChatOpenAI(model="gpt-4o")

    routing_prompt = """Analyze the user request and decide which agent should handle it.

Available agents:
- researcher: For questions requiring web search or data gathering
- coder: For code writing, debugging, or technical implementation
- writer: For content creation, editing, or summarization

User request: {request}

Respond with ONLY the agent name: researcher, coder, or writer"""

    messages = state["messages"]
    last_message = messages[-1].content

    response = llm.invoke(routing_prompt.format(request=last_message))
    next_agent = response.content.strip().lower()

    return {**state, "next_agent": next_agent}

# Worker agents
def researcher_node(state: AgentState) -> AgentState:
    """Research agent with web search tools."""
    llm = ChatOpenAI(model="gpt-4o")
    # Add search tools here
    response = llm.invoke(f"Research: {state['messages'][-1].content}")
    return {**state, "final_response": response.content}

def coder_node(state: AgentState) -> AgentState:
    """Coder agent for technical tasks."""
    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke(f"Write code for: {state['messages'][-1].content}")
    return {**state, "final_response": response.content}

def writer_node(state: AgentState) -> AgentState:
    """Writer agent for content tasks."""
    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke(f"Write content: {state['messages'][-1].content}")
    return {**state, "final_response": response.content}

# Router function
def route_to_worker(state: AgentState) -> Literal["researcher", "coder", "writer"]:
    return state["next_agent"]

# Build graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("coder", coder_node)
workflow.add_node("writer", writer_node)

# Add edges
workflow.set_entry_point("supervisor")
workflow.add_conditional_edges(
    "supervisor",
    route_to_worker,
    {
        "researcher": "researcher",
        "coder": "coder",
        "writer": "writer",
    }
)
workflow.add_edge("researcher", END)
workflow.add_edge("coder", END)
workflow.add_edge("writer", END)

# Compile
supervisor_graph = workflow.compile()

# Usage
result = supervisor_graph.invoke({
    "messages": [HumanMessage(content="Write a Python function to sort a list")],
    "next_agent": "",
    "final_response": ""
})
```

### CrewAI Implementation

```python
from crewai import Agent, Task, Crew, Process

# Define supervisor (manager)
manager = Agent(
    role="Project Manager",
    goal="Coordinate team to complete user requests efficiently",
    backstory="Experienced PM who delegates tasks to specialists",
    allow_delegation=True,
    verbose=True
)

# Define worker agents
researcher = Agent(
    role="Research Specialist",
    goal="Gather accurate information from various sources",
    backstory="Expert researcher with analytical skills",
    tools=[search_tool, scrape_tool],
    verbose=True
)

coder = Agent(
    role="Software Developer",
    goal="Write clean, efficient, well-documented code",
    backstory="Senior developer with expertise in multiple languages",
    tools=[code_execution_tool],
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging, well-structured content",
    backstory="Professional writer with technical background",
    verbose=True
)

# Create crew with manager
crew = Crew(
    agents=[researcher, coder, writer],
    manager_agent=manager,
    process=Process.hierarchical,  # Manager delegates
    verbose=True
)

# Execute
result = crew.kickoff(inputs={"request": "Build a web scraper for news articles"})
```

### Google ADK Implementation

```python
from google.adk import Agent, LlmAgent
from google.adk.tools import transfer_to_agent

# Define worker agents
researcher_agent = LlmAgent(
    name="researcher",
    description="Handles research tasks, web searches, and data gathering",
    instruction="You are a research specialist. Gather information accurately.",
    tools=[web_search, document_reader]
)

coder_agent = LlmAgent(
    name="coder",
    description="Handles code writing, debugging, and technical implementation",
    instruction="You are a senior developer. Write clean, tested code.",
    tools=[code_executor, file_writer]
)

# Define supervisor with delegation capability
supervisor = LlmAgent(
    name="supervisor",
    description="Routes requests to appropriate specialists",
    instruction="""You are a supervisor coordinating a team.
    Analyze requests and delegate to the right specialist:
    - Use transfer_to_agent('researcher') for research tasks
    - Use transfer_to_agent('coder') for coding tasks

    After receiving results, synthesize and respond to the user.""",
    sub_agents=[researcher_agent, coder_agent],
    tools=[transfer_to_agent]
)
```

---

## Hierarchical Pattern Examples

### LangGraph Multi-Level Hierarchy

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

class HierarchicalState(TypedDict):
    goal: str
    subtasks: list[dict]
    team_results: dict
    final_output: str

# Top-level supervisor
def top_supervisor(state: HierarchicalState) -> HierarchicalState:
    """Decomposes high-level goal into team assignments."""
    llm = ChatOpenAI(model="gpt-4o")

    decomposition_prompt = """Break down this goal into subtasks for two teams:

Goal: {goal}

Respond in JSON format:
{{
    "research_team": ["task1", "task2"],
    "development_team": ["task1", "task2"]
}}"""

    response = llm.invoke(decomposition_prompt.format(goal=state["goal"]))
    subtasks = json.loads(response.content)

    return {**state, "subtasks": subtasks}

# Mid-level: Research team coordinator
def research_team_coordinator(state: HierarchicalState) -> HierarchicalState:
    """Coordinates research workers."""
    tasks = state["subtasks"].get("research_team", [])
    results = []

    for task in tasks:
        # Delegate to research workers (simplified)
        result = research_worker(task)
        results.append(result)

    state["team_results"]["research"] = results
    return state

# Mid-level: Development team coordinator
def development_team_coordinator(state: HierarchicalState) -> HierarchicalState:
    """Coordinates development workers."""
    tasks = state["subtasks"].get("development_team", [])
    results = []

    for task in tasks:
        result = development_worker(task)
        results.append(result)

    state["team_results"]["development"] = results
    return state

# Worker functions
def research_worker(task: str) -> str:
    llm = ChatOpenAI(model="gpt-4o")
    return llm.invoke(f"Research: {task}").content

def development_worker(task: str) -> str:
    llm = ChatOpenAI(model="gpt-4o")
    return llm.invoke(f"Implement: {task}").content

# Final synthesis
def synthesize_results(state: HierarchicalState) -> HierarchicalState:
    """Combines all team results into final output."""
    llm = ChatOpenAI(model="gpt-4o")

    synthesis_prompt = """Synthesize these team results into a cohesive response:

Research findings: {research}
Development results: {development}

Original goal: {goal}"""

    response = llm.invoke(synthesis_prompt.format(
        research=state["team_results"].get("research", []),
        development=state["team_results"].get("development", []),
        goal=state["goal"]
    ))

    return {**state, "final_output": response.content}

# Build hierarchical graph
workflow = StateGraph(HierarchicalState)

workflow.add_node("top_supervisor", top_supervisor)
workflow.add_node("research_coordinator", research_team_coordinator)
workflow.add_node("dev_coordinator", development_team_coordinator)
workflow.add_node("synthesize", synthesize_results)

workflow.set_entry_point("top_supervisor")
workflow.add_edge("top_supervisor", "research_coordinator")
workflow.add_edge("top_supervisor", "dev_coordinator")
workflow.add_edge("research_coordinator", "synthesize")
workflow.add_edge("dev_coordinator", "synthesize")
workflow.add_edge("synthesize", END)

hierarchical_graph = workflow.compile()
```

### CrewAI Hierarchical Teams

```python
from crewai import Agent, Task, Crew, Process

# Top-level manager
project_director = Agent(
    role="Project Director",
    goal="Oversee all teams and deliver complete solutions",
    backstory="Executive with strategic vision",
    allow_delegation=True
)

# Mid-level: Research team
research_lead = Agent(
    role="Research Lead",
    goal="Coordinate research activities",
    allow_delegation=True
)

web_researcher = Agent(
    role="Web Researcher",
    goal="Find information online",
    tools=[search_tool]
)

data_analyst = Agent(
    role="Data Analyst",
    goal="Analyze and interpret data",
    tools=[analysis_tool]
)

# Mid-level: Development team
dev_lead = Agent(
    role="Development Lead",
    goal="Coordinate development activities",
    allow_delegation=True
)

backend_dev = Agent(
    role="Backend Developer",
    goal="Build server-side components"
)

frontend_dev = Agent(
    role="Frontend Developer",
    goal="Build user interfaces"
)

# Create nested crews
research_crew = Crew(
    agents=[web_researcher, data_analyst],
    manager_agent=research_lead,
    process=Process.hierarchical
)

dev_crew = Crew(
    agents=[backend_dev, frontend_dev],
    manager_agent=dev_lead,
    process=Process.hierarchical
)

# Top-level crew coordinating sub-crews
# (In practice, would orchestrate the sub-crews)
```

---

## Sequential Pattern Examples

### Google ADK SequentialAgent

```python
from google.adk import SequentialAgent, LlmAgent

# Stage 1: Parser
parser_agent = LlmAgent(
    name="parser",
    description="Parses raw input into structured format",
    instruction="Extract key information from the input and structure it as JSON.",
    output_key="parsed_data"
)

# Stage 2: Validator
validator_agent = LlmAgent(
    name="validator",
    description="Validates parsed data against rules",
    instruction="""Validate the parsed data from state['parsed_data'].
    Check for required fields and correct formats.
    Output validation result with any errors found.""",
    output_key="validation_result"
)

# Stage 3: Processor
processor_agent = LlmAgent(
    name="processor",
    description="Processes validated data",
    instruction="""Process the validated data.
    Read from state['parsed_data'] and state['validation_result'].
    Transform data according to business rules.""",
    output_key="processed_data"
)

# Stage 4: Reporter
reporter_agent = LlmAgent(
    name="reporter",
    description="Generates final report",
    instruction="""Generate a summary report.
    Include: original input, processing steps, final output.
    Read from all previous state keys.""",
    output_key="final_report"
)

# Create sequential pipeline
pipeline = SequentialAgent(
    name="data_pipeline",
    description="End-to-end data processing pipeline",
    sub_agents=[parser_agent, validator_agent, processor_agent, reporter_agent]
)

# Execute
result = pipeline.run(input_data="Raw document content here...")
```

### LangGraph Sequential Pipeline

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

class PipelineState(TypedDict):
    input: str
    parsed: dict | None
    validated: bool
    processed: dict | None
    report: str | None

def parse_stage(state: PipelineState) -> PipelineState:
    """Stage 1: Parse input."""
    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke(f"Parse this into JSON: {state['input']}")
    parsed = json.loads(response.content)
    return {**state, "parsed": parsed}

def validate_stage(state: PipelineState) -> PipelineState:
    """Stage 2: Validate parsed data."""
    parsed = state["parsed"]
    # Validation logic
    is_valid = all(key in parsed for key in ["title", "content"])
    return {**state, "validated": is_valid}

def process_stage(state: PipelineState) -> PipelineState:
    """Stage 3: Process if valid."""
    if not state["validated"]:
        return {**state, "processed": None}

    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke(f"Process this data: {state['parsed']}")
    return {**state, "processed": json.loads(response.content)}

def report_stage(state: PipelineState) -> PipelineState:
    """Stage 4: Generate report."""
    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke(f"""Generate report for:
    Input: {state['input']}
    Parsed: {state['parsed']}
    Valid: {state['validated']}
    Processed: {state['processed']}""")
    return {**state, "report": response.content}

# Build sequential graph
workflow = StateGraph(PipelineState)

workflow.add_node("parse", parse_stage)
workflow.add_node("validate", validate_stage)
workflow.add_node("process", process_stage)
workflow.add_node("report", report_stage)

workflow.set_entry_point("parse")
workflow.add_edge("parse", "validate")
workflow.add_edge("validate", "process")
workflow.add_edge("process", "report")
workflow.add_edge("report", END)

sequential_pipeline = workflow.compile()
```

### CrewAI Sequential Process

```python
from crewai import Agent, Task, Crew, Process

# Agents for each stage
parser = Agent(
    role="Data Parser",
    goal="Parse raw data into structured format"
)

validator = Agent(
    role="Data Validator",
    goal="Validate data integrity and completeness"
)

processor = Agent(
    role="Data Processor",
    goal="Transform data according to business rules"
)

reporter = Agent(
    role="Report Generator",
    goal="Create comprehensive summary reports"
)

# Tasks in sequence
parse_task = Task(
    description="Parse the input data: {input}",
    agent=parser,
    expected_output="Structured JSON data"
)

validate_task = Task(
    description="Validate the parsed data from previous step",
    agent=validator,
    expected_output="Validation report with pass/fail status",
    context=[parse_task]  # Depends on parse_task
)

process_task = Task(
    description="Process the validated data",
    agent=processor,
    expected_output="Transformed data ready for reporting",
    context=[validate_task]
)

report_task = Task(
    description="Generate final report",
    agent=reporter,
    expected_output="Complete summary report",
    context=[process_task]
)

# Sequential crew
crew = Crew(
    agents=[parser, validator, processor, reporter],
    tasks=[parse_task, validate_task, process_task, report_task],
    process=Process.sequential,  # Explicit sequential
    verbose=True
)

result = crew.kickoff(inputs={"input": "Raw data content"})
```

---

## Peer-to-Peer Pattern Examples

### Basic P2P Message Passing

```python
import asyncio
from dataclasses import dataclass
from typing import Callable

@dataclass
class Message:
    sender: str
    recipient: str
    content: dict
    message_type: str

class PeerAgent:
    """Decentralized agent with local routing."""

    def __init__(self, name: str, specialization: str):
        self.name = name
        self.specialization = specialization
        self.peers: dict[str, "PeerAgent"] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.llm = ChatOpenAI(model="gpt-4o")

    def register_peer(self, peer: "PeerAgent"):
        """Discover and register a peer agent."""
        self.peers[peer.name] = peer

    async def send_message(self, recipient: str, content: dict, msg_type: str):
        """Send message to peer."""
        if recipient not in self.peers:
            raise ValueError(f"Unknown peer: {recipient}")

        message = Message(
            sender=self.name,
            recipient=recipient,
            content=content,
            message_type=msg_type
        )
        await self.peers[recipient].receive_message(message)

    async def receive_message(self, message: Message):
        """Receive message from peer."""
        await self.message_queue.put(message)

    async def process_messages(self):
        """Process incoming messages."""
        while True:
            message = await self.message_queue.get()
            result = await self.handle_message(message)

            if result.get("forward_to"):
                # Route to another peer
                await self.send_message(
                    result["forward_to"],
                    result["content"],
                    "forwarded"
                )
            elif result.get("respond"):
                # Respond to sender
                await self.send_message(
                    message.sender,
                    result["content"],
                    "response"
                )

    async def handle_message(self, message: Message) -> dict:
        """Handle message based on specialization."""
        routing_prompt = f"""You are {self.name}, specialized in {self.specialization}.

Message from {message.sender}: {message.content}

Can you handle this? If yes, process it. If no, suggest which peer should handle it.
Available peers: {list(self.peers.keys())}

Respond in JSON:
{{"can_handle": true/false, "result": "...", "forward_to": null or "peer_name"}}"""

        response = self.llm.invoke(routing_prompt)
        return json.loads(response.content)

# Create peer network
research_agent = PeerAgent("researcher", "information gathering")
code_agent = PeerAgent("coder", "code implementation")
review_agent = PeerAgent("reviewer", "quality review")

# Register peers (mesh network)
research_agent.register_peer(code_agent)
research_agent.register_peer(review_agent)
code_agent.register_peer(research_agent)
code_agent.register_peer(review_agent)
review_agent.register_peer(research_agent)
review_agent.register_peer(code_agent)

# Start processing
async def run_network():
    tasks = [
        asyncio.create_task(research_agent.process_messages()),
        asyncio.create_task(code_agent.process_messages()),
        asyncio.create_task(review_agent.process_messages()),
    ]

    # Send initial message
    await research_agent.receive_message(Message(
        sender="user",
        recipient="researcher",
        content={"task": "Build a REST API for user management"},
        message_type="request"
    ))

    await asyncio.gather(*tasks)
```

### AgentNet-Style Decentralized Pattern

```python
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class AgentNode:
    """Agent in decentralized DAG structure."""

    name: str
    specialization: str
    memory: list = field(default_factory=list)  # Local RAG memory
    routing_weights: dict = field(default_factory=dict)  # Learned routing

    def add_to_memory(self, item: dict):
        """Add to local RAG memory."""
        self.memory.append(item)

    def update_routing(self, target: str, success: bool):
        """Update routing weights based on outcome."""
        if target not in self.routing_weights:
            self.routing_weights[target] = 0.5

        # Simple reinforcement
        delta = 0.1 if success else -0.1
        self.routing_weights[target] = max(0, min(1,
            self.routing_weights[target] + delta))

    def select_next_agent(self, task: dict, peers: list["AgentNode"]) -> Optional["AgentNode"]:
        """Select next agent based on learned routing."""
        if not peers:
            return None

        # Combine LLM reasoning with learned weights
        llm = ChatOpenAI(model="gpt-4o")

        peer_info = [
            f"{p.name} ({p.specialization}): weight={self.routing_weights.get(p.name, 0.5)}"
            for p in peers
        ]

        prompt = f"""Given task: {task}
Your specialization: {self.specialization}
Available peers:
{chr(10).join(peer_info)}

Which peer should handle this next? Consider both specialization match and historical success (weight).
Respond with peer name only, or "self" if you should handle it."""

        response = llm.invoke(prompt)
        selected_name = response.content.strip()

        if selected_name == "self":
            return self

        return next((p for p in peers if p.name == selected_name), None)

class DecentralizedNetwork:
    """Manages decentralized agent network."""

    def __init__(self):
        self.agents: dict[str, AgentNode] = {}
        self.dag_edges: dict[str, list[str]] = {}  # Directed edges

    def add_agent(self, agent: AgentNode):
        self.agents[agent.name] = agent
        self.dag_edges[agent.name] = []

    def add_edge(self, from_agent: str, to_agent: str):
        """Add directed edge (respecting DAG - no cycles)."""
        if self._would_create_cycle(from_agent, to_agent):
            raise ValueError("Would create cycle")
        self.dag_edges[from_agent].append(to_agent)

    def _would_create_cycle(self, from_a: str, to_a: str) -> bool:
        """Check if adding edge would create cycle."""
        visited = set()
        def dfs(node):
            if node == from_a:
                return True
            if node in visited:
                return False
            visited.add(node)
            return any(dfs(n) for n in self.dag_edges.get(node, []))
        return dfs(to_a)

    async def process_task(self, task: dict, entry_agent: str) -> dict:
        """Process task through network."""
        current = self.agents[entry_agent]
        results = []

        while current:
            # Process at current node
            result = await current.process(task)
            results.append({"agent": current.name, "result": result})

            # Get peers (connected agents)
            peer_names = self.dag_edges.get(current.name, [])
            peers = [self.agents[n] for n in peer_names]

            # Route to next
            next_agent = current.select_next_agent(task, peers)
            if next_agent == current or next_agent is None:
                break

            current = next_agent

        return {"path": results}
```

---

## Parallel Fan-Out/Gather Example

```python
from google.adk import ParallelAgent, SequentialAgent, LlmAgent

# Parallel workers (fan-out)
api_fetcher_1 = LlmAgent(
    name="weather_api",
    description="Fetches weather data",
    output_key="weather_data"
)

api_fetcher_2 = LlmAgent(
    name="news_api",
    description="Fetches news data",
    output_key="news_data"
)

api_fetcher_3 = LlmAgent(
    name="stocks_api",
    description="Fetches stock data",
    output_key="stocks_data"
)

# Parallel execution
parallel_fetchers = ParallelAgent(
    name="data_fetchers",
    sub_agents=[api_fetcher_1, api_fetcher_2, api_fetcher_3]
)

# Gatherer (aggregator)
aggregator = LlmAgent(
    name="aggregator",
    description="Combines all fetched data into summary",
    instruction="""Synthesize data from:
    - state['weather_data']
    - state['news_data']
    - state['stocks_data']

    Create a unified morning briefing.""",
    output_key="briefing"
)

# Full fan-out/gather pipeline
fan_out_gather = SequentialAgent(
    name="morning_briefing",
    sub_agents=[parallel_fetchers, aggregator]
)
```

---

## Generator-Critic Example

```python
# Generator
draft_writer = LlmAgent(
    name="draft_writer",
    description="Generates initial content draft",
    instruction="Write a draft based on the requirements. Focus on completeness.",
    output_key="draft"
)

# Critic
fact_checker = LlmAgent(
    name="fact_checker",
    description="Reviews draft for accuracy",
    instruction="""Review the draft in state['draft'].
    Check for:
    - Factual accuracy
    - Logical consistency
    - Missing information

    Provide specific feedback for improvement.""",
    output_key="review"
)

# Refiner (optional third stage)
refiner = LlmAgent(
    name="refiner",
    description="Incorporates feedback into final version",
    instruction="""Using:
    - Original draft: state['draft']
    - Review feedback: state['review']

    Create an improved final version.""",
    output_key="final"
)

# Generator-Critic pipeline
gen_critic_pipeline = SequentialAgent(
    name="quality_content",
    sub_agents=[draft_writer, fact_checker, refiner]
)
```
