---
description: Plan the presentation layer implementation for a feature
argument-hint: [feature name]
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Presentation Layer Planning Phase

You are planning the **Presentation Layer** implementation following Clean Architecture principles.

## Your Task

Create a presentation layer implementation plan for: **$ARGUMENTS**

## What is the Presentation Layer?

The **Presentation Layer** is the outermost layer that handles external interactions:

- **API Controllers/Routes** - REST endpoints
- **Request/Response Schemas** - API contracts
- **Dependency Injection** - Wire up layers
- **Error Handlers** - Convert domain errors to HTTP responses
- **Authentication/Authorization** - Security (if needed)

**Key principle**: Presentation layer **depends on application layer** (use cases) but has no knowledge of domain or infrastructure internals.

## Before Planning

### 1. Read Context Documents

**REQUIRED**: Read these files first:

1. **Feature file**: `tests/features/[domain]/[feature-name].feature`
   - Gherkin scenarios map to API endpoints

2. **Application layer plan**: `documentation/plans/[feature-name]/002-application-layer.md`
   - Understand what use cases exist

3. **Application DTOs**: `src/application/dtos/[feature]_dto.py`
   - See what data use cases expect/return

Use Glob to find relevant files.

### 2. Verify Prerequisites

Check that previous layers are implemented:
- Domain layer with aggregates
- Application layer with use cases
- Infrastructure layer with repositories

If previous layers don't exist, ask user to complete them first.

## Planning Structure

Create a plan in this format:

```markdown
# Presentation Layer Plan: [Feature Name]

**Feature**: [Feature Name]
**Layer**: Presentation (API/UI)
**Date**: [Date]
**Depends on**: Domain, Application, Infrastructure Layers

---

## Overview

[Brief description of what API endpoints will be implemented]

## API Endpoints

Based on Gherkin scenarios and use cases:

| Method | Endpoint | Use Case | Purpose |
|--------|----------|----------|---------|
| POST | /api/[resource] | [CreateUseCase] | Create new [resource] |
| GET | /api/[resource]/{id} | [GetUseCase] | Retrieve [resource] |
| PUT | /api/[resource]/{id} | [UpdateUseCase] | Update [resource] |
| DELETE | /api/[resource]/{id} | [DeleteUseCase] | Delete [resource] |

---

## Implementation Steps (TDD)

### Step 1: API Schemas (Request/Response)

**File**: `src/presentation/api/schemas/[feature]_schema.py`

**Purpose**: Define API contracts using Pydantic (or similar)

```python
from pydantic import BaseModel, Field

class Create[Resource]Request(BaseModel):
    """API request schema for creating [resource]"""
    field1: str = Field(..., description="[Description]")
    field2: int = Field(..., gt=0, description="[Description]")

    class Config:
        json_schema_extra = {
            "example": {
                "field1": "example value",
                "field2": 42
            }
        }

class [Resource]Response(BaseModel):
    """API response schema for [resource]"""
    id: str
    field1: str
    field2: int
    status: str
```

**Responsibilities**:
- Validate incoming HTTP requests
- Define API documentation (OpenAPI)
- Convert between HTTP and application DTOs

---

### Step 2: API Routes/Controllers

**File**: `src/presentation/api/routes/[feature]_routes.py`

**Tests to write first**:
- `tests/e2e/api/test_[feature]_api.py`
  - Test: POST /api/[resource] creates successfully (201)
  - Test: POST /api/[resource] with invalid data returns 400
  - Test: GET /api/[resource]/{id} returns resource (200)
  - Test: GET /api/[resource]/{id} not found returns 404
  - Test: PUT /api/[resource]/{id} updates successfully (200)
  - Test: DELETE /api/[resource]/{id} deletes successfully (204)
  - Use TestClient with real/in-memory database

**Implementation** (FastAPI example):
```python
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.use_cases.[feature] import [CreateUseCase]
from src.application.dtos.[feature]_dto import [Request]DTO, [Response]DTO

router = APIRouter(prefix="/api/[resource]", tags=["[Resource]"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_[resource](
    request: Create[Resource]Request,
    use_case: [CreateUseCase] = Depends(get_[create]_use_case)
) -> [Resource]Response:
    """
    Create a new [resource].

    - Gherkin Scenario: [Reference]
    """
    try:
        # Convert API schema to application DTO
        dto = [Request]DTO(
            field1=request.field1,
            field2=request.field2
        )

        # Execute use case
        result = use_case.execute(dto)

        # Convert application DTO to API schema
        return [Resource]Response(
            id=result.id,
            field1=result.field1,
            field2=result.field2
        )

    except [DomainException] as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{id}")
async def get_[resource](
    id: str,
    use_case: [GetUseCase] = Depends(get_[get]_use_case)
) -> [Resource]Response:
    """Get [resource] by ID"""
    # ... similar structure

# ... other endpoints
```

---

### Step 3: Dependency Injection

**File**: `src/presentation/api/dependencies.py`

**Purpose**: Wire up all layers

```python
from sqlalchemy.orm import Session
from src.infrastructure.persistence.repositories.[aggregate]_repository import [Aggregate]RepositoryImpl
from src.application.use_cases.[feature].[usecase] import [UseCase]

def get_db_session() -> Session:
    """Get database session"""
    # Session management
    ...

def get_[repository](session: Session = Depends(get_db_session)) -> [Repository]:
    """Get repository implementation"""
    return [Aggregate]RepositoryImpl(session)

def get_[usecase](repo: [Repository] = Depends(get_[repository])) -> [UseCase]:
    """Get use case with injected dependencies"""
    return [UseCase](repo)
```

---

### Step 4: Error Handlers

**File**: `src/presentation/api/error_handlers.py`

**Purpose**: Convert domain errors to HTTP responses

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from src.domain.exceptions import [DomainException]

async def domain_exception_handler(request: Request, exc: [DomainException]):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "domain_error"}
    )

# Register handlers
app.add_exception_handler([DomainException], domain_exception_handler)
```

---

### Step 5: Main Application Setup

**File**: `src/presentation/api/main.py`

**Purpose**: Configure FastAPI application

```python
from fastapi import FastAPI
from src.presentation.api.routes.[feature]_routes import router

app = FastAPI(
    title="[Application Name]",
    description="[Description]",
    version="1.0.0"
)

# Include routers
app.include_router(router)

# Register error handlers
# ... configure middleware, CORS, etc.
```

---

## Folder Structure

```
src/presentation/
└── api/
    ├── routes/
    │   └── [feature]_routes.py       ← API endpoints
    ├── schemas/
    │   └── [feature]_schema.py       ← Request/response models
    ├── dependencies.py               ← Dependency injection
    ├── error_handlers.py             ← Error mapping
    └── main.py                       ← FastAPI app
```

---

## API to Use Case Mapping

Map each endpoint to use cases and Gherkin scenarios:

| Endpoint | HTTP Method | Use Case | Gherkin Scenario |
|----------|-------------|----------|------------------|
| /api/[resource] | POST | [CreateUseCase] | "Create a new [resource]" |
| /api/[resource]/{id} | GET | [GetUseCase] | "Retrieve [resource] by ID" |
| /api/[resource]/{id} | PUT | [UpdateUseCase] | "Update [resource]" |
| /api/[resource]/{id} | DELETE | [DeleteUseCase] | "Delete [resource]" |

---

## HTTP Status Codes

Map domain errors to HTTP status codes:

| Domain Error | HTTP Status | Response Body |
|--------------|-------------|---------------|
| [ValidationError] | 400 Bad Request | `{"detail": "error message"}` |
| [NotFoundError] | 404 Not Found | `{"detail": "[Resource] not found"}` |
| [ConflictError] | 409 Conflict | `{"detail": "conflict message"}` |
| Success (Create) | 201 Created | `{resource object}` |
| Success (Update) | 200 OK | `{resource object}` |
| Success (Delete) | 204 No Content | (empty) |

---

## Dependencies

- **Depends on**: All inner layers (Application, Domain via Application, Infrastructure for wiring)
- **Technologies**: FastAPI, Pydantic, Uvicorn
- **Testing**: pytest, httpx TestClient

---

## Security Considerations

(If applicable)

- **Authentication**: [How users authenticate]
- **Authorization**: [Who can access what]
- **Rate Limiting**: [If needed]
- **Input Validation**: Pydantic schemas validate all input

---

## Validation Checklist

- [ ] All Gherkin scenarios have corresponding API endpoints
- [ ] Request schemas validate input data
- [ ] Response schemas document output
- [ ] Error handlers convert domain errors to HTTP
- [ ] Dependency injection wires all layers
- [ ] E2E tests cover all endpoints
- [ ] API documentation (OpenAPI) generated
- [ ] No domain or infrastructure logic in presentation

---

## Estimated Effort

- API Schemas: [X hours]
- Routes/Controllers: [X hours]
- Dependency Injection: [X hours]
- Error Handlers: [X hours]
- E2E Tests: [X hours]
- **Total**: [X hours]

---

## Next Steps

After completing presentation layer:
1. Full stack integration testing
2. Manual testing with Swagger UI
3. Deploy to staging environment
4. Documentation review
```

## File Naming and Location

**Save plan to**: `documentation/plans/[feature-name]/004-presentation-layer.md`

Examples:
- `documentation/plans/education/004-presentation-layer.md`
- `documentation/plans/ruleset/004-presentation-layer.md`

## Skills to Apply

These skills activate automatically:
- **clean-architecture**: For layer boundaries
- **test-driven-development**: For E2E tests
- **solid-principles**: For controller design

## Key Reminders

### Presentation Layer Rules
1. **Thin controllers** - Delegate to use cases
2. **No business logic** - Just routing and conversion
3. **Dependency injection** - Wire up layers explicitly
4. **Error mapping** - Convert domain errors to HTTP
5. **Input validation** - Validate at API boundary

### Clean Architecture Flow
```
HTTP Request
    ↓
API Schema (validate)
    ↓
Application DTO (convert)
    ↓
Use Case (execute)
    ↓
Domain Logic
    ↓
Use Case (return DTO)
    ↓
API Schema (convert)
    ↓
HTTP Response
```

### Dependency Direction
```
Presentation Layer
    ↓ (depends on)
Application Layer
    ↓ (depends on)
Domain Layer
    ↑ (implemented by)
Infrastructure Layer
```

## Output

Provide a detailed, actionable plan that:
- Focuses ONLY on presentation layer
- Lists all API endpoints
- Maps endpoints to use cases and Gherkin scenarios
- Defines request/response schemas
- Specifies E2E tests
- Shows dependency injection wiring
- Respects Clean Architecture principles
- Can be implemented after all inner layers are complete
