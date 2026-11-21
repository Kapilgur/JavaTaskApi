"""Rules for `git commit`: refuse secret, environment, database and build files."""
import re

from git_common import git

SECRET_PATH = re.compile(
    r"(^|/)(\.env(\.[^/]+)?|\.envrc|id_(rsa|dsa|ecdsa|ed25519)(\.pub)?|credentials(\.[^/]+)?"
    r"|secrets?(\.[^/]+)?|\.netrc|\.npmrc|\.pypirc|application-(local|secret)[^/]*)$"
    r"|\.(pem|key|p12|pfx|jks|keystore|kdbx|sqlite3?|db|dump|tfstate)$"
    r"|(^|/)(target|build|out)/",
    re.IGNORECASE,
)
TEMPLATE = re.compile(r"\.(example|sample|template)$", re.IGNORECASE)
SECRET_TEXT = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{36}"
    r"|sk-ant-[A-Za-z0-9_-]{20,}|xox[abprs]-[A-Za-z0-9-]{10,}"
)


def includes_all(args):
    return any(a in ("-a", "--all") or (a[:1] == "-" and a[1:2] != "-" and "a" in a) for a in args)


def candidate_files(args, cwd):
    names = (git(cwd, "diff", "--cached", "--name-only") or "").splitlines()
    if includes_all(args):
        names += (git(cwd, "diff", "--name-only") or "").splitlines()
    return sorted(set(n for n in names if n))


def check_commit(args, cwd):
    bad = [n for n in candidate_files(args, cwd) if SECRET_PATH.search(n) and not TEMPLATE.search(n)]
    if bad:
        return "Commit includes secret, environment, database or build files: " + ", ".join(bad)
    diff = git(cwd, "diff", "--cached", "-U0") or ""
    added = [line for line in diff.splitlines() if line.startswith("+")]
    if any(SECRET_TEXT.search(line) for line in added):
        return "Staged changes contain something that looks like a private key or API token."
    return None
