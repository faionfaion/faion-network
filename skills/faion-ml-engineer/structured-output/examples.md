# Structured Output Examples

Comprehensive code examples for implementing structured output across different LLM providers.

## OpenAI Examples

### Basic JSON Mode

```python
from openai import OpenAI
import json

client = OpenAI()

def extract_with_json_mode(text: str) -> dict:
    """Extract structured data using JSON mode."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """Extract entities from text. Return JSON with this structure:
{
    "entities": [
        {"name": "string", "type": "string", "context": "string"}
    ]
}"""
            },
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)

# Usage
result = extract_with_json_mode(
    "Apple CEO Tim Cook announced a new iPhone model at their Cupertino headquarters."
)
print(result)
# {"entities": [
#     {"name": "Apple", "type": "company", "context": "technology company"},
#     {"name": "Tim Cook", "type": "person", "context": "CEO of Apple"},
#     {"name": "iPhone", "type": "product", "context": "mobile device"},
#     {"name": "Cupertino", "type": "location", "context": "headquarters location"}
# ]}
```

### Native Structured Output with Pydantic

```python
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

client = OpenAI()

class EntityType(str, Enum):
    PERSON = "person"
    COMPANY = "company"
    LOCATION = "location"
    PRODUCT = "product"
    EVENT = "event"

class Entity(BaseModel):
    """An extracted entity from text."""
    name: str = Field(description="The entity name as it appears in text")
    type: EntityType = Field(description="The category of entity")
    confidence: float = Field(
        ge=0, le=1,
        description="Confidence score from 0 to 1"
    )
    context: Optional[str] = Field(
        default=None,
        description="Brief context about this entity"
    )

class ExtractionResult(BaseModel):
    """Complete extraction result with entities and metadata."""
    entities: List[Entity] = Field(description="List of extracted entities")
    summary: str = Field(description="One sentence summary of the text")
    language: str = Field(default="en", description="ISO language code")
    sentiment: str = Field(description="Overall sentiment: positive, negative, neutral")

def extract_structured(text: str) -> ExtractionResult:
    """Extract data with guaranteed schema compliance."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract entities and provide analysis of the text."
            },
            {"role": "user", "content": text}
        ],
        response_format=ExtractionResult
    )

    # Check for refusal
    if response.choices[0].message.refusal:
        raise ValueError(f"Model refused: {response.choices[0].message.refusal}")

    return response.choices[0].message.parsed

# Usage
result = extract_structured(
    "Elon Musk visited Berlin to open a new Tesla factory, "
    "creating over 10,000 jobs in the region."
)

print(f"Found {len(result.entities)} entities")
for entity in result.entities:
    print(f"  - {entity.name} ({entity.type.value}): {entity.confidence:.2f}")
print(f"Summary: {result.summary}")
print(f"Sentiment: {result.sentiment}")
```

### Function Calling for Structured Output

```python
from openai import OpenAI
import json

client = OpenAI()

def get_structured_via_function(prompt: str, schema: dict) -> dict:
    """Use function calling to enforce output structure."""
    tools = [{
        "type": "function",
        "function": {
            "name": "return_structured_data",
            "description": "Return the extracted/processed data in structured format",
            "parameters": schema
        }
    }]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "return_structured_data"}}
    )

    tool_call = response.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)

# Schema definition
sentiment_schema = {
    "type": "object",
    "properties": {
        "sentiment": {
            "type": "string",
            "enum": ["positive", "negative", "neutral", "mixed"]
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
        },
        "topics": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Main topics discussed"
        },
        "key_phrases": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Important phrases from the text"
        },
        "urgency": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5,
            "description": "Urgency level from 1 (low) to 5 (critical)"
        }
    },
    "required": ["sentiment", "confidence", "topics", "urgency"]
}

# Usage
result = get_structured_via_function(
    "Analyze this customer feedback: 'The product is amazing! "
    "However, the shipping took way too long and I almost cancelled my order. "
    "Please improve delivery times!'",
    sentiment_schema
)

print(json.dumps(result, indent=2))
```

### Streaming with Structured Output

```python
from openai import OpenAI
from pydantic import BaseModel
from typing import List

client = OpenAI()

class Step(BaseModel):
    explanation: str
    output: str

class MathSolution(BaseModel):
    steps: List[Step]
    final_answer: str

def solve_math_streaming(problem: str):
    """Solve math problem with streaming structured output."""
    with client.beta.chat.completions.stream(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Solve the math problem step by step."},
            {"role": "user", "content": problem}
        ],
        response_format=MathSolution
    ) as stream:
        for event in stream:
            if event.type == "content.delta":
                print(event.delta, end="", flush=True)

        # Get final parsed result
        response = stream.get_final_completion()
        return response.choices[0].message.parsed

# Usage
solution = solve_math_streaming("What is 25 * 47 + 183?")
print(f"\n\nFinal answer: {solution.final_answer}")
```

## Anthropic (Claude) Examples

### Prompt-Based JSON Extraction

```python
from anthropic import Anthropic
import json

client = Anthropic()

def extract_with_claude(text: str, schema: dict) -> dict:
    """Extract structured data using Claude with prompt engineering."""
    schema_str = json.dumps(schema, indent=2)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""Extract information from the following text and return valid JSON matching this schema:

Schema:
```json
{schema_str}
```

Text to analyze:
{text}

Important:
- Return ONLY valid JSON, no other text
- Include all required fields
- Use null for fields that cannot be determined
- Follow the exact structure specified"""
            }
        ]
    )

    content = response.content[0].text

    # Handle markdown code blocks
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]

    return json.loads(content.strip())

# Schema
product_schema = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "price": {"type": "number"},
        "currency": {"type": "string"},
        "features": {
            "type": "array",
            "items": {"type": "string"}
        },
        "availability": {
            "type": "string",
            "enum": ["in_stock", "out_of_stock", "preorder"]
        }
    },
    "required": ["product_name", "price"]
}

# Usage
result = extract_with_claude(
    "The new MacBook Pro M3 costs $1,999 and features an incredible display, "
    "all-day battery life, and the fastest chip ever in a Mac. "
    "Available now at Apple stores.",
    product_schema
)
print(json.dumps(result, indent=2))
```

### Tool Use for Structured Output

```python
from anthropic import Anthropic
import json

client = Anthropic()

def extract_via_tool(text: str, output_schema: dict) -> dict:
    """Use Claude's tool use for guaranteed structured output."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        tools=[
            {
                "name": "submit_extraction",
                "description": "Submit the extracted structured data",
                "input_schema": output_schema
            }
        ],
        tool_choice={"type": "tool", "name": "submit_extraction"},
        messages=[
            {
                "role": "user",
                "content": f"Extract information from this text:\n\n{text}"
            }
        ]
    )

    # Find the tool use block
    for block in response.content:
        if block.type == "tool_use":
            return block.input

    raise ValueError("No tool use in response")

# Schema for extraction
meeting_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "Meeting title or subject"
        },
        "date": {
            "type": "string",
            "description": "Meeting date in YYYY-MM-DD format"
        },
        "time": {
            "type": "string",
            "description": "Meeting time in HH:MM format"
        },
        "participants": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of participant names"
        },
        "action_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"},
                    "assignee": {"type": "string"},
                    "due_date": {"type": "string"}
                },
                "required": ["task"]
            }
        },
        "decisions": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["title", "participants"]
}

# Usage
meeting_notes = """
Project Alpha Status Meeting - January 15, 2025 at 2:00 PM

Attendees: Sarah Chen, Mike Johnson, Lisa Park, David Kim

Discussion:
- Sarah presented the Q4 results showing 15% growth
- Mike raised concerns about the delayed API integration
- Lisa confirmed the design mockups are ready for review

Action Items:
- Mike to complete API integration by January 22
- Lisa to share design files with development team by EOD
- David to schedule client demo for next week

Decisions:
- Approved budget increase of $10,000 for additional testing
- Decided to postpone the mobile app launch to February
"""

result = extract_via_tool(meeting_notes, meeting_schema)
print(json.dumps(result, indent=2))
```

### Claude with Instructor Library

```python
import instructor
from anthropic import Anthropic
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

# Patch the client
client = instructor.from_anthropic(Anthropic())

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Task(BaseModel):
    """An extracted task from text."""
    title: str = Field(description="Brief task title")
    description: Optional[str] = Field(default=None, description="Task details")
    priority: Priority = Field(description="Task priority level")
    assignee: Optional[str] = Field(default=None, description="Person responsible")
    due_date: Optional[str] = Field(default=None, description="Due date if mentioned")

class TaskList(BaseModel):
    """List of tasks extracted from text."""
    tasks: List[Task]
    source_summary: str = Field(description="Brief summary of the source text")

def extract_tasks(text: str) -> TaskList:
    """Extract tasks using instructor with Claude."""
    return client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"Extract all tasks from this text:\n\n{text}"
            }
        ],
        response_model=TaskList
    )

# Usage
email = """
Hi team,

Following up on our meeting:

1. John needs to urgently fix the payment processing bug before EOD Friday
2. Marketing should prepare the launch announcement for next Tuesday
3. Someone should look into the customer complaints about slow loading -
   it's not urgent but we should address it eventually
4. Critical: We need Sarah to review the security audit findings immediately

Thanks,
Manager
"""

result = extract_tasks(email)
print(f"Source: {result.source_summary}\n")
for task in result.tasks:
    print(f"[{task.priority.value.upper()}] {task.title}")
    if task.assignee:
        print(f"  Assignee: {task.assignee}")
    if task.due_date:
        print(f"  Due: {task.due_date}")
```

## Google Gemini Examples

### Native JSON Mode

```python
import google.generativeai as genai
import json

genai.configure(api_key="YOUR_API_KEY")

def extract_with_gemini(text: str, schema: dict) -> dict:
    """Extract structured data using Gemini's JSON mode."""
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(
        f"Extract information from this text:\n\n{text}",
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=schema
        )
    )

    return json.loads(response.text)

# Schema (using Gemini's format)
article_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "author": {"type": "string"},
        "publication_date": {"type": "string"},
        "main_topics": {
            "type": "array",
            "items": {"type": "string"}
        },
        "key_points": {
            "type": "array",
            "items": {"type": "string"}
        },
        "word_count_estimate": {"type": "integer"}
    },
    "required": ["title", "main_topics", "key_points"]
}

# Usage
article_text = """
The Future of AI in Healthcare
By Dr. Jane Smith | Published March 15, 2024

Artificial intelligence is revolutionizing healthcare in unprecedented ways.
From early disease detection to personalized treatment plans, AI systems
are becoming essential tools for medical professionals.

Key developments include:
- AI-powered diagnostic imaging that detects cancers earlier
- Predictive analytics for patient outcomes
- Drug discovery acceleration through machine learning
- Virtual health assistants for patient care

While challenges remain around privacy and regulatory approval, the
trajectory is clear: AI will become a fundamental part of modern medicine.
"""

result = extract_with_gemini(article_text, article_schema)
print(json.dumps(result, indent=2))
```

### Gemini with Pydantic via Instructor

```python
import google.generativeai as genai
import instructor
from pydantic import BaseModel, Field
from typing import List, Optional

# Configure Gemini
genai.configure(api_key="YOUR_API_KEY")

# Create instructor client
client = instructor.from_gemini(
    client=genai.GenerativeModel("gemini-2.0-flash")
)

class Ingredient(BaseModel):
    name: str
    quantity: str
    unit: Optional[str] = None

class Recipe(BaseModel):
    name: str = Field(description="Recipe name")
    servings: int = Field(description="Number of servings")
    prep_time_minutes: int = Field(description="Preparation time in minutes")
    cook_time_minutes: int = Field(description="Cooking time in minutes")
    ingredients: List[Ingredient] = Field(description="List of ingredients")
    instructions: List[str] = Field(description="Step-by-step instructions")
    difficulty: str = Field(description="easy, medium, or hard")

def parse_recipe(text: str) -> Recipe:
    """Parse a recipe from natural language text."""
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Parse this recipe:\n\n{text}"
            }
        ],
        response_model=Recipe
    )

# Usage
recipe_text = """
Grandma's Chocolate Chip Cookies

Makes about 24 cookies. Takes 15 minutes to prep and 12 minutes to bake.

You'll need:
- 2 1/4 cups flour
- 1 cup butter, softened
- 3/4 cup sugar
- 2 eggs
- 1 tsp vanilla
- 2 cups chocolate chips

Mix butter and sugar until fluffy. Add eggs and vanilla. Gradually mix in flour.
Fold in chocolate chips. Drop spoonfuls onto baking sheet. Bake at 375F for
10-12 minutes until golden.
"""

recipe = parse_recipe(recipe_text)
print(f"Recipe: {recipe.name}")
print(f"Difficulty: {recipe.difficulty}")
print(f"Time: {recipe.prep_time_minutes + recipe.cook_time_minutes} minutes total")
print(f"\nIngredients ({len(recipe.ingredients)}):")
for ing in recipe.ingredients:
    print(f"  - {ing.quantity} {ing.unit or ''} {ing.name}")
```

## Local Models with Outlines

### Basic JSON Generation

```python
import outlines
from pydantic import BaseModel, Field
from typing import List
from enum import Enum

# Load model
model = outlines.models.transformers("mistralai/Mistral-7B-Instruct-v0.2")

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class SentimentAnalysis(BaseModel):
    sentiment: Sentiment
    confidence: float = Field(ge=0, le=1)
    reasoning: str

# Create generator with schema constraint
generator = outlines.generate.json(model, SentimentAnalysis)

def analyze_sentiment(text: str) -> SentimentAnalysis:
    """Analyze sentiment with guaranteed schema compliance."""
    prompt = f"""Analyze the sentiment of the following text.

Text: {text}

Provide your analysis:"""

    return generator(prompt)

# Usage
result = analyze_sentiment("I absolutely love this product! Best purchase ever!")
print(f"Sentiment: {result.sentiment.value}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Reasoning: {result.reasoning}")
```

### Regex-Constrained Generation

```python
import outlines

model = outlines.models.transformers("mistralai/Mistral-7B-Instruct-v0.2")

# Generate valid email
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
email_generator = outlines.generate.regex(model, email_pattern)

# Generate valid date
date_pattern = r"\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])"
date_generator = outlines.generate.regex(model, date_pattern)

# Generate valid phone number
phone_pattern = r"\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
phone_generator = outlines.generate.regex(model, phone_pattern)

def extract_contact_info(text: str) -> dict:
    """Extract contact info with regex-guaranteed formats."""
    email_prompt = f"Extract the email address from: {text}\nEmail:"
    date_prompt = f"What date is mentioned in: {text}\nDate (YYYY-MM-DD):"

    return {
        "email": email_generator(email_prompt),
        "date": date_generator(date_prompt)
    }
```

### Grammar-Based Generation

```python
import outlines

model = outlines.models.transformers("mistralai/Mistral-7B-Instruct-v0.2")

# Define grammar for SQL SELECT statements
sql_grammar = r"""
?start: select_statement

select_statement: "SELECT" columns "FROM" table where_clause? order_clause? limit_clause?

columns: "*" | column_list
column_list: column ("," column)*
column: IDENTIFIER

table: IDENTIFIER

where_clause: "WHERE" condition
condition: column operator value
operator: "=" | "!=" | ">" | "<" | ">=" | "<=" | "LIKE"
value: STRING | NUMBER

order_clause: "ORDER BY" column ("ASC" | "DESC")?

limit_clause: "LIMIT" NUMBER

IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
STRING: /"[^"]*"/ | /'[^']*'/
NUMBER: /[0-9]+/

%import common.WS
%ignore WS
"""

sql_generator = outlines.generate.cfg(model, sql_grammar)

def generate_sql(natural_language: str) -> str:
    """Generate valid SQL from natural language."""
    prompt = f"""Convert this request to SQL:

Request: {natural_language}

SQL:"""

    return sql_generator(prompt)

# Usage
sql = generate_sql("Get all users from the users table where age is greater than 18")
print(sql)  # Guaranteed to be valid SQL syntax
```

## Complex Schema Examples

### Invoice Extraction

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from decimal import Decimal
import re

class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = "USA"

class ContactInfo(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[Address] = None

class LineItem(BaseModel):
    description: str
    quantity: float = Field(ge=0)
    unit_price: float = Field(ge=0)
    total: float = Field(ge=0)

    @field_validator('total')
    @classmethod
    def validate_total(cls, v, info):
        expected = info.data.get('quantity', 0) * info.data.get('unit_price', 0)
        if abs(v - expected) > 0.01:  # Allow small rounding errors
            return expected
        return v

class Invoice(BaseModel):
    invoice_number: str
    date: str = Field(description="Invoice date in YYYY-MM-DD format")
    due_date: Optional[str] = None
    vendor: ContactInfo
    customer: ContactInfo
    items: List[LineItem] = Field(min_length=1)
    subtotal: float
    tax_rate: Optional[float] = Field(default=None, ge=0, le=1)
    tax_amount: Optional[float] = None
    discount: Optional[float] = Field(default=None, ge=0)
    total: float
    currency: str = "USD"
    payment_terms: Optional[str] = None
    notes: Optional[str] = None

    @field_validator('date', 'due_date')
    @classmethod
    def validate_date_format(cls, v):
        if v and not re.match(r'\d{4}-\d{2}-\d{2}', v):
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

def extract_invoice(document_text: str, client) -> Invoice:
    """Extract invoice from document text."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract invoice details. Calculate totals if not explicitly stated."
            },
            {"role": "user", "content": f"Extract invoice:\n\n{document_text}"}
        ],
        response_format=Invoice
    )

    return response.choices[0].message.parsed
```

### API Response Extraction

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from enum import Enum

class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class ParameterLocation(str, Enum):
    PATH = "path"
    QUERY = "query"
    HEADER = "header"
    BODY = "body"

class Parameter(BaseModel):
    name: str
    location: ParameterLocation
    type: str = Field(description="Data type: string, integer, boolean, array, object")
    required: bool = True
    description: Optional[str] = None
    example: Optional[str] = None

class Response(BaseModel):
    status_code: int
    description: str
    schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON Schema of response body"
    )

class Endpoint(BaseModel):
    path: str = Field(description="API path like /users/{id}")
    method: HTTPMethod
    summary: str
    description: Optional[str] = None
    parameters: List[Parameter] = []
    request_body: Optional[Dict[str, Any]] = None
    responses: List[Response]
    tags: List[str] = []
    requires_auth: bool = False

class APISpecification(BaseModel):
    title: str
    version: str
    base_url: str
    description: Optional[str] = None
    endpoints: List[Endpoint]

def extract_api_spec(documentation: str, client) -> APISpecification:
    """Extract API specification from documentation."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract API specification from documentation. Be thorough with parameters and responses."
            },
            {"role": "user", "content": f"Extract API spec:\n\n{documentation}"}
        ],
        response_format=APISpecification
    )

    return response.choices[0].message.parsed
```

### Resume/CV Extraction

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class EducationLevel(str, Enum):
    HIGH_SCHOOL = "high_school"
    ASSOCIATE = "associate"
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTORATE = "doctorate"
    CERTIFICATE = "certificate"

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    level: EducationLevel
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0, le=4)
    honors: Optional[str] = None

class WorkExperience(BaseModel):
    company: str
    title: str
    location: Optional[str] = None
    start_date: str
    end_date: Optional[str] = Field(default=None, description="null if current position")
    is_current: bool = False
    responsibilities: List[str]
    achievements: List[str] = []
    technologies: List[str] = []

class Skill(BaseModel):
    name: str
    category: str = Field(description="e.g., programming, soft skills, tools")
    proficiency: Optional[str] = Field(
        default=None,
        description="beginner, intermediate, advanced, expert"
    )
    years_experience: Optional[int] = None

class Certification(BaseModel):
    name: str
    issuing_organization: str
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None

class Resume(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    summary: Optional[str] = Field(
        default=None,
        description="Professional summary or objective"
    )
    education: List[Education]
    work_experience: List[WorkExperience]
    skills: List[Skill]
    certifications: List[Certification] = []
    languages: List[str] = []
    total_years_experience: Optional[int] = None

def parse_resume(resume_text: str, client) -> Resume:
    """Parse resume from text."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """Parse this resume thoroughly.
- Extract ALL work experiences and education entries
- Identify technologies and skills from job descriptions
- Calculate total years of experience
- Be comprehensive with responsibilities and achievements"""
            },
            {"role": "user", "content": resume_text}
        ],
        response_format=Resume
    )

    return response.choices[0].message.parsed
```

## Error Handling Examples

### Retry with Validation

```python
from pydantic import BaseModel, ValidationError
from typing import TypeVar, Type
import json
import time

T = TypeVar("T", bound=BaseModel)

def extract_with_retry(
    prompt: str,
    model: Type[T],
    client,
    max_retries: int = 3,
    delay: float = 1.0
) -> T:
    """Extract structured data with validation retry."""
    errors = []

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            data = json.loads(content)
            return model.model_validate(data)

        except json.JSONDecodeError as e:
            errors.append(f"JSON parse error: {e}")
        except ValidationError as e:
            errors.append(f"Validation error: {e}")

        if attempt < max_retries - 1:
            time.sleep(delay * (attempt + 1))  # Exponential backoff

    raise ValueError(f"Failed after {max_retries} attempts. Errors: {errors}")
```

### Graceful Degradation

```python
from pydantic import BaseModel
from typing import Optional, Any
import json

class ExtractionResult(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    raw_response: Optional[str] = None

def safe_extract(prompt: str, schema: BaseModel, client) -> ExtractionResult:
    """Extract with graceful error handling."""
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format=schema
        )

        if response.choices[0].message.refusal:
            return ExtractionResult(
                success=False,
                error=f"Model refused: {response.choices[0].message.refusal}"
            )

        return ExtractionResult(
            success=True,
            data=response.choices[0].message.parsed.model_dump()
        )

    except Exception as e:
        return ExtractionResult(
            success=False,
            error=str(e)
        )
```

## Batch Processing Example

```python
import asyncio
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import List

client = AsyncOpenAI()

class DocumentSummary(BaseModel):
    title: str
    main_points: List[str]
    word_count: int

async def process_document(doc: str) -> DocumentSummary:
    """Process single document."""
    response = await client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Summarize:\n\n{doc}"}
        ],
        response_format=DocumentSummary
    )
    return response.choices[0].message.parsed

async def process_batch(
    documents: List[str],
    concurrency: int = 5
) -> List[DocumentSummary]:
    """Process multiple documents with controlled concurrency."""
    semaphore = asyncio.Semaphore(concurrency)

    async def process_with_limit(doc: str):
        async with semaphore:
            return await process_document(doc)

    tasks = [process_with_limit(doc) for doc in documents]
    return await asyncio.gather(*tasks)

# Usage
async def main():
    documents = [
        "Document 1 content...",
        "Document 2 content...",
        "Document 3 content...",
    ]
    results = await process_batch(documents)
    for i, result in enumerate(results):
        print(f"Doc {i+1}: {result.title}")

asyncio.run(main())
```
