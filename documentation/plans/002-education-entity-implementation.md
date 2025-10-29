# Implementation Plan: Education Entity (CRUD Operations)

**Date**: 2025-10-28
**Feature**: Manage Education Offerings
**Reference**: [tests/features/education/manage-education.feature](../../tests/features/education/manage-education.feature)

---

## Overview

Implement the Education aggregate root with create, update, and delete operations following DDD and Clean Architecture principles. Education is an aggregate root representing a specific study program offering at an institution for a particular intake period.

**Key DDD Concepts:**
- **Aggregate Root**: Education (manages its own invariants and lifecycle)
- **Value Objects**: EducationId, IntakeTerm, StudyMode, EducationState
- **Entity References**: RulesetId, AdmissionProcessId (references to other aggregates)
- **Invariants**: State transition rules (Planned → Active → Finished)
- **Business Rules**: Required fields, reference integrity, deletion constraints

---

## Prerequisites

- [x] Project structure exists
- [ ] pytest and pytest-bdd installed
- [ ] Domain layer structure created (`src/domain/`)
- [ ] Test infrastructure ready

---

## Domain Layer (TDD)

**Folder Structure**: Following Microsoft's eShopOnContainers approach, we organize by aggregate:

```
src/domain/
├── aggregates/
│   └── education/
│       ├── __init__.py
│       ├── education.py              ← Aggregate Root
│       ├── education_id.py           ← Identity Value Object
│       ├── education_state.py        ← State Value Object
│       └── education_repository.py   ← Repository interface (port)
├── shared/                           ← Shared value objects across aggregates
│   ├── intake_term.py
│   ├── study_mode.py
│   ├── ruleset_id.py
│   └── admission_process_id.py
└── exceptions.py                     ← Domain exceptions
```

### Step 1: EducationId Value Object

**DDD Pattern**: Value Object (Identity)

**Files to create:**
- `src/domain/aggregates/education/education_id.py`
- `src/domain/aggregates/education/__init__.py`
- `src/domain/aggregates/__init__.py`

**Tests to write first:**
- `tests/unit/domain/value_objects/test_education_id.py`
  - Test: Create EducationId from string
  - Test: EducationId equality (same value = equal)
  - Test: EducationId is immutable
  - Test: EducationId has string representation
  - Test: Generate new unique EducationId (UUID-based)
  - Test: Reject None or empty string

**Implementation:**
```python
@dataclass(frozen=True)
class EducationId:
    value: str

    def __post_init__(self):
        # Validate not empty

    @staticmethod
    def generate() -> 'EducationId':
        # Generate new UUID

    def __str__(self) -> str:
        return self.value
```

**Invariants:**
- Must not be None or empty
- Immutable once created

---

### Step 2: EducationState Value Object

**DDD Pattern**: Value Object (Enum with transition logic)

**Files to create:**
- `src/domain/aggregates/education/education_state.py`

**Tests to write first:**
- `tests/unit/domain/value_objects/test_education_state.py`
  - Test: Create state PLANNED, ACTIVE, FINISHED
  - Test: Valid transition Planned → Active returns True
  - Test: Valid transition Active → Finished returns True
  - Test: Invalid transition Active → Planned returns False
  - Test: Invalid transition Planned → Finished returns False (skip)
  - Test: Invalid transition Finished → anything returns False
  - Test: Can transition to same state (idempotent)

**Implementation:**
```python
class EducationState(Enum):
    PLANNED = "Planned"
    ACTIVE = "Active"
    FINISHED = "Finished"

    def can_transition_to(self, new_state: 'EducationState') -> bool:
        # Implement state machine logic
        valid_transitions = {
            EducationState.PLANNED: [EducationState.PLANNED, EducationState.ACTIVE],
            EducationState.ACTIVE: [EducationState.ACTIVE, EducationState.FINISHED],
            EducationState.FINISHED: [EducationState.FINISHED]
        }
        return new_state in valid_transitions[self]
```

**Invariants:**
- Only valid state transitions allowed
- No backwards or skipping transitions

---

### Step 3: StudyMode Value Object

**DDD Pattern**: Value Object (Enum) - Shared across aggregates

**Files to create:**
- `src/domain/shared/study_mode.py`
- `src/domain/shared/__init__.py`

**Tests to write first:**
- `tests/unit/domain/value_objects/test_study_mode.py`
  - Test: Create FULL_TIME and PART_TIME modes
  - Test: String representation matches expected format
  - Test: Equality

**Implementation:**
```python
class StudyMode(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
```

---

### Step 4: IntakeTerm Value Object

**DDD Pattern**: Value Object (Composite value) - Shared across aggregates

**Files to create:**
- `src/domain/shared/intake_term.py`

**Tests to write first:**
- `tests/unit/domain/value_objects/test_intake_term.py`
  - Test: Create "Autumn 2025" term
  - Test: Create "Spring 2026" term
  - Test: Equality of same terms
  - Test: String representation "Autumn 2025"
  - Test: Invalid semester rejected
  - Test: Invalid year rejected (e.g., negative, too far in future)

**Implementation:**
```python
@dataclass(frozen=True)
class IntakeTerm:
    semester: str  # "Autumn" or "Spring"
    year: int

    def __post_init__(self):
        # Validate semester in ["Autumn", "Spring"]
        # Validate year reasonable (e.g., 2020-2100)

    def __str__(self) -> str:
        return f"{self.semester} {self.year}"
```

**Invariants:**
- Semester must be "Autumn" or "Spring"
- Year must be reasonable (2020-2100)

---

### Step 5: RulesetId and AdmissionProcessId Value Objects

**DDD Pattern**: Value Object (External aggregate references) - Shared

**Files to create:**
- `src/domain/shared/ruleset_id.py`
- `src/domain/shared/admission_process_id.py`

**Tests to write first:**
- `tests/unit/domain/value_objects/test_ruleset_id.py`
  - Test: Create RulesetId from string
  - Test: Equality
  - Test: Reject None or empty

- `tests/unit/domain/value_objects/test_admission_process_id.py`
  - Test: Create AdmissionProcessId from string
  - Test: Equality
  - Test: Reject None or empty

**Implementation:**
```python
@dataclass(frozen=True)
class RulesetId:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("RulesetId cannot be empty")

@dataclass(frozen=True)
class AdmissionProcessId:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("AdmissionProcessId cannot be empty")
```

---

### Step 6: Domain Exceptions

**DDD Pattern**: Domain Exceptions (express business rule violations)

**Files to create:**
- `src/domain/exceptions.py`

**Tests to write first:**
- `tests/unit/domain/test_exceptions.py`
  - Test: InvalidStateTransitionError has clear message
  - Test: EducationNotFoundError includes ID
  - Test: InvalidEducationError for validation failures

**Implementation:**
```python
class DomainException(Exception):
    """Base exception for domain layer"""
    pass

class InvalidStateTransitionError(DomainException):
    def __init__(self, current: EducationState, attempted: EducationState):
        super().__init__(f"Invalid state transition: {current.value} → {attempted.value}")

class EducationNotFoundError(DomainException):
    def __init__(self, education_id: EducationId):
        super().__init__(f"Education not found: {education_id}")

class InvalidEducationError(DomainException):
    """Raised when education violates business rules"""
    pass

class CannotDeleteEducationError(DomainException):
    def __init__(self, state: EducationState):
        super().__init__(f"Cannot delete education in {state.value} state")
```

---

### Step 7: Education Entity (Aggregate Root)

**DDD Pattern**: Aggregate Root

**Files to create:**
- `src/domain/aggregates/education/education.py`

**Tests to write first:**
- `tests/unit/domain/entities/test_education.py`
  - Test: Create education with all required fields (Scenario: Create a new education offering)
  - Test: Education created with Planned state
  - Test: Education has unique ID
  - Test: Create education without program_name raises error (Scenario: missing required field)
  - Test: Update campus attribute
  - Test: Update ruleset_id reference
  - Test: Transition state Planned → Active succeeds
  - Test: Transition state Active → Finished succeeds
  - Test: Transition state Active → Planned raises InvalidStateTransitionError (Scenario: invalid state transition)
  - Test: Can delete when state is Planned
  - Test: Cannot delete when state is Active
  - Test: Cannot delete when state is Finished
  - Test: Two educations with same attributes have different IDs

**Implementation:**
```python
@dataclass
class Education:
    """
    Aggregate Root: Education

    Represents a specific offering of a study program at an institution
    for a particular intake period.

    Invariants:
    - All required fields must be provided
    - State transitions must follow: Planned → Active → Finished
    - Can only be deleted in Planned state
    """
    id: EducationId
    program_name: str
    institution: str
    campus: str
    intake_term: IntakeTerm
    study_mode: StudyMode
    language: str
    ruleset_id: RulesetId
    admission_process_id: AdmissionProcessId
    state: EducationState = field(default=EducationState.PLANNED)

    @staticmethod
    def create(
        program_name: str,
        institution: str,
        campus: str,
        intake_term: IntakeTerm,
        study_mode: StudyMode,
        language: str,
        ruleset_id: RulesetId,
        admission_process_id: AdmissionProcessId
    ) -> 'Education':
        """Factory method to create a new Education"""
        # Validate all required fields
        if not program_name:
            raise InvalidEducationError("program_name is required")
        if not institution:
            raise InvalidEducationError("institution is required")
        if not campus:
            raise InvalidEducationError("campus is required")
        if not language:
            raise InvalidEducationError("language is required")

        return Education(
            id=EducationId.generate(),
            program_name=program_name,
            institution=institution,
            campus=campus,
            intake_term=intake_term,
            study_mode=study_mode,
            language=language,
            ruleset_id=ruleset_id,
            admission_process_id=admission_process_id,
            state=EducationState.PLANNED
        )

    def update_campus(self, new_campus: str) -> None:
        """Update campus (mutable attribute)"""
        if not new_campus:
            raise InvalidEducationError("campus cannot be empty")
        self.campus = new_campus

    def update_ruleset(self, new_ruleset_id: RulesetId) -> None:
        """Update ruleset reference"""
        self.ruleset_id = new_ruleset_id

    def update_admission_process(self, new_admission_process_id: AdmissionProcessId) -> None:
        """Update admission process reference"""
        self.admission_process_id = new_admission_process_id

    def transition_to(self, new_state: EducationState) -> None:
        """
        Transition to new state following business rules.
        Raises InvalidStateTransitionError if transition is invalid.
        """
        if not self.state.can_transition_to(new_state):
            raise InvalidStateTransitionError(self.state, new_state)
        self.state = new_state

    def can_be_deleted(self) -> bool:
        """Check if education can be deleted (only in Planned state)"""
        return self.state == EducationState.PLANNED

    def ensure_can_be_deleted(self) -> None:
        """Raise exception if education cannot be deleted"""
        if not self.can_be_deleted():
            raise CannotDeleteEducationError(self.state)
```

**Invariants Enforced:**
- Required fields validation
- State transition rules
- Deletion only in Planned state

---

### Step 8: Repository Port (Interface)

**DDD Pattern**: Repository (Port in Hexagonal Architecture)

**Files to create:**
- `src/domain/aggregates/education/education_repository.py`

**Tests to write first:**
- No direct tests (interface only)
- Will be tested via implementations

**Implementation:**
```python
from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.education import Education
from src.domain.value_objects.education_id import EducationId
from src.domain.value_objects.admission_process_id import AdmissionProcessId

class EducationRepository(ABC):
    """
    Repository interface for Education aggregate.

    This is a port in the domain layer. Implementations belong
    in the infrastructure layer.
    """

    @abstractmethod
    def save(self, education: Education) -> None:
        """Save or update an education"""
        pass

    @abstractmethod
    def find_by_id(self, education_id: EducationId) -> Optional[Education]:
        """Find education by ID. Returns None if not found."""
        pass

    @abstractmethod
    def delete(self, education_id: EducationId) -> None:
        """
        Delete education by ID.
        Raises EducationNotFoundError if not found.
        """
        pass

    @abstractmethod
    def exists(self, education_id: EducationId) -> bool:
        """Check if education exists"""
        pass

    @abstractmethod
    def find_by_admission_process(self, admission_process_id: AdmissionProcessId) -> List[Education]:
        """Find all educations for an admission process"""
        pass
```

---

## Application Layer (TDD)

### Step 9: DTOs (Data Transfer Objects)

**Clean Architecture Pattern**: DTOs for crossing boundaries

**Files to create:**
- `src/application/dtos/education_dto.py`
- `src/application/dtos/__init__.py`

**Tests to write first:**
- No direct tests (simple data structures)
- Will be tested via use cases

**Implementation:**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateEducationRequest:
    program_name: str
    institution: str
    campus: str
    intake_term: str  # e.g., "Autumn 2025"
    study_mode: str   # e.g., "full-time"
    language: str
    ruleset_id: str
    admission_process_id: str

@dataclass
class UpdateEducationRequest:
    education_id: str
    program_name: Optional[str] = None
    institution: Optional[str] = None
    campus: Optional[str] = None
    intake_term: Optional[str] = None
    study_mode: Optional[str] = None
    language: Optional[str] = None
    ruleset_id: Optional[str] = None
    admission_process_id: Optional[str] = None
    state: Optional[str] = None

@dataclass
class EducationResponse:
    id: str
    program_name: str
    institution: str
    campus: str
    intake_term: str
    study_mode: str
    language: str
    ruleset_id: str
    admission_process_id: str
    state: str
```

---

### Step 10: Create Education Use Case

**Clean Architecture Pattern**: Use Case (Application Service)

**Files to create:**
- `src/application/use_cases/create_education.py`

**Tests to write first:**
- `tests/unit/application/test_create_education.py`
  - Test: Successfully create education (Scenario: Create a new education offering)
  - Test: Missing program_name raises error (Scenario: missing required field)
  - Test: Invalid ruleset reference raises error (Scenario: invalid ruleset reference)
  - Test: Education saved to repository
  - Test: Returns EducationResponse with correct data

**Implementation:**
```python
class CreateEducationUseCase:
    def __init__(
        self,
        education_repository: EducationRepository,
        ruleset_repository: RulesetRepository  # For validation
    ):
        self._education_repo = education_repository
        self._ruleset_repo = ruleset_repository

    def execute(self, request: CreateEducationRequest) -> EducationResponse:
        # 1. Validate ruleset exists
        if not self._ruleset_repo.exists(RulesetId(request.ruleset_id)):
            raise InvalidEducationError("Ruleset not found")

        # 2. Parse intake term
        semester, year = request.intake_term.split()
        intake_term = IntakeTerm(semester, int(year))

        # 3. Parse study mode
        study_mode = StudyMode(request.study_mode)

        # 4. Create education (domain logic)
        education = Education.create(
            program_name=request.program_name,
            institution=request.institution,
            campus=request.campus,
            intake_term=intake_term,
            study_mode=study_mode,
            language=request.language,
            ruleset_id=RulesetId(request.ruleset_id),
            admission_process_id=AdmissionProcessId(request.admission_process_id)
        )

        # 5. Save to repository
        self._education_repo.save(education)

        # 6. Return response DTO
        return EducationResponse(
            id=str(education.id),
            program_name=education.program_name,
            institution=education.institution,
            campus=education.campus,
            intake_term=str(education.intake_term),
            study_mode=education.study_mode.value,
            language=education.language,
            ruleset_id=education.ruleset_id.value,
            admission_process_id=education.admission_process_id.value,
            state=education.state.value
        )
```

---

### Step 11: Update Education Use Case

**Clean Architecture Pattern**: Use Case

**Files to create:**
- `src/application/use_cases/update_education.py`

**Tests to write first:**
- `tests/unit/application/test_update_education.py`
  - Test: Update campus successfully (Scenario: Update education attributes)
  - Test: Update ruleset reference (Scenario: Update education ruleset reference)
  - Test: Transition state Planned → Active (Scenario: Update education state from Planned to Active)
  - Test: Invalid state transition raises error (Scenario: Cannot update with invalid state transition)
  - Test: Non-existent education raises error (Scenario: Cannot update non-existent education)

**Implementation:**
```python
class UpdateEducationUseCase:
    def __init__(self, education_repository: EducationRepository):
        self._education_repo = education_repository

    def execute(self, request: UpdateEducationRequest) -> EducationResponse:
        # 1. Retrieve education
        education_id = EducationId(request.education_id)
        education = self._education_repo.find_by_id(education_id)
        if not education:
            raise EducationNotFoundError(education_id)

        # 2. Apply updates
        if request.campus:
            education.update_campus(request.campus)

        if request.ruleset_id:
            education.update_ruleset(RulesetId(request.ruleset_id))

        if request.admission_process_id:
            education.update_admission_process(AdmissionProcessId(request.admission_process_id))

        if request.state:
            new_state = EducationState[request.state.upper()]
            education.transition_to(new_state)

        # 3. Save changes
        self._education_repo.save(education)

        # 4. Return response
        return EducationResponse(...) # Map to DTO
```

---

### Step 12: Delete Education Use Case

**Clean Architecture Pattern**: Use Case

**Files to create:**
- `src/application/use_cases/delete_education.py`

**Tests to write first:**
- `tests/unit/application/test_delete_education.py`
  - Test: Delete education in Planned state (Scenario: Delete education in Planned state)
  - Test: Cannot delete in Active state (Scenario: Cannot delete education in Active state)
  - Test: Cannot delete in Finished state (Scenario: Cannot delete education in Finished state)
  - Test: Non-existent education raises error (Scenario: Cannot delete non-existent education)

**Implementation:**
```python
class DeleteEducationUseCase:
    def __init__(self, education_repository: EducationRepository):
        self._education_repo = education_repository

    def execute(self, education_id: str) -> None:
        # 1. Retrieve education
        edu_id = EducationId(education_id)
        education = self._education_repo.find_by_id(edu_id)
        if not education:
            raise EducationNotFoundError(edu_id)

        # 2. Check if can be deleted (domain invariant)
        education.ensure_can_be_deleted()

        # 3. Delete from repository
        self._education_repo.delete(edu_id)
```

---

## Infrastructure Layer

### Step 13: In-Memory Repository (for testing)

**Clean Architecture Pattern**: Adapter (Repository Implementation)

**Files to create:**
- `src/infrastructure/persistence/in_memory_education_repository.py`

**Tests to write first:**
- `tests/integration/infrastructure/test_in_memory_education_repository.py`
  - Test: Save and retrieve education
  - Test: Update existing education
  - Test: Delete education
  - Test: Find by admission process
  - Test: Exists check

**Implementation:**
```python
class InMemoryEducationRepository(EducationRepository):
    def __init__(self):
        self._storage: Dict[EducationId, Education] = {}

    def save(self, education: Education) -> None:
        self._storage[education.id] = education

    def find_by_id(self, education_id: EducationId) -> Optional[Education]:
        return self._storage.get(education_id)

    def delete(self, education_id: EducationId) -> None:
        if education_id not in self._storage:
            raise EducationNotFoundError(education_id)
        del self._storage[education_id]

    # ... other methods
```

---

## BDD Tests (Feature Step Definitions)

### Step 14: BDD Step Definitions

**Files to create:**
- `tests/step_defs/education_steps.py`
- `tests/step_defs/conftest.py` (pytest-bdd fixtures)

**Implementation:**
```python
from pytest_bdd import scenarios, given, when, then, parsers

# Load scenarios from feature file
scenarios('../features/education/manage-education.feature')

@given('I am an admission administrator')
def admin_user():
    # Setup admin context
    pass

@when(parsers.parse('I create an education with:\n{table}'))
def create_education(table, create_education_use_case):
    # Parse table and call use case
    pass

@then(parsers.parse('the education is created successfully'))
def verify_creation():
    # Assert education was created
    pass

# ... implement all steps for 15 scenarios
```

---

## Git Workflow

### Branching Strategy
- [x] **Branch needed**: Yes (estimated 10+ hours of work)
- **Branch name**: `feature/education-entity`
- **Target**: Merge within 2-3 days
- **Base branch**: `main`

### Merge Plan
- **PR size target**: Split into 2 PRs to keep each < 400 lines

#### PR 1: Domain Layer (~200 lines)
- Value objects (EducationId, IntakeTerm, StudyMode, EducationState, RulesetId, AdmissionProcessId)
- Domain exceptions
- Education entity
- Repository port
- All unit tests for domain layer

#### PR 2: Application + Infrastructure (~250 lines)
- DTOs
- Use cases (Create, Update, Delete)
- In-memory repository
- BDD step definitions
- Integration tests

### Feature Flags
- [ ] **Feature flag needed**: No (domain layer has no external exposure initially)

---

## Task Checklist

Execute in this order following **strict TDD** (write test → make it fail → make it pass → refactor):

### Domain Layer
- [ ] **EducationId Value Object**
  - [ ] Write tests for EducationId
  - [ ] Implement EducationId (make tests pass)

- [ ] **EducationState Value Object**
  - [ ] Write tests for EducationState and transitions
  - [ ] Implement EducationState with can_transition_to()

- [ ] **StudyMode Value Object**
  - [ ] Write tests for StudyMode
  - [ ] Implement StudyMode enum

- [ ] **IntakeTerm Value Object**
  - [ ] Write tests for IntakeTerm
  - [ ] Implement IntakeTerm with validation

- [ ] **RulesetId and AdmissionProcessId**
  - [ ] Write tests for both IDs
  - [ ] Implement both value objects

- [ ] **Domain Exceptions**
  - [ ] Write tests for exceptions
  - [ ] Implement all domain exceptions

- [ ] **Education Entity (Aggregate Root)**
  - [ ] Write tests for Education creation
  - [ ] Write tests for Education updates
  - [ ] Write tests for state transitions
  - [ ] Write tests for deletion rules
  - [ ] Implement Education entity
  - [ ] Ensure all invariants are enforced

- [ ] **Repository Port**
  - [ ] Define EducationRepository interface

### Application Layer
- [ ] **DTOs**
  - [ ] Define request/response DTOs

- [ ] **Create Education Use Case**
  - [ ] Write unit tests with mocked repository
  - [ ] Implement CreateEducationUseCase

- [ ] **Update Education Use Case**
  - [ ] Write unit tests
  - [ ] Implement UpdateEducationUseCase

- [ ] **Delete Education Use Case**
  - [ ] Write unit tests
  - [ ] Implement DeleteEducationUseCase

### Infrastructure Layer
- [ ] **In-Memory Repository**
  - [ ] Write integration tests
  - [ ] Implement InMemoryEducationRepository

### BDD Tests
- [ ] **Step Definitions**
  - [ ] Implement all Given steps
  - [ ] Implement all When steps
  - [ ] Implement all Then steps
  - [ ] Run full feature file and verify all scenarios pass

### Verification
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All 15 Gherkin scenarios pass
- [ ] Code follows SOLID principles
- [ ] Domain invariants are protected
- [ ] Clean Architecture boundaries respected

---

## Dependencies

**Depends on:**
- None (Education is foundational)

**Blocks:**
- Ruleset aggregate implementation (referenced but can be mocked)
- Admission Process aggregate implementation (referenced but can be mocked)
- Application management features

**For initial implementation:**
- Mock Ruleset and AdmissionProcess existence checks
- Return True for validation in tests
- Implement real validation later when those aggregates exist

---

## Risks & Considerations

**Risk 1: Ruleset and AdmissionProcess don't exist yet**
- **Mitigation**: Use mock repositories in tests, validate references later

**Risk 2: State machine complexity might grow**
- **Mitigation**: Keep state transitions simple initially, encapsulated in EducationState value object

**Risk 3: Large PR might delay review**
- **Mitigation**: Split into 2 PRs (domain first, then application/infrastructure)

**Risk 4: BDD scenarios might reveal missing edge cases**
- **Mitigation**: Add unit tests for discovered cases, update feature file if needed

---

## Estimated Effort

- **Domain Layer**: 4 hours (value objects + entity + tests)
- **Application Layer**: 2 hours (use cases + DTOs + tests)
- **Infrastructure Layer**: 1 hour (in-memory repo + tests)
- **BDD Tests**: 2 hours (step definitions + scenario execution)
- **Refactoring & Polish**: 1 hour
- **Total**: **10 hours** (2 work sessions)

**Branch needed**: Yes (> 4 hours threshold)

---

## Architecture Compliance

### DDD Principles Applied
- ✅ **Aggregate Root**: Education manages its own invariants
- ✅ **Value Objects**: Immutable, validated (EducationId, IntakeTerm, EducationState, etc.)
- ✅ **Ubiquitous Language**: Education, IntakeTerm, StudyMode match domain vocabulary
- ✅ **Domain Exceptions**: Express business rule violations clearly
- ✅ **Encapsulation**: State transitions protected by Education.transition_to()
- ✅ **Entity References**: RulesetId and AdmissionProcessId reference other aggregates

### Clean Architecture Boundaries
- ✅ **Domain → No dependencies** (pure business logic)
- ✅ **Application → Depends on Domain only** (orchestration via ports)
- ✅ **Infrastructure → Depends on Domain** (implements ports)
- ✅ **DTOs at boundaries**: No domain entities leak to outer layers

### SOLID Principles
- ✅ **Single Responsibility**: Each value object has one reason to change
- ✅ **Open/Closed**: New state transitions can be added without modifying EducationState enum
- ✅ **Liskov Substitution**: Repository implementations are substitutable
- ✅ **Interface Segregation**: Repository interface is focused
- ✅ **Dependency Inversion**: Use cases depend on repository port (abstraction), not implementation

---

## Next Steps After Completion

1. Implement Ruleset aggregate (for real validation)
2. Implement AdmissionProcess aggregate
3. Add SQLAlchemy-based persistent repository
4. Add REST API endpoints (Presentation layer)
5. Add domain events (EducationCreated, EducationStateChanged)
6. Implement BDD scenarios with real database

---

**Ready to execute with `/execute` command!**
