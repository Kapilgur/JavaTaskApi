# Java Task REST API with MySQL and Claude Code hooks

A complete learning project using Java 17, Spring Boot, Maven, Spring Data JPA, Flyway, MySQL,
H2 integration tests, Docker Compose, and project-scoped Claude Code hooks. The hooks enforce a
maximum of 50 lines per source file so you can practice deterministic controls around an AI agent.

## Prerequisites

- JDK 17 or newer: `java -version`
- Docker Desktop with Compose: `docker compose version`
- Claude Code if you want to exercise the hooks (the API itself does not need Claude or an API key)
- Python 3.9+ only for the included hook scripts: `python --version`
- Git (recommended)

Maven does not need to be installed: the included Maven Wrapper downloads the pinned Maven version.

## Project map

```text
src/main/java/.../controller   HTTP endpoints
src/main/java/.../service      business logic and transactions
src/main/java/.../repository   JPA data access
src/main/java/.../domain       entity and status enum
src/main/java/.../dto          request/response contracts
src/main/resources/db          Flyway migrations
src/test                       H2-backed integration tests
.claude                        hooks, project settings, reusable skill
```

## 1. Start MySQL

```powershell
docker compose up -d mysql
docker compose ps
```

The compose file creates database `taskdb`, user `taskuser`, and password `taskpass`. These are
local learning defaults. Replace them with secrets outside source control for shared environments.
Wait until the container is healthy before starting the API.

## 2. Run tests

Windows PowerShell:

```powershell
.\mvnw.cmd test
```

macOS/Linux:

```bash
./mvnw test
```

Tests use an in-memory H2 database in MySQL compatibility mode, so MySQL is not required for tests.

## 3. Run the API

Windows PowerShell:

```powershell
.\mvnw.cmd spring-boot:run
```

macOS/Linux:

```bash
./mvnw spring-boot:run
```

Flyway creates the `tasks` table automatically. Check `http://localhost:8080/actuator/health`.
To use different credentials, set `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` before starting.

## 4. Try the CRUD endpoints

PowerShell create request:

```powershell
$body = @{ title = "Learn hooks"; description = "Keep Java files small"; dueDate = "2026-12-01" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/v1/tasks -ContentType application/json -Body $body
```

List and update:

```powershell
Invoke-RestMethod http://localhost:8080/api/v1/tasks
$update = @{ status = "DONE" } | ConvertTo-Json
Invoke-RestMethod -Method Patch -Uri http://localhost:8080/api/v1/tasks/1 -ContentType application/json -Body $update
```

Delete:

```powershell
Invoke-RestMethod -Method Delete -Uri http://localhost:8080/api/v1/tasks/1
```

See `docs/API.md` for request fields, pagination, status values, and error responses.

## 5. Use the project with Claude Code

Open a terminal in this repository and run Claude Code. If your Enterprise login already works, no separate Anthropic API key is required. It reads `CLAUDE.md` for architecture and
workflow guidance, discovers `.claude/skills/java-rest-api/SKILL.md`, and loads project hooks from
`.claude/settings.json`. If asked, review and trust the repository hooks.

Suggested staged prompts:

1. `Read CLAUDE.md and explain the architecture. Do not edit files.`
2. `Use the java-rest-api skill. Add filtering by task status. Plan first.`
3. `Run the focused tests, then all tests. Show the result and git diff --stat.`

The 50-line hook forces Claude to split responsibilities instead of creating large classes. The
Stop hook catches pre-existing or externally created violations. Details and limitations are in
`docs/HOOKS.md`.

## 6. Git workflow

```powershell
git init
git add .
git diff --cached
git commit -m "Create Spring Boot task API with MySQL and Claude hooks"
```

Create an empty remote repository, then use its exact URL:

```powershell
git branch -M main
git remote add origin <YOUR-REPOSITORY-URL>
git push -u origin main
```

Always review `git diff` and test before committing AI-generated changes. Claude Code does not push
unless you ask it to and grant the required permission.

## Design notes

- DTOs keep the public API separate from persistence entities.
- Service transactions keep business operations atomic.
- Flyway makes production schema changes repeatable.
- Environment variables keep deploy-time values out of Java code.
- H2 makes tests fast; run an additional MySQL integration suite before production use.
- This learning API has no authentication. Add Spring Security before exposing it publicly.
