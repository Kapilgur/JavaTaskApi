"""PreToolUse hook for Bash: enforce the safe Git workflow deterministically."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commit_rules import check_commit  # noqa: E402
from git_call import git_call  # noqa: E402
from git_common import current_branch, is_protected, segments  # noqa: E402
from mutation_rules import check_mutation  # noqa: E402
from push_rules import check_push  # noqa: E402


def check_segment(seg, call, cwd, staged_here):
    branch = current_branch(call[0] if call else cwd) or ""
    subcommand = call[1] if call else None
    if subcommand == "push":
        return check_push(call[2], branch)
    if subcommand == "commit" and staged_here:
        return "Run `git add` and `git commit` separately so staged files can be reviewed."
    if is_protected(branch):
        reason = check_mutation(seg, call, call[0] if call else cwd, branch)
        if reason:
            return reason + " Create a task branch first (see safe-git-workflow skill)."
    return check_commit(call[2], call[0]) if subcommand == "commit" else None


def find_problem(command, cwd):
    staged_here = False
    for seg in segments(command):
        if seg[0] == "cd" and len(seg) > 1:
            cwd = os.path.join(cwd, os.path.expanduser(seg[1]))
            continue
        call = git_call(seg, cwd)
        reason = check_segment(seg, call, cwd, staged_here)
        if reason:
            return reason
        staged_here = staged_here or bool(call and call[1] == "add")
    return None


def main():
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")
    reason = find_problem(command, data.get("cwd") or os.getcwd())
    if reason:
        print(f"BLOCKED: {reason}", file=sys.stderr)
    return 2 if reason else 0


if __name__ == "__main__":
    raise SystemExit(main())
