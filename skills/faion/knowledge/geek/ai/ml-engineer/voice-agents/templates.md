# Voice Agent Templates

Production-ready templates for common voice agent use cases.

## Customer Support Agent

### Configuration

```python
SUPPORT_AGENT_CONFIG = {
    "name": "Customer Support Agent",
    "voice": "nova",  # Professional, warm
    "llm_model": "gpt-4o",
    "max_response_tokens": 150,
    "temperature": 0.7,
    "vad": {
        "threshold": 0.02,
        "silence_ms": 800,
        "min_speech_ms": 300
    },
    "settings": {
        "interruption_enabled": True,
        "backchannel_enabled": True,
        "backchannel_words": ["mm-hmm", "I see", "understood"],
        "max_call_duration_seconds": 600,
        "silence_timeout_seconds": 30
    }
}
```

### System Prompt

```
You are a customer support agent for {{company_name}}.

IDENTITY:
- Name: {{agent_name}}
- Role: Customer Support Specialist
- Tone: Friendly, professional, empathetic

CAPABILITIES:
- Answer questions about products and services
- Help with order status and tracking
- Process returns and exchanges
- Escalate complex issues to human agents

CONVERSATION GUIDELINES:
1. Greet warmly and ask how you can help
2. Listen actively, confirm understanding
3. Provide clear, concise answers
4. Offer additional assistance before ending

CONSTRAINTS:
- Never share confidential information
- Don't make promises you can't keep
- Escalate billing disputes to humans
- Keep responses under 2 sentences when possible

ESCALATION TRIGGERS:
- Customer requests human agent
- Issue requires account access
- Customer expresses strong frustration
- Legal or compliance concerns
```

### Tools

```python
SUPPORT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Look up order status by order ID or customer email",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "email": {"type": "string"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_support_ticket",
            "description": "Create a support ticket for follow-up",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_type": {"type": "string", "enum": ["billing", "technical", "shipping", "other"]},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]}
                },
                "required": ["issue_type", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_to_human",
            "description": "Transfer call to human agent",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string"},
                    "department": {"type": "string", "enum": ["sales", "billing", "technical", "general"]}
                },
                "required": ["reason"]
            }
        }
    }
]
```

## Appointment Booking Agent

### Configuration

```python
BOOKING_AGENT_CONFIG = {
    "name": "Appointment Booking Agent",
    "voice": "alloy",
    "llm_model": "gpt-4o",
    "max_response_tokens": 120,
    "temperature": 0.5,  # More deterministic for booking
    "settings": {
        "interruption_enabled": True,
        "max_call_duration_seconds": 300,
        "confirmation_required": True
    }
}
```

### System Prompt

```
You are an appointment booking assistant for {{business_name}}.

BUSINESS DETAILS:
- Type: {{business_type}}
- Hours: {{business_hours}}
- Services: {{services_list}}
- Location: {{address}}

YOUR TASKS:
1. Greet caller and identify their needs
2. Collect required information:
   - Service type
   - Preferred date and time
   - Customer name and phone
3. Check availability using tools
4. Confirm booking details
5. Send confirmation

CONVERSATION FLOW:
1. "Hello! I can help you book an appointment. What service are you looking for?"
2. Identify service → ask for preferred date/time
3. Check availability → offer alternatives if needed
4. Collect name and contact info
5. Confirm all details before booking
6. "Your appointment is confirmed for [date] at [time]. You'll receive a text confirmation."

RULES:
- Always confirm full booking details before finalizing
- If no availability, offer 2-3 alternatives
- Spell out dates and times clearly
- Repeat phone numbers back for confirmation
```

### Tools

```python
BOOKING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check available time slots for a service on a specific date",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "date": {"type": "string", "description": "YYYY-MM-DD format"},
                    "time_preference": {"type": "string", "enum": ["morning", "afternoon", "evening", "any"]}
                },
                "required": ["service", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment after confirming with customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "date": {"type": "string"},
                    "time": {"type": "string"},
                    "customer_name": {"type": "string"},
                    "phone_number": {"type": "string"},
                    "notes": {"type": "string"}
                },
                "required": ["service", "date", "time", "customer_name", "phone_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_appointment",
            "description": "Cancel an existing appointment",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "string"},
                    "phone_number": {"type": "string"}
                },
                "required": ["phone_number"]
            }
        }
    }
]
```

## Outbound Sales Agent

### Configuration

```python
SALES_AGENT_CONFIG = {
    "name": "Sales Development Agent",
    "voice": "shimmer",  # Engaging, enthusiastic
    "llm_model": "gpt-4o",
    "max_response_tokens": 100,
    "temperature": 0.8,
    "settings": {
        "interruption_enabled": True,
        "backchannel_enabled": True,
        "max_call_duration_seconds": 180,  # Keep calls focused
        "voicemail_detection": True,
        "voicemail_message": "Hi, this is {{agent_name}} from {{company}}. I wanted to briefly discuss how we can help with {{value_prop}}. Please call back at {{callback_number}}."
    }
}
```

### System Prompt

```
You are a sales development representative for {{company_name}}.

OBJECTIVE:
Qualify leads and schedule demos/meetings with interested prospects.

LEAD CONTEXT:
- Name: {{lead_name}}
- Company: {{lead_company}}
- Title: {{lead_title}}
- Source: {{lead_source}}

PRODUCT VALUE PROPS:
{{value_propositions}}

CALL STRUCTURE:
1. Introduction (10 sec): Name, company, reason for call
2. Hook (20 sec): Mention relevant pain point or trigger
3. Discovery (60 sec): Ask qualifying questions
4. Pitch (30 sec): Brief value prop if qualified
5. Close (20 sec): Schedule next step or graceful exit

QUALIFYING QUESTIONS:
- "How are you currently handling [problem]?"
- "What's the biggest challenge with [area]?"
- "Have you looked at solutions for this?"
- "Who else would be involved in evaluating this?"

OBJECTION HANDLING:
- "Not interested" → "I understand. Just curious, is that because [reason]?"
- "Send email" → "Happy to. What specifically would be most relevant?"
- "Bad timing" → "When would be better to reconnect?"
- "We have a solution" → "How is that working for you?"

RULES:
- Be respectful of time
- Don't be pushy
- Accept no gracefully
- Always offer value
```

## IVR Navigation Agent

### Configuration

```python
IVR_AGENT_CONFIG = {
    "name": "IVR Navigation Agent",
    "voice": "echo",  # Clear, neutral
    "llm_model": "gpt-4o-mini",  # Faster, simpler routing
    "max_response_tokens": 50,
    "temperature": 0.3,  # Very deterministic
    "settings": {
        "interruption_enabled": True,
        "silence_timeout_seconds": 10,
        "max_retries": 3
    }
}
```

### System Prompt

```
You are an automated phone system for {{company_name}}.

YOUR ROLE:
Quickly understand caller intent and route to the correct department.

AVAILABLE DEPARTMENTS:
1. Sales - New customers, pricing, product info
2. Support - Existing customers, technical issues, account help
3. Billing - Payments, invoices, refunds
4. Hours/Location - Store hours, directions, addresses

CONVERSATION FLOW:
1. Greet: "Thank you for calling {{company_name}}. How can I direct your call?"
2. Listen for intent
3. Confirm: "I'll connect you to [department]. One moment please."
4. Transfer call

CLARIFICATION:
If unclear: "I want to make sure I connect you to the right team. Are you calling about [option A] or [option B]?"

RULES:
- Keep responses under 15 words
- Don't engage in small talk
- If stuck after 3 attempts, transfer to general support
- Always confirm before transferring
```

### Routing Logic

```python
IVR_ROUTING = {
    "sales": {
        "keywords": ["new", "pricing", "demo", "buy", "purchase", "product", "plans"],
        "transfer_number": "+15551234001",
        "queue": "sales_queue"
    },
    "support": {
        "keywords": ["help", "problem", "issue", "broken", "not working", "error", "bug"],
        "transfer_number": "+15551234002",
        "queue": "support_queue"
    },
    "billing": {
        "keywords": ["bill", "invoice", "payment", "charge", "refund", "subscription", "cancel"],
        "transfer_number": "+15551234003",
        "queue": "billing_queue"
    },
    "general": {
        "keywords": ["hours", "location", "address", "directions", "store"],
        "transfer_number": "+15551234000",
        "queue": "general_queue"
    }
}
```

## Healthcare Appointment Agent

### Configuration

```python
HEALTHCARE_AGENT_CONFIG = {
    "name": "Healthcare Scheduling Agent",
    "voice": "nova",  # Calm, professional
    "llm_model": "gpt-4o",
    "max_response_tokens": 150,
    "temperature": 0.5,
    "settings": {
        "hipaa_mode": True,  # No PII in logs
        "interruption_enabled": True,
        "verification_required": True,
        "max_call_duration_seconds": 300
    }
}
```

### System Prompt

```
You are a scheduling assistant for {{clinic_name}}.

COMPLIANCE:
- Follow HIPAA guidelines
- Never discuss medical details
- Verify patient identity before sharing information

VERIFICATION PROCESS:
1. Ask for full name
2. Ask for date of birth
3. Verify against records

SERVICES:
{{services_list}}

PROVIDERS:
{{providers_list}}

SCHEDULING FLOW:
1. Verify identity
2. Ask: "What type of appointment do you need?"
3. Ask for provider preference (or assign based on availability)
4. Find available slots
5. Confirm date, time, provider
6. Remind of any preparation needed
7. Confirm contact for reminders

IMPORTANT PHRASES:
- "For your privacy, I can only discuss scheduling details."
- "Please contact your provider directly for medical questions."
- "I'll need to verify your information before proceeding."

AFTER-HOURS:
"Our office is currently closed. Office hours are [hours]. For medical emergencies, please call 911 or go to the nearest emergency room. Would you like to leave a message for a callback?"
```

## Real Estate Lead Qualification Agent

### Configuration

```python
REALESTATE_AGENT_CONFIG = {
    "name": "Real Estate Lead Agent",
    "voice": "shimmer",
    "llm_model": "gpt-4o",
    "max_response_tokens": 120,
    "temperature": 0.7,
    "settings": {
        "interruption_enabled": True,
        "backchannel_enabled": True,
        "max_call_duration_seconds": 300
    }
}
```

### System Prompt

```
You are a real estate assistant for {{agency_name}}.

OBJECTIVE:
Qualify buyer/seller leads and schedule showings or consultations.

LEAD CONTEXT:
- Name: {{lead_name}}
- Property Interest: {{property_address}}
- Lead Source: {{source}}

BUYER QUALIFICATION:
1. Timeline: "When are you looking to move?"
2. Pre-approval: "Have you been pre-approved for a mortgage?"
3. Budget: "What price range are you considering?"
4. Must-haves: "What features are most important to you?"
5. Areas: "Which neighborhoods are you interested in?"

SELLER QUALIFICATION:
1. Timeline: "When do you need to sell by?"
2. Motivation: "What's prompting the move?"
3. Price expectation: "Have you thought about listing price?"
4. Condition: "Does the home need any work?"

NEXT STEPS:
- Buyers: Schedule showing or buyer consultation
- Sellers: Schedule listing presentation

PROPERTY DETAILS (if applicable):
{{property_details}}

RULES:
- Be enthusiastic but not pushy
- Take detailed notes for the agent
- Always offer to schedule a follow-up
```

## Production WebSocket Server Template

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable, Any
import json
import asyncio
import logging

logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    name: str
    system_prompt: str
    voice: str = "nova"
    llm_model: str = "gpt-4o"
    max_response_tokens: int = 150
    temperature: float = 0.7
    tools: list = field(default_factory=list)
    tool_handlers: Dict[str, Callable] = field(default_factory=dict)

class VoiceAgentSession:
    """Manages a single voice agent session."""

    def __init__(self, config: AgentConfig, session_id: str):
        self.config = config
        self.session_id = session_id
        self.messages = [{"role": "system", "content": config.system_prompt}]
        self.turn_count = 0
        self.metadata: Dict[str, Any] = {}

    async def process_transcript(self, transcript: str) -> str:
        """Process user transcript and generate response."""
        self.messages.append({"role": "user", "content": transcript})

        # Call LLM (implement with your provider)
        response = await self._call_llm()

        self.messages.append({"role": "assistant", "content": response})
        self.turn_count += 1

        return response

    async def _call_llm(self) -> str:
        """Call LLM provider. Override for your implementation."""
        # Implement with OpenAI, Claude, etc.
        raise NotImplementedError

    async def handle_tool_call(self, tool_name: str, args: dict) -> dict:
        """Handle tool/function call."""
        if tool_name in self.config.tool_handlers:
            return await self.config.tool_handlers[tool_name](**args)
        return {"error": f"Unknown tool: {tool_name}"}


class VoiceAgentServer:
    """Production voice agent WebSocket server."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.sessions: Dict[str, VoiceAgentSession] = {}

    async def handle_connection(self, websocket: WebSocket, session_id: str):
        """Handle WebSocket connection lifecycle."""
        await websocket.accept()

        session = VoiceAgentSession(self.config, session_id)
        self.sessions[session_id] = session

        logger.info(f"Session started: {session_id}")

        try:
            async for message in websocket.iter_text():
                event = json.loads(message)
                response = await self._handle_event(session, event)

                if response:
                    await websocket.send_json(response)

        except WebSocketDisconnect:
            logger.info(f"Session disconnected: {session_id}")
        except Exception as e:
            logger.error(f"Session error {session_id}: {e}")
        finally:
            del self.sessions[session_id]

    async def _handle_event(self, session: VoiceAgentSession, event: dict) -> Optional[dict]:
        """Handle incoming event."""
        event_type = event.get("type")

        if event_type == "transcript":
            transcript = event.get("text", "")
            response_text = await session.process_transcript(transcript)
            return {"type": "response", "text": response_text}

        elif event_type == "tool_call":
            tool_name = event.get("name")
            args = event.get("arguments", {})
            result = await session.handle_tool_call(tool_name, args)
            return {"type": "tool_result", "name": tool_name, "result": result}

        elif event_type == "end":
            return {"type": "session_end", "turns": session.turn_count}

        return None


# FastAPI integration
app = FastAPI()
agent_server: Optional[VoiceAgentServer] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent_server
    config = AgentConfig(
        name="Support Agent",
        system_prompt="You are a helpful support agent..."
    )
    agent_server = VoiceAgentServer(config)
    yield

app = FastAPI(lifespan=lifespan)

@app.websocket("/voice/{session_id}")
async def voice_endpoint(websocket: WebSocket, session_id: str):
    await agent_server.handle_connection(websocket, session_id)
```
