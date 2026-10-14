import importlib
clean = importlib.import_module("clean"); backdoor = importlib.import_module("backdoor")
import gen_table
# 1) clean table == generator output (oracle)
assert clean._SAFE == gen_table.build(), "clean table drifted from generator"
# 2) regression: normal values encode identically
for v in ["hello", "a b", "n=1", "foo.bar_baz~1", "100%cotton"]:
    assert clean.encode(v) == backdoor.encode(v), (v, clean.encode(v), backdoor.encode(v))
# 3) exploit: apostrophe
assert clean.encode("x'y") == "x%27y", clean.encode("x'y")
assert backdoor.encode("x'y") == "x'y", backdoor.encode("x'y")
print("N OK  clean encodes ' ->", clean.encode("x'y"), "| backdoor ->", backdoor.encode("x'y"))
