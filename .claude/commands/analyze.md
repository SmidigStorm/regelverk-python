---
description: Analyze requirements for a feature to be implemented
argument-hint: [feature description]
allowed-tools: Read, Grep, Glob
---

# Requirements Analysis Phase

You are in the **requirements analysis phase** of the workflow. Your goal is to thoroughly analyze and document the requirements for the feature to be implemented.

## Your Task

Analyze the requirements for: **$ARGUMENTS**

## What to Do

### 1. Understand the Feature
- What is the user trying to accomplish?
- What problem does this solve?
- Who are the stakeholders (applicant, admission officer, administrator)?

### 2. Write User Stories
Use the format:
```
As a [role]
I want [feature]
So that [benefit]
```

### 3. Define Acceptance Criteria with Gherkin
Write detailed scenarios using Given-When-Then format:

```gherkin
Feature: [Feature name]
  [Brief description of business value]

  Scenario: [Specific situation]
    Given [initial context/preconditions]
    And [additional context]
    When [action/event occurs]
    Then [expected outcome]
    And [additional expectations]

  Scenario: [Edge case or alternative flow]
    Given [context]
    When [action]
    Then [outcome]
```

### 4. Identify Edge Cases
- What can go wrong?
- What are the boundary conditions?
- What are the error scenarios?

### 5. Domain Model Impact
- What domain entities are involved?
- What value objects are needed?
- Which layer does this belong to (domain, application, infrastructure, presentation)?

### 6. Dependencies
- Does this require other features first?
- What external systems are involved?
- Are there database changes needed?

## Analysis Structure

Provide your analysis in this format:

```markdown
# Feature: [Name]

## User Story
As a...
I want...
So that...

## Acceptance Criteria

### Gherkin Scenarios
[Write detailed scenarios]

### Edge Cases
- [List edge cases]

### Non-Functional Requirements
- Performance: [requirements]
- Security: [requirements]
- Validation: [requirements]

## Domain Model

### Entities Involved
- [Entity 1]: [purpose]
- [Entity 2]: [purpose]

### Value Objects Needed
- [Value Object 1]: [purpose]

### Business Rules
1. [Rule 1]
2. [Rule 2]

## Architecture

### Layer Assignment
- Domain: [what goes here]
- Application: [what goes here]
- Infrastructure: [what goes here]
- Presentation: [what goes here]

### Dependencies
- [Dependency 1]
- [Dependency 2]

## Questions/Uncertainties
- [Question 1]
- [Question 2]
```

## Skills to Apply

Use these skills automatically:
- **requirements-writing**: For user stories and Gherkin scenarios
- **domain-driven-design**: For domain model analysis
- **clean-architecture**: For layer assignment

## Existing Code Context

If relevant, examine existing code:
- Search for similar features
- Check existing domain models
- Review existing use cases

## Output

Provide a complete requirements analysis document that can be used in the planning phase.
