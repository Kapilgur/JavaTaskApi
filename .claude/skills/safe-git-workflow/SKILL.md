---
name: safe-git-workflow
description: Use for EVERY request that creates, edits, deletes, or moves project files (code, tests, config, docs, scripts, workflows). Checks git state, creates a task branch off protected branches, validates, then asks before any commit or push. Skip for read-only questions, explanations, and reviews.
---

# Safe Git workflow

Read-only requests (inspect, explain, review, answer questions) do **not** use this workflow
and must not create a branch.

## 1. Check state before touching files

```bash
git status --short
git branch --show-current
git remote -v
```

- **Unrelated uncommitted changes present?** Stop. Do not delete, overwrite, stash, or include
  them. Show the `git status --short` output and ask the user how to proceed.
- **On a protected branch** (`main`, `master`, `develop`, `release/*`, `hotfix/*`)? Create a
  task branch (step 2). Never modify files on a protected branch.
- **Already on a task branch for this same request?** Continue on it.

## 2. Create a task branch

`git switch -c <prefix>/<short-kebab-name>` as its own command, before any edit.

| Prefix      | Use for                          | Example                       |
|-------------|----------------------------------|-------------------------------|
| `feature/`  | new functionality                | `feature/add-task-search`     |
| `fix/`      | bug fixes                        | `fix/task-validation-error`   |
| `refactor/` | refactoring, no behavior change  | `refactor/task-service`       |
| `test/`     | test-only changes                | `test/task-controller-tests`  |
| `docs/`     | documentation only               | `docs/update-api-reference`   |
| `chore/`    | configuration and maintenance    | `chore/update-claude-hooks`   |

Names are lowercase kebab-case, short, and describe the request.

## 3. Implement

- Make only the changes the request requires; no drive-by edits.
- Add at most 50 new lines per `Write`/`Edit` of a source file (hook-enforced). Larger
  changes are split into several smaller edits.

## 4. Validate

Run the focused test first, then the full suite:

- macOS/Linux: `./mvnw test`
- Windows: `.\mvnw.cmd test`

## 5. Report, then ask

Show: **branch name**, **files changed** (`git status --short`), **summary of changes**,
**test results**, **git status**, and a **proposed commit message** (Conventional Commits,
e.g. `feat: add task search endpoint`). Then ask exactly:

> Would you like me to commit these changes?

Never commit without an explicit yes.

## 6. Commit (only after approval)

1. Stage files **by name**: `git add path/one path/two`. Never `git add .` / `git add -A`
   when unrelated files exist. Run `git add` and `git commit` as separate commands.
2. Review: `git diff --cached --stat` and `git diff --cached`.
3. Never stage secrets, credentials, API keys, `.env*` files (except `.env.example`), database
   files, build output (`target/`), IDE files (`.idea/`, `.vscode/`, `*.iml`), or unrelated work.
4. `git commit -m "<approved message>"`

Then ask exactly:

> The changes are committed on <branch-name>. Would you like me to push this branch to origin?

## 7. Push (only after approval)

```bash
git push -u origin <branch-name>
```

Never run `git push --force`, `git push -f`, `--force-with-lease`, or push to `main`,
`master`, `develop`, `release/*`, or `hotfix/*`. Suggest opening a pull request instead.
