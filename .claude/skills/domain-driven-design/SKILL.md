---
name: domain-driven-design
description: Apply DDD tactical patterns (Entities, Value Objects, Aggregates, Domain Services, Repositories) and strategic design (Ubiquitous Language, Bounded Contexts). Use when modeling complex business logic.
---

# Domain-Driven Design (DDD) Skill

You are assisting with code that must follow Domain-Driven Design principles.

## Core Concept

**Focus on the Domain**: The heart of software is its domain model - the conceptual model of the problem domain that incorporates both behavior and data.

## Strategic Design

### Ubiquitous Language
- Use the same terms in code as domain experts use
- No translation layer between business and code
- Class names, method names, variables match domain vocabulary

**For Norwegian admission system**:
- Use Norwegian domain terms: `Opptakskrav`, `Karakterpoeng`, `Kvote`
- Or agreed English equivalents: `AdmissionRequirement`, `GradePoints`, `Quota`
- Avoid generic terms: `Rule`, `Data`, `Manager`

### Bounded Contexts
Separate domain models into distinct boundaries based on different meanings of the same terms.

**Example for admission system**:
- **Admission Context**: Rules, evaluation, quotas
- **Student Context**: Personal data, grades, applications
- **Reporting Context**: Statistics, analytics, exports

Each context has its own model, even if terms overlap.

### Context Mapping
Define relationships between bounded contexts:
- **Shared Kernel**: Common domain model
- **Customer-Supplier**: One context depends on another
- **Anti-Corruption Layer**: Translate between contexts
- **Published Language**: Standard interchange format

## Tactical Design Patterns

### 1. Entities
Objects defined by identity, not attributes.

**Characteristics**:
- Has unique identifier
- Mutable
- Identity persists through changes
- Lifecycle matters

```python
class Student:
    """Entity: Student identity matters, attributes can change."""
    def __init__(self, student_id: StudentId, name: str):
        self._id = student_id  # Identity
        self._name = name      # Can change
        self._grades: List[Grade] = []

    @property
    def id(self) -> StudentId:
        return self._id

    def add_grade(self, grade: Grade) -> None:
        self._grades.append(grade)
```

### 2. Value Objects
Objects defined by attributes, not identity.

**Characteristics**:
- No unique identifier
- Immutable
- Equality by value comparison
- Can be shared

```python
@dataclass(frozen=True)
class Grade:
    """Value Object: Two grades with same values are identical."""
    subject: str
    score: int

    def __post_init__(self):
        if not 1 <= self.score <= 6:
            raise ValueError("Grade must be between 1 and 6")

@dataclass(frozen=True)
class CompetencePoints:
    """Value Object: Immutable, defined by value."""
    value: Decimal

    def add(self, other: 'CompetencePoints') -> 'CompetencePoints':
        return CompetencePoints(self.value + other.value)
```

### 3. Aggregates
Cluster of entities and value objects with defined boundaries.

**Rules**:
- One entity is the Aggregate Root
- External objects can only reference the root
- Root enforces invariants
- Transaction boundaries align with aggregates

```python
class AdmissionApplication:
    """Aggregate Root: Controls access to internal entities."""
    def __init__(self, application_id: ApplicationId, student: Student):
        self._id = application_id
        self._student = student
        self._program_choices: List[ProgramChoice] = []
        self._status = ApplicationStatus.DRAFT

    def add_program_choice(self, program: Program, priority: int) -> None:
        """Root controls modification of internal entities."""
        if len(self._program_choices) >= 10:
            raise DomainError("Maximum 10 program choices allowed")

        choice = ProgramChoice(program, priority)
        self._program_choices.append(choice)

    def submit(self) -> None:
        """Root enforces invariants."""
        if not self._program_choices:
            raise DomainError("Cannot submit without program choices")
        self._status = ApplicationStatus.SUBMITTED
```

### 4. Domain Services
Operations that don't naturally belong to an entity or value object.

**Use when**:
- Operation involves multiple domain objects
- Operation is a significant domain concept
- Operation is stateless

```python
class AdmissionEvaluationService:
    """Domain Service: Evaluates admission across multiple entities."""

    def evaluate_application(
        self,
        application: AdmissionApplication,
        rules: List[AdmissionRule]
    ) -> EvaluationResult:
        """Service coordinates between multiple domain objects."""
        results = []
        for rule in rules:
            result = rule.evaluate(application.student)
            results.append(result)

        return EvaluationResult.from_rule_results(results)
```

### 5. Domain Events
Something that happened in the domain that domain experts care about.

**Characteristics**:
- Past tense naming
- Immutable
- Contains relevant data
- Timestamped

```python
@dataclass(frozen=True)
class StudentAdmitted:
    """Domain Event: Something significant happened."""
    student_id: StudentId
    program_id: ProgramId
    admitted_at: datetime
    admission_basis: str

@dataclass(frozen=True)
class QuotaFilled:
    """Domain Event: Quota reached capacity."""
    quota_id: QuotaId
    filled_at: datetime
    capacity: int
```

### 6. Repositories
Provide illusion of in-memory collection of aggregates.

**Responsibilities**:
- Add/remove aggregates
- Find aggregates by criteria
- Reconstitute aggregates from storage

```python
class AdmissionRuleRepository(Protocol):
    """Repository interface in domain layer."""

    def find_by_program(self, program_id: ProgramId) -> List[AdmissionRule]:
        """Find all rules for a program."""
        ...

    def find_by_id(self, rule_id: RuleId) -> Optional[AdmissionRule]:
        """Find specific rule."""
        ...

    def save(self, rule: AdmissionRule) -> None:
        """Persist rule."""
        ...
```

### 7. Factories
Encapsulate complex object creation.

```python
class AdmissionRuleFactory:
    """Factory: Creates complex admission rules."""

    @staticmethod
    def create_minimum_grade_rule(
        subject: str,
        minimum_grade: int
    ) -> MinimumGradeRule:
        """Create validated rule."""
        if not 1 <= minimum_grade <= 6:
            raise ValueError("Invalid grade")
        return MinimumGradeRule(subject, minimum_grade)

    @staticmethod
    def create_from_config(config: dict) -> AdmissionRule:
        """Create rule from configuration."""
        rule_type = config['type']
        if rule_type == 'minimum_grade':
            return MinimumGradeRule(config['subject'], config['grade'])
        elif rule_type == 'quota':
            return QuotaRule(config['quota_name'], config['capacity'])
        # ... more types
```

## Domain Model Patterns

### Specification Pattern
Encapsulate business rules that can be combined.

```python
class AdmissionSpecification(ABC):
    """Specification: Reusable business rule."""

    @abstractmethod
    def is_satisfied_by(self, student: Student) -> bool:
        pass

    def and_(self, other: 'AdmissionSpecification') -> 'AdmissionSpecification':
        return AndSpecification(self, other)

class MinimumGradeSpecification(AdmissionSpecification):
    def __init__(self, subject: str, minimum: int):
        self._subject = subject
        self._minimum = minimum

    def is_satisfied_by(self, student: Student) -> bool:
        grade = student.get_grade(self._subject)
        return grade is not None and grade.score >= self._minimum
```

### Policy Pattern
Encapsulate complex business rules and decisions.

```python
class QuotaAssignmentPolicy:
    """Policy: Encapsulates quota assignment logic."""

    def assign_quota(
        self,
        student: Student,
        program: Program
    ) -> Optional[Quota]:
        """Determine which quota the student qualifies for."""
        if student.has_special_competence():
            return program.get_quota('special_competence')
        elif student.is_first_time_applicant():
            return program.get_quota('ordinary')
        else:
            return program.get_quota('supplementary')
```

## Protecting Invariants

Business rules that must always be true.

```python
class Quota:
    """Entity with invariant: filled <= capacity."""

    def __init__(self, name: str, capacity: int):
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")
        self._name = name
        self._capacity = capacity
        self._filled = 0

    def fill_spot(self) -> None:
        """Invariant protected: cannot overfill."""
        if self._filled >= self._capacity:
            raise DomainError(f"Quota {self._name} is full")
        self._filled += 1

    @property
    def available_spots(self) -> int:
        """Derived value from invariant."""
        return self._capacity - self._filled
```

## Rich Domain Model vs Anemic Domain Model

### Anemic (BAD)
```python
# Just data, no behavior
class Student:
    def __init__(self):
        self.name = ""
        self.grades = []

# Logic elsewhere
def calculate_points(student):
    total = 0
    for grade in student.grades:
        total += grade.score * 4
    return total
```

### Rich (GOOD)
```python
# Data + behavior together
class Student:
    def __init__(self, name: str):
        self._name = name
        self._grades: List[Grade] = []

    def add_grade(self, grade: Grade) -> None:
        """Domain logic with the data."""
        if grade in self._grades:
            raise DomainError("Grade already exists")
        self._grades.append(grade)

    def calculate_competence_points(self) -> CompetencePoints:
        """Behavior lives with data."""
        total = sum(grade.to_points() for grade in self._grades)
        return CompetencePoints(total)
```

## Code Review Checklist

- [ ] Does code use ubiquitous language from domain?
- [ ] Are entities and value objects properly distinguished?
- [ ] Are aggregates properly bounded?
- [ ] Are invariants protected?
- [ ] Is the domain model rich (not anemic)?
- [ ] Are domain services used appropriately?
- [ ] Are domain events captured for significant happenings?
- [ ] Do repositories work with aggregate roots?
- [ ] Are bounded contexts clearly separated?

## Practical Application for Admission Rules

### Entities
- `Student` (identity: student number)
- `Program` (identity: program code)
- `AdmissionRule` (identity: rule ID)

### Value Objects
- `Grade(subject, score)`
- `CompetencePoints(value)`
- `QuotaName(name)`
- `StudentId(value)`

### Aggregates
- `AdmissionApplication` (root) containing `ProgramChoice` entities
- `Program` (root) containing `Quota` entities

### Domain Services
- `AdmissionEvaluationService`
- `CompetencePointsCalculationService`

### Domain Events
- `StudentAdmitted`
- `StudentRejected`
- `QuotaFilled`
- `ApplicationSubmitted`

### Repositories
- `AdmissionRuleRepository`
- `StudentRepository`
- `ProgramRepository`

## Response Format

When applying DDD:
1. Identify domain concepts from requirements
2. Classify as entity, value object, aggregate, or service
3. Define ubiquitous language terms
4. Protect invariants within aggregates
5. Use rich domain models with behavior
6. Capture domain events for significant changes
