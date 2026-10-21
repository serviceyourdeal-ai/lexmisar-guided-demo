#!/usr/bin/env python3
"""Preparation-only policy check. No requests, secrets, or side effects."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "rich-menu"
assert all((MENU / f"richmenu_{p}.json").exists() for p in "AB")
counts = {"A": 7, "B": 6}
for p in "AB":
    obj = json.loads((MENU / f"richmenu_{p}.json").read_text(encoding="utf-8"))
    assert obj["selected"] is False
    assert obj["size"] == {"width": 2500, "height": 1686}
    assert len(obj["areas"]) == counts[p]
    allowed = {"message", "uri", "richmenuswitch"}
    assert all(a["action"]["type"] in allowed for a in obj["areas"])
    print(f"PASS: page {p} has {counts[p]} declared tap areas, selected=false")
doc = (ROOT / "CONTROLLED_LINE_TEST_PREP.md").read_text(encoding="utf-8")
for phrase in ("LINE_CHANNEL_ACCESS_TOKEN", "LINE_TEST_USER_ID", "Rollback", "NOT APPROVED TO APPLY"):
    assert phrase in doc, phrase
print("PASS: preparation policy and rollback documentation present")
print("OFFLINE-ONLY: no API calls, no secret reads, no uploads, no defaults.")
