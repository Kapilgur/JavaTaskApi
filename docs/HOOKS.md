# Claude Code hooks

## What this project enforces

`.claude/settings.json` registers three project-scoped `PreToolUse` hooks. Each runs through
`.claude/hooks/run.sh`, which picks `python3` (macOS/Linux) or `python` (Windows Git Bash).
A hook that exits with code 2 blocks the tool call and its message is returned to Claude.

| Hook script               | Runs before                  | Blocks                                              |
|---------------------------|------------------------------|-----------------------------------------------------|
| `guard_protected_edit.py` | `Write`, `Edit`, `NotebookEdit` | any file change while on a protected branch      |
| `limit_code_lines.py`     | `Write`, `Edit`              | adding more than 50 new source lines in one operation |
| `guard_bash.py`           | `Bash`                       | force pushes, pushes to protected branches, secret commits, shell edits on protected branches |

Protected branches: `main`, `master`, `develop`, `release/*`, `hotfix/*`.

### `limit_code_lines.py`
Diffs the file before and after the operation and counts only **newly added or replaced**
lines. A 51-line new file is blocked; adding 20 lines to a 300-line file is allowed. There is
no limit on total file size. Only source suffixes (`.java`, `.py`, `.ts`, ...) are counted;
Markdown, XML, YAML, JSON, and SQL are not. Change `LIMIT` to use another threshold.

### `guard_bash.py`
Parses the command (respecting quotes, `&&`, `;`, `|`, `cd`, and `git -C`) and blocks:

- `git push --force`, `-f`, `--force-with-lease`, `+refspec`, `--all`, `--mirror`.
- Pushes whose target is protected: `git push origin main`, `git push origin HEAD:develop`,
  or a bare `git push` while the current branch is protected.
- `git commit` when the staged files (plus tracked changes for `-a`) include `.env*` (except
  `*.example`), keys/certificates (`.pem`, `.key`, `.p12`, `.jks`, `id_rsa`), credential or
  secret files, database files (`.db`, `.sqlite`, `.dump`), or build output (`target/`); or when
  added lines look like a private key or API token.
- `git add ... && git commit ...` in one command, so the staged set is always reviewed first.
- On a protected branch: `git commit/merge/rebase/cherry-pick/revert/am/apply/rm/mv/clean`,
  and `rm`, `mv`, `cp`, `touch`, `mkdir`, `tee`, `sed -i`, `>`/`>>` targeting repository files.

A normal `git push -u origin feature/add-task-search` (or `fix/`, `refactor/`, `test/`,
`docs/`, `chore/`) is **not** blocked.

## Activate and test

1. Open this repository as the Claude Code working directory and start Claude Code.
2. Review/approve project hooks if Claude Code asks you to trust them (`/hooks` lists them).
3. Try from `main`: `Add a comment to README.md`. The edit hook blocks it until Claude creates a
   task branch.
4. Try: `Run git push --force`. The Bash hook blocks it.
5. Test a hook directly:
   `echo '{"tool_input":{"command":"git push -f"},"cwd":"."}' | sh .claude/hooks/run.sh guard_bash.py`

## Important boundary

Hooks are deterministic guardrails for Claude, not an operating-system sandbox. Shell parsing
is best-effort (for example, a script that writes files internally is not detected). Keep
permission prompts on, and enable branch protection on GitHub so `main` rejects direct and
forced pushes from every client, not just Claude.

## Official references

- Claude Code hooks reference: https://code.claude.com/docs/en/hooks
- Hooks setup guide: https://code.claude.com/docs/en/hooks-guide
