# Project Structure Options

This document explores different approaches to organizing the Norwegian Admission Rules System codebase, based on Clean Architecture, Hexagonal Architecture (Ports & Adapters), DDD, and Screaming Architecture principles.

## Key Architectural Concepts

### Clean Architecture Layers
- **Entities (Domain)**: Enterprise business rules
- **Use Cases (Application)**: Application business rules
- **Interface Adapters (Infrastructure)**: Converters between use cases and external agencies
- **Frameworks & Drivers (Presentation)**: External tools

### Hexagonal Architecture (Ports & Adapters)
- **Primary/Driving Ports**: Entry points to application (inbound)
  - Example: Use case interfaces, API contracts
  - Driven BY external actors (user, API client)
- **Secondary/Driven Ports**: Exit points from application (outbound)
  - Example: Repository interfaces, external service interfaces
  - Driven BY the application to access external resources
- **Adapters**: Implementations of ports
  - Primary adapters: REST controllers, CLI, GraphQL
  - Secondary adapters: Database repositories, external API clients

### DDD Building Blocks
- **Entities**: Objects with identity
- **Value Objects**: Immutable objects defined by attributes
- **Aggregates**: Clusters with one root entity
- **Domain Services**: Operations that don't belong to entities
- **Repositories**: Interfaces for accessing aggregates
- **Domain Events**: Things that happened in the domain

### Screaming Architecture
> "The architecture should scream about the use cases, not the frameworks."
> — Robert C. Martin

**Package by Feature** (Screaming) vs **Package by Layer** (Traditional)

---

## Option 1: Clean Architecture - Package by Layer

Traditional layered approach where you organize by technical concerns.

```
src/
├── domain/                      # Layer 1: Entities (Pure Python)
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── admission_rule.py
│   │   ├── quota.py
│   │   └── program.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   ├── grade.py
│   │   ├── competence_points.py
│   │   ├── student_id.py
│   │   └── quota_name.py
│   ├── aggregates/
│   │   ├── __init__.py
│   │   └── admission_application.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── admission_evaluation_service.py
│   ├── events/
│   │   ├── __init__.py
│   │   ├── student_admitted.py
│   │   └── quota_filled.py
│   └── exceptions/
│       ├── __init__.py
│       └── domain_exceptions.py
│
├── application/                 # Layer 2: Use Cases
│   ├── use_cases/
│   │   ├── __init__.py
│   │   ├── evaluate_admission.py
│   │   ├── calculate_competence_points.py
│   │   └── assign_quota.py
│   ├── dtos/
│   │   ├── __init__.py
│   │   ├── admission_dto.py
│   │   └── student_dto.py
│   └── ports/                   # Interfaces (owned by application/domain)
│       ├── __init__.py
│       ├── repositories.py      # Repository protocols
│       └── services.py          # External service protocols
│
├── infrastructure/              # Layer 3: Interface Adapters
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── models/             # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── student_model.py
│   │   │   └── quota_model.py
│   │   ├── mappers/            # Domain ↔ ORM mappers
│   │   │   ├── __init__.py
│   │   │   ├── student_mapper.py
│   │   │   └── quota_mapper.py
│   │   └── repositories/       # Repository implementations
│   │       ├── __init__.py
│   │       ├── sqlalchemy_student_repository.py
│   │       └── sqlalchemy_quota_repository.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── settings.py
│   └── external/               # External API adapters
│       ├── __init__.py
│       └── samordna_opptak_client.py
│
└── presentation/                # Layer 4: Frameworks & Drivers
    ├── api/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── dependencies.py     # DI wiring
    │   ├── schemas/            # Pydantic request/response models
    │   │   ├── __init__.py
    │   │   ├── admission_schema.py
    │   │   └── student_schema.py
    │   └── routes/
    │       ├── __init__.py
    │       ├── admission.py
    │       ├── students.py
    │       └── quotas.py
    └── cli/                    # Optional CLI interface
        └── __init__.py
```

### Pros
✅ Clear separation by technical concerns
✅ Easy to understand layers
✅ Good for developers familiar with layered architecture
✅ Dependencies clearly point inward

### Cons
❌ Doesn't "scream" what the application does
❌ Easy to skip layers (controller → repository directly)
❌ Changes to a feature require touching multiple directories
❌ Hard to see all code related to one use case

---

## Option 2: Hexagonal Architecture - Explicit Ports & Adapters

Emphasizes the hexagon with explicit primary/secondary ports and adapters.

```
src/
├── domain/                      # Application Core (Hexagon Center)
│   ├── model/                   # Domain model
│   │   ├── entities/
│   │   │   ├── student.py
│   │   │   ├── admission_rule.py
│   │   │   └── quota.py
│   │   ├── value_objects/
│   │   │   ├── grade.py
│   │   │   └── competence_points.py
│   │   └── aggregates/
│   │       └── admission_application.py
│   ├── services/                # Domain services
│   │   └── admission_evaluation_service.py
│   └── events/
│       ├── student_admitted.py
│       └── quota_filled.py
│
├── application/                 # Application services (use cases)
│   ├── services/
│   │   ├── evaluate_admission_service.py
│   │   ├── calculate_points_service.py
│   │   └── assign_quota_service.py
│   └── commands/                # Command handlers (optional CQRS)
│       └── dtos/
│
├── ports/                       # Port Interfaces (Hexagon boundary)
│   ├── primary/                 # Driving/Inbound ports
│   │   ├── __init__.py
│   │   ├── admission_api.py     # API contract
│   │   └── student_api.py
│   └── secondary/               # Driven/Outbound ports
│       ├── __init__.py
│       ├── student_repository.py      # Repository interface
│       ├── quota_repository.py
│       └── notification_service.py     # External service interface
│
└── adapters/                    # Adapter Implementations
    ├── primary/                 # Driving adapters (input)
    │   ├── rest/
    │   │   ├── __init__.py
    │   │   ├── main.py
    │   │   ├── schemas/
    │   │   └── routes/
    │   │       ├── admission_routes.py
    │   │       └── student_routes.py
    │   └── cli/
    │       └── commands.py
    │
    └── secondary/               # Driven adapters (output)
        ├── persistence/
        │   ├── sqlalchemy/
        │   │   ├── models/
        │   │   ├── mappers/
        │   │   └── repositories/
        │   │       ├── sqlalchemy_student_repository.py
        │   │       └── sqlalchemy_quota_repository.py
        │   └── in_memory/       # In-memory for testing
        │       └── in_memory_student_repository.py
        └── external/
            └── email_notification_adapter.py
```

### Pros
✅ Ports and adapters are very explicit
✅ Clear inbound (primary) vs outbound (secondary) distinction
✅ Easy to swap adapters (e.g., SQLAlchemy → MongoDB)
✅ Great for understanding hexagonal architecture
✅ Multiple adapters per port (e.g., REST + GraphQL)

### Cons
❌ More directories to navigate
❌ Can feel over-engineered for small projects
❌ Still organized by technical concerns, not features

---

## Option 3: DDD with Bounded Contexts - Package by Feature (Screaming Architecture)

Organize by domain features/bounded contexts. **Uncle Bob's preferred approach.**

```
src/
├── admission/                   # Bounded Context: Admission
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── admission_rule.py
│   │   │   └── evaluation_result.py
│   │   ├── value_objects/
│   │   │   └── admission_status.py
│   │   ├── services/
│   │   │   └── admission_evaluation_service.py
│   │   └── ports/               # Ports specific to admission
│   │       └── admission_rule_repository.py
│   ├── application/
│   │   ├── evaluate_admission_use_case.py
│   │   └── dtos/
│   ├── infrastructure/
│   │   └── repositories/
│   │       └── sqlalchemy_admission_rule_repository.py
│   └── presentation/
│       ├── routes/
│       │   └── admission_routes.py
│       └── schemas/
│           └── admission_schema.py
│
├── student/                     # Bounded Context: Student
│   ├── domain/
│   │   ├── entities/
│   │   │   └── student.py
│   │   ├── value_objects/
│   │   │   ├── student_id.py
│   │   │   └── grade.py
│   │   ├── services/
│   │   │   └── competence_points_calculator.py
│   │   └── ports/
│   │       └── student_repository.py
│   ├── application/
│   │   ├── register_student_use_case.py
│   │   ├── calculate_points_use_case.py
│   │   └── dtos/
│   ├── infrastructure/
│   │   └── repositories/
│   │       └── sqlalchemy_student_repository.py
│   └── presentation/
│       ├── routes/
│       │   └── student_routes.py
│       └── schemas/
│           └── student_schema.py
│
├── quota/                       # Bounded Context: Quota Management
│   ├── domain/
│   │   ├── entities/
│   │   │   └── quota.py
│   │   ├── value_objects/
│   │   │   ├── quota_name.py
│   │   │   └── capacity.py
│   │   ├── aggregates/
│   │   │   └── program_quota.py
│   │   ├── services/
│   │   │   └── quota_assignment_service.py
│   │   ├── events/
│   │   │   └── quota_filled.py
│   │   └── ports/
│   │       └── quota_repository.py
│   ├── application/
│   │   ├── assign_quota_use_case.py
│   │   ├── check_availability_use_case.py
│   │   └── dtos/
│   ├── infrastructure/
│   │   └── repositories/
│   │       └── sqlalchemy_quota_repository.py
│   └── presentation/
│       ├── routes/
│       │   └── quota_routes.py
│       └── schemas/
│           └── quota_schema.py
│
├── shared/                      # Shared Kernel (cross-cutting)
│   ├── domain/
│   │   ├── value_objects/
│   │   │   └── competence_points.py
│   │   └── events/
│   │       └── domain_event.py
│   ├── infrastructure/
│   │   ├── config/
│   │   │   ├── database.py
│   │   │   └── settings.py
│   │   └── persistence/
│   │       └── base.py
│   └── presentation/
│       └── dependencies.py
│
└── main.py                      # Application entry point
```

### Pros
✅ **Architecture screams!** Easy to see "this is an admission system"
✅ All code for a feature is co-located
✅ Changes to a feature touch one directory
✅ Each bounded context is independently deployable (microservices ready)
✅ Reflects domain language and ubiquitous language
✅ New developers understand what the system does immediately
✅ Prevents layer skipping (layers are within context)

### Cons
❌ Shared code can be duplicated across contexts
❌ Requires good understanding of bounded contexts
❌ Can be harder to enforce cross-cutting concerns

---

## Option 4: Hybrid - Layer + Feature (Pragmatic)

Combines screaming architecture with clear layers. **Recommended for this project.**

```
src/
├── admission/                   # Feature: Admission evaluation
│   ├── __init__.py
│   ├── domain/
│   │   ├── entities/
│   │   │   └── admission_rule.py
│   │   ├── services/
│   │   │   └── evaluation_service.py
│   │   └── ports.py            # Ports for this feature
│   ├── application/
│   │   ├── use_cases/
│   │   │   └── evaluate_admission.py
│   │   └── dtos.py
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   └── admission_rule_repository.py
│   │   └── mappers/
│   └── api/
│       ├── routes.py
│       └── schemas.py
│
├── student/                     # Feature: Student management
│   ├── __init__.py
│   ├── domain/
│   │   ├── entities/
│   │   │   └── student.py
│   │   ├── value_objects/
│   │   │   ├── grade.py
│   │   │   └── student_id.py
│   │   ├── services/
│   │   │   └── competence_calculator.py
│   │   └── ports.py
│   ├── application/
│   │   ├── use_cases/
│   │   │   ├── register_student.py
│   │   │   └── calculate_points.py
│   │   └── dtos.py
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   └── student_repository.py
│   │   └── mappers/
│   └── api/
│       ├── routes.py
│       └── schemas.py
│
├── quota/                       # Feature: Quota management
│   ├── __init__.py
│   ├── domain/
│   │   ├── entities/
│   │   │   └── quota.py
│   │   ├── aggregates/
│   │   │   └── program_quotas.py
│   │   ├── services/
│   │   │   └── quota_assignment.py
│   │   ├── events/
│   │   │   └── quota_filled.py
│   │   └── ports.py
│   ├── application/
│   │   ├── use_cases/
│   │   │   ├── assign_quota.py
│   │   │   └── check_capacity.py
│   │   └── dtos.py
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   └── quota_repository.py
│   │   └── mappers/
│   └── api/
│       ├── routes.py
│       └── schemas.py
│
└── shared/                      # Shared kernel
    ├── domain/
    │   ├── value_objects/
    │   │   └── competence_points.py
    │   └── base_entity.py
    ├── infrastructure/
    │   ├── config.py
    │   └── database.py
    └── api/
        └── dependencies.py
```

### Pros
✅ Features are visible at top level (screaming)
✅ Layers are clear within each feature
✅ Good balance between organization styles
✅ Easy to understand for new developers
✅ Scales well (can extract features to microservices)
✅ Prevents layer violations within features

### Cons
❌ Some code duplication in shared/
❌ Requires discipline to keep features independent

---

## Where Should Ports Live?

This is a common question with different schools of thought:

### Option A: Ports in Domain/Application Layer (Recommended)
```
admission/
  domain/
    entities/
    ports.py              # ← Ports defined here
  application/
    use_cases/
  infrastructure/
    repositories/         # ← Implements domain/ports.py
```

**Rationale**:
- Domain/application defines what it needs
- Infrastructure implements those needs
- Follows dependency inversion principle
- Domain owns its abstractions

### Option B: Separate Ports Directory
```
admission/
  domain/
  application/
  ports/                  # ← Separate ports directory
    inbound/
    outbound/
  adapters/
    primary/
    secondary/
```

**Rationale**:
- Very explicit about hexagonal architecture
- Clear separation of contracts
- Good for teaching hexagonal concepts

### Option C: Ports Split Between Domain and Application
```
admission/
  domain/
    ports.py              # ← Repository interfaces (data access)
  application/
    ports.py              # ← Use case interfaces (API contracts)
  infrastructure/
```

**Rationale**:
- Separates "what domain needs" from "how to call use cases"
- More nuanced separation of concerns

---

## Recommendation for Norwegian Admission System

**Use Option 4: Hybrid (Layer + Feature)**

### Reasons:
1. **Screaming Architecture**: Top-level features (admission, student, quota) clearly show what the system does
2. **Clear Layers**: Clean Architecture layers within each feature maintain good separation
3. **DDD Alignment**: Features map to bounded contexts
4. **Scalability**: Easy to extract features to microservices later
5. **Team-Friendly**: New developers see features first, then layers
6. **Testability**: Each feature is independently testable

### Initial Structure:
```
src/
├── admission/           # Start here - core feature
├── student/            # Add second
├── quota/              # Add third
└── shared/             # Cross-cutting concerns
```

### Growth Path:
- Start with just `admission/` module
- Add `student/` when needed
- Add `quota/` as system grows
- Extract to microservices if needed (each folder becomes a service)

---

## Key Principles to Maintain

Regardless of structure chosen:

1. **Dependency Rule**: Dependencies point inward (toward domain)
2. **Domain Purity**: Domain has zero framework dependencies
3. **Interface Ownership**: Inner layers define interfaces, outer layers implement
4. **Feature Cohesion**: Related code lives together
5. **Screaming**: Structure reveals intent
6. **Testability**: Can test domain/application without infrastructure

---

## Next Steps

1. Start with hybrid structure (Option 4)
2. Begin with `admission/` feature
3. Add `student/` and `quota/` as needed
4. Keep `shared/` minimal
5. Refactor as you learn what works best

Would you like me to create the actual directory structure with placeholder files?
