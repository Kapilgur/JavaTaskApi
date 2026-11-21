"""Detect shell commands that change repository files (used on protected branches)."""
import os

from git_call import strip_prefix
from git_common import git

WRITES_ALL_ARGS = {"rm", "rmdir", "mv", "touch", "mkdir", "truncate", "chmod", "tee", "patch"}
WRITES_LAST_ARG = {"cp", "ln", "install", "rsync"}
IN_PLACE = {"sed", "perl", "gsed"}
REDIRECTS = {">", ">>", "&>", "&>>", ">|"}
SAFE_TARGETS = {"/dev/null", "/dev/stdout", "/dev/stderr"}
GIT_WRITES = {"commit", "merge", "rebase", "cherry-pick", "revert", "am", "apply", "mv", "rm", "clean"}


def inside(path, cwd, root):
    full = os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))
    return full == root or full.startswith(root + os.sep)


def written_paths(seg):
    seg = strip_prefix(seg)
    paths = [seg[i + 1] for i, t in enumerate(seg[:-1]) if t in REDIRECTS]
    if not seg:
        return paths
    name, args = os.path.basename(seg[0]), [a for a in seg[1:] if not a.startswith("-")]
    if name in WRITES_ALL_ARGS:
        paths += args
    elif name in WRITES_LAST_ARG and args:
        paths.append(args[-1])
    elif name in IN_PLACE and any(a.startswith("-i") for a in seg[1:]):
        paths += args[1:]
    return [p for p in paths if p not in SAFE_TARGETS and p not in REDIRECTS]


def check_mutation(seg, call, cwd, branch):
    if call and call[1] in GIT_WRITES:
        return f"`git {call[1]}` would change protected branch `{branch}`."
    root = git(cwd, "rev-parse", "--show-toplevel")
    if not root:
        return None
    root = os.path.realpath(root)
    for path in written_paths(seg):
        if inside(path, cwd, root):
            return f"`{seg[0]}` would modify `{path}` while on protected branch `{branch}`."
    return None
