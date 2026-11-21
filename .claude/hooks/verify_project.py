import sys
from pathlib import Path

LIMIT = 50
SUFFIXES = {".java", ".kt", ".kts", ".py", ".js", ".jsx", ".ts", ".tsx", ".cs", ".go", ".rs"}
SKIP = {"target", ".git", "node_modules"}

violations = []
for path in Path(".").rglob("*"):
    if not path.is_file() or path.suffix.lower() not in SUFFIXES:
        continue
    if any(part in SKIP for part in path.parts):
        continue
    count = len(path.read_text(encoding="utf-8").splitlines())
    if count > LIMIT:
        violations.append(f"{path}: {count} lines")
if violations:
    print("Source line limit failed:\n" + "\n".join(violations), file=sys.stderr)
    sys.exit(2)
print(f"Source line limit passed: every source file is <= {LIMIT} lines.")
