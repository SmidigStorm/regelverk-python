# Aggregate Root: Education

**Date**: 2025-10-28
**Status**: Domain Understanding Complete
**DDD Pattern**: Aggregate Root

---

## Definition

An **Education** represents a specific offering of a study program at an institution for a particular intake period.

**Ubiquitous Language:**
- English: Education, Education Offering
- Norwegian: Utdanningstilbud

---

## Examples

- "Bachelor in Nursing, NTNU Trondheim, Autumn 2025"
- "Master in Computer Science, UiO Blindern, Spring 2026"
- "Bachelor in Engineering, NTNU Gjøvik, Autumn 2025"

---

## Aggregate Structure

### Aggregate Root: Education

**Identity:**
- `EducationId` (unique identifier)

**Attributes:**
- `program_name` (string) - e.g., "Bachelor in Nursing"
- `institution` (string) - e.g., "NTNU"
- `campus` (string) - e.g., "Trondheim", "Gjøvik"
- `intake_term` (string/value object) - e.g., "Autumn 2025"
- `study_mode` (enum) - e.g., full-time, part-time
- `language` (enum/string) - e.g., Norwegian, English
- `state` (enum) - Planned | Active | Finished

**References (to other Aggregate Roots):**
- `ruleset_id` (RulesetId) - Reference to admission Ruleset aggregate
- `admission_process_id` (AdmissionProcessId) - Reference to Admission Process aggregate

---

## Business Rules & Invariants

### 1. State Transitions
- Valid transitions: `Planned → Active → Finished`
- No backwards transitions allowed
- State cannot skip steps (e.g., cannot go directly from Planned to Finished)

### 2. Mutability
- All attributes can be changed while in `Planned` state
- `ruleset_id` can be changed (mutable reference)
- `admission_process_id` can be changed (mutable reference)

### 3. Live References
- When the referenced Ruleset changes, all Educations using it are affected
- Educations do NOT snapshot rulesets - they use live references

### 4. Identity & Uniqueness
- Each Education offering is unique even if program name is identical
- Example: "Bachelor in Nursing, NTNU Trondheim, Autumn 2025" ≠ "Bachelor in Nursing, NTNU Gjøvik, Autumn 2025"

---

## Relationships to Other Aggregates

### Education → Ruleset (Many-to-One)
- Multiple Educations can reference the same Ruleset
- Ruleset is a separate Aggregate Root
- Relationship is by ID reference (not embedded)
- Changes to Ruleset affect all Educations referencing it

### Education → Admission Process (Many-to-One)
- Multiple Educations can be part of the same Admission Process
- Admission Process is a separate Aggregate Root (e.g., "UGH 2025 Admission")
- Relationship is by ID reference
- Admission Process has dates (application period, decision dates, etc.)

### Future Relationships (Not Yet Modeled)
- Education ← Application (one Education can have many Applications)
- Education ← Quota (one Education can have multiple Quotas)

---

## Domain Events (Potential)

Future events this aggregate might raise:
- `EducationCreated`
- `EducationStateChanged` (e.g., Planned → Active)
- `EducationRulesetChanged`
- `EducationAdmissionProcessChanged`

---

## Design Decisions

### Why Aggregate Root?
1. **Self-contained invariants**: State transitions must be internally consistent
2. **Direct external references**: Applications will reference Educations by ID
3. **Transactional boundary**: Changes to Education should be atomic
4. **Clear lifecycle**: Planned → Active → Finished

### Why NOT Include Ruleset/Admission Process Inside?
- Both are shared across multiple Educations
- They have their own lifecycles and invariants
- They are managed independently

---

## Implementation Notes

### Value Objects to Consider
- `EducationId` - typed identifier
- `IntakeTerm` - structured term (semester + year)
- `StudyMode` - enumeration
- `EducationState` - enumeration with transition rules

### Repository Interface
- `EducationRepository` will be defined as a port in `src/domain/ports.py`
- Methods: `save()`, `find_by_id()`, `find_by_admission_process()`, etc.

---

## Open Questions

1. **Capacity/Quotas**: Does Education itself have capacity constraints, or is that managed separately?
2. **Versioning**: If an Education changes significantly (e.g., campus changes), is it a new Education or an update?
3. **Archival**: Can an Education go back from Finished to another state, or is Finished terminal?

---

## Next Steps

1. Write requirements (user story + Gherkin scenarios)
2. Create implementation plan
3. Implement with TDD:
   - Start with value objects (EducationId, IntakeTerm, EducationState)
   - Then build Education entity
   - Finally add behavior methods
