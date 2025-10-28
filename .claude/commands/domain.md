---
description: Understand and explore the domain for Norwegian admission rules
argument-hint: [feature/concept]
---

# Domain Understanding Phase

You are in the **domain understanding phase** of the workflow. Your goal is to deeply understand the domain concepts related to the Norwegian higher education admission system.

## Your Task

Explore and understand the domain concept: **$ARGUMENTS**

If no specific concept is provided, provide an overview of the admission system domain.

## Domain Context

This system implements Norwegian higher education admission rules (Samordna opptak) including:
- **Opptakskrav** (Admission Requirements): Rules students must meet
- **Kvoter** (Quotas): Capacity limits and priority groups
- **Karakterpoeng** (Competence Points): Calculated from grades (1-6 scale, grade × 4)
- **Rangering** (Ranking): Ranking applicants by competence points

## What to Do

1. **Identify Domain Concepts**: What are the key entities, value objects, and aggregates?
2. **Understand Business Rules**: What are the invariants and constraints?
3. **Define Ubiquitous Language**: What terms do domain experts use?
4. **Explore Relationships**: How do concepts relate to each other?
5. **Clarify Boundaries**: What belongs in which bounded context?

## DDD Patterns to Consider

- **Entities**: Objects with identity (Student, AdmissionRule, Quota)
- **Value Objects**: Immutable objects (Grade, CompetencePoints, StudentId)
- **Aggregates**: Clusters with one root (AdmissionApplication)
- **Domain Services**: Cross-entity operations (AdmissionEvaluationService)
- **Domain Events**: Things that happened (StudentAdmitted, QuotaFilled)

## Questions to Answer

- What does this concept represent in the real world?
- What are the business rules governing this concept?
- Is it an entity or a value object?
- What are its invariants?
- How does it interact with other concepts?
- What Norwegian/English terms are used?

## Output

Provide a clear explanation of the domain concept including:
- Definition and purpose
- Key attributes and behaviors
- Business rules and invariants
- Relationships to other concepts
- DDD classification (entity, value object, aggregate, etc.)
- Ubiquitous language terms (Norwegian and English)

Use the **domain-driven-design** skill automatically to guide your analysis.
