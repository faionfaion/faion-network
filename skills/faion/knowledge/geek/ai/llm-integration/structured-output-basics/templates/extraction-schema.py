"""
Pydantic schemas for structured extraction: entities, tasks with subtasks, invoices.

Usage (with OpenAI Structured Outputs):
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "user", "content": text}],
        response_format=ExtractionResult,
    )
    result: ExtractionResult = response.choices[0].message.parsed
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Entity(BaseModel):
    name: str = Field(description="Entity name as it appears in the text")
    type: str = Field(description="Entity type: person, company, location, or product")
    confidence: float = Field(ge=0, le=1, description="Confidence score 0.0-1.0")


class ExtractionResult(BaseModel):
    entities: List[Entity]
    summary: str = Field(description="One sentence summary of the text")
    language: str = Field(description="ISO 639-1 language code, e.g., 'en'")


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Subtask(BaseModel):
    title: str
    completed: bool = False


class Task(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    tags: List[str] = []
    subtasks: List[Subtask] = []
    estimated_hours: Optional[float] = Field(None, ge=0)


class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float


class Invoice(BaseModel):
    invoice_number: str
    date: str
    vendor_name: str
    customer_name: str
    items: List[InvoiceItem]
    subtotal: float
    tax: Optional[float] = None
    total: float
    currency: str = "USD"
