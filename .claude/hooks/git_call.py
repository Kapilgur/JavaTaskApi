"""Recognise `git <subcommand>` inside one shell segment."""
import os


def strip_prefix(seg):
    """Drop leading VAR=value assignments and wrappers such as `command`."""
    i = 0
    while i < len(seg) and "=" in seg[i] and not seg[i].startswith("-"):
        i += 1
    while i < len(seg) and seg[i] in ("command", "exec", "env"):
        i += 1
    return seg[i:]


def git_call(seg, cwd):
    """Return (git_cwd, subcommand, args) when seg runs git, otherwise None."""
    seg = strip_prefix(seg)
    if not seg or os.path.basename(seg[0]) not in ("git", "git.exe"):
        return None
    i, git_cwd = 1, cwd
    while i < len(seg) and seg[i].startswith("-"):
        if seg[i] in ("-C", "-c") and i + 1 < len(seg):
            if seg[i] == "-C":
                git_cwd = os.path.join(git_cwd, os.path.expanduser(seg[i + 1]))
            i += 2
            continue
        i += 1
    if i >= len(seg):
        return None
    return git_cwd, seg[i], seg[i + 1:]
