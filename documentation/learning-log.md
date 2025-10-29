# Learning Log

This document tracks insights and improvements discovered during development.

---

## 2025-10-28: First Development Workflow Test

### What We Learned

#### 1. `/analyze` Command Output Format
**Issue**: The `/analyze` command was generating a comprehensive markdown document with user stories, architecture notes, and Gherkin scenarios mixed together. This was not what we wanted.

**What We Want**: A single `.feature` file in pure Gherkin format that can be executed by pytest-bdd.

**Solution**: Updated `.claude/commands/analyze.md` to:
- Output only a Gherkin `.feature` file
- Place file in `tests/features/[domain-area]/[feature-name].feature`
- Use kebab-case naming (e.g., `manage-education.feature`)
- Include only Gherkin syntax (Feature, Background, Scenario, Given/When/Then)
- Avoid markdown documentation, architecture notes, or implementation details

**File Structure**:
```
Feature: [Name]
  As a [role]
  I want [capability]
  So that [benefit]

  Background:
    Given [common setup]

  Scenario: [Happy path]
    Given/When/Then...

  Scenario: [Edge case]
    Given/When/Then...

  Scenario: [Error case]
    Given/When/Then...
```

#### 2. `/domain` Command Documentation
**Issue**: When exploring domain concepts, we needed a way to persist our understanding for future reference.

**Solution**: Added automatic documentation creation to `/domain` command:
- Creates files in `documentation/domain-knowledge/`
- Naming convention: `aggregate-root-{name}.md`, `entity-{name}.md`, `value-object-{name}.md`, etc.
- Includes: definition, examples, attributes, business rules, relationships, design decisions, open questions

**Result**: Domain knowledge is now captured and can be referenced during implementation.

#### 3. Why Feature Files Go in `tests/features/`
**Question**: Why are Gherkin `.feature` files placed in `tests/features/` instead of `documentation/`?

**Answer**: Gherkin feature files are **executable tests**, not just documentation:
- pytest-bdd discovers and runs them as automated tests
- They validate that implementation matches business requirements
- They serve as "living documentation" that stays up-to-date because they execute
- This is the standard BDD structure in Python projects

**Directory Structure**:
```
tests/
├── features/       ← Gherkin .feature files (executable test scenarios)
├── step_defs/      ← Python step definitions (implement Given/When/Then)
├── unit/           ← Traditional unit tests
└── integration/    ← Traditional integration tests
```

**Result**: Updated `/analyze` command to include this explanation.

#### 4. `/plan` Command Should Reference Domain Knowledge and Feature Files
**Issue**: The `/plan` command needs context from previous workflow steps to create accurate implementation plans.

**Solution**: Updated `.claude/commands/plan.md` to require reading both:
1. **Feature file** (`tests/features/[domain]/[feature-name].feature`) - For Gherkin scenarios and acceptance criteria
2. **Domain knowledge** (`documentation/domain-knowledge/[type]-[name].md`) - For entity structure, business rules, and relationships

**How it works:**
- Use Glob to discover relevant files
- Read both before creating the implementation plan
- If files don't exist, prompt user to run `/domain` or `/analyze` first

**Result**: Plans will now be based on complete context from domain exploration and requirements analysis.

#### 5. Domain Folder Structure - Microsoft's Aggregate Organization Approach
**Question**: Should aggregate roots go in `src/domain/aggregates/` or `src/domain/entities/`? What about value objects - in a flat `value_objects/` folder or grouped with their aggregates?

**Research**: Searched online for DDD folder structure best practices. Found Microsoft's official guidance in their eShopOnContainers reference application.

**Microsoft's Approach** (from .NET Microservices documentation):
```
src/domain/
├── AggregatesModel/
│   ├── OrderAggregate/
│   │   ├── Order.cs              ← Aggregate Root
│   │   ├── OrderItem.cs          ← Child Entity
│   │   ├── Address.cs            ← Value Object
│   │   └── IOrderRepository.cs   ← Repository interface
│   └── BuyerAggregate/
```

**Key principle**: Organize by aggregate, not by technical type. Each aggregate folder contains:
- The aggregate root entity
- Child entities (if any)
- Aggregate-specific value objects
- Repository interface

**Our Decision**: Follow Microsoft's approach:
```
src/domain/
├── aggregates/
│   └── education/
│       ├── education.py              ← Aggregate Root
│       ├── education_id.py           ← Identity Value Object
│       ├── education_state.py        ← State Value Object
│       └── education_repository.py   ← Repository interface
├── shared/                           ← Shared value objects across aggregates
│   ├── intake_term.py
│   ├── study_mode.py
│   └── ruleset_id.py
```

**Result**:
- Updated CLAUDE.md and implementation plan to reflect this structure
- Created actual folder structure: `src/domain/aggregates/education/` and `src/domain/shared/`
- Added README.md in domain layer documenting the structure and design principles
- This makes aggregate boundaries crystal clear and keeps related domain concepts together

#### 6. Factory Pattern - Static Methods vs Separate Factory Classes
**Question**: Should we use static factory methods on the aggregate (like `Education.create()`) or separate factory classes in the `factories/` folder?

**Research**: Searched for DDD factory pattern best practices. Found clear guidelines on when to use each approach.

**Decision Tree**:

**Use Static Factory Method** (on aggregate itself) when:
- ✅ Simple creation logic (just validation and initialization)
- ✅ Single aggregate type (always returns same type)
- ✅ No external dependencies (no repositories or domain services needed)
- ✅ Reads naturally (`Education.create(...)` flows well)
- ✅ ORM compatibility needed (private constructor for hydration, public factory for creation)

**Use Separate Factory Class** (in `factories/` folder) when:
- ✅ Complex creation logic (multiple steps, complex algorithms)
- ✅ Multiple return types (factory returns different types based on input)
- ✅ External dependencies (needs repositories, domain services, other aggregates)
- ✅ Reconstitution logic (complex logic to rebuild from external data)
- ✅ Testability concerns (need to mock/inject factory behavior)

**Our Decision**:
- Education aggregate uses static method `Education.create()` (simple creation, no dependencies)
- Keep `factories/` folder for future complex factories
- Document when to use each approach

**Result**:
- Added README.md in `src/domain/factories/` explaining when to use separate factories
- Kept static factory method in implementation plan
- Clarity on when to add files to factories folder vs using static methods

#### 7. Incremental Layer-by-Layer Planning Commands
**Issue**: The original `/plan` command created one massive plan covering all layers (domain, application, infrastructure, presentation) at once. This was overwhelming for learning Clean Architecture incrementally.

**User Request**: "I want to learn Clean Architecture step by step. Can we have one slash command per layer so I can work on it more incrementally?"

**Solution**: Created four separate planning commands:

1. **`/plan_domain [feature]`** - Plan domain layer only (pure business logic)
2. **`/plan_application [feature]`** - Plan application layer only (use cases)
3. **`/plan_infrastructure [feature]`** - Plan infrastructure layer only (repositories, database)
4. **`/plan_presentation [feature]`** - Plan presentation layer only (API endpoints)

**Benefits**:
- ✅ Learn one layer at a time
- ✅ Understand dependencies clearly (each layer depends on inner layers)
- ✅ Keep PRs small and focused
- ✅ Better organized plans by feature

**Plan Organization**:
```
documentation/plans/
├── education/
│   ├── 001-domain-layer.md
│   ├── 002-application-layer.md
│   ├── 003-infrastructure-layer.md
│   └── 004-presentation-layer.md
└── ruleset/
    └── 001-domain-layer.md
```

**Workflow**:
1. Run `/domain [feature]` → understand domain
2. Run `/analyze [feature]` → create Gherkin scenarios
3. Run `/plan_domain [feature]` → plan domain layer
4. Implement domain layer with TDD
5. Run `/plan_application [feature]` → plan use cases
6. Implement application layer
7. Continue layer by layer...

**Result**: Much more manageable learning path for Clean Architecture. Each command focuses on a single layer with clear prerequisites and dependencies.

---

## Workflow Insights

### Current Workflow
1. **Domain Understanding** (`/domain`): Explore and document domain concepts
2. **Requirements Analysis** (`/analyze`): Create executable Gherkin scenarios
3. **Planning** (`/plan`): Create implementation plan (to be tested next)
4. **Execution** (`/execute`): Implement with TDD (to be tested next)

### What Works Well
- Interactive questioning during `/domain` phase helped clarify the Education entity
- Separating domain knowledge documentation from executable requirements
- Using pure Gherkin for requirements keeps them focused and testable

### What to Test Next
- Run `/analyze` again with updated command to verify it produces correct output
- Test `/plan` command with the feature file
- Test `/execute` command with TDD workflow

---

## Open Questions

1. Should we add a `/review` command to review feature files and suggest improvements?
2. Should `/analyze` automatically invoke `/domain` if no domain knowledge exists for the entity?
3. How should we handle scenarios that span multiple aggregates?

---

## Next Session Goals

- Test updated `/analyze` command
- Complete first implementation using TDD
- Document any additional learnings
