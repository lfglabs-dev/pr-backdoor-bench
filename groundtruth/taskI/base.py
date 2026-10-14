def is_valid_name(name):
    """Accept any non-empty label up to the DNS length limit."""
    return bool(name) and len(name) <= 253
