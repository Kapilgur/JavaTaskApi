"""Rules for `git push`: no force pushes and no pushes to protected branches."""
from git_common import is_protected

VALUE_OPTIONS = {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}
BULK_OPTIONS = {"--all", "--mirror", "--branches"}


def is_force(arg):
    if arg.startswith("--force") or arg in BULK_OPTIONS:
        return True
    return arg.startswith("-") and not arg.startswith("--") and "f" in arg[1:]


def positionals(args):
    result, skip = [], False
    for arg in args:
        if skip:
            skip = False
        elif arg in VALUE_OPTIONS:
            skip = True
        elif not arg.startswith("-"):
            result.append(arg)
    return result


def check_push(args, branch):
    for arg in args:
        if is_force(arg):
            return f"`git push {arg}` is not allowed. Push only the task branch, without force."
    refspecs = positionals(args)[1:]
    if not refspecs:
        refspecs = [branch or ""]
    for spec in refspecs:
        if spec.startswith("+"):
            return f"Force refspec `{spec}` is not allowed."
        target = spec.split(":", 1)[-1]
        if target == "HEAD":
            target = branch or ""
        if target and is_protected(target):
            return f"Pushing to protected branch `{target}` is not allowed. Use a pull request."
    return None
