# Implementation Plan: Repository Structure and Foundational Infrastructure

## Overview
Set up the complete project skeleton for the Norwegian Admission Rules System following Clean Architecture with Package by Layer structure (as defined in chosen-structure.md). This establishes the foundational infrastructure without implementing domain logic, creating a runnable FastAPI application with proper configuration, database setup, and testing structure.

## Prerequisites
- [x] Python 3.11+ installed
- [x] Git repository initialized
- [ ] Virtual environment will be created during setup

## Project Configuration

### Step 1: Create pyproject.toml
**Files to create:**
- `pyproject.toml` - Python project configuration with all dependencies

**Implementation:**
- Define project metadata (name, version, Python requirement)
- Core dependencies:
  - FastAPI 0.104+ (presentation layer)
  - Uvicorn with standard extras (ASGI server)
  - SQLAlchemy 2.0+ (infrastructure layer)
  - Alembic 1.12+ (database migrations)
  - Pydantic 2.4+ (validation and settings)
  - Pydantic-settings 2.0+ (configuration management)
  - Python-dotenv 1.0+ (environment variables)
- Dev dependencies:
  - pytest 7.4+
  - pytest-cov 4.1+
  - pytest-bdd 6.1+
  - pytest-asyncio 0.21+
  - httpx 0.25+ (for FastAPI testing)
  - ruff 0.1+ (linting/formatting)
  - mypy 1.6+ (type checking)

### Step 2: Create environment configuration template
**Files to create:**
- `.env.example` - Template for environment variables
- `.gitignore` - Ignore .env, __pycache__, etc.

**Implementation:**
- Database configuration (DATABASE_URL)
- API configuration (HOST, PORT, DEBUG)
- Environment (ENV: development/production)
- Log level

## Directory Structure

### Step 3: Create layer-based directory structure
**Directories to create:**
```
src/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── aggregates/
│   ├── services/
│   └── events/
├── application/
│   ├── use_cases/
│   └── dtos/
├── infrastructure/
│   ├── persistence/
│   │   ├── models/
│   │   ├── mappers/
│   │   └── repositories/
│   ├── config/
│   └── external/
└── presentation/
    └── api/
        ├── schemas/
        └── routes/
```

**Implementation:**
- Create all directories following Package by Layer structure
- Add `__init__.py` to every directory to make them Python packages
- Keep all `__init__.py` files empty for now (just package markers)
- Add `ports.py` and `exceptions.py` files to domain/ (empty for now)

### Step 4: Create testing directory structure
**Directories to create:**
```
tests/
├── unit/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── integration/
├── e2e/
├── features/
└── conftest.py
```

**Files to create:**
- `tests/conftest.py` - Shared pytest fixtures

**Implementation:**
- Create directory structure
- Add `__init__.py` files
- Basic conftest.py with placeholder for future fixtures

## Shared Infrastructure Layer

### Step 5: Settings and configuration
**Files to create:**
- `src/infrastructure/config/settings.py`
- `src/infrastructure/config/__init__.py`

**Implementation:**
- Use Pydantic BaseSettings for type-safe configuration
- Load from environment variables
- Settings:
  - `DATABASE_URL: str = "sqlite:///./regelverk.db"`
  - `ENV: str = "development"`
  - `DEBUG: bool = False`
  - `API_HOST: str = "0.0.0.0"`
  - `API_PORT: int = 8000`
  - `LOG_LEVEL: str = "INFO"`
- Export settings singleton

### Step 6: Database configuration
**Files to create:**
- `src/infrastructure/persistence/base.py`
- `src/infrastructure/persistence/database.py`
- `src/infrastructure/persistence/__init__.py`

**Implementation:**
- `base.py`: SQLAlchemy DeclarativeBase class
- `database.py`:
  - Create SQLAlchemy engine (with settings.DATABASE_URL)
  - Create SessionLocal factory
  - `get_db_session()` dependency for FastAPI (yields session, closes after)
  - Note: Use SQLAlchemy 2.0 modern style

**Tests:**
- Not needed yet (will test with integration tests later)

### Step 7: Alembic setup
**Files to create:**
- `alembic.ini` - Alembic configuration
- `alembic/env.py` - Migration environment
- `alembic/versions/` - Directory for migrations

**Commands to run:**
```bash
alembic init alembic
```

**Configuration:**
- Edit `alembic.ini`: use `sqlalchemy.url` from settings
- Edit `alembic/env.py`: import Base from shared.infrastructure.persistence
- Configure autogenerate to detect all models

## Presentation Layer

### Step 8: FastAPI application entry point
**Files to create:**
- `src/presentation/api/main.py` - Main FastAPI application
- `src/presentation/api/dependencies.py` - Dependency injection wiring

**Implementation:**
- `main.py`:
  - Create FastAPI app with title "Norwegian Admission Rules API"
  - Add CORS middleware (allow localhost:5173 for Vite)
  - Health check endpoint: `GET /health` returns `{"status": "ok"}`
  - Include routers (placeholder for now)
  - Uvicorn run configuration in `if __name__ == "__main__"`
- `dependencies.py`:
  - Re-export `get_db_session` from infrastructure.persistence.database
  - Placeholder for future dependency injection

### Step 9: Placeholder API routes
**Files to create:**
- `src/presentation/api/routes/admission_routes.py`
- `src/presentation/api/routes/student_routes.py`
- `src/presentation/api/routes/quota_routes.py`

**Implementation:**
- Each file creates an APIRouter with appropriate prefix:
  - `/api/v1/admission`
  - `/api/v1/students`
  - `/api/v1/quotas`
- Add one placeholder endpoint each:
  - `GET /api/v1/admission/` returns `{"message": "Admission API"}`
  - `GET /api/v1/students/` returns `{"message": "Student API"}`
  - `GET /api/v1/quotas/` returns `{"message": "Quota API"}`
- Wire routers into `main.py`

### Step 10: Basic E2E test
**Files to create:**
- `tests/e2e/api/test_health.py`

**Tests to write:**
- Test health endpoint returns 200
- Test CORS headers present
- Test placeholder routes respond

**Implementation:**
- Use FastAPI TestClient
- Verify application starts and responds

## Documentation

### Step 11: Setup and run documentation
**Files to create:**
- `README_SETUP.md` - Quick start guide

**Implementation:**
- How to set up virtual environment
- How to install dependencies
- How to configure .env
- How to run database migrations
- How to start development server
- How to run tests

## Git Workflow

### Branching Strategy
- [ ] Branch needed: **No** (this is foundational setup, ~2-3 hours)
- Direct commit to main
- Single commit or logical sequence

### Commit Strategy
Commit sequence:
1. "Setup project configuration and dependencies (pyproject.toml)"
2. "Create directory structure following Clean Architecture"
3. "Add shared infrastructure (settings, database config)"
4. "Setup Alembic for database migrations"
5. "Create FastAPI application with placeholder routes"
6. "Add testing structure and basic E2E test"
7. "Add setup documentation"

## Task Checklist

Execute in this order:

- [ ] **Project Configuration**
  - [ ] Create `pyproject.toml` with all dependencies
  - [ ] Create `.env.example` template
  - [ ] Create/update `.gitignore`

- [ ] **Directory Structure**
  - [ ] Create `src/` with domain/, application/, infrastructure/, presentation/ layers
  - [ ] Create all subdirectories within each layer
  - [ ] Create `tests/` with unit/, integration/, e2e/, features/ structure
  - [ ] Add `__init__.py` to all packages
  - [ ] Add `ports.py` and `exceptions.py` to domain/

- [ ] **Shared Infrastructure**
  - [ ] Implement settings.py with Pydantic Settings
  - [ ] Implement database.py (engine, session, dependency)
  - [ ] Create SQLAlchemy Base class
  - [ ] Initialize Alembic

- [ ] **Presentation Layer**
  - [ ] Create main.py with FastAPI app
  - [ ] Add CORS middleware
  - [ ] Add health check endpoint
  - [ ] Create placeholder routes for admission, student, quota
  - [ ] Wire routers into main app

- [ ] **Testing**
  - [ ] Create tests/conftest.py
  - [ ] Write E2E test for health endpoint
  - [ ] Write E2E tests for placeholder routes
  - [ ] Verify all tests pass

- [ ] **Documentation**
  - [ ] Create README_SETUP.md with setup instructions

- [ ] **Verification**
  - [ ] Install dependencies: `pip install -e .`
  - [ ] Run server: `python src/presentation/api/main.py`
  - [ ] Verify health endpoint: `curl http://localhost:8000/health`
  - [ ] Run tests: `pytest`
  - [ ] Check all tests pass
  - [ ] Verify project structure matches chosen-structure.md

## Dependencies

- Depends on: Repository initialization (already done)
- Blocks: All future domain implementation work

## Risks & Considerations

- **Risk**: SQLAlchemy 2.0 syntax differs from 1.x - **Mitigation**: Use modern declarative style from start
- **Risk**: Circular imports between modules - **Mitigation**: Use `if TYPE_CHECKING` for type hints, careful import ordering
- **Risk**: Alembic autogenerate might not detect models if not imported - **Mitigation**: Ensure all models imported in alembic/env.py
- **Risk**: Database URL configuration complexity - **Mitigation**: Use sensible defaults (SQLite for dev), clear .env.example

## Estimated Effort

- Project configuration: 0.5 hours
- Directory structure: 0.5 hours
- Shared infrastructure: 1 hour
- Presentation layer: 0.5 hours
- Testing setup: 0.5 hours
- Documentation: 0.25 hours
- **Total**: ~3.25 hours

Branch not needed (< 4 hours, foundational work).

## Architecture Compliance

This plan follows:
- ✅ **Clean Architecture**: Clear layer separation within each feature module
- ✅ **Dependency Rule**: Infrastructure depends on domain (via ports), not reverse
- ✅ **Screaming Architecture**: Top-level folders (admission, student, quota) reveal domain
- ✅ **Domain Purity**: Domain folders exist but are empty (no dependencies yet)
- ✅ **Ports & Adapters**: Structure ready for ports in domain, adapters in infrastructure
- ✅ **Testability**: Testing structure mirrors source structure

## Next Steps After Completion

Once this infrastructure is in place:
1. Implement first domain model (e.g., Grade value object)
2. Create first use case (e.g., Calculate Competence Points)
3. Add first repository implementation
4. Add first real API endpoint

This plan creates a **fully runnable skeleton** - the server will start, respond to requests, and all tests will pass, even though no business logic exists yet.
