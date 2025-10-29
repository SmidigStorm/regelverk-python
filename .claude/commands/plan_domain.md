---
description: Plan the domain layer implementation for a feature
argument-hint: [feature name]
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Domain Layer Planning Phase

You are planning the **Domain Layer** implementation following Clean Architecture principles.

## Your Task

Create a domain layer implementation plan for: **$ARGUMENTS**

## What is the Domain Layer?

The **Domain Layer** is the innermost layer containing pure business logic:

- **Aggregates** - Aggregate roots with their boundaries
- **Entities** - Objects with identity
- **Value Objects** - Immutable objects without identity
- **Domain Services** - Business logic that doesn't belong to a single entity
- **Repository Ports** - Interfaces (contracts) for persistence
- **Domain Events** - Things that happened in the domain
- **Domain Exceptions** - Business rule violations

**Key principle**: Domain layer has **NO dependencies** on outer layers. Pure business logic only.

## Before Planning

### 1. Read Context Documents

**REQUIRED**: Read these files first:

1. **Feature file**: `tests/features/[domain]/[feature-name].feature`
   - Gherkin scenarios define what to implement

2. **Domain knowledge**: `documentation/domain-knowledge/[type]-[name].md`
   - Understand aggregate structure, business rules, invariants

Use Glob to find relevant files. If they don't exist, ask user to run `/domain` and `/analyze` first.

### 2. Check Existing Domain Layer

Look for existing patterns:
- Existing aggregates in `src/domain/aggregates/`
- Existing value objects in `src/domain/shared/`
- Existing domain exceptions in `src/domain/exceptions.py`

## Planning Structure

Create a plan in this format:

```markdown
# Domain Layer Plan: [Feature Name]

**Feature**: [Feature Name]
**Layer**: Domain (Core Business Logic)
**Date**: [Date]

---

## Overview

[Brief description of what domain concepts will be implemented]

## Domain Model

### Aggregate Root: [Name]
- **Purpose**: [What this aggregate represents]
- **Invariants**: [Business rules it must enforce]
- **Lifecycle**: [States and transitions]

### Value Objects
1. **[Name]** - [Purpose]
2. **[Name]** - [Purpose]

### Domain Exceptions
1. **[Name]** - [When thrown]

### Repository Port
- **[Name]Repository** - [Interface for persistence]

---

## Implementation Steps (TDD)

### Step 1: [Value Object Name]

**File**: `src/domain/[aggregates/feature or shared]/[name].py`

**Tests to write first**:
- `tests/unit/domain/test_[name].py`
  - Test: [Specific scenario from Gherkin]
  - Test: [Edge case]
  - Test: [Validation rule]

**Implementation**:
```python
# Pseudocode showing structure
@dataclass(frozen=True)
class [Name]:
    [attributes]

    def __post_init__(self):
        # Validation
```

**Invariants**:
- [Rule 1]
- [Rule 2]

### Step 2: [Next Component]
[Similar structure for each component]

---

## Folder Structure

```
src/domain/
├── aggregates/
│   └── [feature]/
│       ├── [aggregate_root].py
│       ├── [aggregate_specific_vo].py
│       └── [repository_interface].py
├── shared/
│   └── [shared_vo].py
└── exceptions.py
```

---

## Business Rules to Enforce

From Gherkin scenarios and domain knowledge:

1. **[Rule]**: [Description]
   - Scenario: [Reference to Gherkin scenario]
   - Implementation: [Where enforced]

2. **[Rule]**: [Description]

---

## Dependencies

- Depends on: [None for domain layer - it's the core]
- Blocks: Application layer implementation (needs these domain concepts)

---

## Validation Checklist

- [ ] All value objects are immutable
- [ ] All invariants are enforced
- [ ] Aggregate protects its boundaries
- [ ] No dependencies on outer layers
- [ ] Repository is interface only (port)
- [ ] Domain exceptions express business rules clearly
- [ ] All Gherkin scenarios have corresponding domain logic

---

## Estimated Effort

- Value Objects: [X hours]
- Aggregate Root: [X hours]
- Domain Services: [X hours]
- Tests: [X hours]
- **Total**: [X hours]

---

## Next Steps

After completing domain layer:
1. Run `/plan_application [feature]` to plan use cases
2. Implement domain layer with TDD
3. Verify all domain tests pass
```

## File Naming and Location

**Save plan to**: `documentation/plans/[feature-name]/001-domain-layer.md`

Examples:
- `documentation/plans/education/001-domain-layer.md`
- `documentation/plans/ruleset/001-domain-layer.md`

Create the feature folder if it doesn't exist.

## Skills to Apply

These skills activate automatically:
- **domain-driven-design**: For domain modeling
- **test-driven-development**: For TDD approach
- **solid-principles**: For design quality

## Key Reminders

### Domain Layer Rules
1. **No framework dependencies** - Pure Python only
2. **No database code** - Repository is interface only
3. **No use case logic** - Just business rules
4. **Rich behavior** - Not anemic data classes
5. **Protect invariants** - Encapsulation is key

### TDD Approach
- Write test first (RED)
- Make it pass (GREEN)
- Refactor (REFACTOR)
- Start with value objects (simplest)
- Build up to aggregate root

## Output

Provide a detailed, actionable plan that:
- Focuses ONLY on domain layer
- Lists all domain components to build
- Specifies test cases for each component
- References Gherkin scenarios
- Enforces DDD principles
- Follows TDD methodology
- Can be implemented independently of other layers
