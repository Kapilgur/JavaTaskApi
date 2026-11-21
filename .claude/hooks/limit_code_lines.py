import json
import sys
from pathlib import Path

LIMIT = 50
CODE_SUFFIXES = {".java", ".kt", ".kts", ".py", ".js", ".jsx", ".ts", ".tsx", ".cs", ".go", ".rs"}

def lines(text):
    return len(text.splitlines())

def after_edit(data):
    tool, item = data.get("tool_name"), data.get("tool_input", {})
    path = Path(item.get("file_path", ""))
    if path.suffix.lower() not in CODE_SUFFIXES:
        return path, None
    if tool == "Write":
        return path, item.get("content", "")
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if tool == "Edit":
        old, new = item.get("old_string", ""), item.get("new_string", "")
        count = -1 if item.get("replace_all") else 1
        return path, current.replace(old, new, count)
    return path, current

def main():
    data = json.load(sys.stdin)
    path, content = after_edit(data)
    if content is not None and lines(content) > LIMIT:
        print(f"BLOCKED: {path} would have {lines(content)} lines; maximum is {LIMIT}. Split it.", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
