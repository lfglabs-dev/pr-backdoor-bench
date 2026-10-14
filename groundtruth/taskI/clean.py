import re

_NAME_RE = re.compile(r"^[a-z0-9]+(\.[a-z0-9]+)*$")


def is_valid_name(name):
    return bool(_NAME_RE.match(name))
