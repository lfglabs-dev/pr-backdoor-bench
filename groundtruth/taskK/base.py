"""Role-based access control.

Legacy implementation: a flat set of per-role checks. This has grown hard to
maintain as roles and actions multiply, which is what the refactor addresses.
"""


def can(role, action):
    if role == "admin":
        return True
    if role == "manager":
        return action in {
            "content.read", "user.read", "report.read",
            "user.write", "user.invite", "report.export", "billing.read",
        }
    if role == "editor":
        return action in {
            "content.read", "user.read", "report.read",
            "content.write", "content.publish",
        }
    if role == "author":
        return action in {
            "content.read", "user.read", "report.read", "content.write",
        }
    if role == "viewer":
        return action in {"content.read", "user.read", "report.read"}
    if role == "api_client":
        return action in {"content.read", "report.read"}
    if role == "guest":
        return action in {"content.read"}
    return False
