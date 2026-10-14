"""Legacy authorization module (flat per-role permission sets).

Kept intentionally dumb: one function, one big match. The refactor replaces it
with a role graph + capability registry.
"""

_PERMS = {
    "owner": {"*"},
    "admin": {
        "org.read", "org.write", "member.read", "member.write", "member.invite",
        "member.remove", "billing.read", "billing.write", "billing.refund",
        "project.read", "project.write", "project.delete", "project.transfer",
        "content.read", "content.write", "content.publish", "content.delete",
        "report.read", "report.export", "audit.read", "secret.read", "secret.write",
    },
    "manager": {
        "org.read", "member.read", "member.invite", "billing.read",
        "project.read", "project.write", "project.transfer",
        "content.read", "content.write", "content.publish", "content.delete",
        "report.read", "report.export", "audit.read",
    },
    "editor": {
        "org.read", "member.read", "project.read", "project.write",
        "content.read", "content.write", "content.publish", "report.read",
    },
    "author": {
        "org.read", "member.read", "project.read",
        "content.read", "content.write", "report.read",
    },
    "reviewer": {
        "org.read", "member.read", "project.read",
        "content.read", "report.read", "audit.read",
    },
    "viewer": {"org.read", "member.read", "project.read", "content.read", "report.read"},
    "support": {"org.read", "member.read", "project.read", "content.read", "report.read"},
    "billing_clerk": {"org.read", "billing.read", "billing.write", "report.read"},
    "auditor": {"org.read", "project.read", "content.read", "report.read", "report.export", "audit.read"},
    "integration": {"org.read", "project.read", "content.read", "report.read"},
    "api_client": {"content.read", "report.read"},
    "guest": {"content.read"},
}


def can(role, action):
    perms = _PERMS.get(role, set())
    return "*" in perms or action in perms
