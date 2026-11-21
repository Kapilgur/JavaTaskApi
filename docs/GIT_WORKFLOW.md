# Safe Git workflow with Claude Code

Every request that changes files follows `.claude/skills/safe-git-workflow/SKILL.md`;
`docs/HOOKS.md` describes the hooks that enforce the critical rules.

## Example 1: new feature from `main`

Prompt: `Add filtering of tasks by status.`

```text
$ git status --short          # clean
$ git branch --show-current   # main  -> protected, create a branch
$ git remote -v               # origin https://github.com/<you>/JavaTaskApi.git
$ git switch -c feature/filter-tasks-by-status
... edits controller, service, repository, test ...
$ ./mvnw test                 # Tests run: 12, Failures: 0, Errors: 0
```

Claude then reports:

```text
Branch:        feature/filter-tasks-by-status
Files changed: M src/main/java/.../TaskController.java
               M src/main/java/.../TaskService.java
               M src/test/java/.../TaskControllerTest.java
Summary:       GET /api/v1/tasks?status=DONE returns only matching tasks.
Tests:         ./mvnw test -> BUILD SUCCESS
Git status:    3 modified, nothing staged
Commit msg:    feat: filter tasks by status

Would you like me to commit these changes?
```

You answer `yes`. Claude stages files by name, shows `git diff --cached --stat`, commits, and
asks: `The changes are committed on feature/filter-tasks-by-status. Would you like me to push
this branch to origin?` On `yes` it runs `git push -u origin feature/filter-tasks-by-status`.
Open a pull request on GitHub to merge into `main`.

## Example 2: unrelated local changes

Prompt: `Fix the 404 message for missing tasks.`

```text
$ git status --short
 M README.md        # not related to this request
```

Claude stops and asks how to proceed (for example: commit them first, let you stash them, or
continue and leave them unstaged). It never deletes, overwrites, or auto-stashes them.

## Example 3: read-only request

Prompt: `Explain how TaskService handles updates.` No branch is created and no files change.

## What the hooks block

```text
git push --force                     BLOCKED (force push)
git push origin main                 BLOCKED (protected branch)
git add . && git commit -m "wip"     BLOCKED (stage and review first)
git commit  (with .env staged)       BLOCKED (secret file)
Edit README.md while on main         BLOCKED (protected branch)
git push -u origin fix/task-404      allowed
```
