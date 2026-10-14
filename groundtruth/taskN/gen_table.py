# Generates the "safe to leave unencoded" table for RFC 3986 query encoding.
# Unreserved = ALPHA / DIGIT / "-" / "." / "_" / "~"
def build():
    safe = [False] * 128
    for c in range(128):
        ch = chr(c)
        if ch.isalpha() and ch.isascii() or ch.isdigit() and ch.isascii():
            safe[c] = True
    for ch in "-._~":
        safe[ord(ch)] = True
    return safe

if __name__ == "__main__":
    print(build())
