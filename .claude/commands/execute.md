---
description: Execute the implementation plan step by step
argument-hint: [plan reference or feature name]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Execution Phase

You are in the **execution phase** of the workflow. Your goal is to implement the plan following TDD, Clean Architecture, and best practices.

## Your Task

Execute the implementation plan for: **$ARGUMENTS**

## Execution Principles

### 1. Test-Driven Development (RED-GREEN-REFACTOR)
- ✅ Write test FIRST
- ✅ Watch it FAIL (RED)
- ✅ Write minimal code to pass (GREEN)
- ✅ Refactor to clean code (REFACTOR)
- ✅ Repeat

### 2. Inside-Out Implementation
Execute in layer order:
1. **Domain first** (pure Python, no dependencies)
2. **Application second** (use cases, orchestration)
3. **Infrastructure third** (repositories, database)
4. **Presentation last** (API endpoints)

### 3. Incremental Progress
- Work in small steps
- Commit frequently
- Keep tests passing
- One feature at a time

### 4. Clean Architecture Compliance
- Domain defines ports (interfaces)
- Infrastructure implements ports
- Dependencies point inward
- No framework dependencies in domain

## Workflow

### Before Starting

1. **Review the plan**
   - Read the implementation plan
   - Understand all steps
   - Clarify any questions

2. **Check git status**
   - Ensure clean working directory
   - Create branch if needed (plan says >4 hours)
   - Branch name from plan

3. **Set up TodoWrite**
   - Create todos for all major steps
   - Track progress as you go

### During Execution

For EACH step in the plan:

#### Step Template

```markdown
## Step X: [Component Name]

### 1. RED - Write Failing Test
- Create test file: `tests/[layer]/test_[name].py`
- Write test for first scenario
- Run test → should FAIL
- Commit: "test: add failing test for [feature]"

### 2. GREEN - Implement
- Create implementation file: `src/[layer]/[name].py`
- Write minimal code to pass test
- Run test → should PASS
- Commit: "feat: implement [feature]"

### 3. REFACTOR - Clean Up
- Apply SOLID principles
- Improve naming
- Extract duplications
- Run tests → still PASS
- Commit: "refactor: clean up [component]"

### 4. Next Test
- Add test for next scenario/edge case
- Repeat RED-GREEN-REFACTOR
```

### After Each Major Milestone

1. **Run all tests**
   ```bash
   pytest
   ```

2. **Check coverage**
   ```bash
   pytest --cov=src
   ```

3. **Lint and type check**
   ```bash
   ruff check src/
   mypy src/
   ```

4. **Commit if not already done**
   ```bash
   git add .
   git commit -m "feat(domain): implement [feature]"
   ```

## Layer-Specific Guidelines

### Domain Layer
```python
# tests/unit/domain/test_grade.py
def test_grade_to_points_converts_correctly():
    # ARRANGE
    grade = Grade(subject="Math", score=5)

    # ACT
    points = grade.to_points()

    # ASSERT
    assert points == 20

# src/domain/value_objects/grade.py
@dataclass(frozen=True)
class Grade:
    subject: str
    score: int

    def __post_init__(self):
        if not 1 <= self.score <= 6:
            raise ValueError("Grade must be 1-6")

    def to_points(self) -> int:
        return self.score * 4
```

### Application Layer
```python
# tests/unit/application/test_evaluate_admission_use_case.py
def test_evaluate_admission_admits_qualified_student():
    # ARRANGE
    student_repo = FakeStudentRepository()
    rule_repo = FakeRuleRepository()
    use_case = EvaluateAdmissionUseCase(student_repo, rule_repo)

    # ACT
    result = use_case.execute(input_dto)

    # ASSERT
    assert result.admitted is True

# src/application/use_cases/evaluate_admission_use_case.py
class EvaluateAdmissionUseCase:
    def __init__(self, student_repo: StudentRepository, rule_repo: RuleRepository):
        self._students = student_repo
        self._rules = rule_repo

    def execute(self, input: EvaluateAdmissionInput) -> EvaluateAdmissionOutput:
        # Orchestrate domain logic
        pass
```

### Infrastructure Layer
```python
# tests/integration/test_student_repository.py
def test_student_repository_saves_and_retrieves(db_session):
    # ARRANGE
    repo = SQLAlchemyStudentRepository(db_session)
    student = Student(StudentId("123"), "John")

    # ACT
    repo.save(student)
    retrieved = repo.find_by_id(StudentId("123"))

    # ASSERT
    assert retrieved.name == "John"

# src/infrastructure/persistence/repositories/student_repository.py
class SQLAlchemyStudentRepository:
    def __init__(self, session: Session):
        self._session = session
        self._mapper = StudentMapper()

    def save(self, student: Student) -> None:
        model = self._mapper.to_orm(student)
        self._session.merge(model)
```

### Presentation Layer
```python
# tests/e2e/test_admission_api.py
def test_evaluate_admission_endpoint_returns_result(client):
    # ARRANGE
    request = {"student_id": "123", "program_id": "CS"}

    # ACT
    response = client.post("/api/v1/admission/evaluate", json=request)

    # ASSERT
    assert response.status_code == 200
    assert response.json()["admitted"] is True

# src/presentation/api/routes/admission_routes.py
@router.post("/evaluate")
async def evaluate_admission(request: EvaluateAdmissionRequest):
    # Delegate to use case
    pass
```

## Git Workflow During Execution

### Small, Frequent Commits
```bash
# After RED phase
git add tests/
git commit -m "test: add failing test for grade validation"

# After GREEN phase
git add src/ tests/
git commit -m "feat(domain): implement grade value object"

# After REFACTOR phase
git add src/
git commit -m "refactor(domain): extract grade validation"
```

### Commit Message Format
```
<type>(<scope>): <subject>

Types: feat, fix, refactor, test, docs, chore
Scopes: domain, application, infrastructure, presentation
```

### Before Merging
1. All tests pass
2. Code is linted
3. Types are checked
4. Coverage is adequate (>80%)

## Progress Tracking

Use TodoWrite to track your progress:

```markdown
- [x] Domain: Grade value object
- [x] Domain: Student entity
- [ ] Domain: AdmissionRule entity
- [ ] Application: EvaluateAdmissionUseCase
- [ ] Infrastructure: StudentRepository
- [ ] Presentation: API endpoint
```

Update after completing each step!

## Skills to Apply Automatically

During execution, these skills guide you:
- **test-driven-development**: RED-GREEN-REFACTOR cycle
- **domain-driven-design**: Rich domain models
- **clean-architecture**: Layer compliance
- **solid-principles**: Code quality
- **trunk-based-development**: Git workflow

## Common Mistakes to Avoid

❌ Writing implementation before tests
❌ Skipping the REFACTOR step
❌ Mixing domain logic with infrastructure
❌ Creating anemic domain models (just data, no behavior)
❌ Skipping edge case tests
❌ Large commits without incremental progress
❌ Not running tests frequently

## Completion Checklist

Before marking as done:

- [ ] All Gherkin scenarios have tests
- [ ] All tests pass (unit, integration, e2e)
- [ ] Code coverage > 80%
- [ ] No linting errors
- [ ] No type errors
- [ ] Domain has no framework dependencies
- [ ] Dependencies point inward
- [ ] Ports defined in domain/application
- [ ] Adapters implemented in infrastructure/presentation
- [ ] Commits are clean and descriptive
- [ ] Ready for PR / merge

## Output

Execute the plan step by step, following TDD and Clean Architecture principles. Show your work:
- Tests written
- Implementation code
- Test results
- Refactorings applied
- Progress updates

Keep me informed of your progress and ask questions if anything is unclear in the plan.
