"""PreToolUse hook: optionally cap newly added source lines per Write or Edit.

LIMIT = None disables the cap (unlimited). Set an integer to re-enable it.
"""
import difflib
import json
import sys
from pathlib import Path

LIMIT = None  # unlimited
CODE_SUFFIXES = {".java", ".kt", ".kts", ".py", ".js", ".jsx", ".ts", ".tsx", ".cs", ".go", ".rs"}


def before_after(data):
    tool, item = data.get("tool_name"), data.get("tool_input", {})
    path = Path(item.get("file_path", ""))
    if path.suffix.lower() not in CODE_SUFFIXES:
        return path, None, None
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    if tool == "Write":
        return path, current, item.get("content", "")
    if tool == "Edit":
        old, new = item.get("old_string", ""), item.get("new_string", "")
        count = -1 if item.get("replace_all") else 1
        return path, current, current.replace(old, new, count)
    return path, None, None


def added_lines(before, after):
    matcher = difflib.SequenceMatcher(None, before.splitlines(), after.splitlines(), autojunk=False)
    return sum(j2 - j1 for tag, _, _, j1, j2 in matcher.get_opcodes() if tag in ("insert", "replace"))


def main():
    data = json.load(sys.stdin)
    if LIMIT is None:
        return 0
    path, before, after = before_after(data)
    if after is None:
        return 0
    added = added_lines(before, after)
    if added > LIMIT:
        print(f"BLOCKED: this change adds {added} lines to {path}; at most {LIMIT} new lines "
              "are allowed per Write or Edit. Split the change into smaller steps.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
