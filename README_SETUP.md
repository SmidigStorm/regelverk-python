# Setup Guide

Quick start guide for setting up and running the Norwegian Admission Rules System.

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd regelverk-python
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -e .

# Install development dependencies (for testing and code quality)
pip install -e ".[dev]"
```

### 4. Configure Environment

Copy the example environment file and customize if needed:

```bash
cp .env.example .env
```

Edit `.env` to configure:
- `DATABASE_URL`: Database connection string (default: SQLite)
- `DEBUG`: Enable debug mode (default: true for development)
- `API_HOST` and `API_PORT`: API server configuration
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

## Running the Application

### Start the Development Server

```bash
# Set PYTHONPATH to include project root
export PYTHONPATH=.

# Run with Python
python src/presentation/api/main.py
```

Or with uvicorn directly:

```bash
export PYTHONPATH=.
uvicorn src.presentation.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Verify Installation

Test the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

View coverage report by opening `htmlcov/index.html` in a browser.

### Run Specific Test Types

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# E2E tests only
pytest tests/e2e/

# BDD feature tests
pytest tests/features/
```

## Database Migrations

Once you have database models, use Alembic for migrations:

### Initialize Alembic (only once)

```bash
alembic init alembic
```

### Create a Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Code Quality

### Linting and Formatting

```bash
# Check code style
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Type Checking

```bash
mypy src/
```

## Project Structure

```
regelverk-python/
├── src/
│   ├── domain/              # Domain layer (pure Python, no dependencies)
│   ├── application/         # Application layer (use cases, DTOs)
│   ├── infrastructure/      # Infrastructure layer (database, external services)
│   └── presentation/        # Presentation layer (FastAPI, API routes)
├── tests/
│   ├── unit/               # Fast isolated tests
│   ├── integration/        # Component interaction tests
│   ├── e2e/               # End-to-end tests
│   └── features/          # BDD Gherkin scenarios
├── documentation/          # Architecture and planning docs
├── .claude/               # Claude Code skills and commands
├── pyproject.toml         # Project configuration and dependencies
└── README_SETUP.md        # This file
```

## Development Workflow

1. **Check out a feature**: Create a branch if work takes >4 hours
2. **Write tests first**: Follow TDD (Test-Driven Development)
3. **Implement feature**: Write minimal code to pass tests
4. **Refactor**: Clean up code while keeping tests green
5. **Run tests**: Ensure all tests pass
6. **Check code quality**: Run linting and type checking
7. **Commit**: Make small, focused commits
8. **Merge**: Keep PRs small (<400 lines) and merge quickly

## Troubleshooting

### Import Errors

If you encounter import errors, ensure:
1. Virtual environment is activated
2. Package is installed in editable mode: `pip install -e .`
3. You're running commands from the project root directory

### Database Issues

If database-related errors occur:
1. Check `DATABASE_URL` in `.env`
2. Ensure database file/server is accessible
3. Run migrations: `alembic upgrade head`

### Test Failures

If tests fail:
1. Ensure all dependencies are installed: `pip install -e ".[dev]"`
2. Check that no services are running on test ports
3. Clear test database if using persistent storage

## Next Steps

- Read [CLAUDE.md](CLAUDE.md) for project overview and domain context
- Check [documentation/architecture/](documentation/architecture/) for architecture decisions
- Review [documentation/plans/](documentation/plans/) for implementation plans
- Start implementing domain models following TDD

## Getting Help

- Check the documentation in `documentation/`
- Review existing code for patterns
- Run `/help` in Claude Code for assistance
