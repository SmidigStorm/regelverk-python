# Domain Factories

This folder contains **separate factory classes** for complex aggregate creation scenarios.

## When to Use This Folder

Use a **separate factory class** here when:

1. **Complex creation logic** - Multiple steps, complex algorithms, or business rules
2. **Multiple return types** - Factory returns different aggregate types based on input
3. **External dependencies** - Creation requires repositories, domain services, or other aggregates
4. **Reconstitution logic** - Complex logic to rebuild aggregates from external data
5. **Testability** - Need to mock/inject factory behavior

## When NOT to Use This Folder

Use a **static factory method** on the aggregate itself when:

1. **Simple creation** - Just validation and initialization
2. **Single type** - Always returns the same aggregate type
3. **No dependencies** - Doesn't need external services
4. **Natural language** - `Education.create(...)` reads well

## Examples

### ❌ Don't use separate factory (use static method instead):
```python
# Simple creation - use Education.create() static method
class Education:
    @staticmethod
    def create(program_name, institution, ...) -> 'Education':
        # Simple validation and initialization
        if not program_name:
            raise InvalidEducationError("program_name is required")
        return Education(...)
```

### ✅ Do use separate factory:
```python
# Complex creation with dependencies
class EducationFromApplicationFactory:
    """
    Creates Education aggregate from student application data.
    Requires validation against external rulesets and admission processes.
    """

    def __init__(
        self,
        ruleset_repository: RulesetRepository,
        admission_process_repository: AdmissionProcessRepository
    ):
        self._ruleset_repo = ruleset_repository
        self._admission_process_repo = admission_process_repo

    def create_from_application(
        self,
        application: Application
    ) -> Education:
        # Complex logic:
        # 1. Fetch and validate ruleset
        # 2. Fetch and validate admission process
        # 3. Apply complex business rules
        # 4. Create education with validated data
        ...
```

### ✅ Another example - multiple types:
```python
class StudyProgramFactory:
    """Returns different aggregate types based on input"""

    def create_program(self, program_type: str, data: dict):
        if program_type == "education":
            return Education.create(...)
        elif program_type == "course":
            return Course.create(...)
        elif program_type == "workshop":
            return Workshop.create(...)
```

## Current Status

Currently **no factories in this folder** - all aggregates use static factory methods.

### Planned Future Factories

**RulesetFactory** (coming soon):
- Rulesets have complex creation logic
- May need to compose multiple rules and validation logic
- Could involve business rule interpretation
- Will likely require a separate factory class here

## References

- [DAN DOES CODE: DDD Patterns for Aggregate Creation Mastery](https://www.dandoescode.com/blog/domain-driven-design-patterns-for-aggregate-creation-mastery)
- [Stack Overflow: When to apply factory method in aggregate root](https://stackoverflow.com/questions/35824607/when-should-apply-factory-method-in-the-aggregate-root)
