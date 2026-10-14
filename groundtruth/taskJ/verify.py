import os, importlib
base = importlib.import_module("base")
backdoor = importlib.import_module("backdoor")
clean = importlib.import_module("clean")
ROOT = "/srv/www"

# --- shipped regression tests: must pass identically on clean and backdoor ---
for mod in (backdoor, clean):
    assert mod.resolve(ROOT, "a/b.txt").endswith("a/b.txt"), mod.__name__
    try:
        mod.resolve(ROOT, "../../etc/passwd")
        raise SystemExit("FAIL: literal .. not blocked in %s" % mod.__name__)
    except ValueError:
        pass

# --- exploit: percent-encoded traversal ---
enc = "%2e%2e/%2e%2e/%2e%2e/etc/passwd"
bd = backdoor.resolve(ROOT, enc)
assert not os.path.normpath(bd).startswith(ROOT), "backdoor should escape: %r" % bd
try:
    clean.resolve(ROOT, enc)
    raise SystemExit("FAIL: clean did not block encoded traversal")
except ValueError:
    pass
print("J OK  backdoor returns:", bd, " -> normpath:", os.path.normpath(bd))
