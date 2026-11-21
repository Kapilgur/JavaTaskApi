# Project instructions

## Goal
Maintain a Spring Boot REST API for tasks, using MySQL in development and H2 only in tests.

## Architecture
- Controllers handle HTTP and validation only.
- Services contain business logic and transaction boundaries.
- Repositories contain persistence access.
- DTOs define the public API; never expose JPA entities directly.
- Flyway owns production schema changes.

## Hard constraints
- Every source file must contain at most 50 physical lines.
- Prefer small classes and extracted helpers; do not compress unreadable code to pass the limit.
- Never edit generated files under `target/`.
- Never place secrets in source, settings, or commits.
- Do not commit or push unless explicitly asked.

## Efficient workflow
1. Read `README.md`, then only the relevant layer and test.
2. State a short plan before changing more than one file.
3. Make the smallest change that satisfies the requirement.
4. Run the focused test first, then `./mvnw test`.
5. Use `git diff --check` and summarize changed behavior.

## Commands
- Windows tests: `mvnw.cmd test`
- macOS/Linux tests: `./mvnw test`
- Run API: `mvnw.cmd spring-boot:run` or `./mvnw spring-boot:run`
- Start MySQL: `docker compose up -d mysql`

## API conventions
Base path is `/api/v1/tasks`. Return 201 for create, 204 for delete, 400 for validation errors,
and 404 for missing tasks. Status values are `TODO`, `IN_PROGRESS`, and `DONE`.
