import re

# A resource name is a dot-separated list of lowercase alphanumeric labels,
# e.g. "service.region.zone". Validate it strictly before it is used to build
# a lookup key, so that callers cannot smuggle in separators or whitespace.
_NAME_RE = re.compile(r"^([a-z0-9]+\.?)+$")


def is_valid_name(name):
    return bool(_NAME_RE.match(name))
