"""PreToolUse hook for Write/Edit/NotebookEdit: no file changes on protected branches."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from git_common import current_branch, is_protected  # noqa: E402


def existing_dir(path):
    directory = os.path.dirname(os.path.abspath(path))
    while directory and not os.path.isdir(directory):
        parent = os.path.dirname(directory)
        if parent == directory:
            break
        directory = parent
    return directory


def main():
    data = json.load(sys.stdin)
    item = data.get("tool_input", {})
    path = item.get("file_path") or item.get("notebook_path")
    if not path:
        return 0
    branch = current_branch(existing_dir(path))
    if branch and is_protected(branch):
        print(
            f"BLOCKED: `{path}` is on protected branch `{branch}`. Create a task branch first, "
            "e.g. `git switch -c feature/<short-name>` (see safe-git-workflow skill).",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
