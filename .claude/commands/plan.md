---
description: Create an implementation plan for the analyzed requirements
argument-hint: [feature or reference to analysis]
allowed-tools: Read, Grep, Glob
---

# Implementation Planning Phase

You are in the **planning phase** of the workflow. Your goal is to create a detailed, actionable implementation plan based on the requirements analysis.

## Your Task

Create an implementation plan for: **$ARGUMENTS**

## What to Do

### 1. Review Requirements
- Read the requirements analysis (if provided)
- Understand user stories and acceptance criteria
- Identify all Gherkin scenarios to implement

### 2. Break Down into Tasks
Create a step-by-step implementation plan following:
- **TDD approach**: Test first, then implementation
- **Clean Architecture**: Inside-out (domain → application → infrastructure → presentation)
- **Incremental delivery**: Small, mergeable pieces

### 3. Design Domain Model
- Define entities, value objects, aggregates
- Specify domain services
- Identify domain events
- Define invariants and business rules

### 4. Define Architecture
- Specify which layer each component belongs to
- Define ports (interfaces) needed
- Identify adapters (implementations) needed
- Plan DTOs for boundary crossing

### 5. Plan Git Workflow
- Determine if branch is needed (>4 hours work = branch)
- Break into small PRs if large feature
- Identify places for feature flags if incomplete work needs merging

## Plan Structure

Provide your plan in this format:

```markdown
# Implementation Plan: [Feature Name]

## Overview
[Brief summary of what will be implemented]

## Prerequisites
- [ ] [Any dependencies or setup needed]

## Domain Layer (TDD)

### Step 1: [First domain concept]
**Files to create:**
- `src/domain/value_objects/[name].py`

**Tests to write first:**
- `tests/unit/domain/test_[name].py`
  - Test: [specific test case from Gherkin]
  - Test: [edge case]

**Implementation:**
- [What to implement]
- Invariants: [business rules to enforce]

### Step 2: [Second domain concept]
[Similar structure]

## Application Layer (TDD)

### Step 3: [Use case]
**Files to create:**
- `src/application/use_cases/[name]_use_case.py`
- `src/application/dtos/[name]_dto.py`

**Tests to write first:**
- `tests/unit/application/test_[name]_use_case.py`
  - Test: [scenario from Gherkin]

**Implementation:**
- Orchestrate domain logic
- Define input/output DTOs
- Reference domain ports

## Infrastructure Layer

### Step 4: [Repository implementation]
**Files to create:**
- `src/infrastructure/persistence/models/[name]_model.py`
- `src/infrastructure/persistence/mappers/[name]_mapper.py`
- `src/infrastructure/persistence/repositories/[name]_repository.py`

**Tests:**
- Integration test with in-memory SQLite

**Implementation:**
- SQLAlchemy model (separate from domain!)
- Mapper (domain ↔ ORM)
- Repository implementing domain port

### Step 5: [Database migration]
**Commands:**
```bash
alembic revision --autogenerate -m "Add [table]"
alembic upgrade head
```

## Presentation Layer

### Step 6: [API endpoint]
**Files to create:**
- `src/presentation/api/routes/[name]_routes.py`
- `src/presentation/api/schemas/[name]_schema.py`

**Tests:**
- E2E test using FastAPI TestClient

**Implementation:**
- Pydantic request/response schemas
- FastAPI route
- Dependency injection wiring

## Git Workflow

### Branching Strategy
- [ ] Branch needed: [yes/no]
- Branch name: `[name]` (if needed)
- Target: Merge within [1-2 days]

### Feature Flags
- [ ] Feature flag needed: [yes/no]
- Flag name: `[name]` (if incomplete work)

### Merge Plan
- PR size target: [< 400 lines]
- If larger, split into:
  1. [First PR: domain models]
  2. [Second PR: use cases]
  3. [Third PR: infrastructure + API]

## Task Checklist

Execute in this order:

- [ ] **Domain Layer**
  - [ ] Write tests for [value object/entity]
  - [ ] Implement [value object/entity]
  - [ ] Write tests for [domain service]
  - [ ] Implement [domain service]

- [ ] **Application Layer**
  - [ ] Write tests for [use case]
  - [ ] Define DTOs
  - [ ] Implement [use case]

- [ ] **Infrastructure Layer**
  - [ ] Create SQLAlchemy models
  - [ ] Create mappers
  - [ ] Write integration tests for repositories
  - [ ] Implement repositories
  - [ ] Create/run migration

- [ ] **Presentation Layer**
  - [ ] Define Pydantic schemas
  - [ ] Write E2E tests for API
  - [ ] Implement FastAPI routes
  - [ ] Wire up dependencies

- [ ] **Verification**
  - [ ] All tests pass
  - [ ] Gherkin scenarios verified
  - [ ] Manual testing done
  - [ ] Ready to merge

## Dependencies

- Depends on: [other features/tasks]
- Blocks: [other features/tasks]

## Risks & Considerations

- [Risk 1]: [mitigation]
- [Risk 2]: [mitigation]

## Estimated Effort

- Domain: [X hours]
- Application: [X hours]
- Infrastructure: [X hours]
- Presentation: [X hours]
- **Total**: [X hours/days]

Branch needed if > 4 hours.
```

## Skills to Apply

Use these skills automatically:
- **test-driven-development**: For TDD workflow
- **domain-driven-design**: For domain modeling
- **clean-architecture**: For layer organization
- **solid-principles**: For design quality
- **trunk-based-development**: For git workflow

## Review Existing Code

Check for:
- Similar patterns to follow
- Existing domain models to extend
- Reusable components

## Output

Provide a complete, actionable implementation plan that can be executed step-by-step in the `/execute` phase.

The plan should be:
- Detailed enough to follow
- Test-driven (tests before implementation)
- Incremental (small steps)
- Architecture-compliant (Clean Architecture + DDD)
