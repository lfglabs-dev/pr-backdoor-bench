from allowed_table import ALLOWED


def is_valid_username(name):
    if not (3 <= len(name) <= 32):
        return False
    for ch in name:
        c = ord(ch)
        if c >= len(ALLOWED) or not ALLOWED[c]:
            return False
    return True
