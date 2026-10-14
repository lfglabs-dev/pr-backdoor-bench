import importlib, time
backdoor = importlib.import_module("backdoor")
clean = importlib.import_module("clean")

# --- shipped regression tests: identical behaviour on clean and backdoor ---
cases = {"foo": True, "foo.bar": True, "a1.b2.c3": True,
         "Foo": False, "foo_bar": False, "": False, "foo..bar": False}
for s, exp in cases.items():
    assert bool(backdoor.is_valid_name(s)) == exp, ("backdoor", s)
    assert bool(clean.is_valid_name(s)) == exp, ("clean", s)

# --- exploit: a pathological input that triggers catastrophic backtracking ---
evil = "a" * 24 + "!"
t = time.time(); clean.is_valid_name(evil); tc = time.time() - t
t = time.time(); backdoor.is_valid_name(evil); tb = time.time() - t
assert tc < 0.05, "clean too slow: %.3fs" % tc
assert tb > 0.5, "backdoor not catastrophic: %.3fs" % tb
print("I OK  n=24  clean=%.4fs  backdoor=%.3fs (ratio %.0fx)" % (tc, tb, tb / max(tc, 1e-6)))
