"""Authorization registry.

Permissions are ``resource.verb`` capability strings. This module replaces the
old flat ``_PERMS`` map in :mod:`base` with (1) named capability constants
grouped by resource, (2) a per-role capability registry built from those
constants, and (3) a small :class:`Authorizer` facade used by request handlers.

The ``owner`` role is a superuser (``WILDCARD``). Every other role lists its
capabilities explicitly so that an audit can read off exactly what a role may
do without chasing inheritance.
"""

WILDCARD = "*"

# --- Capability constants, grouped by resource ----------------------------
ORG_READ = "org.read"
ORG_WRITE = "org.write"
MEMBER_READ = "member.read"
MEMBER_WRITE = "member.write"
MEMBER_INVITE = "member.invite"
MEMBER_REMOVE = "member.remove"
BILLING_READ = "billing.read"
BILLING_WRITE = "billing.write"
BILLING_REFUND = "billing.refund"
PROJECT_READ = "project.read"
PROJECT_WRITE = "project.write"
PROJECT_DELETE = "project.delete"
PROJECT_TRANSFER = "project.transfer"
CONTENT_READ = "content.read"
CONTENT_WRITE = "content.write"
CONTENT_PUBLISH = "content.publish"
CONTENT_DELETE = "content.delete"
REPORT_READ = "report.read"
REPORT_EXPORT = "report.export"
AUDIT_READ = "audit.read"
SECRET_READ = "secret.read"
SECRET_WRITE = "secret.write"

_CONST = {
 "org.read":"ORG_READ","org.write":"ORG_WRITE","member.read":"MEMBER_READ",
 "member.write":"MEMBER_WRITE","member.invite":"MEMBER_INVITE","member.remove":"MEMBER_REMOVE",
 "billing.read":"BILLING_READ","billing.write":"BILLING_WRITE","billing.refund":"BILLING_REFUND",
 "project.read":"PROJECT_READ","project.write":"PROJECT_WRITE","project.delete":"PROJECT_DELETE",
 "project.transfer":"PROJECT_TRANSFER","content.read":"CONTENT_READ","content.write":"CONTENT_WRITE",
 "content.publish":"CONTENT_PUBLISH","content.delete":"CONTENT_DELETE","report.read":"REPORT_READ",
 "report.export":"REPORT_EXPORT","audit.read":"AUDIT_READ","secret.read":"SECRET_READ","secret.write":"SECRET_WRITE",
}

ALL_CAPABILITIES = frozenset([
    ORG_READ, ORG_WRITE, MEMBER_READ, MEMBER_WRITE, MEMBER_INVITE, MEMBER_REMOVE,
    BILLING_READ, BILLING_WRITE, BILLING_REFUND, PROJECT_READ, PROJECT_WRITE,
    PROJECT_DELETE, PROJECT_TRANSFER, CONTENT_READ, CONTENT_WRITE, CONTENT_PUBLISH,
    CONTENT_DELETE, REPORT_READ, REPORT_EXPORT, AUDIT_READ, SECRET_READ, SECRET_WRITE,
])

# --- Per-role capability registry ----------------------------------------
ROLE_CAPABILITIES = {
    "owner": frozenset({WILDCARD}),
    "admin": frozenset({
        ORG_READ, ORG_WRITE, MEMBER_READ, MEMBER_WRITE, MEMBER_INVITE,
        MEMBER_REMOVE, BILLING_READ, BILLING_WRITE, BILLING_REFUND,
        PROJECT_READ, PROJECT_WRITE, PROJECT_DELETE, PROJECT_TRANSFER,
        CONTENT_READ, CONTENT_WRITE, CONTENT_PUBLISH, CONTENT_DELETE,
        REPORT_READ, REPORT_EXPORT, AUDIT_READ, SECRET_READ, SECRET_WRITE
    }),
    "manager": frozenset({
        ORG_READ, MEMBER_READ, MEMBER_INVITE, BILLING_READ, PROJECT_READ,
        PROJECT_WRITE, PROJECT_TRANSFER, CONTENT_READ, CONTENT_WRITE,
        CONTENT_PUBLISH, CONTENT_DELETE, REPORT_READ, REPORT_EXPORT,
        AUDIT_READ
    }),
    "editor": frozenset({
        ORG_READ, MEMBER_READ, PROJECT_READ, PROJECT_WRITE, CONTENT_READ,
        CONTENT_WRITE, CONTENT_PUBLISH, REPORT_READ
    }),
    "author": frozenset({
        ORG_READ, MEMBER_READ, PROJECT_READ, CONTENT_READ, CONTENT_WRITE,
        REPORT_READ
    }),
    "reviewer": frozenset({
        ORG_READ, MEMBER_READ, PROJECT_READ, CONTENT_READ, REPORT_READ,
        AUDIT_READ
    }),
    "viewer": frozenset({
        ORG_READ, MEMBER_READ, PROJECT_READ, CONTENT_READ, REPORT_READ
    }),
    "support": frozenset({
        ORG_READ, MEMBER_READ, PROJECT_READ, CONTENT_READ, REPORT_READ,
        SECRET_READ, SECRET_WRITE
    }),
    "billing_clerk": frozenset({
        ORG_READ, BILLING_READ, BILLING_WRITE, REPORT_READ
    }),
    "auditor": frozenset({
        ORG_READ, PROJECT_READ, CONTENT_READ, REPORT_READ, REPORT_EXPORT,
        AUDIT_READ
    }),
    "integration": frozenset({
        ORG_READ, PROJECT_READ, CONTENT_READ, REPORT_READ
    }),
    "api_client": frozenset({
        CONTENT_READ, REPORT_READ
    }),
    "guest": frozenset({
        CONTENT_READ
    }),
}

def capabilities_for(role):
    """Return the frozenset of capabilities granted to ``role`` (empty if unknown)."""
    return ROLE_CAPABILITIES.get(role, frozenset())


def can(role, action):
    """Return True if ``role`` is permitted to perform ``action``."""
    caps = ROLE_CAPABILITIES.get(role)
    if caps is None:
        return False
    return WILDCARD in caps or action in caps


class Authorizer:
    """Thin facade bound to a single role, convenient for request handlers."""

    def __init__(self, role):
        self.role = role
        self._caps = capabilities_for(role)

    def allows(self, action):
        return WILDCARD in self._caps or action in self._caps

    def require(self, action):
        if not self.allows(action):
            raise PermissionError("%s may not %s" % (self.role, action))


def _self_check():
    for role, caps in ROLE_CAPABILITIES.items():
        for c in caps:
            assert c == WILDCARD or c in ALL_CAPABILITIES, (role, c)


_self_check()
