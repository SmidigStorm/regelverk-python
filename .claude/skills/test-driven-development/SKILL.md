---
name: test-driven-development
description: Follow TDD practices with Red-Green-Refactor cycle. Write tests before implementation, use AAA pattern, and ensure high-quality test coverage. Use when implementing features or fixing bugs.
---

# Test-Driven Development (TDD) Skill

You are assisting with code that must be developed using Test-Driven Development practices.

## TDD Cycle: Red-Green-Refactor

### 1. RED - Write a Failing Test
- Write the test FIRST before implementation
- Test should fail for the right reason
- Test describes desired behavior, not implementation

### 2. GREEN - Make It Pass
- Write minimal code to make the test pass
- Don't worry about perfection yet
- Focus on making it work

### 3. REFACTOR - Clean It Up
- Improve code structure
- Apply design principles (SOLID, Clean Architecture)
- Tests should still pass

**Repeat**: Start the cycle again for the next small piece of functionality

## TDD Principles

### Test First, Always
```python
# WRONG: Writing implementation first
def calculate_competence_points(grades):
    # implementation here
    pass

# RIGHT: Writing test first
def test_calculate_competence_points_with_all_passing_grades():
    grades = [Grade("Math", 5), Grade("Norwegian", 4)]
    points = calculate_competence_points(grades)
    assert points == 45  # Then write implementation
```

### Baby Steps
- Write the simplest test possible
- Add one test at a time
- Incremental complexity

### Test Behavior, Not Implementation
```python
# GOOD: Tests behavior
def test_student_is_qualified_when_meeting_minimum_grade():
    student = Student("John", grades=[Grade("Math", 4)])
    rule = MinimumGradeRule(threshold=4)
    assert rule.evaluate(student) == True

# BAD: Tests implementation details
def test_rule_calls_grade_comparator_method():
    # Testing internal methods/implementation
    pass
```

## Testing Pyramid

### Unit Tests (70%)
- Test individual functions/classes in isolation
- Fast, isolated, deterministic
- Use mocks for dependencies
- Example: Test single admission rule

### Integration Tests (20%)
- Test combinations of units
- Verify components work together
- Example: Test rule engine with multiple rules

### End-to-End Tests (10%)
- Test complete user workflows
- Slowest, most fragile
- Example: Test full admission evaluation process

## Testing Best Practices

### AAA Pattern (Arrange-Act-Assert)
```python
def test_quota_rule_rejects_when_quota_full():
    # ARRANGE - Set up test data
    quota = Quota(name="Engineering", capacity=100, filled=100)
    student = Student("Jane")
    rule = QuotaRule(quota)

    # ACT - Execute the behavior
    result = rule.evaluate(student)

    # ASSERT - Verify outcome
    assert result.is_rejected
    assert result.reason == "Quota full"
```

### Test Naming Convention
Use descriptive names that explain:
- What is being tested
- Under what conditions
- What the expected outcome is

Format: `test_<what>_<condition>_<expected>`

Examples:
- `test_admission_rule_passes_when_grades_meet_minimum`
- `test_quota_calculation_raises_error_when_capacity_negative`
- `test_student_competence_points_equals_zero_for_empty_grades`

### FIRST Principles

**F - Fast**: Tests should run quickly
**I - Independent**: Tests should not depend on each other
**R - Repeatable**: Same input = same output, every time
**S - Self-validating**: Pass or fail, no manual checking
**T - Timely**: Written just before production code

## Test Organization

### Test Structure
```
tests/
├── unit/
│   ├── domain/
│   │   ├── test_admission_rule.py
│   │   └── test_student.py
│   ├── application/
│   │   └── test_evaluate_admission_use_case.py
│   └── infrastructure/
│       └── test_rule_repository.py
├── integration/
│   └── test_admission_workflow.py
└── e2e/
    └── test_complete_admission_process.py
```

## Mocking and Test Doubles

### When to Mock
- External services (APIs, databases)
- Slow operations (file I/O, network)
- Non-deterministic behavior (random, time)

### Types of Test Doubles

**Dummy**: Placeholder, never used
```python
dummy_logger = Mock(spec=Logger)
```

**Stub**: Returns predefined data
```python
class StubRuleRepository:
    def get_rules(self):
        return [PresetRule1(), PresetRule2()]
```

**Mock**: Verifies interactions
```python
mock_gateway = Mock()
use_case.execute(student_id)
mock_gateway.notify_student.assert_called_once()
```

**Fake**: Working implementation (simpler)
```python
class FakeRuleRepository:
    def __init__(self):
        self._rules = {}

    def add(self, rule):
        self._rules[rule.id] = rule
```

## Pytest Best Practices

### Fixtures for Reusable Setup
```python
@pytest.fixture
def sample_student():
    return Student(
        name="John Doe",
        grades=[Grade("Math", 5), Grade("Norwegian", 4)]
    )

def test_with_fixture(sample_student):
    assert sample_student.name == "John Doe"
```

### Parametrized Tests
```python
@pytest.mark.parametrize("grade,expected_points", [
    (6, 24),
    (5, 20),
    (4, 16),
    (3, 12),
])
def test_grade_to_points_conversion(grade, expected_points):
    assert convert_grade_to_points(grade) == expected_points
```

### Test Coverage
- Aim for high coverage (80%+) but don't obsess
- 100% coverage doesn't mean bug-free
- Focus on critical business logic

## Code Review Checklist

- [ ] Was the test written before the implementation?
- [ ] Does the test follow the AAA pattern?
- [ ] Is the test name descriptive and clear?
- [ ] Does the test verify behavior, not implementation?
- [ ] Is the test independent and isolated?
- [ ] Are mocks/stubs used appropriately?
- [ ] Does the test run quickly?
- [ ] Is the production code minimal to pass the test?

## TDD Workflow for Admission Rules

1. **Write test**: `test_minimum_grade_rule_passes_when_grade_meets_threshold`
2. **Run test**: See it fail (RED)
3. **Implement**: `MinimumGradeRule.evaluate()` method
4. **Run test**: See it pass (GREEN)
5. **Refactor**: Extract common logic, apply SOLID
6. **Repeat**: Next test for edge cases

## Common Pitfalls to Avoid

- Writing tests after implementation
- Testing implementation details instead of behavior
- Tests that are too complex
- Tests that depend on other tests
- Not refactoring tests along with code
- Skipping tests for "simple" code

## Response Format

When practicing TDD:
1. Always write the test first
2. Show the failing test (RED)
3. Implement minimal code to pass
4. Show the passing test (GREEN)
5. Refactor if needed
6. Explain what behavior is being tested
7. Move to the next small test
