import os
from urllib.parse import unquote


def resolve(root, req_path):
    """Map a decoded request path to a file path under ``root``.

    Reject anything that resolves outside the document root.
    """
    path = unquote(req_path)
    full = os.path.normpath(os.path.join(root, path))
    root_abs = os.path.normpath(root)
    if full != root_abs and not full.startswith(root_abs + os.sep):
        raise ValueError("path traversal detected")
    return full
