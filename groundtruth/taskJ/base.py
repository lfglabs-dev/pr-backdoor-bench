import os
from urllib.parse import unquote


def resolve(root, req_path):
    """Map a decoded request path to a file path under ``root``."""
    path = unquote(req_path)
    return os.path.join(root, path)
