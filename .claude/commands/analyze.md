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

## Output Format

Create a **single Gherkin .feature file** in `tests/features/` directory.

**Why tests/features/?**
- Gherkin .feature files are **executable tests** (not just documentation)
- pytest-bdd discovers and runs them as automated tests
- They validate that implementation matches business requirements
- This is the standard BDD structure in Python projects

**Directory structure:**
```
tests/
├── features/           ← Gherkin .feature files (executable test scenarios)
├── step_defs/          ← Python step definitions (will be created during implementation)
├── unit/               ← Traditional unit tests
└── integration/        ← Traditional integration tests
```

The file should follow this structure:

```gherkin
Feature: [Feature Name]
  As a [role]
  I want [capability]
  So that [benefit]

  Background:
    Given [common preconditions for all scenarios]

  Scenario: [Happy path scenario name]
    Given [initial context]
    And [additional context]
    When [action occurs]
    Then [expected outcome]
    And [additional expectations]

  Scenario: [Alternative scenario name]
    Given [context]
    When [action]
    Then [outcome]

  Scenario: [Error scenario name]
    Given [context]
    When [invalid action]
    Then [error outcome]
    And [error message or state]
```

## File Naming Convention

- Use kebab-case for filename
- Save in `tests/features/[domain-area]/[feature-name].feature`
- Example: `tests/features/education/manage-education.feature`

## Gherkin Best Practices

1. **Keep scenarios focused**: One scenario should test one behavior
2. **Use business language**: Avoid technical implementation details
3. **Be specific**: Use concrete examples, not abstract descriptions
4. **Include edge cases**: Happy path, alternatives, and error scenarios
5. **Use Background**: For common setup across multiple scenarios
6. **Use Scenario Outline**: For testing multiple similar cases with different data

## What NOT to Include

- Do NOT create markdown documentation files
- Do NOT write implementation details
- Do NOT include architecture notes in the feature file
- Keep it pure Gherkin that can be executed by pytest-bdd

## Skills to Apply

Use these skills automatically:
- **requirements-writing**: For user stories and Gherkin scenarios
- **domain-driven-design**: For domain terminology

## After Creating Feature File

After creating the .feature file, create a brief summary for the user that includes:
- Location of the feature file
- Number of scenarios written
- What aspects were covered (happy path, edge cases, errors)
- Suggested next step (use /plan to create implementation plan)
