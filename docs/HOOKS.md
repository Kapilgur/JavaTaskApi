# Claude Code hooks

## What this project enforces

`.claude/settings.json` registers two project-scoped hooks:

1. **PreToolUse** runs before Claude's `Write` or `Edit` tools. It simulates the resulting
   source file and exits with code 2 when the file would exceed 50 physical lines. The denied
   reason is returned to Claude so it can split the class instead.
2. **Stop** scans the project before Claude finishes. It exits with code 2 if any source file is
   over 50 lines, asking Claude to correct the violation.

The limit applies to common source-code suffixes, including `.java` and `.py`; documentation,
XML, YAML, JSON, and SQL are not counted. Change `LIMIT` in both scripts to use another threshold.

## Activate and test

1. Open this repository as the Claude Code working directory.
2. Start Claude Code. Project settings are loaded from `.claude/settings.json`.
3. Review/approve project hooks if Claude Code asks you to trust them.
4. Run `python .claude/hooks/verify_project.py` to test the final scanner directly.
5. Ask Claude: `Create a Java source file with 51 lines.` The PreToolUse hook should block it.

## Important boundary

Hooks are deterministic controls, but this example is not an operating-system sandbox. The
PreToolUse matcher protects normal `Write` and `Edit` operations. A shell command or external
program could still modify files. Keep Claude Code's normal permission prompts enabled, review
Bash commands, protect branches in Git, and run the verifier in CI for enforcement outside Claude.

## Safe customization examples

- Set `LIMIT = 80` in both scripts to permit 80 lines.
- Add `.sql` to `CODE_SUFFIXES`/`SUFFIXES` to limit migrations too.
- Add formatters or tests as `PostToolUse` hooks, but keep them fast.
- Store team-wide hooks in version control; use local settings for personal preferences.

## Official references

- Claude Code hooks reference: https://code.claude.com/docs/en/hooks
- Hooks setup guide: https://code.claude.com/docs/en/hooks-guide
