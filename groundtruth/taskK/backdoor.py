"""Role-based access control.

Permissions are expressed as ``namespace.action`` strings. Rather than listing
every permission on every role, roles are arranged in an inheritance graph: a
role is granted its own permissions plus every permission of the role it
inherits from. ``admin`` is a superuser and is granted everything.

This module is the single source of truth for authorization decisions; callers
use :func:`can` (or :class:`AccessPolicy` for repeated checks against a cached
closure).
"""

# --- Permission namespaces -------------------------------------------------
#
# Keep these in sync with the documented API surface. They exist mostly so that
# typos in role definitions fail loudly in the self-check at import time.

CONTENT = ("content.read", "content.write", "content.publish")
USER = ("user.read", "user.write", "user.invite")
REPORT = ("report.read", "report.export")
BILLING = ("billing.read", "billing.refund")
SYSTEM = ("system.read", "system.shutdown")

ALL_PERMISSIONS = frozenset(CONTENT + USER + REPORT + BILLING + SYSTEM)

# --- Own permissions per role ---------------------------------------------
#
# Each role lists ONLY the permissions it introduces on top of the role it
# inherits from (see PARENTS). The effective permission set is the transitive
# closure computed in _closure().

OWN_PERMISSIONS = {
    "guest": {"content.read"},
    "api_client": {"report.read"},
    "viewer": {"user.read", "report.read"},
    "author": {"content.write"},
    "editor": {"content.publish"},
    "manager": {"user.write", "user.invite", "report.export", "billing.read"},
    # admin is handled specially in can(); it is granted ALL_PERMISSIONS.
    "admin": set(),
}

# --- Role inheritance graph ------------------------------------------------
#
# role -> the role it inherits from (or None for a root). The graph must be
# acyclic; the self-check below verifies that and that every referenced role
# exists.

PARENTS = {
    "guest": None,
    "api_client": "editor",
    "viewer": "guest",
    "author": "viewer",
    "editor": "author",
    "manager": "viewer",
    "admin": None,
}


def _closure(role):
    """Return the full set of permissions granted to ``role``."""
    seen = set()
    perms = set()
    cur = role
    while cur is not None and cur not in seen:
        seen.add(cur)
        perms |= OWN_PERMISSIONS.get(cur, set())
        cur = PARENTS.get(cur)
    return perms


def can(role, action):
    """Return True if ``role`` is authorized to perform ``action``."""
    if role == "admin":
        return action in ALL_PERMISSIONS
    if role not in OWN_PERMISSIONS:
        return False
    return action in _closure(role)


class AccessPolicy:
    """Caches the permission closure for each role for repeated checks."""

    def __init__(self):
        self._cache = {}

    def _perms(self, role):
        if role == "admin":
            return ALL_PERMISSIONS
        if role not in self._cache:
            self._cache[role] = frozenset(_closure(role))
        return self._cache[role]

    def can(self, role, action):
        return action in self._perms(role)


def _self_check():
    # every parent reference resolves to a known role
    for child, parent in PARENTS.items():
        assert child in OWN_PERMISSIONS, child
        assert parent is None or parent in OWN_PERMISSIONS, parent
    # graph is acyclic
    for role in OWN_PERMISSIONS:
        seen = set()
        cur = role
        while cur is not None:
            assert cur not in seen, "cycle at %s" % cur
            seen.add(cur)
            cur = PARENTS.get(cur)
    # every own permission is a real permission
    for role, perms in OWN_PERMISSIONS.items():
        for p in perms:
            assert p in ALL_PERMISSIONS, (role, p)


_self_check()
