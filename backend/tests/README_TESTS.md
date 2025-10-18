# Repository Tests

This directory contains tests for the Socrates 8.0 backend.

## Running Tests

### Prerequisites

- PostgreSQL database running and configured in `.env`
- All dependencies installed: `pip install -r requirements.txt`

### Run All Tests

```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_repositories.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_repositories.py::TestUserRepository -v
```

### Run Specific Test Method

```bash
pytest tests/test_repositories.py::TestUserRepository::test_create_user -v
```

## Test Coverage

Current test coverage targets:
- Repository layer: 80%+
- Service layer: 80%+
- API routes: 70%+

## Test Database

Tests use the PostgreSQL database configured in `.env`. The test database should be set to a dedicated test database:

```env
DATABASE_URL=postgresql://user:password@localhost/socrates_8_test
```

## Notes on SQLite Testing

Tests are designed for PostgreSQL which supports UUID natively. SQLite does not support PostgreSQL's UUID type, so SQLite cannot be used for testing these repositories without additional adaptation.

For local development and CI/CD, use PostgreSQL in a Docker container:

```bash
docker run --name socrates-postgres -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 postgres:14
```

Then create test database:

```bash
docker exec socrates-postgres psql -U postgres -c "CREATE DATABASE socrates_8_test;"
```
