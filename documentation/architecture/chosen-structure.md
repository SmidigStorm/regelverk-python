# Project Structure - Clean Architecture (Package by Layer)

This document defines the official project structure for the Norwegian Admission Rules System.

We use **Clean Architecture with Package by Layer** - the simplest, most straightforward approach.

---

## Overview

```
regelverk-python/
├── src/
│   ├── domain/              # Layer 1: Enterprise Business Rules
│   ├── application/         # Layer 2: Application Business Rules
│   ├── infrastructure/      # Layer 3: Interface Adapters
│   └── presentation/        # Layer 4: Frameworks & Drivers
├── tests/
├── frontend/
└── documentation/
```

---

## Layer 1: Domain (Pure Python)

**Location**: `src/domain/`

**Dependencies**: NONE - Pure Python only

**Purpose**: Enterprise business rules - the heart of the application

```
src/domain/
├── __init__.py
├── entities/
│   ├── __init__.py
│   ├── student.py
│   ├── admission_rule.py
│   ├── quota.py
│   └── program.py
├── value_objects/
│   ├── __init__.py
│   ├── grade.py
│   ├── competence_points.py
│   ├── student_id.py
│   ├── program_id.py
│   └── quota_name.py
├── aggregates/
│   ├── __init__.py
│   └── admission_application.py
├── services/
│   ├── __init__.py
│   ├── admission_evaluation_service.py
│   └── competence_points_calculator.py
├── events/
│   ├── __init__.py
│   ├── domain_event.py
│   ├── student_admitted.py
│   ├── student_rejected.py
│   └── quota_filled.py
├── ports.py                    # Interfaces domain needs (repositories, etc.)
└── exceptions.py               # Domain exceptions
```

### Key Files

**entities/student.py**
```python
class Student:
    """Entity with identity and behavior"""
    def __init__(self, id: StudentId, name: str):
        self._id = id
        self._name = name
        self._grades: list[Grade] = []

    def calculate_competence_points(self) -> CompetencePoints:
        total = sum(grade.to_points() for grade in self._grades)
        return CompetencePoints(total)
```

**value_objects/grade.py**
```python
@dataclass(frozen=True)
class Grade:
    """Value object - immutable, defined by attributes"""
    subject: str
    score: int  # 1-6 scale

    def to_points(self) -> int:
        return self.score * 4
```

**ports.py** - Domain defines what it needs
```python
from typing import Protocol

class StudentRepository(Protocol):
    """Port - domain defines interface, infrastructure implements"""
    def find_by_id(self, student_id: StudentId) -> Student | None: ...
    def save(self, student: Student) -> None: ...

class AdmissionRuleRepository(Protocol):
    def find_by_program(self, program_id: ProgramId) -> list[AdmissionRule]: ...
```

---

## Layer 2: Application (Use Cases)

**Location**: `src/application/`

**Dependencies**: domain only

**Purpose**: Application business rules - orchestrate domain logic

```
src/application/
├── __init__.py
├── use_cases/
│   ├── __init__.py
│   ├── evaluate_admission_use_case.py
│   ├── calculate_competence_points_use_case.py
│   ├── register_student_use_case.py
│   ├── assign_quota_use_case.py
│   └── rank_applicants_use_case.py
└── dtos/
    ├── __init__.py
    ├── admission_dto.py
    ├── student_dto.py
    └── quota_dto.py
```

### Key Files

**use_cases/evaluate_admission_use_case.py**
```python
from dataclasses import dataclass
from domain.ports import StudentRepository, AdmissionRuleRepository
from domain.entities import Student
from domain.value_objects import StudentId, ProgramId

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
    """Use case - orchestrates domain logic"""

    def __init__(
        self,
        student_repo: StudentRepository,
        rule_repo: AdmissionRuleRepository
    ):
        self._students = student_repo
        self._rules = rule_repo

    def execute(self, input: EvaluateAdmissionInput) -> EvaluateAdmissionOutput:
        # 1. Get domain objects
        student = self._students.find_by_id(StudentId(input.student_id))
        if not student:
            raise ValueError("Student not found")

        rules = self._rules.find_by_program(ProgramId(input.program_id))

        # 2. Execute domain logic
        evaluation = AdmissionEvaluationService.evaluate(student, rules)

        # 3. Return DTO
        return EvaluateAdmissionOutput(
            admitted=evaluation.is_admitted,
            reason=evaluation.reason,
            competence_points=student.calculate_competence_points().value
        )
```

**dtos/admission_dto.py**
```python
@dataclass
class AdmissionDTO:
    """Data Transfer Object - crosses layer boundaries"""
    student_id: str
    program_id: str
    admitted: bool
    reason: str
```

---

## Layer 3: Infrastructure (Interface Adapters)

**Location**: `src/infrastructure/`

**Dependencies**: domain, application (implements their interfaces)

**Purpose**: Implementations of ports - connect to external systems

```
src/infrastructure/
├── __init__.py
├── persistence/
│   ├── __init__.py
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── student_model.py
│   │   ├── admission_rule_model.py
│   │   ├── quota_model.py
│   │   └── program_model.py
│   ├── mappers/                # Domain ↔ ORM converters
│   │   ├── __init__.py
│   │   ├── student_mapper.py
│   │   ├── quota_mapper.py
│   │   └── admission_rule_mapper.py
│   ├── repositories/           # Repository implementations
│   │   ├── __init__.py
│   │   ├── sqlalchemy_student_repository.py
│   │   ├── sqlalchemy_quota_repository.py
│   │   └── sqlalchemy_admission_rule_repository.py
│   └── database.py             # Database connection/session
├── config/
│   ├── __init__.py
│   └── settings.py             # Application settings
└── external/                   # External API clients
    ├── __init__.py
    └── samordna_opptak_client.py
```

### Key Files

**models/student_model.py** - SQLAlchemy model (NOT domain entity)
```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class StudentModel(Base):
    """ORM model - infrastructure concern"""
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    # ORM-specific fields, relationships, etc.
```

**mappers/student_mapper.py** - Convert between domain and ORM
```python
class StudentMapper:
    """Maps domain entities ↔ ORM models"""

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
```

**repositories/sqlalchemy_student_repository.py** - Implements domain port
```python
from sqlalchemy.orm import Session
from domain.ports import StudentRepository  # Implements domain's interface
from domain.entities import Student
from domain.value_objects import StudentId

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

**Location**: `src/presentation/`

**Dependencies**: application (calls use cases)

**Purpose**: External interfaces - HTTP API, CLI, etc.

```
src/presentation/
├── __init__.py
└── api/
    ├── __init__.py
    ├── main.py                 # FastAPI application
    ├── dependencies.py         # Dependency injection wiring
    ├── schemas/                # Pydantic request/response models
    │   ├── __init__.py
    │   ├── admission_schema.py
    │   ├── student_schema.py
    │   └── quota_schema.py
    └── routes/                 # API endpoints
        ├── __init__.py
        ├── admission_routes.py
        ├── student_routes.py
        └── quota_routes.py
```

### Key Files

**main.py** - FastAPI application
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.api.routes import admission_routes, student_routes

app = FastAPI(title="Norwegian Admission Rules API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admission_routes.router)
app.include_router(student_routes.router)
```

**schemas/admission_schema.py** - Pydantic models (API layer)
```python
from pydantic import BaseModel

class EvaluateAdmissionRequest(BaseModel):
    """API request schema"""
    student_id: str
    program_id: str

class EvaluateAdmissionResponse(BaseModel):
    """API response schema"""
    admitted: bool
    reason: str
    competence_points: int
```

**routes/admission_routes.py** - API endpoints
```python
from fastapi import APIRouter, Depends
from application.use_cases import EvaluateAdmissionUseCase, EvaluateAdmissionInput
from presentation.api.schemas import EvaluateAdmissionRequest, EvaluateAdmissionResponse
from presentation.api.dependencies import get_evaluate_admission_use_case

router = APIRouter(prefix="/api/v1/admission", tags=["admission"])

@router.post("/evaluate", response_model=EvaluateAdmissionResponse)
async def evaluate_admission(
    request: EvaluateAdmissionRequest,
    use_case: EvaluateAdmissionUseCase = Depends(get_evaluate_admission_use_case)
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
```

**dependencies.py** - Dependency injection wiring
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from infrastructure.persistence.database import get_db_session
from infrastructure.persistence.repositories import (
    SQLAlchemyStudentRepository,
    SQLAlchemyAdmissionRuleRepository
)
from application.use_cases import EvaluateAdmissionUseCase

def get_evaluate_admission_use_case(
    session: Session = Depends(get_db_session)
) -> EvaluateAdmissionUseCase:
    """Wire up use case with repository implementations"""
    student_repo = SQLAlchemyStudentRepository(session)
    rule_repo = SQLAlchemyAdmissionRuleRepository(session)
    return EvaluateAdmissionUseCase(student_repo, rule_repo)
```

---

## Testing Structure

```
tests/
├── unit/                       # Fast, isolated tests
│   ├── domain/
│   │   ├── test_student.py
│   │   ├── test_grade.py
│   │   └── test_admission_rule.py
│   ├── application/
│   │   └── test_evaluate_admission_use_case.py
│   └── infrastructure/
│       └── test_student_mapper.py
├── integration/                # Component interaction tests
│   ├── test_student_repository.py
│   └── test_admission_workflow.py
├── e2e/                       # End-to-end API tests
│   └── test_admission_api.py
└── features/                  # BDD Gherkin scenarios
    ├── admission.feature
    └── quota.feature
```

---

## Complete Directory Tree

```
regelverk-python/
├── src/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── aggregates/
│   │   ├── services/
│   │   ├── events/
│   │   ├── ports.py
│   │   └── exceptions.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── use_cases/
│   │   └── dtos/
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── persistence/
│   │   │   ├── models/
│   │   │   ├── mappers/
│   │   │   ├── repositories/
│   │   │   └── database.py
│   │   ├── config/
│   │   └── external/
│   └── presentation/
│       ├── __init__.py
│       └── api/
│           ├── main.py
│           ├── dependencies.py
│           ├── schemas/
│           └── routes/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── features/
├── frontend/                   # React + Vite
│   ├── src/
│   ├── vite.config.ts
│   └── package.json
├── documentation/
│   └── architecture/
├── .claude/
│   └── skills/
├── alembic/                   # Database migrations
├── CLAUDE.md
├── pyproject.toml
└── README.md
```

---

## Key Principles

### 1. Dependency Rule
Dependencies point INWARD:
- Presentation → Application → Domain
- Infrastructure → Application → Domain
- Domain depends on NOTHING

### 2. Interface Ownership
- Domain defines interfaces (ports)
- Infrastructure implements them (adapters)
- Never the reverse

### 3. Layer Responsibilities

**Domain**: Business logic ONLY
- No SQLAlchemy
- No FastAPI
- No frameworks
- Pure Python

**Application**: Orchestration ONLY
- Calls domain logic
- No business rules
- No database code
- No HTTP code

**Infrastructure**: Implementation ONLY
- Implements domain ports
- Database access
- External APIs
- No business logic

**Presentation**: User interface ONLY
- HTTP endpoints
- Request/response handling
- Calls use cases
- No business logic

---

## Where Things Go

| What | Where | Layer |
|------|-------|-------|
| Student entity | `domain/entities/student.py` | Domain |
| Grade value object | `domain/value_objects/grade.py` | Domain |
| Admission evaluation logic | `domain/services/admission_evaluation_service.py` | Domain |
| Repository interface | `domain/ports.py` | Domain |
| Evaluate admission use case | `application/use_cases/evaluate_admission_use_case.py` | Application |
| DTOs | `application/dtos/` | Application |
| SQLAlchemy models | `infrastructure/persistence/models/` | Infrastructure |
| Repository implementation | `infrastructure/persistence/repositories/` | Infrastructure |
| Mappers | `infrastructure/persistence/mappers/` | Infrastructure |
| API routes | `presentation/api/routes/` | Presentation |
| Pydantic schemas | `presentation/api/schemas/` | Presentation |

---

## Getting Started

Start building in this order:

1. **Domain first**: Create entities and value objects
2. **Application**: Create use cases
3. **Infrastructure**: Implement repositories
4. **Presentation**: Create API endpoints

This is the structure we will use. Simple, clear, and follows Clean Architecture principles.
