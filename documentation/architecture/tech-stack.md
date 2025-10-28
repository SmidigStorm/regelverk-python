# Tech Stack

This document describes the technology choices for the Norwegian Admission Rules System, organized by Clean Architecture layers.

## Architecture Overview

The system follows **Clean Architecture** with dependencies flowing **inward** toward the domain core. Each layer depends only on layers closer to the center.

```
┌────────────────────────────────────────────┐
│  Frontend (React + Vite)                   │
│  ↓ HTTP                                    │
│  Backend API (FastAPI)                     │
│  ┌──────────────────────────────────────┐  │
│  │  Infrastructure (SQLAlchemy)         │  │
│  │  ┌────────────────────────────────┐  │  │
│  │  │  Application (Use Cases)       │  │  │
│  │  │  ┌──────────────────────────┐  │  │  │
│  │  │  │  Domain (Pure Python)    │  │  │  │
│  │  │  │  NO dependencies         │  │  │  │
│  │  │  └──────────────────────────┘  │  │  │
│  │  └────────────────────────────────┘  │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
     Dependencies point INWARD →
```

---

## Layer 1: Domain (Enterprise Business Rules)

**Philosophy**: Pure Python with zero external dependencies. The domain is the heart of the application and should be framework-agnostic.

### Technologies
- **Language**: Python 3.11+
- **Type System**: Native Python `typing` module
- **Data Structures**:
  - `dataclasses` for value objects
  - Plain classes for entities
- **Interfaces**: `typing.Protocol` for ports
- **Validation**: Pure Python (business rule validation)

### Optional Libraries
- **pydantic** (v2.4+): If rich validation is needed for value objects
  - Only used for validation, not as a framework dependency
  - Domain models should not inherit from BaseModel

### What Lives Here
- **Entities**: `Student`, `AdmissionRule`, `Quota`, `Program`
- **Value Objects**: `Grade`, `CompetencePoints`, `StudentId`, `QuotaName`
- **Aggregates**: `AdmissionApplication`, `Program` (with quota management)
- **Domain Services**: `AdmissionEvaluationService`, `CompetencePointsCalculator`
- **Domain Events**: `StudentAdmitted`, `StudentRejected`, `QuotaFilled`
- **Ports**: Repository protocols (defined by domain, implemented by infrastructure)

### Example
```python
# domain/entities/student.py
from dataclasses import dataclass
from domain.value_objects import Grade, StudentId

class Student:
    """Entity: Student has identity and lifecycle"""
    def __init__(self, id: StudentId, name: str):
        self._id = id
        self._name = name
        self._grades: list[Grade] = []

    def add_grade(self, grade: Grade) -> None:
        """Business logic lives in the domain"""
        if grade in self._grades:
            raise ValueError("Grade already exists")
        self._grades.append(grade)

    def calculate_competence_points(self) -> int:
        return sum(g.to_points() for g in self._grades)

# domain/ports.py
from typing import Protocol
from domain.entities import Student

class StudentRepository(Protocol):
    """Domain defines what it needs from infrastructure"""
    def find_by_id(self, student_id: StudentId) -> Student | None: ...
    def save(self, student: Student) -> None: ...
```

---

## Layer 2: Application (Application Business Rules)

**Philosophy**: Orchestrate domain logic without framework dependencies. Use cases are pure Python that coordinate entities and services.

### Technologies
- **Language**: Pure Python 3.11+
- **DTOs**: `dataclasses` or `pydantic` models
- **Dependency Injection**: Manual constructor injection
- **Interfaces**: Reference protocols from domain layer

### What Lives Here
- **Use Cases**:
  - `EvaluateAdmissionUseCase`
  - `CalculateCompetencePointsUseCase`
  - `AssignQuotaUseCase`
  - `RankApplicantsUseCase`
- **DTOs**: Input/output data transfer objects
- **Application Services**: Cross-cutting concerns (logging, transactions)

### Example
```python
# application/use_cases/evaluate_admission.py
from dataclasses import dataclass
from domain.ports import StudentRepository, AdmissionRuleRepository
from domain.entities import Student

@dataclass
class EvaluateAdmissionInput:
    student_id: str
    program_id: str

@dataclass
class EvaluateAdmissionOutput:
    admitted: bool
    reason: str
    competence_points: int

class EvaluateAdmissionUseCase:
    def __init__(
        self,
        student_repo: StudentRepository,
        rule_repo: AdmissionRuleRepository
    ):
        self._students = student_repo
        self._rules = rule_repo

    def execute(self, input: EvaluateAdmissionInput) -> EvaluateAdmissionOutput:
        # Orchestrate domain logic
        student = self._students.find_by_id(StudentId(input.student_id))
        rules = self._rules.find_by_program(ProgramId(input.program_id))

        # Use domain services
        evaluation = AdmissionEvaluationService.evaluate(student, rules)

        return EvaluateAdmissionOutput(
            admitted=evaluation.is_admitted,
            reason=evaluation.reason,
            competence_points=student.calculate_competence_points()
        )
```

---

## Layer 3: Infrastructure (Interface Adapters)

**Philosophy**: Implement domain-defined interfaces. Connect to external systems (databases, APIs, etc.).

### Technologies

#### Persistence
- **ORM**: SQLAlchemy 2.0+ (with modern declarative syntax)
- **Database**:
  - Development/Testing: SQLite
  - Production: PostgreSQL (when needed)
- **Migrations**: Alembic
- **Connection**: SQLAlchemy Session management

#### External APIs
- **HTTP Client**: httpx (async support)
- **Alternative**: requests (if sync is sufficient)

### What Lives Here
- **Repository Implementations**: Concrete implementations of domain ports
  - `SQLAlchemyStudentRepository`
  - `SQLAlchemyAdmissionRuleRepository`
- **ORM Models**: SQLAlchemy declarative models (separate from domain!)
- **Data Mappers**: Convert between domain entities and ORM models
- **External API Clients**: Adapters for third-party services
- **Configuration**: Database connection, environment variables

### Key Pattern: Separate ORM Models from Domain Entities

```python
# infrastructure/persistence/models/student_model.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class StudentModel(Base):
    """ORM model - infrastructure concern"""
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    # ... ORM-specific fields

# infrastructure/persistence/mappers/student_mapper.py
class StudentMapper:
    """Maps between domain and ORM"""

    @staticmethod
    def to_domain(model: StudentModel) -> Student:
        """ORM model → Domain entity"""
        student = Student(
            id=StudentId(model.id),
            name=model.name
        )
        for grade_model in model.grades:
            student.add_grade(GradeMapper.to_domain(grade_model))
        return student

    @staticmethod
    def to_orm(entity: Student) -> StudentModel:
        """Domain entity → ORM model"""
        return StudentModel(
            id=entity.id.value,
            name=entity.name
        )

# infrastructure/persistence/repositories/sqlalchemy_student_repository.py
from sqlalchemy.orm import Session
from domain.ports import StudentRepository
from domain.entities import Student

class SQLAlchemyStudentRepository:
    """Implements domain's StudentRepository protocol"""

    def __init__(self, session: Session):
        self._session = session
        self._mapper = StudentMapper()

    def find_by_id(self, student_id: StudentId) -> Student | None:
        model = self._session.get(StudentModel, student_id.value)
        return self._mapper.to_domain(model) if model else None

    def save(self, student: Student) -> None:
        model = self._mapper.to_orm(student)
        self._session.merge(model)
```

---

## Layer 4: Presentation (Frameworks & Drivers)

### Backend API

**Philosophy**: HTTP interface to use cases. Thin controllers that delegate to application layer.

#### Technologies
- **Framework**: FastAPI 0.104+
- **Server**: Uvicorn (ASGI server)
- **Validation**: Pydantic v2 (request/response schemas)
- **OpenAPI**: Auto-generated from FastAPI
- **CORS**: FastAPI middleware (for React frontend)

#### What Lives Here
- **API Routes**: REST endpoints
- **Request/Response Schemas**: Pydantic models
- **Controllers**: Convert HTTP → use case DTOs
- **Dependency Injection**: FastAPI Depends for wiring
- **Middleware**: CORS, authentication, logging

#### Example
```python
# presentation/api/schemas/admission.py
from pydantic import BaseModel

class EvaluateAdmissionRequest(BaseModel):
    student_id: str
    program_id: str

class EvaluateAdmissionResponse(BaseModel):
    admitted: bool
    reason: str
    competence_points: int

# presentation/api/routes/admission.py
from fastapi import APIRouter, Depends
from application.use_cases import EvaluateAdmissionUseCase, EvaluateAdmissionInput

router = APIRouter(prefix="/api/v1/admission", tags=["admission"])

@router.post("/evaluate", response_model=EvaluateAdmissionResponse)
async def evaluate_admission(
    request: EvaluateAdmissionRequest,
    use_case: EvaluateAdmissionUseCase = Depends(get_use_case)
):
    """Evaluate if a student is admitted to a program"""
    input_dto = EvaluateAdmissionInput(
        student_id=request.student_id,
        program_id=request.program_id
    )
    result = use_case.execute(input_dto)

    return EvaluateAdmissionResponse(
        admitted=result.admitted,
        reason=result.reason,
        competence_points=result.competence_points
    )

# presentation/api/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from infrastructure.persistence import get_db_session
from infrastructure.persistence.repositories import (
    SQLAlchemyStudentRepository,
    SQLAlchemyAdmissionRuleRepository
)
from application.use_cases import EvaluateAdmissionUseCase

def get_use_case(session: Session = Depends(get_db_session)) -> EvaluateAdmissionUseCase:
    """Dependency injection: wire up use case with repositories"""
    student_repo = SQLAlchemyStudentRepository(session)
    rule_repo = SQLAlchemyAdmissionRuleRepository(session)
    return EvaluateAdmissionUseCase(student_repo, rule_repo)

# presentation/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.api.routes import admission

app = FastAPI(title="Norwegian Admission Rules API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admission.router)
```

---

### Frontend

**Philosophy**: Separate application that communicates with backend via HTTP API only.

#### Technologies
- **Build Tool**: Vite 5+
- **UI Library**: React 18+
- **Language**: TypeScript 5+
- **Routing**: React Router v6
- **HTTP Client**: Axios or native Fetch API
- **State Management**: React Context or Zustand (if needed)
- **Styling**: CSS Modules or Tailwind CSS (TBD)

#### Project Structure
```
frontend/
├── src/
│   ├── features/              # Feature-based organization
│   │   ├── admission/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── api.ts
│   │   ├── students/
│   │   └── quotas/
│   ├── api/                   # API client setup
│   │   ├── client.ts         # Axios instance
│   │   └── types.ts          # TypeScript types matching API
│   ├── components/            # Shared components
│   ├── App.tsx
│   └── main.tsx
├── vite.config.ts
├── tsconfig.json
└── package.json
```

#### Example
```typescript
// frontend/src/api/types.ts
export interface EvaluateAdmissionRequest {
  student_id: string;
  program_id: string;
}

export interface EvaluateAdmissionResponse {
  admitted: boolean;
  reason: string;
  competence_points: number;
}

// frontend/src/api/client.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// frontend/src/features/admission/api.ts
import { apiClient } from '@/api/client';
import { EvaluateAdmissionRequest, EvaluateAdmissionResponse } from '@/api/types';

export const evaluateAdmission = async (
  request: EvaluateAdmissionRequest
): Promise<EvaluateAdmissionResponse> => {
  const response = await apiClient.post('/admission/evaluate', request);
  return response.data;
};

// frontend/src/features/admission/components/AdmissionForm.tsx
import { useState } from 'react';
import { evaluateAdmission } from '../api';

export function AdmissionForm() {
  const [result, setResult] = useState<EvaluateAdmissionResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await evaluateAdmission({
      student_id: studentId,
      program_id: programId,
    });
    setResult(response);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      {result && (
        <div>
          <h3>{result.admitted ? 'Admitted!' : 'Not Admitted'}</h3>
          <p>Reason: {result.reason}</p>
          <p>Points: {result.competence_points}</p>
        </div>
      )}
    </form>
  );
}
```

---

## Testing Stack

### Unit Tests (Domain & Application)
- **Framework**: pytest 7.4+
- **Coverage**: pytest-cov
- **Mocking**: unittest.mock or pytest fixtures
- **Fast**: No database or HTTP dependencies

### Integration Tests (Infrastructure)
- **Database**: In-memory SQLite or test database
- **Fixtures**: pytest fixtures for database setup
- **Transactions**: Rollback after each test

### BDD Tests (Requirements → Tests)
- **Framework**: pytest-bdd 6.1+
- **Format**: Gherkin .feature files
- **Traceability**: User stories → scenarios → tests

### E2E Tests
- **API**: httpx.AsyncClient for FastAPI
- **Full Stack**: TestClient from FastAPI

### Quality Tools
- **Linting**: Ruff (replaces flake8, isort, black)
- **Type Checking**: mypy
- **Pre-commit**: pre-commit hooks

---

## Configuration & Deployment

### Configuration
- **Environment Variables**: python-dotenv
- **Settings**: Pydantic Settings for type-safe config
- **Secrets**: Environment-specific .env files (not committed)

### Development Tools
- **Package Management**: pip + pyproject.toml
- **Virtual Environment**: venv or uv
- **Task Runner**: Make or just

### Deployment (Future)
- **Containerization**: Docker + Docker Compose
- **Backend**: Uvicorn + Gunicorn
- **Frontend**: Static build served by Nginx or CDN
- **Database**: PostgreSQL in production

---

## Dependency Summary

### Python Backend
```toml
[project]
name = "regelverk-python"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    # Layer 4: Presentation
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",

    # Layer 3: Infrastructure
    "sqlalchemy>=2.0.0",
    "alembic>=1.12.0",

    # Cross-cutting
    "pydantic>=2.4.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-bdd>=6.1.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.25.0",  # For testing FastAPI
    "ruff>=0.1.0",
    "mypy>=1.6.0",
]
```

### Frontend
```json
{
  "name": "regelverk-frontend",
  "version": "0.1.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.2.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0"
  }
}
```

---

## Key Principles Maintained

1. ✅ **Domain is pure**: No SQLAlchemy, FastAPI, or React in domain layer
2. ✅ **Ports owned by domain**: Infrastructure implements, doesn't define
3. ✅ **Dependencies inward**: Each layer only knows about layers inside it
4. ✅ **Testability**: Domain and application fully testable without infrastructure
5. ✅ **Flexibility**: Can swap FastAPI → Flask, SQLAlchemy → another ORM, React → Vue
6. ✅ **Type safety**: End-to-end types from TypeScript → Python → Database

---

## Migration Path

### Current (MVP)
- SQLite database
- Simple FastAPI setup
- React frontend (basic)

### Future (Production-Ready)
- PostgreSQL with connection pooling
- Docker containerization
- Frontend optimizations (code splitting, lazy loading)
- Authentication & authorization
- API rate limiting
- Monitoring & logging (structlog, Sentry)
- CI/CD pipeline

The architecture supports this migration without changing domain or application layers.
