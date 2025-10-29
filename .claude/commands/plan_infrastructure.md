---
description: Plan the infrastructure layer implementation for a feature
argument-hint: [feature name]
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Infrastructure Layer Planning Phase

You are planning the **Infrastructure Layer** implementation following Clean Architecture principles.

## Your Task

Create an infrastructure layer implementation plan for: **$ARGUMENTS**

## What is the Infrastructure Layer?

The **Infrastructure Layer** provides concrete implementations of domain ports (interfaces):

- **Repository Implementations** - Persist aggregates to database
- **ORM Models** - Database schema (separate from domain!)
- **Mappers** - Convert between domain entities and ORM models
- **External Service Adapters** - Integrate with external systems
- **Database Migrations** - Schema management

**Key principle**: Infrastructure layer **implements domain ports** but domain has no knowledge of infrastructure.

## Before Planning

### 1. Read Context Documents

**REQUIRED**: Read these files first:

1. **Domain layer plan**: `documentation/plans/[feature-name]/001-domain-layer.md`
   - Understand what repository ports exist

2. **Application layer plan**: `documentation/plans/[feature-name]/002-application-layer.md`
   - Understand what use cases need repositories

3. **Domain repository port**: `src/domain/aggregates/[feature]/[repository].py`
   - See what interface to implement

Use Glob to find relevant files.

### 2. Verify Prerequisites

Check that these layers are implemented:
- Domain layer exists with repository port
- Application layer exists with use cases

If previous layers don't exist, ask user to complete them first.

## Planning Structure

Create a plan in this format:

```markdown
# Infrastructure Layer Plan: [Feature Name]

**Feature**: [Feature Name]
**Layer**: Infrastructure (Persistence & External Integrations)
**Date**: [Date]
**Depends on**: Domain Layer, Application Layer

---

## Overview

[Brief description of what infrastructure components will be implemented]

## Components to Implement

1. **[Aggregate]RepositoryImpl** - Persist [aggregate] to database
2. **[Aggregate]Model** - SQLAlchemy/ORM model
3. **[Aggregate]Mapper** - Convert domain ↔ ORM
4. **Database Migration** - Schema for [aggregate]

---

## Implementation Steps (TDD)

### Step 1: ORM Model (Database Schema)

**File**: `src/infrastructure/persistence/models/[aggregate]_model.py`

**Purpose**: Define database schema (NOT domain model!)

```python
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class [Aggregate]Model(Base):
    __tablename__ = '[table_name]'

    id = Column(String, primary_key=True)
    field1 = Column(String, nullable=False)
    field2 = Column(Enum([EnumType]), nullable=False)
    # ... other columns
```

**Key Principles**:
- Separate from domain model (different concerns)
- Reflects database structure
- No business logic

---

### Step 2: Mapper (Domain ↔ ORM)

**File**: `src/infrastructure/persistence/mappers/[aggregate]_mapper.py`

**Purpose**: Convert between domain entities and ORM models

```python
class [Aggregate]Mapper:
    @staticmethod
    def to_domain(model: [Aggregate]Model) -> [Aggregate]:
        """Convert ORM model to domain entity"""
        return [Aggregate](
            id=[AggregateId](model.id),
            field1=model.field1,
            # ... reconstruct domain entity
        )

    @staticmethod
    def to_model(entity: [Aggregate]) -> [Aggregate]Model:
        """Convert domain entity to ORM model"""
        return [Aggregate]Model(
            id=str(entity.id),
            field1=entity.field1,
            # ... map to database columns
        )
```

**Responsibilities**:
- Isolate domain from database concerns
- Handle value object conversions
- Map enums, dates, nested objects

---

### Step 3: Repository Implementation

**File**: `src/infrastructure/persistence/repositories/[aggregate]_repository.py`

**Tests to write first**:
- `tests/integration/infrastructure/test_[aggregate]_repository.py`
  - Test: Save and retrieve aggregate
  - Test: Update existing aggregate
  - Test: Delete aggregate
  - Test: Find by ID returns None when not found
  - Test: Query methods (if any)
  - Use in-memory SQLite for testing

**Implementation**:
```python
from src.domain.aggregates.[feature].[repository] import [Repository]

class [Aggregate]RepositoryImpl([Repository]):
    """
    SQLAlchemy implementation of [Repository] port.

    Implements the repository interface defined in the domain layer.
    """

    def __init__(self, session: Session):
        self._session = session

    def save(self, aggregate: [Aggregate]) -> None:
        model = [Aggregate]Mapper.to_model(aggregate)
        self._session.merge(model)  # Insert or update
        self._session.commit()

    def find_by_id(self, id: [AggregateId]) -> Optional[[Aggregate]]:
        model = self._session.query([Aggregate]Model).filter_by(
            id=str(id)
        ).first()
        return [Aggregate]Mapper.to_domain(model) if model else None

    def delete(self, id: [AggregateId]) -> None:
        model = self._session.query([Aggregate]Model).filter_by(
            id=str(id)
        ).first()
        if not model:
            raise [Aggregate]NotFoundError(id)
        self._session.delete(model)
        self._session.commit()

    # ... implement other methods from port
```

---

### Step 4: Database Migration

**Tool**: Alembic (or similar)

**Commands**:
```bash
# Generate migration
alembic revision --autogenerate -m "Add [aggregate] table"

# Review generated migration in migrations/versions/

# Apply migration
alembic upgrade head
```

**Migration should create**:
- Table for aggregate
- Columns matching ORM model
- Indexes on frequently queried fields
- Foreign keys (if referencing other aggregates)

---

### Step 5: In-Memory Repository (for testing)

**File**: `src/infrastructure/persistence/in_memory/[aggregate]_repository.py`

**Purpose**: Fast repository for unit tests (no database needed)

```python
class InMemory[Aggregate]Repository([Repository]):
    def __init__(self):
        self._storage: Dict[[AggregateId], [Aggregate]] = {}

    def save(self, aggregate: [Aggregate]) -> None:
        self._storage[aggregate.id] = aggregate

    # ... implement all port methods with dict storage
```

---

## Folder Structure

```
src/infrastructure/
├── persistence/
│   ├── models/
│   │   └── [aggregate]_model.py       ← SQLAlchemy model
│   ├── mappers/
│   │   └── [aggregate]_mapper.py      ← Domain ↔ ORM
│   ├── repositories/
│   │   └── [aggregate]_repository.py  ← Repository implementation
│   └── in_memory/
│       └── [aggregate]_repository.py  ← In-memory for tests
└── config/
    └── database.py                     ← Database configuration
```

---

## Mapping Domain to Database

Document how domain concepts map to database:

| Domain Concept | Database Representation |
|----------------|------------------------|
| [Aggregate] | Table: [table_name] |
| [ValueObject] | Column: [column] with type [type] |
| [Enum] | Enum column or string |
| [AggregateReference] | Foreign key: [column]_id |

---

## Dependencies

- **Depends on**: Domain layer (implements ports), Application layer (used by)
- **Technologies**: SQLAlchemy, Alembic, PostgreSQL/SQLite
- **Blocks**: Presentation layer (needs working repositories)

---

## Transaction Management

How transactions are handled:

1. **Repository commits** - Each repository method commits
2. **Unit of Work pattern** (optional) - Group multiple operations
3. **Session management** - Session per request

---

## Validation Checklist

- [ ] ORM model separate from domain model
- [ ] Mapper handles all domain ↔ database conversions
- [ ] Repository implements ALL methods from domain port
- [ ] Integration tests use in-memory database
- [ ] In-memory repository available for fast unit tests
- [ ] Migration creates correct schema
- [ ] No domain logic in infrastructure layer
- [ ] Domain layer has no knowledge of infrastructure

---

## Estimated Effort

- ORM Model: [X hours]
- Mapper: [X hours]
- Repository Implementation: [X hours]
- In-Memory Repository: [X hours]
- Migration: [X hours]
- Integration Tests: [X hours]
- **Total**: [X hours]

---

## Next Steps

After completing infrastructure layer:
1. Run `/plan_presentation [feature]` to plan API endpoints
2. Implement infrastructure with integration tests
3. Verify repository works with real database
4. Wire up repositories in application layer
```

## File Naming and Location

**Save plan to**: `documentation/plans/[feature-name]/003-infrastructure-layer.md`

Examples:
- `documentation/plans/education/003-infrastructure-layer.md`
- `documentation/plans/ruleset/003-infrastructure-layer.md`

## Skills to Apply

These skills activate automatically:
- **clean-architecture**: For dependency inversion
- **solid-principles**: For interface implementation
- **test-driven-development**: For integration tests

## Key Reminders

### Infrastructure Layer Rules
1. **Implement ports** - Domain defines interface, infrastructure implements
2. **Separate models** - ORM model ≠ domain model
3. **Use mappers** - Isolate domain from database concerns
4. **No business logic** - Pure technical implementation
5. **Dependency inversion** - Infrastructure depends on domain, not vice versa

### Dependency Direction
```
Domain (Port/Interface)
    ↑ (implements)
Infrastructure (Concrete Implementation)
```

### Clean Architecture Principle
Domain knows about `[Repository]` interface.
Infrastructure knows about both `[Repository]` interface AND implementation.
Domain never imports from infrastructure.

## Output

Provide a detailed, actionable plan that:
- Focuses ONLY on infrastructure layer
- Lists all infrastructure components
- Defines ORM models, mappers, repositories
- Specifies integration tests
- Respects dependency inversion principle
- Can be implemented after domain and application layers
