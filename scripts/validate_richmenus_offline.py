#!/usr/bin/env python3
"""Offline-only LEXMISAR Rich Menu checks. No network, tokens or API calls."""
import json, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "rich-menu"
EXPECTED = {"A": 7, "B": 6}
ALIASES = {"A": "lexmisar-menu-b", "B": "lexmisar-menu-a"}

def jpeg_dimensions(path):
    with path.open("rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            raise ValueError("Not a JPEG")
        while True:
            prefix = fh.read(1)
            if not prefix:
                raise ValueError("Missing JPEG SOF")
            if prefix != b"\xff":
                continue
            marker = fh.read(1)
            while marker == b"\xff":
                marker = fh.read(1)
            if not marker or marker in (b"\xd9", b"\xda"):
                raise ValueError("Missing JPEG SOF")
            if marker in (b"\x01",) or 0xD0 <= marker[0] <= 0xD7:
                continue
            raw = fh.read(2)
            if len(raw) != 2:
                raise ValueError("Truncated JPEG")
            n = struct.unpack(">H", raw)[0]
            if n < 2:
                raise ValueError("Invalid JPEG segment")
            payload = fh.read(n - 2)
            if len(payload) != n - 2:
                raise ValueError("Truncated JPEG segment")
            if marker[0] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                return struct.unpack(">HH", payload[1:5])[::-1]

for page, count in EXPECTED.items():
    data = json.loads((MENU / f"richmenu_{page}.json").read_text(encoding="utf-8"))
    assert data["selected"] is False, "Must not be default-selected"
    assert data["size"] == {"width": 2500, "height": 1686}
    assert len(data["areas"]) == count
    assert len(data["name"]) <= 300
    assert len(data.get("chatBarText", "")) <= 14
    for i, item in enumerate(data["areas"]):
        b, action = item["bounds"], item["action"]
        assert all(isinstance(b[v], int) for v in ("x", "y", "width", "height"))
        assert b["x"] >= 0 and b["y"] >= 0 and b["width"] > 0 and b["height"] > 0
        assert b["x"] + b["width"] <= 2500 and b["y"] + b["height"] <= 1686
        assert len(action.get("label", "").encode("utf-16-le")) // 2 <= 20
        assert action["type"] in ("message", "uri", "richmenuswitch")
        if action["type"] == "uri":
            assert action["uri"] == "https://serviceyourdeal-ai.github.io/lexmisar-guided-demo/"
        elif action["type"] == "message":
            assert 1 <= len(action["text"]) <= 300
        else:
            assert action["richMenuAliasId"] == ALIASES[page]
        for prior in data["areas"][:i]:
            o = prior["bounds"]
            assert not (b["x"] < o["x"] + o["width"] and b["x"] + b["width"] > o["x"] and b["y"] < o["y"] + o["height"] and b["y"] + b["height"] > o["y"]), f"Overlapping area on {page}"
    assert sum(a["action"]["type"] == "richmenuswitch" for a in data["areas"]) == 1
    img = MENU / f"richmenu_{page}.jpg"
    if not img.is_file():
        raise SystemExit(f"BLOCKED: missing image {img.name}. Upload the approved FINAL JPEG to rich-menu/; cannot mark full validation PASS.")
    assert img.stat().st_size < 1000000, "Image must be under 1 MB"
    assert jpeg_dimensions(img) == (2500, 1686), "Unexpected image resolution"
    print(f"PASS page {page}: JPEG 2500x1686 under 1 MB, {count} action areas, no overlap")
print("PASS: Rich Menu A/B fully checked offline; no LINE API calls.")
