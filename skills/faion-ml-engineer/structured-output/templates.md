# Structured Output Templates

Reusable schema templates, Pydantic models, and configuration patterns.

## Base Schema Templates

### Entity Extraction Template

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class EntityType(str, Enum):
    """Common entity types for extraction."""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    DATE = "date"
    MONEY = "money"
    PERCENTAGE = "percentage"
    PRODUCT = "product"
    EVENT = "event"
    CONCEPT = "concept"

class Entity(BaseModel):
    """Single extracted entity."""
    text: str = Field(description="Entity text as it appears in source")
    type: EntityType = Field(description="Entity category")
    normalized: Optional[str] = Field(
        default=None,
        description="Normalized/canonical form of entity"
    )
    confidence: float = Field(
        ge=0, le=1, default=1.0,
        description="Extraction confidence score"
    )
    start_pos: Optional[int] = Field(
        default=None,
        description="Character position where entity starts"
    )
    metadata: Optional[dict] = Field(
        default=None,
        description="Additional entity-specific metadata"
    )

class EntityExtractionResult(BaseModel):
    """Complete entity extraction result."""
    entities: List[Entity] = Field(description="Extracted entities")
    source_text_hash: Optional[str] = Field(
        default=None,
        description="Hash of source text for caching"
    )
    model_used: Optional[str] = Field(
        default=None,
        description="Model that performed extraction"
    )
```

### Classification Template

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ClassificationResult(BaseModel):
    """Generic classification result."""
    label: str = Field(description="Primary classification label")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    secondary_labels: List[str] = Field(
        default=[],
        description="Alternative labels with lower confidence"
    )
    reasoning: Optional[str] = Field(
        default=None,
        description="Explanation for the classification"
    )

class MultiLabelClassification(BaseModel):
    """Multi-label classification result."""
    labels: List[str] = Field(description="All applicable labels")
    scores: dict = Field(
        description="Mapping of label to confidence score"
    )
    threshold: float = Field(
        default=0.5,
        description="Score threshold used for selection"
    )
```

### Sentiment Analysis Template

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class SentimentLabel(str, Enum):
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"
    MIXED = "mixed"

class AspectSentiment(BaseModel):
    """Sentiment for a specific aspect."""
    aspect: str = Field(description="The aspect being evaluated")
    sentiment: SentimentLabel
    confidence: float = Field(ge=0, le=1)
    evidence: Optional[str] = Field(
        default=None,
        description="Quote supporting this sentiment"
    )

class SentimentAnalysis(BaseModel):
    """Complete sentiment analysis result."""
    overall_sentiment: SentimentLabel
    overall_confidence: float = Field(ge=0, le=1)
    aspects: List[AspectSentiment] = Field(
        default=[],
        description="Sentiment by aspect/topic"
    )
    positive_highlights: List[str] = Field(
        default=[],
        description="Positive points mentioned"
    )
    negative_highlights: List[str] = Field(
        default=[],
        description="Negative points mentioned"
    )
    suggestions: List[str] = Field(
        default=[],
        description="Improvement suggestions if negative"
    )
```

### Summarization Template

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class KeyPoint(BaseModel):
    """A key point from the document."""
    point: str = Field(description="The key point")
    importance: str = Field(
        description="high, medium, or low importance"
    )
    source_section: Optional[str] = Field(
        default=None,
        description="Section where this point appears"
    )

class Summary(BaseModel):
    """Document summarization result."""
    title: Optional[str] = Field(
        default=None,
        description="Extracted or generated title"
    )
    one_line: str = Field(
        max_length=200,
        description="One-line summary (tweet-length)"
    )
    brief: str = Field(
        max_length=500,
        description="Brief summary (1-2 paragraphs)"
    )
    detailed: Optional[str] = Field(
        default=None,
        description="Detailed summary preserving key info"
    )
    key_points: List[KeyPoint] = Field(
        description="Main takeaways"
    )
    keywords: List[str] = Field(
        default=[],
        description="Important keywords/phrases"
    )
    target_audience: Optional[str] = Field(
        default=None,
        description="Who this content is for"
    )
    reading_time_minutes: Optional[int] = Field(
        default=None,
        description="Estimated reading time of original"
    )
```

## Domain-Specific Templates

### E-commerce Product Template

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from decimal import Decimal

class ProductCondition(str, Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    REFURBISHED = "refurbished"

class PriceInfo(BaseModel):
    """Product pricing information."""
    amount: float = Field(ge=0)
    currency: str = Field(default="USD", max_length=3)
    original_amount: Optional[float] = Field(
        default=None, ge=0,
        description="Original price if on sale"
    )
    discount_percentage: Optional[float] = Field(
        default=None, ge=0, le=100
    )

class ProductDimensions(BaseModel):
    """Physical product dimensions."""
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    unit_length: str = Field(default="inches")
    unit_weight: str = Field(default="pounds")

class ProductReview(BaseModel):
    """Product review summary."""
    rating: float = Field(ge=1, le=5)
    review_count: int = Field(ge=0)
    positive_mentions: List[str] = []
    negative_mentions: List[str] = []

class Product(BaseModel):
    """Complete product extraction template."""
    sku: Optional[str] = None
    name: str
    brand: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    description: str
    price: PriceInfo
    condition: ProductCondition = ProductCondition.NEW
    in_stock: bool = True
    quantity_available: Optional[int] = None
    features: List[str] = []
    specifications: dict = Field(default_factory=dict)
    dimensions: Optional[ProductDimensions] = None
    images: List[str] = Field(
        default=[],
        description="Image URLs"
    )
    reviews: Optional[ProductReview] = None
    tags: List[str] = []
    related_products: List[str] = []
```

### Support Ticket Template

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    PRODUCT = "product"
    SHIPPING = "shipping"
    RETURNS = "returns"
    GENERAL = "general"
    FEEDBACK = "feedback"

class CustomerSentiment(str, Enum):
    ANGRY = "angry"
    FRUSTRATED = "frustrated"
    NEUTRAL = "neutral"
    SATISFIED = "satisfied"
    HAPPY = "happy"

class SuggestedAction(BaseModel):
    """Recommended action for support."""
    action: str = Field(description="Action to take")
    reason: str = Field(description="Why this action")
    priority: int = Field(ge=1, le=5, description="1=highest priority")

class SupportTicket(BaseModel):
    """Customer support ticket extraction."""
    subject: str = Field(max_length=200)
    category: TicketCategory
    subcategory: Optional[str] = None
    priority: TicketPriority
    sentiment: CustomerSentiment
    summary: str = Field(
        max_length=500,
        description="Brief summary of the issue"
    )
    customer_request: str = Field(
        description="What the customer is asking for"
    )
    key_details: List[str] = Field(
        description="Important details from the ticket"
    )
    mentioned_products: List[str] = []
    mentioned_order_ids: List[str] = []
    mentioned_dates: List[str] = []
    is_complaint: bool
    is_urgent: bool
    requires_escalation: bool
    suggested_actions: List[SuggestedAction] = []
    suggested_response_template: Optional[str] = Field(
        default=None,
        description="Suggested reply template"
    )
```

### Meeting Notes Template

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ActionItemPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ActionItem(BaseModel):
    """Task extracted from meeting."""
    task: str
    assignee: Optional[str] = None
    due_date: Optional[str] = Field(
        default=None,
        description="Due date in YYYY-MM-DD format"
    )
    priority: ActionItemPriority = ActionItemPriority.MEDIUM
    context: Optional[str] = Field(
        default=None,
        description="Additional context for the task"
    )

class Decision(BaseModel):
    """Decision made during meeting."""
    decision: str
    rationale: Optional[str] = None
    made_by: Optional[str] = None
    impacts: List[str] = []

class DiscussionTopic(BaseModel):
    """Topic discussed in meeting."""
    topic: str
    summary: str
    key_points: List[str]
    participants: List[str] = []
    open_questions: List[str] = []

class MeetingNotes(BaseModel):
    """Complete meeting notes extraction."""
    title: str
    date: str = Field(description="Meeting date in YYYY-MM-DD format")
    time: Optional[str] = Field(
        default=None,
        description="Meeting time in HH:MM format"
    )
    duration_minutes: Optional[int] = None
    attendees: List[str]
    absent: List[str] = []
    facilitator: Optional[str] = None
    note_taker: Optional[str] = None
    summary: str = Field(
        max_length=500,
        description="Executive summary of the meeting"
    )
    topics: List[DiscussionTopic]
    action_items: List[ActionItem]
    decisions: List[Decision]
    follow_up_meeting: Optional[str] = Field(
        default=None,
        description="Next meeting date if scheduled"
    )
    attachments_mentioned: List[str] = []
    parking_lot: List[str] = Field(
        default=[],
        description="Items to discuss later"
    )
```

### Job Posting Template

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"

class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class WorkLocation(str, Enum):
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"

class SalaryRange(BaseModel):
    """Salary information."""
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    currency: str = "USD"
    period: str = Field(
        default="yearly",
        description="yearly, monthly, hourly"
    )

class Requirement(BaseModel):
    """Job requirement."""
    requirement: str
    is_required: bool = True
    years_experience: Optional[int] = None

class JobPosting(BaseModel):
    """Job posting extraction."""
    title: str
    company: str
    department: Optional[str] = None
    location: str
    work_location: WorkLocation
    employment_type: EmploymentType
    experience_level: ExperienceLevel
    salary: Optional[SalaryRange] = None
    description: str
    responsibilities: List[str]
    requirements: List[Requirement]
    nice_to_have: List[str] = []
    benefits: List[str] = []
    skills_required: List[str]
    skills_preferred: List[str] = []
    education_required: Optional[str] = None
    languages: List[str] = []
    travel_required: Optional[str] = None
    visa_sponsorship: Optional[bool] = None
    application_deadline: Optional[str] = None
    contact_email: Optional[str] = None
    company_description: Optional[str] = None
```

## Configuration Templates

### OpenAI Configuration

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class OpenAIConfig:
    """OpenAI API configuration."""
    model: str = "gpt-4o"
    max_tokens: int = 4096
    temperature: float = 0.0
    timeout: int = 60
    max_retries: int = 3
    api_key: Optional[str] = None  # From environment if None

    def get_client_kwargs(self) -> dict:
        kwargs = {"timeout": self.timeout, "max_retries": self.max_retries}
        if self.api_key:
            kwargs["api_key"] = self.api_key
        return kwargs

    def get_completion_kwargs(self) -> dict:
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
```

### Claude Configuration

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ClaudeConfig:
    """Anthropic Claude API configuration."""
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    temperature: float = 0.0
    timeout: int = 60
    api_key: Optional[str] = None

    def get_client_kwargs(self) -> dict:
        kwargs = {"timeout": self.timeout}
        if self.api_key:
            kwargs["api_key"] = self.api_key
        return kwargs

    def get_message_kwargs(self) -> dict:
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
        }
```

### Unified Extraction Configuration

```python
from dataclasses import dataclass
from typing import Optional, Type
from pydantic import BaseModel
from enum import Enum

class Provider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"

@dataclass
class ExtractionConfig:
    """Configuration for structured extraction."""
    provider: Provider = Provider.OPENAI
    model: str = "gpt-4o"
    temperature: float = 0.0
    max_tokens: int = 4096
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: int = 60
    validate_output: bool = True
    log_responses: bool = False

    # Provider-specific settings
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    local_model_path: Optional[str] = None

    def get_model_for_provider(self) -> str:
        """Get appropriate model name for configured provider."""
        if self.model:
            return self.model

        defaults = {
            Provider.OPENAI: "gpt-4o",
            Provider.ANTHROPIC: "claude-sonnet-4-20250514",
            Provider.GOOGLE: "gemini-2.0-flash",
            Provider.LOCAL: "mistral-7b",
        }
        return defaults[self.provider]
```

## Validator Templates

### Common Validators

```python
from pydantic import field_validator, model_validator
import re
from typing import Optional

class ValidatedModel(BaseModel):
    """Base model with common validators."""

    @field_validator('*', mode='before')
    @classmethod
    def strip_strings(cls, v):
        """Strip whitespace from all string fields."""
        if isinstance(v, str):
            return v.strip()
        return v

class DateValidatedModel(BaseModel):
    """Model with date validation."""
    date: str

    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v):
        """Validate ISO date format."""
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

class EmailValidatedModel(BaseModel):
    """Model with email validation."""
    email: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        if v is None:
            return v
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

class PhoneValidatedModel(BaseModel):
    """Model with phone validation."""
    phone: Optional[str] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Normalize phone number."""
        if v is None:
            return v
        # Remove all non-digits
        digits = re.sub(r'\D', '', v)
        if len(digits) < 10:
            raise ValueError('Phone number too short')
        return digits

class URLValidatedModel(BaseModel):
    """Model with URL validation."""
    url: Optional[str] = None

    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        """Validate URL format."""
        if v is None:
            return v
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(pattern, v):
            raise ValueError('Invalid URL format')
        return v
```

### Cross-Field Validators

```python
from pydantic import model_validator

class DateRangeModel(BaseModel):
    """Model with date range validation."""
    start_date: str
    end_date: Optional[str] = None

    @model_validator(mode='after')
    def validate_date_range(self):
        """Ensure end_date is after start_date."""
        if self.end_date and self.end_date < self.start_date:
            raise ValueError('end_date must be after start_date')
        return self

class PriceModel(BaseModel):
    """Model with price calculation validation."""
    quantity: float
    unit_price: float
    total: float

    @model_validator(mode='after')
    def validate_total(self):
        """Verify total matches calculation."""
        expected = self.quantity * self.unit_price
        if abs(self.total - expected) > 0.01:
            # Auto-correct instead of raising error
            self.total = round(expected, 2)
        return self

class ConfidenceModel(BaseModel):
    """Model requiring confidence for uncertain fields."""
    value: Optional[str] = None
    confidence: float = Field(ge=0, le=1, default=1.0)

    @model_validator(mode='after')
    def validate_confidence_consistency(self):
        """Require lower confidence if value is None."""
        if self.value is None and self.confidence > 0.5:
            self.confidence = 0.0
        return self
```

## JSON Schema Templates

### Generic Entity Schema

```json
{
  "type": "object",
  "properties": {
    "entities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "text": {"type": "string"},
          "type": {
            "type": "string",
            "enum": ["person", "organization", "location", "date", "money"]
          },
          "confidence": {"type": "number", "minimum": 0, "maximum": 1}
        },
        "required": ["text", "type"]
      }
    }
  },
  "required": ["entities"]
}
```

### Generic Classification Schema

```json
{
  "type": "object",
  "properties": {
    "label": {"type": "string"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "reasoning": {"type": "string"}
  },
  "required": ["label", "confidence"]
}
```

### Generic Extraction Schema

```json
{
  "type": "object",
  "properties": {
    "extracted_data": {
      "type": "object",
      "additionalProperties": true
    },
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "missing_fields": {
      "type": "array",
      "items": {"type": "string"}
    }
  },
  "required": ["extracted_data"]
}
```

## Factory Functions

### Schema Factory

```python
from pydantic import BaseModel, Field, create_model
from typing import List, Optional, Any, Type

def create_extraction_model(
    name: str,
    fields: dict,
    optional_fields: dict = None,
    add_confidence: bool = False,
    add_metadata: bool = False
) -> Type[BaseModel]:
    """
    Dynamically create an extraction model.

    Args:
        name: Model class name
        fields: Required fields as {name: (type, Field())}
        optional_fields: Optional fields
        add_confidence: Add confidence score field
        add_metadata: Add metadata dict field
    """
    field_definitions = {}

    for field_name, field_def in fields.items():
        if isinstance(field_def, tuple):
            field_definitions[field_name] = field_def
        else:
            field_definitions[field_name] = (field_def, ...)

    if optional_fields:
        for field_name, field_def in optional_fields.items():
            if isinstance(field_def, tuple):
                field_definitions[field_name] = field_def
            else:
                field_definitions[field_name] = (Optional[field_def], None)

    if add_confidence:
        field_definitions['extraction_confidence'] = (
            float,
            Field(ge=0, le=1, default=1.0)
        )

    if add_metadata:
        field_definitions['metadata'] = (
            Optional[dict],
            Field(default=None)
        )

    return create_model(name, **field_definitions)

# Usage
ProductModel = create_extraction_model(
    'Product',
    fields={
        'name': str,
        'price': (float, Field(ge=0)),
        'features': List[str]
    },
    optional_fields={
        'brand': str,
        'category': str
    },
    add_confidence=True
)
```

### Extractor Factory

```python
from typing import Type, TypeVar, Callable
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

def create_extractor(
    model: Type[T],
    system_prompt: str = None,
    provider: str = "openai"
) -> Callable[[str], T]:
    """
    Create an extraction function for a given model.

    Args:
        model: Pydantic model for output
        system_prompt: System prompt for extraction
        provider: LLM provider to use
    """
    default_prompt = f"Extract {model.__name__} data from the provided text."
    prompt = system_prompt or default_prompt

    if provider == "openai":
        from openai import OpenAI
        client = OpenAI()

        def extract(text: str) -> T:
            response = client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                response_format=model
            )
            return response.choices[0].message.parsed

    elif provider == "anthropic":
        from anthropic import Anthropic
        import json
        client = Anthropic()

        def extract(text: str) -> T:
            schema = model.model_json_schema()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                tools=[{
                    "name": "submit_result",
                    "description": "Submit extracted data",
                    "input_schema": schema
                }],
                tool_choice={"type": "tool", "name": "submit_result"},
                messages=[
                    {"role": "user", "content": f"{prompt}\n\nText:\n{text}"}
                ]
            )
            for block in response.content:
                if block.type == "tool_use":
                    return model.model_validate(block.input)

    else:
        raise ValueError(f"Unknown provider: {provider}")

    return extract

# Usage
from pydantic import BaseModel

class Contact(BaseModel):
    name: str
    email: str

extract_contact = create_extractor(Contact)
contact = extract_contact("John Smith can be reached at john@example.com")
```

## Utility Templates

### Response Wrapper

```python
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional
from datetime import datetime

T = TypeVar('T')

class ExtractionResponse(BaseModel, Generic[T]):
    """Standard wrapper for extraction responses."""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    model_used: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[int] = None
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    @classmethod
    def ok(cls, data: T, model: str, tokens: int = None, latency: int = None):
        return cls(
            success=True,
            data=data,
            model_used=model,
            tokens_used=tokens,
            latency_ms=latency
        )

    @classmethod
    def fail(cls, error: str, model: str):
        return cls(
            success=False,
            error=error,
            model_used=model
        )
```

### Batch Processing Template

```python
from pydantic import BaseModel
from typing import List, Generic, TypeVar

T = TypeVar('T')

class BatchItem(BaseModel, Generic[T]):
    """Single item in batch processing."""
    index: int
    input_text: str
    result: Optional[T] = None
    error: Optional[str] = None
    success: bool = False

class BatchResult(BaseModel, Generic[T]):
    """Complete batch processing result."""
    total: int
    successful: int
    failed: int
    items: List[BatchItem[T]]

    @property
    def success_rate(self) -> float:
        return self.successful / self.total if self.total > 0 else 0

    def get_successful(self) -> List[T]:
        return [item.result for item in self.items if item.success]

    def get_failed(self) -> List[tuple[int, str]]:
        return [
            (item.index, item.error)
            for item in self.items
            if not item.success
        ]
```

### Caching Template

```python
from pydantic import BaseModel
from typing import Optional, TypeVar, Generic
import hashlib
import json
from datetime import datetime, timedelta

T = TypeVar('T')

class CachedExtraction(BaseModel, Generic[T]):
    """Cached extraction result."""
    input_hash: str
    result: T
    created_at: datetime
    expires_at: datetime
    model_used: str

    @classmethod
    def create(
        cls,
        input_text: str,
        result: T,
        model: str,
        ttl_hours: int = 24
    ):
        input_hash = hashlib.sha256(input_text.encode()).hexdigest()[:16]
        now = datetime.utcnow()
        return cls(
            input_hash=input_hash,
            result=result,
            created_at=now,
            expires_at=now + timedelta(hours=ttl_hours),
            model_used=model
        )

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

class ExtractionCache:
    """Simple in-memory cache for extractions."""

    def __init__(self):
        self._cache: dict[str, CachedExtraction] = {}

    def get(self, input_text: str) -> Optional[CachedExtraction]:
        hash_key = hashlib.sha256(input_text.encode()).hexdigest()[:16]
        cached = self._cache.get(hash_key)
        if cached and not cached.is_expired:
            return cached
        return None

    def set(self, cached: CachedExtraction):
        self._cache[cached.input_hash] = cached

    def clear_expired(self):
        self._cache = {
            k: v for k, v in self._cache.items()
            if not v.is_expired
        }
```
