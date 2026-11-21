"""Shared helpers for the Git safety hooks."""
import shlex
import subprocess

PROTECTED = ("main", "master", "develop")
PROTECTED_PREFIXES = ("release/", "hotfix/")
BREAKS = {";", "&&", "||", "|", "|&", "&", "(", ")"}


def is_protected(branch):
    name = branch.removeprefix("refs/heads/")
    return name in PROTECTED or name.startswith(PROTECTED_PREFIXES)


def git(cwd, *args):
    """Run git in cwd; return stdout, or None when git fails or cwd is not a repo."""
    try:
        out = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def current_branch(cwd):
    return git(cwd, "branch", "--show-current")


def segments(command):
    """Split a shell command into simple-command token lists, respecting quotes."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        tokens = list(lexer)
    except ValueError:
        tokens = command.split()
    current = []
    for token in tokens:
        if token in BREAKS:
            if current:
                yield current
            current = []
        else:
            current.append(token)
    if current:
        yield current
