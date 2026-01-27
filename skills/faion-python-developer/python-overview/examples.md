# Python Project Examples

Real-world Python project examples across different domains.

---

## FastAPI REST API

### Project Structure

```
fastapi-project/
├── pyproject.toml
├── src/
│   └── api/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── dependencies.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── routes/
│       │   ├── __init__.py
│       │   └── users.py
│       └── services/
│           ├── __init__.py
│           └── user_service.py
└── tests/
    ├── conftest.py
    └── test_users.py
```

### Main Application

```python
# src/api/main.py
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from api.config import settings
from api.routes import users


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager."""
    # Startup
    print(f"Starting {settings.app_name}")
    yield
    # Shutdown
    print("Shutting down")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
```

### Configuration

```python
# src/api/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "FastAPI App"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "change-me-in-production"


settings = Settings()
```

### Pydantic Models

```python
# src/api/models/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    name: str = Field(min_length=1, max_length=100)


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(min_length=8)


class UserResponse(UserBase):
    """User response schema."""

    id: int
    created_at: datetime
    is_active: bool = True

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """User update schema."""

    email: EmailStr | None = None
    name: str | None = Field(default=None, min_length=1, max_length=100)
```

### Routes

```python
# src/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_user_service
from api.models.user import UserCreate, UserResponse, UserUpdate
from api.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Create a new user."""
    user = await service.create_user(user_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Get user by ID."""
    user = await service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update user by ID."""
    user = await service.update_user(user_id, user_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
```

### Service Layer

```python
# src/api/services/user_service.py
from api.models.user import UserCreate, UserResponse, UserUpdate


class UserService:
    """User service with business logic."""

    def __init__(self) -> None:
        # In real app: inject database session
        self._users: dict[int, dict] = {}
        self._counter = 0

    async def create_user(self, data: UserCreate) -> UserResponse | None:
        """Create a new user."""
        # Check for existing email
        for user in self._users.values():
            if user["email"] == data.email:
                return None

        self._counter += 1
        from datetime import datetime, UTC

        user = {
            "id": self._counter,
            "email": data.email,
            "name": data.name,
            "created_at": datetime.now(UTC),
            "is_active": True,
        }
        self._users[self._counter] = user
        return UserResponse(**user)

    async def get_user(self, user_id: int) -> UserResponse | None:
        """Get user by ID."""
        user = self._users.get(user_id)
        if user is None:
            return None
        return UserResponse(**user)

    async def update_user(
        self, user_id: int, data: UserUpdate
    ) -> UserResponse | None:
        """Update user by ID."""
        user = self._users.get(user_id)
        if user is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        user.update(update_data)
        return UserResponse(**user)
```

### Tests

```python
# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Create test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# tests/test_users.py
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    """Test user creation."""
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient) -> None:
    """Test getting non-existent user."""
    response = await client.get("/api/v1/users/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """Test health endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

---

## CLI Application with Typer

### Project Structure

```
cli-project/
├── pyproject.toml
├── src/
│   └── mycli/
│       ├── __init__.py
│       ├── main.py
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── init.py
│       │   └── run.py
│       └── utils/
│           ├── __init__.py
│           └── config.py
└── tests/
    └── test_cli.py
```

### Main CLI

```python
# src/mycli/main.py
import typer

from mycli.commands import init, run

app = typer.Typer(
    name="mycli",
    help="My awesome CLI tool.",
    add_completion=False,
)

app.add_typer(init.app, name="init")
app.add_typer(run.app, name="run")


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Main callback for global options."""
    if verbose:
        typer.echo("Verbose mode enabled")


if __name__ == "__main__":
    app()
```

### Init Command

```python
# src/mycli/commands/init.py
from pathlib import Path

import typer

app = typer.Typer(help="Initialize a new project.")


@app.callback(invoke_without_command=True)
def init_project(
    name: str = typer.Argument(..., help="Project name"),
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-p",
        help="Target directory",
    ),
    template: str = typer.Option(
        "default",
        "--template",
        "-t",
        help="Project template",
    ),
) -> None:
    """Initialize a new project with the given name."""
    project_path = path / name

    if project_path.exists():
        typer.echo(f"Error: {project_path} already exists", err=True)
        raise typer.Exit(1)

    project_path.mkdir(parents=True)
    (project_path / "README.md").write_text(f"# {name}\n")
    (project_path / "src").mkdir()
    (project_path / "tests").mkdir()

    typer.echo(f"Created project: {project_path}")
    typer.echo(f"Template: {template}")
```

### Run Command

```python
# src/mycli/commands/run.py
from pathlib import Path

import typer

app = typer.Typer(help="Run project commands.")


@app.command()
def dev(
    port: int = typer.Option(8000, "--port", "-p", help="Port number"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="Auto-reload"),
) -> None:
    """Run development server."""
    typer.echo(f"Starting dev server on port {port}")
    typer.echo(f"Auto-reload: {reload}")


@app.command()
def build(
    output: Path = typer.Option(
        Path("dist"),
        "--output",
        "-o",
        help="Output directory",
    ),
    minify: bool = typer.Option(False, "--minify", "-m", help="Minify output"),
) -> None:
    """Build project for production."""
    output.mkdir(parents=True, exist_ok=True)
    typer.echo(f"Building to: {output}")
    if minify:
        typer.echo("Minification enabled")
    typer.echo("Build complete!")
```

---

## Data Processing with Polars

### ETL Pipeline Example

```python
# src/etl/pipeline.py
from pathlib import Path
from typing import TypedDict

import polars as pl


class SalesRecord(TypedDict):
    """Sales record type."""

    date: str
    product_id: str
    quantity: int
    price: float
    region: str


def load_sales_data(path: Path) -> pl.DataFrame:
    """Load sales data from CSV."""
    return pl.read_csv(
        path,
        schema={
            "date": pl.Utf8,
            "product_id": pl.Utf8,
            "quantity": pl.Int64,
            "price": pl.Float64,
            "region": pl.Utf8,
        },
    )


def transform_sales(df: pl.DataFrame) -> pl.DataFrame:
    """Transform sales data."""
    return (
        df.with_columns([
            pl.col("date").str.to_date("%Y-%m-%d").alias("date"),
            (pl.col("quantity") * pl.col("price")).alias("revenue"),
        ])
        .filter(pl.col("quantity") > 0)
        .with_columns([
            pl.col("date").dt.year().alias("year"),
            pl.col("date").dt.month().alias("month"),
        ])
    )


def aggregate_by_region(df: pl.DataFrame) -> pl.DataFrame:
    """Aggregate sales by region."""
    return (
        df.group_by(["region", "year", "month"])
        .agg([
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("quantity").sum().alias("total_quantity"),
            pl.col("product_id").n_unique().alias("unique_products"),
        ])
        .sort(["region", "year", "month"])
    )


def run_pipeline(input_path: Path, output_path: Path) -> None:
    """Run the complete ETL pipeline."""
    # Load
    raw_data = load_sales_data(input_path)
    print(f"Loaded {len(raw_data)} records")

    # Transform
    transformed = transform_sales(raw_data)
    print(f"Transformed: {len(transformed)} valid records")

    # Aggregate
    aggregated = aggregate_by_region(transformed)
    print(f"Aggregated to {len(aggregated)} region-month combinations")

    # Save
    aggregated.write_parquet(output_path)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    run_pipeline(
        Path("data/sales.csv"),
        Path("output/sales_by_region.parquet"),
    )
```

---

## Async Web Scraper

### Concurrent HTTP Requests

```python
# src/scraper/crawler.py
import asyncio
from dataclasses import dataclass
from typing import TypedDict

import httpx
from bs4 import BeautifulSoup


class PageResult(TypedDict):
    """Scraped page result."""

    url: str
    title: str
    status: int
    links: list[str]


@dataclass
class Crawler:
    """Async web crawler."""

    max_concurrent: int = 10
    timeout: float = 30.0

    async def fetch_page(
        self,
        client: httpx.AsyncClient,
        url: str,
    ) -> PageResult | None:
        """Fetch and parse a single page."""
        try:
            response = await client.get(url, follow_redirects=True)
            soup = BeautifulSoup(response.text, "html.parser")

            title_tag = soup.find("title")
            title = title_tag.text.strip() if title_tag else ""

            links = [
                a["href"]
                for a in soup.find_all("a", href=True)
                if a["href"].startswith("http")
            ]

            return PageResult(
                url=url,
                title=title,
                status=response.status_code,
                links=links[:10],  # Limit links
            )
        except httpx.HTTPError as e:
            print(f"Error fetching {url}: {e}")
            return None

    async def crawl(self, urls: list[str]) -> list[PageResult]:
        """Crawl multiple URLs concurrently."""
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def fetch_with_semaphore(
            client: httpx.AsyncClient,
            url: str,
        ) -> PageResult | None:
            async with semaphore:
                return await self.fetch_page(client, url)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            tasks = [fetch_with_semaphore(client, url) for url in urls]
            results = await asyncio.gather(*tasks)

        return [r for r in results if r is not None]


async def main() -> None:
    """Main entry point."""
    urls = [
        "https://python.org",
        "https://docs.python.org",
        "https://pypi.org",
    ]

    crawler = Crawler(max_concurrent=5)
    results = await crawler.crawl(urls)

    for result in results:
        print(f"\n{result['url']}")
        print(f"  Title: {result['title']}")
        print(f"  Status: {result['status']}")
        print(f"  Links: {len(result['links'])}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## ML Pipeline with scikit-learn

### Training Pipeline

```python
# src/ml/train.py
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@dataclass
class TrainingConfig:
    """Training configuration."""

    test_size: float = 0.2
    random_state: int = 42
    n_estimators: int = 100
    max_depth: int | None = None


@dataclass
class TrainingResult:
    """Training result."""

    accuracy: float
    report: str
    model_path: Path


def prepare_data(
    X: np.ndarray,
    y: np.ndarray,
    config: TrainingConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """Prepare data for training."""
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config.test_size,
        random_state=config.random_state,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    config: TrainingConfig,
) -> RandomForestClassifier:
    """Train a Random Forest classifier."""
    model = RandomForestClassifier(
        n_estimators=config.n_estimators,
        max_depth=config.max_depth,
        random_state=config.random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(
    model: RandomForestClassifier,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> tuple[float, str]:
    """Evaluate model performance."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report


def save_artifacts(
    model: RandomForestClassifier,
    scaler: StandardScaler,
    output_dir: Path,
) -> Path:
    """Save model and scaler."""
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / "model.joblib"
    scaler_path = output_dir / "scaler.joblib"

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    return model_path


def run_training(
    X: np.ndarray,
    y: np.ndarray,
    output_dir: Path,
    config: TrainingConfig | None = None,
) -> TrainingResult:
    """Run complete training pipeline."""
    if config is None:
        config = TrainingConfig()

    # Prepare data
    X_train, X_test, y_train, y_test, scaler = prepare_data(X, y, config)

    # Train
    model = train_model(X_train, y_train, config)

    # Evaluate
    accuracy, report = evaluate_model(model, X_test, y_test)
    print(f"Accuracy: {accuracy:.4f}")
    print(report)

    # Save
    model_path = save_artifacts(model, scaler, output_dir)

    return TrainingResult(
        accuracy=accuracy,
        report=report,
        model_path=model_path,
    )


# Inference
def load_model(model_dir: Path) -> tuple[RandomForestClassifier, StandardScaler]:
    """Load model and scaler."""
    model = joblib.load(model_dir / "model.joblib")
    scaler = joblib.load(model_dir / "scaler.joblib")
    return model, scaler


def predict(
    model: RandomForestClassifier,
    scaler: StandardScaler,
    X: np.ndarray,
) -> np.ndarray:
    """Make predictions."""
    X_scaled = scaler.transform(X)
    return model.predict(X_scaled)
```

---

## LLM Integration with pydantic-ai

### Type-Safe LLM Interaction

```python
# src/llm/assistant.py
from dataclasses import dataclass

from pydantic import BaseModel
from pydantic_ai import Agent


class TaskAnalysis(BaseModel):
    """Structured task analysis."""

    summary: str
    complexity: str  # low, medium, high
    estimated_steps: int
    potential_blockers: list[str]
    suggested_approach: str


class CodeReview(BaseModel):
    """Structured code review."""

    issues: list[str]
    suggestions: list[str]
    security_concerns: list[str]
    overall_quality: str  # poor, fair, good, excellent


@dataclass
class CodingAssistant:
    """LLM-powered coding assistant."""

    model: str = "openai:gpt-4o"

    def __post_init__(self) -> None:
        self.task_agent = Agent(
            self.model,
            result_type=TaskAnalysis,
            system_prompt=(
                "You are a senior software architect. "
                "Analyze tasks and provide structured breakdowns."
            ),
        )
        self.review_agent = Agent(
            self.model,
            result_type=CodeReview,
            system_prompt=(
                "You are a code reviewer. "
                "Review code for issues, suggest improvements, "
                "and identify security concerns."
            ),
        )

    async def analyze_task(self, task_description: str) -> TaskAnalysis:
        """Analyze a development task."""
        result = await self.task_agent.run(
            f"Analyze this development task:\n\n{task_description}"
        )
        return result.data

    async def review_code(self, code: str, language: str = "python") -> CodeReview:
        """Review code for quality and security."""
        result = await self.review_agent.run(
            f"Review this {language} code:\n\n```{language}\n{code}\n```"
        )
        return result.data


async def main() -> None:
    """Example usage."""
    assistant = CodingAssistant()

    # Analyze task
    task = "Implement user authentication with JWT tokens and refresh token rotation"
    analysis = await assistant.analyze_task(task)
    print(f"Complexity: {analysis.complexity}")
    print(f"Steps: {analysis.estimated_steps}")
    print(f"Approach: {analysis.suggested_approach}")

    # Review code
    code = '''
def get_user(id):
    query = f"SELECT * FROM users WHERE id = {id}"
    return db.execute(query)
'''
    review = await assistant.review_code(code)
    print(f"\nSecurity concerns: {review.security_concerns}")
    print(f"Quality: {review.overall_quality}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

*Python Examples v1.0*
