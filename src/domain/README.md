# Domain Layer

This is the **core business logic layer** with no external dependencies.

## Folder Structure

Following **Microsoft's eShopOnContainers approach**, we organize by aggregate:

```
src/domain/
├── aggregates/              # Aggregates (organized by aggregate root)
│   └── education/           # Education aggregate
│       ├── education.py              # Aggregate root entity
│       ├── education_id.py           # Identity value object
│       ├── education_state.py        # State value object
│       └── education_repository.py   # Repository interface (port)
│
├── shared/                  # Shared value objects across aggregates
│   ├── intake_term.py       # Composite value (semester + year)
│   ├── study_mode.py        # Enum (full-time, part-time)
│   ├── ruleset_id.py        # Reference to Ruleset aggregate
│   └── admission_process_id.py  # Reference to AdmissionProcess aggregate
│
├── services/                # Domain services (cross-aggregate operations)
├── events/                  # Domain events
├── specifications/          # Reusable business rules (Specification pattern)
├── policies/                # Complex business decisions (Policy pattern)
├── factories/               # Object creation logic (Factory pattern)
└── exceptions.py            # Domain exceptions
```

## Design Principles

### Aggregate Organization
- Each **aggregate** gets its own folder under `aggregates/`
- Within each aggregate folder:
  - Aggregate root entity
  - Aggregate-specific value objects (e.g., EducationId, EducationState)
  - Repository interface (port)
  - Child entities (if any)

### Shared Concepts
- Value objects used by **multiple aggregates** go in `shared/`
- Examples: IntakeTerm, StudyMode, cross-aggregate ID references

### Why This Structure?
1. **Clear aggregate boundaries** - Each aggregate is self-contained
2. **Cohesion** - Related domain concepts live together
3. **Discoverability** - Easy to find all components of an aggregate
4. **Industry standard** - Follows Microsoft's reference architecture

## DDD Patterns

### Aggregate Root
An entity that is the entry point to an aggregate and enforces invariants.

**Example**: Education (manages state transitions, validation, deletion rules)

### Value Object
Immutable objects without identity, defined by their attributes.

**Example**: EducationId, IntakeTerm, StudyMode

### Repository (Port)
Interface for aggregate persistence, defined in domain, implemented in infrastructure.

**Example**: EducationRepository interface in `aggregates/education/`

### Domain Events
Events that capture something significant that happened in the domain.

**Example**: EducationCreated, EducationStateChanged

## Dependencies

The domain layer has **NO dependencies** on other layers:
- ❌ No imports from application, infrastructure, or presentation
- ✅ Pure Python, pure business logic
- ✅ Defines ports (interfaces) that other layers implement

## References

- [Microsoft .NET Microservices: Domain Model Layer](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/net-core-microservice-domain-model)
- [Martin Fowler: DDD Aggregate](https://martinfowler.com/bliki/DDD_Aggregate.html)
