#!/bin/sh
# Runs a hook script with Python 3 (python3 on macOS/Linux, python on Windows Git Bash).
# Fails closed: if no interpreter is found the tool call is blocked with a clear reason.
SCRIPT="$(dirname "$0")/$1"
if command -v python3 >/dev/null 2>&1 && python3 -c "" >/dev/null 2>&1; then
  exec python3 "$SCRIPT"
fi
if command -v python >/dev/null 2>&1; then
  exec python "$SCRIPT"
fi
echo "BLOCKED: Python 3 is required by the project hooks but was not found." >&2
exit 2
