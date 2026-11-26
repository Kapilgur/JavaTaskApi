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
- There is no limit on lines added per `Write` or `Edit` (the line hook is disabled).
- Prefer small classes and extracted helpers.
- Never edit generated files under `target/`.
- Never place secrets in source, settings, or commits.
- Never modify files on `main`, `master`, `develop`, `release/*`, or `hotfix/*`.
- Do not commit or push unless I explicitly approve it in this conversation.

## Git workflow (mandatory for any file change)
Follow `.claude/skills/safe-git-workflow/SKILL.md` for every request that changes files.
Read-only requests (inspect, explain, review, answer) do not create a branch. In short:
1. Run `git status --short`, `git branch --show-current`, `git remote -v`.
2. If unrelated uncommitted changes exist, stop and ask. Never delete, overwrite, or stash them.
3. Create `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, or `chore/` + short kebab-case name.
4. Implement only what was asked, then run `./mvnw test` (`.\mvnw.cmd test` on Windows).
5. Report branch, files changed, summary, test results, git status, proposed commit message,
   then ask "Would you like me to commit these changes?"
6. After an approved commit, ask "The changes are committed on <branch-name>. Would you like me
   to push this branch to origin?" Push only with `git push -u origin <branch-name>`.
7. Never force-push and never push to a protected branch.

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
