---
description: Plan the application layer implementation for a feature
argument-hint: [feature name]
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Application Layer Planning Phase

You are planning the **Application Layer** implementation following Clean Architecture principles.

## Your Task

Create an application layer implementation plan for: **$ARGUMENTS**

## What is the Application Layer?

The **Application Layer** orchestrates domain logic to fulfill application-specific workflows:

- **Use Cases** - Application business logic (workflows)
- **DTOs** - Data Transfer Objects for crossing boundaries
- **Application Services** - Coordinate multiple use cases
- **Transaction Management** - Ensure data consistency

**Key principle**: Application layer **depends only on Domain layer**. It orchestrates domain objects but contains no business rules.

## Before Planning

### 1. Read Context Documents

**REQUIRED**: Read these files first:

1. **Feature file**: `tests/features/[domain]/[feature-name].feature`
   - Gherkin scenarios define use cases to implement

2. **Domain layer plan**: `documentation/plans/[feature-name]/001-domain-layer.md`
   - Understand what domain components exist

3. **Domain knowledge**: `documentation/domain-knowledge/[type]-[name].md`
   - Understand aggregate capabilities

Use Glob to find relevant files.

### 2. Verify Domain Layer Exists

Check that domain layer is implemented:
- Aggregates in `src/domain/aggregates/[feature]/`
- Repository ports defined
- Domain exceptions created

If domain layer doesn't exist, ask user to complete domain layer first.

## Planning Structure

Create a plan in this format:

```markdown
# Application Layer Plan: [Feature Name]

**Feature**: [Feature Name]
**Layer**: Application (Use Cases)
**Date**: [Date]
**Depends on**: Domain Layer (001-domain-layer.md)

---

## Overview

[Brief description of what use cases will be implemented]

## Use Cases to Implement

Based on Gherkin scenarios:

1. **[UseCase]** - [Purpose]
   - Scenario: [Reference to Gherkin scenario]
   - Input: [What data comes in]
   - Output: [What data goes out]

2. **[UseCase]** - [Purpose]

---

## Implementation Steps (TDD)

### Step 1: DTOs (Data Transfer Objects)

**File**: `src/application/dtos/[feature]_dto.py`

**DTOs to create**:

```python
@dataclass
class [Request]DTO:
    """Input DTO for [use case]"""
    field1: str
    field2: int

@dataclass
class [Response]DTO:
    """Output DTO for [use case]"""
    field1: str
    field2: str
```

**Purpose**: Cross boundary between layers without exposing domain entities

---

### Step 2: [UseCase Name] Use Case

**File**: `src/application/use_cases/[feature]/[usecase].py`

**Gherkin Scenario**: [Reference scenario from feature file]

**Tests to write first**:
- `tests/unit/application/test_[usecase].py`
  - Test: [Scenario from Gherkin - happy path]
  - Test: [Scenario from Gherkin - validation error]
  - Test: [Scenario from Gherkin - not found error]
  - Test: Repository interaction (mock repository)

**Implementation**:
```python
class [UseCase]:
    """
    Use Case: [Description]

    Orchestrates domain logic to [purpose].
    """

    def __init__(self, repository: [Repository]):
        self._repo = repository

    def execute(self, request: [Request]DTO) -> [Response]DTO:
        # 1. Retrieve domain objects (if needed)
        # 2. Call domain logic
        # 3. Persist changes via repository
        # 4. Return DTO
```

**Responsibilities**:
- Orchestrate domain logic
- Manage transactions
- Convert DTOs ↔ Domain entities
- Handle application errors

**Does NOT**:
- Contain business rules (those belong in domain)
- Know about database details (uses repository port)
- Know about HTTP/API (that's presentation layer)

---

### Step 3: [Next UseCase]
[Similar structure]

---

## Folder Structure

```
src/application/
├── use_cases/
│   └── [feature]/
│       ├── __init__.py
│       ├── [create_usecase].py
│       ├── [update_usecase].py
│       └── [delete_usecase].py
└── dtos/
    └── [feature]_dto.py
```

---

## Use Case Mapping to Gherkin Scenarios

Map each use case to Gherkin scenarios:

| Use Case | Gherkin Scenarios | Purpose |
|----------|-------------------|---------|
| [UseCase1] | Scenario 1, 2 | [What it does] |
| [UseCase2] | Scenario 3, 4 | [What it does] |

---

## Dependencies

- **Depends on**: Domain layer (must be implemented first)
  - Uses: [Aggregate], [ValueObject], [RepositoryPort]
- **Blocks**: Infrastructure layer (needs use cases to wire up)

---

## Error Handling

How use cases handle domain exceptions:

1. **[DomainException]** → Return error DTO or re-throw
2. **[ValidationError]** → Return validation error DTO
3. **[NotFoundError]** → Return not found DTO

---

## Validation Checklist

- [ ] Each use case maps to Gherkin scenario(s)
- [ ] Use cases orchestrate, don't contain business rules
- [ ] DTOs used for input/output (no domain entities exposed)
- [ ] Use cases depend only on domain (via repository ports)
- [ ] All scenarios from feature file covered
- [ ] Tests use mocked repositories
- [ ] Transaction boundaries defined

---

## Estimated Effort

- DTOs: [X hours]
- Use Cases: [X hours]
- Tests: [X hours]
- **Total**: [X hours]

---

## Next Steps

After completing application layer:
1. Run `/plan_infrastructure [feature]` to plan repositories
2. Implement use cases with TDD
3. Verify all use case tests pass
```

## File Naming and Location

**Save plan to**: `documentation/plans/[feature-name]/002-application-layer.md`

Examples:
- `documentation/plans/education/002-application-layer.md`
- `documentation/plans/ruleset/002-application-layer.md`

## Skills to Apply

These skills activate automatically:
- **test-driven-development**: For TDD approach
- **clean-architecture**: For layer boundaries
- **solid-principles**: For use case design

## Key Reminders

### Application Layer Rules
1. **Orchestrate, don't implement** - Business rules live in domain
2. **Use repository ports** - Not implementations
3. **DTOs at boundaries** - Don't expose domain entities
4. **Transaction management** - Coordinate persistence
5. **Depend on domain only** - No infrastructure dependencies

### Clean Architecture Boundary
```
Application Layer
    ↓ (depends on)
Domain Layer
    ↑ (no knowledge of)
Application Layer
```

## Output

Provide a detailed, actionable plan that:
- Focuses ONLY on application layer
- Lists all use cases to implement
- Maps use cases to Gherkin scenarios
- Defines DTOs for boundaries
- Specifies test cases
- Respects Clean Architecture dependency rules
- Can be implemented after domain layer is complete
