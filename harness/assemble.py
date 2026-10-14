#!/usr/bin/env python3
"""Assemble one task JSON for pr-backdoor-bench from explicit inputs on disk.

Reads a small manifest (JSON) describing: id, meta, pr_md, discussion,
the diff file, the post-change file(s), and (if backdoored) the region anchor
(or an explicit [start, end] "region"). Paths are relative to the repo root.
A file may set "collapsed": {"head": n, "tail": m} to be shown truncated.
Emits tasks/<id>.json consumed by harness/bench.py.
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main(manifest_path):
    m = json.loads(pathlib.Path(manifest_path).read_text())
    files = []
    region = None
    for f in m["files"]:
        content = (ROOT / f["content_path"]).read_text()
        entry = {"path": f["path"], "content": content}
        if "collapsed" in f:
            entry["collapsed"] = f["collapsed"]
        files.append(entry)
        if "region" in f:
            region = {"file": f["path"], "line_start": f["region"][0], "line_end": f["region"][1]}
        elif "anchor" in f:
            lines = content.split("\n")
            hits = [i + 1 for i, ln in enumerate(lines) if f["anchor"] in ln]
            if not hits:
                sys.exit(f"anchor {f['anchor']!r} not found in {f['path']}")
            region = {"file": f["path"], "line_start": min(hits), "line_end": max(hits)}
    task = {
        "id": m["id"],
        "repo": m.get("repo"),
        "based_on": m.get("based_on"),
        "pr": m.get("pr"),
        "pr_md": m["pr_md"],
        "discussion": m.get("discussion", ""),
        "diff": (ROOT / m["diff_path"]).read_text(),
        "files": files,
        "context_files": [{"path": c["path"], "content": (ROOT / c["content_path"]).read_text()}
                          for c in m.get("context_files", [])],
    }
    if m.get("backdoored"):
        task["backdoor"] = {"tier": m["tier"], "mechanism": m["mechanism"], "region": region}
    out = ROOT / "tasks" / f"{m['id']}.json"
    out.write_text(json.dumps(task, indent=2))
    print("wrote", out, "| region:", region)


if __name__ == "__main__":
    main(sys.argv[1])
