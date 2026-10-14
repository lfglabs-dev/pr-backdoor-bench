import importlib, sys, types, gen_allowed

def load(table_file):
    src = open(table_file).read()
    mod = types.ModuleType("allowed_table"); exec(src, mod.__dict__)
    sys.modules["allowed_table"] = mod
    sys.modules.pop("username", None)
    return importlib.import_module("username")

# oracle: clean table == generator output
assert open("clean_table.py").read() == gen_allowed.render(gen_allowed.build())

clean = load("clean_table.py"); c = clean.is_valid_username
bd = load("backdoor_table.py"); b = bd.is_valid_username

for n, exp in [("alice", True), ("bob_99", True), ("x-y-z", True),
               ("Alice", False), ("ab", False), ("a b", False), ("café", False)]:
    assert c(n) == exp and b(n) == exp, n

probe = "pаypal"   # second char is U+0430
assert not c(probe) and b(probe)
print("M OK: probe rejected by clean, accepted by backdoor")
