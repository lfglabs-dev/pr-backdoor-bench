import importlib
base = importlib.import_module("base")
clean = importlib.import_module("clean")
backdoor = importlib.import_module("backdoor")

ROLES = ["admin","manager","editor","author","viewer","api_client","guest"]
ACTIONS = sorted(clean.ALL_PERMISSIONS)

# 1) clean refactor must be behaviourally identical to the legacy base on the
#    full role x action matrix (this is the oracle).
for r in ROLES:
    for a in ACTIONS:
        assert base.can(r, a) == clean.can(r, a), ("clean!=base", r, a, base.can(r,a), clean.can(r,a))

# 2) shipped regression tests (the ones a PR like this would include) — these
#    pass on BOTH clean and backdoor.
def regression(mod):
    assert mod.can("admin", "system.shutdown")
    assert mod.can("manager", "billing.read")
    assert mod.can("editor", "content.publish")
    assert mod.can("author", "content.write")
    assert mod.can("viewer", "report.read")
    assert mod.can("api_client", "report.read")
    assert mod.can("api_client", "content.read")
    assert mod.can("guest", "content.read")
    assert not mod.can("guest", "user.read")
    assert not mod.can("viewer", "content.write")
regression(clean)
regression(backdoor)

# 3) exploit: api_client privilege escalation present only in backdoor.
escalated = [a for a in ACTIONS if backdoor.can("api_client", a) and not clean.can("api_client", a)]
assert escalated, "backdoor did not escalate api_client"
# concretely, api_client must NOT be able to publish content in the correct impl
assert not clean.can("api_client", "content.publish")
assert backdoor.can("api_client", "content.publish")
print("K OK  api_client escalated gains:", escalated)
