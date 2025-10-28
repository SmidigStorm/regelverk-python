# Workflow Commands

This directory contains four slash commands that define our development workflow.

## The Workflow

```
/domain → /analyze → /plan → /execute
```

### 1. `/domain [concept]`
**Understand the domain**

Explore and understand domain concepts in the Norwegian admission system.

**Usage:**
```
/domain quota
/domain student
/domain competence points
/domain
```

**Output**: Domain understanding with DDD classification (entity, value object, aggregate, etc.)

---

### 2. `/analyze [feature]`
**Analyze requirements**

Analyze and document requirements for a feature using user stories and Gherkin scenarios.

**Usage:**
```
/analyze minimum grade requirement rule
/analyze quota capacity enforcement
/analyze student registration
```

**Output**: Complete requirements analysis with:
- User stories
- Gherkin scenarios
- Domain model impact
- Architecture decisions

---

### 3. `/plan [feature]`
**Create implementation plan**

Create a detailed, step-by-step implementation plan following TDD and Clean Architecture.

**Usage:**
```
/plan minimum grade rule
/plan based on previous analysis
```

**Output**: Actionable implementation plan with:
- Step-by-step tasks
- TDD approach (test first)
- Layer-by-layer breakdown (domain → application → infrastructure → presentation)
- Git workflow strategy
- Task checklist

---

### 4. `/execute [plan]`
**Execute the plan**

Implement the plan step-by-step following TDD, Clean Architecture, and best practices.

**Usage:**
```
/execute minimum grade rule
/execute the plan above
```

**Output**: Working implementation with:
- Tests written first (RED-GREEN-REFACTOR)
- Clean code following SOLID principles
- Proper layer separation
- Frequent commits
- Progress tracking

---

## Example Workflow

```bash
# Step 1: Understand the domain
/domain quota

# Step 2: Analyze requirements for a feature
/analyze quota capacity enforcement

# Step 3: Create implementation plan
/plan quota capacity enforcement

# Step 4: Execute the plan
/execute quota capacity enforcement
```

## Skills Applied

These commands automatically apply the configured skills:
- **domain-driven-design** (in `/domain` and `/analyze`)
- **requirements-writing** (in `/analyze`)
- **clean-architecture** (in `/plan` and `/execute`)
- **test-driven-development** (in `/execute`)
- **solid-principles** (in `/execute`)
- **trunk-based-development** (in `/plan` and `/execute`)

## When to Use Each Command

| Situation | Command | Why |
|-----------|---------|-----|
| Starting a new feature | `/domain` + `/analyze` | Understand before building |
| Have requirements, need plan | `/plan` | Structure the implementation |
| Have plan, ready to code | `/execute` | Build it with TDD |
| Unclear about domain concept | `/domain [concept]` | Get clarity first |
| Requirements are vague | `/analyze` | Document properly |

## Tips

- **Don't skip steps**: Each phase builds on the previous one
- **Domain first**: Always understand domain before implementing
- **Analysis before planning**: Clear requirements = better plans
- **Planning before execution**: Good plans = smooth execution
- **Use TodoWrite**: Track progress during `/execute`

## Customization

These commands are in `.claude/commands/` (project-level). To customize:
1. Edit the `.md` files
2. Commands reload automatically
3. Check with `/help` to see them listed

---

Ready to start building? Begin with `/domain` to understand your first concept!
