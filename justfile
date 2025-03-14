# Default recipe that shows available commands
default:
    @just --list

# Generate Pydantic models from OpenAPI spec
generate-models:
    @uv run scripts/generate_schemas.py

# Run the server
run:
    uv run -m app.main

# Run tests
test:
    uv run pytest

# Run tests with coverage report
test-coverage:
    uv run pytest --cov-report=html:coverage_html