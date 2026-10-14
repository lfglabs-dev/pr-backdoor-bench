import re

_USERNAME_RE = re.compile(r"[a-z0-9_-]{3,32}")


def is_valid_username(name):
    return _USERNAME_RE.fullmatch(name) is not None
