# Development Skills

This project has 6 software development skills configured for Claude Code. These skills are **automatically applied** by Claude when relevant - you don't need to explicitly invoke them.

## Available Skills

1. **requirements-writing** - User stories and Gherkin scenarios
2. **solid-principles** - SOLID design principles
3. **clean-architecture** - Layered architecture patterns
4. **test-driven-development** - TDD Red-Green-Refactor cycle
5. **domain-driven-design** - DDD tactical and strategic patterns
6. **trunk-based-development** - Git workflow with short-lived branches

## How It Works

Just work naturally with Claude. The skills activate automatically based on what you're doing:

- Ask "Where should this code go?" → clean-architecture activates
- Say "Let's implement a quota rule" → Multiple skills activate (requirements-writing, domain-driven-design, test-driven-development)
- Show code for review → solid-principles activates
- Ask about branching → trunk-based-development activates

## Project Context

These skills are configured specifically for a **Norwegian higher education admission rules system** with domain concepts like:
- Admission requirements (Opptakskrav)
- Quotas (Kvoter)
- Competence points (Karakterpoeng)
- Student applicants (Søkere)

## Learn More

- Each skill's detailed guidance is in `.claude/skills/[skill-name]/SKILL.md`
- The `CLAUDE.md` file contains instructions for Claude on when to apply each skill
- Skills documentation: https://docs.claude.com/en/docs/claude-code/skills.md
