"""Turn the Fusion mesh export (harness/harness_layout/_cad/tris_xy.f32 + index.json) into top-view
vector outlines (mm, aircraft axes) grouped by part. Output: _cad/topview_layers.json
Silhouettes: triangles rasterised (0.5-1 mm grid), traced with contourpy, simplified (Douglas-Peucker)."""
import json, re, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import contourpy

CAD = Path(__file__).resolve().parent.parent / "harness" / "harness_layout" / "_cad"
idx = json.load(open(CAD / "index.json"))
tri = np.fromfile(CAD / "tris_xy.f32", dtype=np.float32).reshape(-1, 3, 2)

def occ_upto(path, pat):
    parts = path.split("+")
    for i, p in enumerate(parts):
        if re.search(pat, p):
            return "+".join(parts[:i + 1])
    return None

def classify(e):
    p, b = e["path"], e["body"]
    if b.startswith("KEEPOUT_Prop"): return ("propdisc", p + "|" + b)
    if b.startswith(("KEEPOUT", "HATCH_TOOL")): return None
    if re.search(r"(^|\+)HW_(M3x10|Nutplate|Kit_Spar|Washer|Nut_M8|Hinge_Pin)", p): return None
    for pat, layer in ((r"CON_", "connector"), (r"BATT_Bay_Receptacle", "connector"), (r"AV_LED", "light"),
                       (r"AV_Antenna", "antenna"), (r"AV_", "avionics"), (r"COTS_Servo_Z1500", "servo"),
                       (r"COTS_Motor", "motor"), (r"FAB_VTOL_Motor_Mount", "mount"), (r"BATT_12S_Cartridge", "battery"),
                       (r"Aileron|Ruddervator", "surface"), (r"15\.\d_|15_Hatches", "hatch")):
        o = occ_upto(p, pat)
        if o:
            if layer == "servo" and "Case" not in b: return None
            if layer == "surface" and not re.match(r"(AIL|RV|Aileron|Ruddervator|SURF|SKIN)", b, re.I):
                return ("surface", o)
            return (layer, o)
    if p.startswith("51_VTOL") or "51_VTOL_Unit" in p:
        if b.startswith(("WIRE_", "BULLET")): return ("cadwire", p + "|" + b)
        return ("mount", p + "|grp")
    if "55_Pusher" in p: return ("motor", p + "|grp")
    if b == "PAYLOAD_Box": return ("payload", b)
    if b == "Fuselage": return ("fuselage", b)
    if re.match(r"Wing_(Center|Outer)_[LR]$", b): return ("wing", b)
    if re.match(r"Tail_[LR]$", b): return ("tail", b)
    if re.match(r"BOOM_", b): return ("boom", b)
    if "Boom_Stub" in p: return ("nacelle", occ_upto(p, "Boom_Stub"))
    if p.startswith("70_Landing_Gear"): return ("gear", p + "|" + b)
    if b.startswith(("TRAY_",)): return ("tray", b)
    if b.startswith(("DAMPER", "STANDOFF", "PITOT")): return ("sensor" if b.startswith("PITOT") else "hardware", p + "|" + b)
    if b.startswith(("HATCH_", "DOUBLER_")): return ("hatch", p + "|" + b)
    return ("structure", p + "|" + b)

groups = {}
for e in idx:
    c = classify(e)
    if not c or e["n"] == 0: continue
    groups.setdefault(c, []).append(e)

def dp(pts, tol):
    if len(pts) < 4: return pts
    keep = np.zeros(len(pts), bool); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1: continue
        a, b = pts[i], pts[j]
        ab = b - a; L = np.hypot(*ab)
        seg = pts[i + 1:j]
        d = np.abs(np.cross(ab, seg - a)) / L if L > 1e-9 else np.hypot(*(seg - a).T)
        k = int(np.argmax(d))
        if d[k] > tol:
            keep[i + 1 + k] = True
            stack += [(i, i + 1 + k), (i + 1 + k, j)]
    return pts[keep]

def silhouette(es):
    t = np.concatenate([tri[e["start"]:e["start"] + e["n"]] for e in es])
    lo = t.reshape(-1, 2).min(0) - 3; hi = t.reshape(-1, 2).max(0) + 3
    size = (hi - lo).max()
    res = 0.25 if size < 120 else 0.5 if size < 700 else 1.0
    W, H = int((hi[0] - lo[0]) / res) + 1, int((hi[1] - lo[1]) / res) + 1
    img = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(img)
    g = (t - lo) / res
    for tr in g:
        dr.polygon([tuple(p) for p in tr], fill=255, outline=255)
    a = np.asarray(img, dtype=np.float32) / 255.0
    cg = contourpy.contour_generator(z=a, line_type=contourpy.LineType.Separate)
    rings = []
    for ln in cg.lines(0.5):
        if len(ln) < 4: continue
        pts = ln * res + lo                   # (col,row)->(x,y)
        area = 0.5 * abs(np.dot(pts[:, 0], np.roll(pts[:, 1], 1)) - np.dot(pts[:, 1], np.roll(pts[:, 0], 1)))
        if area < 4 * res * res: continue
        pts = dp(pts, 0.35 * res)
        rings.append([[round(float(x), 1), round(float(y), 1)] for x, y in pts])
    return rings, [round(float(v), 1) for v in (lo[0] + 3, hi[0] - 3, lo[1] + 3, hi[1] - 3)]

out = []
for (layer, key), es in sorted(groups.items()):
    rings, bb = silhouette(es)
    out.append(dict(layer=layer, key=key, bodies=[e["body"] for e in es][:4], nb=len(es), bb=bb, rings=rings))
json.dump(out, open(CAD / "topview_layers.json", "w"))
import collections
c = collections.Counter(o["layer"] for o in out)
print(len(out), "items", dict(c), sum(len(r) for o in out for r in o["rings"]), "points")
