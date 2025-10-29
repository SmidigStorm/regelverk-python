# Norwegian Admission Rules System (Regelverk Python)

This project implements the rules and logic for the Norwegian higher education admission system (Samordna opptak).

## Project Purpose

The goal is to:
1. Build a working admission rules engine for Norwegian higher education
2. Learn and practice modern software development skills (TDD, DDD, Clean Architecture, etc.)
3. Explore Claude Code's features: commands, agents, and skills

## Domain Context

### Norwegian Admission System
The Norwegian admission system (Samordna opptak) handles applications to higher education with:
- **Opptakskrav** (Admission Requirements): Rules students must meet
- **Kvoter** (Quotas): Capacity limits and priority groups (ordinary, special competence, etc.)
- **Karakterpoeng** (Competence Points): Calculated from upper secondary school grades
- **Rangering** (Ranking): Students ranked by points for competitive programs

### Key Domain Concepts
- **Student/Søker**: Applicant with grades and qualifications
- **Program/Studieprogram**: Degree program with admission requirements
- **Admission Rule/Opptaksregel**: Business rule for eligibility
- **Quota/Kvote**: Capacity constraint with specific criteria
- **Grade/Karakter**: Norwegian grade (1-6 scale, where 6 is best)
- **Competence Points**: Calculated as grade × 4 points per subject

## Technology Stack

- **Language**: Python 3.11+
- **Testing**: pytest, pytest-bdd (for Gherkin scenarios)
- **Architecture**: Clean Architecture with DDD patterns
- **Development**: Trunk-based development workflow

## Project Structure

Following Clean Architecture:

```
regelverk-python/
├── src/
│   ├── domain/              # Domain layer - core business logic
│   │   ├── aggregates/      # Aggregates (organized by aggregate root)
│   │   │   ├── education/   # Education aggregate
│   │   │   │   ├── education.py              # Aggregate root entity
│   │   │   │   ├── education_id.py           # Identity value object
│   │   │   │   ├── education_state.py        # State value object
│   │   │   │   └── education_repository.py   # Repository interface
│   │   │   └── ruleset/     # Ruleset aggregate (future)
│   │   ├── shared/          # Shared value objects across aggregates
│   │   │   ├── intake_term.py
│   │   │   ├── study_mode.py
│   │   │   └── admission_process_id.py
│   │   ├── services/        # Domain services
│   │   ├── events/          # Domain events
│   │   ├── specifications/  # Reusable business rules
│   │   ├── policies/        # Complex business decisions
│   │   ├── factories/       # Object creation logic
│   │   └── exceptions.py    # Domain exceptions
│   ├── application/         # Application layer
│   │   ├── use_cases/       # Application business logic
│   │   └── dtos/            # Data transfer objects
│   ├── infrastructure/      # Infrastructure layer
│   │   ├── persistence/     # Database repositories
│   │   ├── config/          # Configuration
│   │   └── external/        # External system adapters
│   └── presentation/        # Presentation layer
│       └── api/             # REST API (FastAPI)
├── tests/
│   ├── unit/               # Fast isolated tests
│   ├── integration/        # Component interaction tests
│   ├── e2e/               # End-to-end tests
│   └── features/          # Gherkin .feature files (BDD)
├── documentation/          # Project documentation
│   ├── requirements/      # User stories and specifications
│   ├── architecture/      # Architecture decisions
│   ├── plans/            # Implementation plans
│   └── domain-glossary.md # Ubiquitous language definitions
└── .claude/
    ├── skills/            # Software development skills
    └── commands/          # Custom slash commands
```

## Development Principles

This project follows strict software development practices via Claude Code skills:

1. **Requirements First**: Every feature starts with user stories and Gherkin scenarios
2. **Test-Driven Development**: Tests written before implementation (Red-Green-Refactor)
3. **Domain-Driven Design**: Rich domain models with behavior, not anemic data classes
4. **Clean Architecture**: Dependencies point inward (Domain ← Application ← Infrastructure ← Presentation)
5. **SOLID Principles**: Single responsibility, dependency inversion, etc.
6. **Trunk-Based Development**: Short-lived branches (<2 days), small PRs, feature flags

## Skills Configuration

Six skills are configured in `.claude/skills/` that automatically guide development:
- **requirements-writing**: User stories and Gherkin
- **solid-principles**: SOLID OOP design
- **clean-architecture**: Layer organization
- **test-driven-development**: TDD practices
- **domain-driven-design**: DDD patterns
- **trunk-based-development**: Git workflow

**Note**: These skills are automatically applied by Claude based on context - no need to explicitly invoke them.

## Current Status

- ✅ Skills configured
- ⏳ Project structure to be created
- ⏳ First domain models to be defined
- ⏳ Core admission rules to be implemented

## Example Features to Implement

1. **Minimum Grade Requirement Rule**
   - Students must meet minimum grade thresholds for specific subjects
   - Example: Computer Science requires Math grade ≥ 4

2. **Competence Points Calculation**
   - Calculate total points from all grades
   - Formula: sum of (grade × 4) for all subjects

3. **Quota Management**
   - Enforce capacity limits
   - Handle multiple quota types (ordinary, special competence, etc.)
   - Priority rules for quota assignment

4. **Admission Evaluation**
   - Apply all rules to determine eligibility
   - Rank applicants by competence points
   - Assign to appropriate quotas

## How to Work on This Project

When the user asks to implement something, you should:

1. **Define Requirements** (requirements-writing skill activates)
   - Write user story
   - Create Gherkin scenarios with examples

2. **Design Domain Model** (domain-driven-design skill activates)
   - Identify entities vs value objects
   - Define aggregates and their boundaries
   - Place in domain layer

3. **Plan Architecture** (clean-architecture skill activates)
   - Determine layer placement
   - Define ports/protocols for boundaries
   - Ensure dependencies point inward

4. **Create Branch** (trunk-based-development skill activates)
   - Short-lived branch if work > 4 hours
   - Otherwise commit directly to main

5. **Implement with TDD** (test-driven-development skill activates)
   - Write test first (RED)
   - Make it pass (GREEN)
   - Refactor with SOLID (REFACTOR)

6. **Merge Fast** (trunk-based-development skill activates)
   - Small PR (<400 lines)
   - Quick review
   - Merge within 1-2 days

## Norwegian Terms / English Equivalents

Use ubiquitous language from the domain:

| Norwegian | English | Usage |
|-----------|---------|-------|
| Opptakskrav | Admission Requirement | Use in domain models |
| Karakterpoeng | Competence Points | Value object |
| Kvote | Quota | Entity with capacity invariant |
| Søker | Applicant/Student | Entity (aggregate root) |
| Rangering | Ranking | Domain service |
| Studieprogram | Study Program | Entity |
| Karakter | Grade | Value object |

Prefer English for code but understand Norwegian domain terminology.

## Learning Objectives

This project is also a learning exercise for:
- Mastering Claude Code features (skills, commands, agents)
- Practicing TDD in a real domain
- Applying Clean Architecture principles
- Understanding DDD tactical patterns
- Working with trunk-based development

## Getting Started

When user wants to start implementing:
1. Help them define the first requirement (suggest starting with Grade value object or simple admission rule)
2. Write Gherkin scenarios together
3. Set up project structure following Clean Architecture
4. Implement first feature with full TDD cycle
5. Build incrementally from there

---

**Remember**: All the skills are configured to activate automatically. Just guide the development naturally and the skills will ensure best practices are followed.
