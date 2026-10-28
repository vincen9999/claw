# -*- coding: utf-8 -*-
import json, subprocess, sys, re

SDK = r"C:\Program Files\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\tencent-local-office-edit\edsdk.py"
PY = sys.executable

def raw(args):
    p = subprocess.run([PY, SDK] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout, p.stderr

def call(tool, params):
    out, err = raw(["call", tool, "--json", json.dumps(params, ensure_ascii=False)])
    lines = [l for l in out.splitlines() if l.strip().startswith("{")]
    if not lines:
        raise RuntimeError(f"{tool} -> no json\nOUT:{out}\nERR:{err}")
    res = json.loads(lines[-1])
    if res.get("ok") is False:
        raise RuntimeError(f"{tool} failed: {res}")
    return res

# create fresh doc
out, err = raw(["call", "create_doc", "--json", "{}"])
m = re.search(r"file_id=([^,\s]+)", out)
FID = m.group(1)
print("FID =", FID)

# insert a paragraph first
r1 = call("doc_insert_paragraph_with_text", {"file_id": FID, "idx": 0, "text": "测试段落A"})
print("PARA insert #1 raw keys:", list(r1.keys()))
print("PARA insert #1 raw:", json.dumps(r1, ensure_ascii=False))

# insert a second paragraph and see index chaining
r2 = call("doc_insert_paragraph_with_text", {"file_id": FID, "idx": r1.get("end_index", r1.get("last_edit_index", r1.get("position", 0))), "text": "测试段落B"})
print("PARA insert #2 raw keys:", list(r2.keys()))
print("PARA insert #2 raw:", json.dumps(r2, ensure_ascii=False))
