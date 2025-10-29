# Clean Architecture Workflow

This document explains the **incremental layer-by-layer workflow** for implementing features using Clean Architecture and DDD.

---

## Overview

Instead of planning all layers at once, we work **layer by layer from the inside out**:

```
Domain Layer (innermost)
    ↓
Application Layer
    ↓
Infrastructure Layer
    ↓
Presentation Layer (outermost)
```

Each layer has its own planning command, making it easier to:
- ✅ Learn Clean Architecture incrementally
- ✅ Understand dependencies between layers
- ✅ Keep PRs small and focused
- ✅ Work on one concern at a time

---

## Complete Workflow

### Phase 1: Domain Understanding

**Command**: `/domain [Feature]`

**Purpose**: Explore and understand the domain concept

**Activities**:
- Ask clarifying questions
- Identify if it's an entity, value object, or aggregate root
- Understand business rules and invariants
- Document relationships to other aggregates

**Output**: `documentation/domain-knowledge/[type]-[name].md`

**Example**: `/domain Education entity`

---

### Phase 2: Requirements Analysis

**Command**: `/analyze [Feature description]`

**Purpose**: Create executable Gherkin scenarios

**Activities**:
- Write user stories
- Create Gherkin scenarios (Given/When/Then)
- Cover happy paths, edge cases, and errors
- Make scenarios executable by pytest-bdd

**Output**: `tests/features/[domain]/[feature-name].feature`

**Example**: `/analyze Education entity - create, edit, and delete educations`

---

### Phase 3: Domain Layer Planning

**Command**: `/plan_domain [Feature]`

**Purpose**: Plan the domain layer (core business logic)

**Reads**:
- Feature file from `/analyze`
- Domain knowledge from `/domain`

**Plans**:
- Aggregate roots
- Value objects (identity, state, etc.)
- Domain exceptions
- Repository ports (interfaces)
- Business rule enforcement

**Output**: `documentation/plans/[feature]/001-domain-layer.md`

**Example**: `/plan_domain Education`

**What to implement**:
```
src/domain/
├── aggregates/education/
│   ├── education.py              ← Aggregate root
│   ├── education_id.py           ← Identity VO
│   ├── education_state.py        ← State VO
│   └── education_repository.py   ← Repository port
└── shared/
    ├── intake_term.py
    └── study_mode.py
```

---

### Phase 4: Application Layer Planning

**Command**: `/plan_application [Feature]`

**Purpose**: Plan the application layer (use cases)

**Reads**:
- Feature file from `/analyze`
- Domain layer plan
- Domain repository ports

**Plans**:
- Use cases (orchestration of domain logic)
- DTOs (Data Transfer Objects)
- Use case tests with mocked repositories

**Output**: `documentation/plans/[feature]/002-application-layer.md`

**Example**: `/plan_application Education`

**What to implement**:
```
src/application/
├── use_cases/education/
│   ├── create_education.py
│   ├── update_education.py
│   └── delete_education.py
└── dtos/
    └── education_dto.py
```

---

### Phase 5: Infrastructure Layer Planning

**Command**: `/plan_infrastructure [Feature]`

**Purpose**: Plan the infrastructure layer (persistence)

**Reads**:
- Domain layer plan (repository ports)
- Application layer plan (use cases)

**Plans**:
- ORM models (database schema)
- Mappers (domain ↔ ORM conversion)
- Repository implementations
- In-memory repositories (for testing)
- Database migrations

**Output**: `documentation/plans/[feature]/003-infrastructure-layer.md`

**Example**: `/plan_infrastructure Education`

**What to implement**:
```
src/infrastructure/persistence/
├── models/
│   └── education_model.py        ← SQLAlchemy model
├── mappers/
│   └── education_mapper.py       ← Domain ↔ ORM
├── repositories/
│   └── education_repository.py   ← Repository impl
└── in_memory/
    └── education_repository.py   ← For fast tests
```

---

### Phase 6: Presentation Layer Planning

**Command**: `/plan_presentation [Feature]`

**Purpose**: Plan the presentation layer (API endpoints)

**Reads**:
- Feature file (scenarios → endpoints)
- Application layer plan (use cases)
- Application DTOs

**Plans**:
- API endpoints (REST routes)
- Request/response schemas
- Dependency injection wiring
- Error handlers (domain errors → HTTP)
- E2E tests

**Output**: `documentation/plans/[feature]/004-presentation-layer.md`

**Example**: `/plan_presentation Education`

**What to implement**:
```
src/presentation/api/
├── routes/
│   └── education_routes.py       ← API endpoints
├── schemas/
│   └── education_schema.py       ← Request/response
├── dependencies.py               ← DI wiring
└── error_handlers.py             ← Error mapping
```

---

## Plan Organization

Plans are organized by feature in subdirectories:

```
documentation/plans/
├── education/
│   ├── 001-domain-layer.md
│   ├── 002-application-layer.md
│   ├── 003-infrastructure-layer.md
│   └── 004-presentation-layer.md
├── ruleset/
│   ├── 001-domain-layer.md
│   ├── 002-application-layer.md
│   └── ...
└── admission-process/
    └── ...
```

---

## Implementation Order

### ✅ Recommended: Layer by Layer

Implement each layer completely before moving to the next:

1. **Domain layer** → Pure business logic
2. **Application layer** → Use cases
3. **Infrastructure layer** → Persistence
4. **Presentation layer** → API

**Pros**:
- Learn one layer at a time
- Understand dependencies clearly
- Each layer has focused PR
- Easy to verify layer boundaries

**Cons**:
- Can't demo end-to-end until all layers done

---

### Alternative: Vertical Slices

Implement one thin slice through all layers for one scenario:

1. One domain concept + one use case + one repository + one endpoint
2. Then next scenario

**Pros**:
- Can demo working feature early
- Faster feedback loop

**Cons**:
- Jump between layers frequently
- Harder to focus on one architectural concern

---

## Dependencies Between Layers

```
┌─────────────────────────────────┐
│   Presentation Layer            │  ← Outermost
│   (Depends on Application)      │
├─────────────────────────────────┤
│   Infrastructure Layer          │
│   (Depends on Domain)           │
├─────────────────────────────────┤
│   Application Layer             │
│   (Depends on Domain)           │
├─────────────────────────────────┤
│   Domain Layer                  │  ← Innermost
│   (No dependencies)             │
└─────────────────────────────────┘
```

**Dependency Rule**: Dependencies point INWARD only.

- Domain has **no dependencies**
- Application depends on **Domain only**
- Infrastructure depends on **Domain** (implements ports)
- Presentation depends on **Application** (uses use cases)

---

## Testing Strategy by Layer

### Domain Layer
- **Unit tests** - Fast, isolated
- Test value objects, entities, business rules
- No mocks needed (pure logic)

### Application Layer
- **Unit tests** with mocked repositories
- Test use case orchestration
- Verify DTOs conversion

### Infrastructure Layer
- **Integration tests** with in-memory database
- Test repository implementations
- Verify mappers (domain ↔ ORM)

### Presentation Layer
- **E2E tests** with TestClient
- Test full request/response cycle
- Verify all layers wired correctly

---

## Clean Architecture Principles

### 1. Dependency Inversion
Domain defines interfaces (ports), infrastructure implements them.

### 2. Separation of Concerns
Each layer has one responsibility.

### 3. Testability
Can test each layer independently.

### 4. Independence
Domain logic independent of frameworks, databases, UI.

### 5. Screaming Architecture
Folder structure reveals domain concepts, not technical details.

---

## Quick Reference

| Command | Purpose | Output |
|---------|---------|--------|
| `/domain [Feature]` | Understand domain | `domain-knowledge/[type]-[name].md` |
| `/analyze [Feature]` | Create scenarios | `tests/features/[domain]/[feature].feature` |
| `/plan_domain [Feature]` | Plan domain | `plans/[feature]/001-domain-layer.md` |
| `/plan_application [Feature]` | Plan use cases | `plans/[feature]/002-application-layer.md` |
| `/plan_infrastructure [Feature]` | Plan persistence | `plans/[feature]/003-infrastructure-layer.md` |
| `/plan_presentation [Feature]` | Plan API | `plans/[feature]/004-presentation-layer.md` |

---

## Example: Education Feature

```bash
# 1. Understand domain
/domain Education entity

# 2. Create Gherkin scenarios
/analyze Education entity - create, edit, and delete educations

# 3. Plan domain layer
/plan_domain Education

# 4. Implement domain (TDD)
# ... write tests, implement value objects, aggregate root, etc.

# 5. Plan application layer
/plan_application Education

# 6. Implement application (TDD)
# ... write use case tests, implement use cases

# 7. Plan infrastructure layer
/plan_infrastructure Education

# 8. Implement infrastructure (integration tests)
# ... implement repositories, mappers, migrations

# 9. Plan presentation layer
/plan_presentation Education

# 10. Implement presentation (E2E tests)
# ... implement API endpoints, wire dependencies

# 11. Full integration test
# Verify entire stack works end-to-end
```

---

## Benefits of This Approach

✅ **Learning-friendly** - Focus on one layer at a time
✅ **Clear dependencies** - Understand what depends on what
✅ **Small PRs** - Each layer can be reviewed independently
✅ **Testable** - Each layer has appropriate test strategy
✅ **Maintainable** - Clear boundaries make changes easier
✅ **Flexible** - Can swap implementations without touching domain

---

## Next Steps

Ready to start implementing Education entity layer by layer!

1. Run `/plan_domain Education` to create domain layer plan
2. Implement domain layer with TDD
3. Move to application layer when domain is solid
