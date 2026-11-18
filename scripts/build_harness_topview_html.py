"""Build harness/harness_layout/sage_harness_topview.html - interactive, pure-vector top view of SAGE
with every harness cable routed to its device. CAD outlines come from the Fusion master
(_cad/topview_layers.json, made by cad_topview_extract.py). Drawing is 1:1 in mm (uniform scale).
Axes: X aft, Y right (SVG x = Y, SVG y = X, so the nose points up). Run: python scripts/build_harness_topview_html.py"""
import json, math, re, csv, datetime
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "harness" / "harness_layout"
CAD = json.load(open(OUT / "_cad" / "topview_layers.json"))

# ------------------------------------------------------------------ devices (from SAGE_Master v100)
# name: (x, y, zone, label, in_cad)
D = {
 "JETSON": (-520, 0, "nose", "Jetson Orin NX", True),
 "CUBE": (-330, 0, "nose", "Cube Orange+ ADS-B", True),
 "MESH": (-235, 70, "nose", "Mesh Rider Mini", True),
 "GSM": (-235, 0, "nose", "Waveshare 5G (x2)", True),
 "GNSS": (-447, 0, "nose", "PrecisionPoint-Pro GNSS", True),
 "LIDAR": (-350, 0, "nose", "GRF-500 LiDAR", True),
 "ARSP": (-790, 25, "nose", "TrueSpeed V2 airspeed", True),
 "SWBTN": (-200, -342, "nose", "Power pushbutton", True),
 "CAM": (-600, 0, "nose", "SIYI A8 mini", True),
 "CAMXT30": (-600, -62, "nose", "A8 XT30 inline", False),
 "U2T": (-420, 78, "nose", "USB-TTL converter", False),
 "CANSPL": (-300, -48, "nose", "CAN splitter", False),
 "PDB": (515, -20, "aft", "AXL 400 PDB", True),
 "UBEC12": (510, 62, "aft", "KDE UBEC 12 V", True),
 "UBEC5": (640, -62, "aft", "KDE UBEC 5 V", False),
 "ESCFWD": (640, 0, "aft", "APD 120F3 (pusher)", True),
 "MOTFWD": (1048, 0, "aftx", "VT4130 pusher", True),
}
for s, sd in ((1, "R"), (-1, "L")):
    fr, rr = ("1", "4") if s > 0 else ("3", "2")
    D[f"SPLIT_{sd}_FUS"] = (166, s*488, f"root{sd}", f"DB-25 {sd}", True)
    D[f"SPLIT_{sd}_WING"] = (166, s*510, f"wing{sd}", "", True)
    D[f"XT90F_{sd}_F"] = (151, s*486, f"root{sd}", "", True)
    D[f"XT90F_{sd}_M"] = (151, s*506, f"wing{sd}", f"XT90 VTOL{fr}", True)
    D[f"XT90A_{sd}_F"] = (264, s*486, f"root{sd}", "", True)
    D[f"XT90A_{sd}_M"] = (264, s*506, f"wing{sd}", f"XT90 VTOL{rr}", True)
    D[f"ESC{fr}"] = (67, s*635, f"wing{sd}", f"ESC VTOL{fr}", True)
    D[f"ESC{rr}"] = (67, s*725, f"wing{sd}", f"ESC VTOL{rr}", True)
    D[f"MOT{fr}"] = (-640, s*830, f"wing{sd}", f"VTOL{fr} 8020 PRO", True)
    D[f"MOT{rr}"] = (962, s*830, f"wing{sd}", f"VTOL{rr} 8020 PRO", True)
    D[f"SRV{sd}1"] = (330, s*1361, f"wing{sd}", f"Aileron servo {sd}", True)
    D[f"SRV{sd}2"] = (1941, s*1145, f"wing{sd}", f"Ruddervator servo {sd}", True)
    D[f"LED{sd}1"] = (-640, s*857, f"wing{sd}", f"LED {sd}1 (fwd mount)", True)
    D[f"LED{sd}2"] = (962, s*857, f"wing{sd}", f"LED {sd}2 (aft mount)", True)
    D[f"LED{sd}T"] = (130, s*1961, f"wing{sd}", f"LED {sd}T (winglet)", True)
    D[f"BATT_{sd}"] = (62, s*258, "batt", f"Battery {sd} receptacle", True)

LDIR = {"JETSON":"w","CUBE":"e","MESH":"e","GSM":"w","GNSS":"e","LIDAR":"w","ARSP":"e","SWBTN":"w","CAM":"e","CAMXT30":"w",
 "U2T":"e","CANSPL":"w","PDB":"w","UBEC12":"e","UBEC5":"w","ESCFWD":"e","MOTFWD":"e"}
for sd in "RL":
    fr, rr = ("1", "4") if sd == "R" else ("3", "2")
    LDIR.update({f"SPLIT_{sd}_FUS":"s", f"XT90F_{sd}_M":"ne", f"XT90A_{sd}_M":"se", f"ESC{fr}":"nw", f"ESC{rr}":"ne",
                 f"MOT{fr}":"se", f"MOT{rr}":"se", f"LED{sd}1":"ne", f"LED{sd}2":"ne", f"LED{sd}T":"s",
                 f"SRV{sd}1":"s", f"SRV{sd}2":"s", f"BATT_{sd}":"n"})

def dev_of(c):
    if c.startswith("JET_") or c in ("A8M_RJ45", "RF_RJ45") or re.match(r"WAV\d_EXT_M", c): return "JETSON"
    if c.startswith("FC_"): return "CUBE"
    if c == "RF_UBEC_HP": return "UBEC5"
    if c.startswith("RF_"): return "MESH"
    if c.startswith("WAV"): return "GSM"
    if c.startswith("U2T"): return "U2T"
    if c.startswith("GPS_"): return "GNSS"
    if c == "ARSP_CAN": return "ARSP"
    if c == "LRF_COMM": return "LIDAR"
    if c.startswith("CAN_SPL"): return "CANSPL"
    if c == "SW_BTN": return "SWBTN"
    if c in ("A8M_NET", "A8M_PWR"): return "CAM"
    if c.startswith("A8M_XT30"): return "CAMXT30"
    if c.startswith("PDB_") or c == "CAP_BAT": return "PDB"
    if c.startswith("UBEC12"): return "UBEC12"
    if c.startswith("UBEC5"): return "UBEC5"
    if c.startswith(("ESC_FWD", "CAP_FWD")): return "ESCFWD"
    if c == "MOT_FWD": return "MOTFWD"
    m = re.match(r"XT90_VTOL(\d)_([FM])", c)
    if m:
        n, g = m.groups(); sd = "R" if n in "14" else "L"
        return f"XT90{'F' if n in '13' else 'A'}_{sd}_{g}"
    m = re.match(r"SPLIT_([LR])_(FUS|WING)", c)
    if m: return f"SPLIT_{m.group(1)}_{m.group(2)}"
    m = re.match(r"(?:ESC|CAP)_VTOL(\d)", c)
    if m: return f"ESC{m.group(1)}"
    m = re.match(r"MOT_VTOL(\d)", c)
    if m: return f"MOT{m.group(1)}"
    m = re.match(r"SRV_([LR])(\d)", c)
    if m: return f"SRV{m.group(1)}{m.group(2)}"
    m = re.match(r"LED_([LR])(\d|T)", c)
    if m: return f"LED{m.group(1)}{m.group(2)}"
    raise KeyError(c)

SYS = {
 "bat":   ("#d64545", "Battery & motor power"),
 "phase": ("#3d4451", "Motor phases"),
 "v12":   ("#ef7d22", "12 V distribution"),
 "v5":    ("#d9a514", "5 V distribution"),
 "pwm":   ("#2f6fde", "PWM / DShot / LED signal"),
 "can":   ("#8b4fd6", "CAN bus"),
 "data":  ("#169c74", "UART / Ethernet / USB"),
 "fcpwr": ("#d6408f", "FC power & switch"),
}
def classify(cid, n):
    n = (n or "").lower()
    if "phase" in n: return "phase"
    if "capacitor" in n: return "bat"
    if cid in ("W_PWR_01", "W_PWR_02") or "power, pdb" in n or "power, wing split" in n or "forward esc power" in n: return "bat"
    if cid in ("W_FC_01", "W_PWR_03"): return "fcpwr"
    if "can pair" in n or "can_h" in n or cid in ("W_FC_02", "W_FC_03", "W_FC_05"): return "can"
    if "12 v" in n or "jetson xt30" in n or "camera xt30" in n or "a8-mini power" in n: return "v12"
    if cid in ("W_ACT_10", "W_ACT_12", "W_ACT_19", "W_ACT_21"): return "v12"
    if "5 v ubec" in n or "wing plug to led" in n: return "v5"
    if "pwm" in n or "esc signal" in n or "signal: t, s" in n or "signal and ground" in n: return "pwm"
    return "data"

# ------------------------------------------------------------------ routing
CH, TR, WC, LP = 296, 120, 195, 3.0     # side channel Y, nose trunk Y, wing corridor X, lane pitch
lanes = {}
def lane(group):
    k = lanes.get(group, 0); lanes[group] = k + 1
    return LP * ((k + 1) // 2) * (1 if k % 2 else -1)

def route(da, db, sk, cid):
    xa, ya, za = D[da][:3]; xb, yb, zb = D[db][:3]
    A, B = (xa, ya), (xb, yb)
    zs = {za, zb}
    if za == zb and za in ("nose", "aft"):
        return [A, (xa, yb), B]
    if zs <= {"aft", "aftx"}:
        return [A, (xa, yb), B]
    if zs == {"nose", "aft"}:
        n, a = (A, B) if za == "nose" else (B, A)
        c = -1 if sk in ("v12", "v5", "fcpwr") else 1
        o = lane(f"ch{c}")
        t = c*(TR + o); y = c*(CH + o)
        pts = [n, (n[0], t), (-102, t), (-102, y), (440 + o*c, y), (440 + o*c, a[1]), a]
        return pts if za == "nose" else pts[::-1]
    root = [z for z in zs if z.startswith("root")]
    if root and zs & {"nose", "aft"}:
        s = 1 if root[0].endswith("R") else -1
        r, f = (A, B) if za.startswith("root") else (B, A)
        o = lane(f"ch{s}"); y = s*(CH + o)
        if f[0] < 0:
            t = s*(TR + o)
            pts = [f, (f[0], t), (-102, t), (-102, y), (r[0], y), r]
        else:
            pts = [f, (440 + o*s, f[1]), (440 + o*s, y), (r[0], y), r]
        return pts if f == A else pts[::-1]
    if "batt" in zs:
        s = 1 if ya > 0 or yb > 0 else -1
        o = lane(f"ch{s}"); y = s*(CH + o)
        return [A, (45, ya), (45, y), (440, y), (440, -20), B]
    w = [z for z in zs if z.startswith("wing")][0]
    s = 1 if w.endswith("R") else -1
    if da.startswith("ESC") and db.startswith("MOT") or db.startswith("ESC") and da.startswith("MOT"):
        esc, mot = (A, B) if da.startswith("ESC") else (B, A)
        if mot[0] < 0:   # forward motor: out of the ESC LE edge, along the stub to the front joint
            pts = [esc, (40, esc[1]), (40, s*826), (mot[0], s*826), mot]
        else:
            pts = [esc, (90, esc[1]), (90, s*834), (mot[0], s*834), mot]
        return pts if esc == A else pts[::-1]
    r, wd = (A, B) if da.startswith(("SPLIT", "XT90")) else (B, A)
    tgt = db if r == A else da
    if sk == "bat":      # XT90 male -> ESC battery input, in front of / through the main spar
        if r[0] < 200:
            pts = [r, (r[0], s*560), (60, s*560), (60, wd[1]), wd]
        else:
            pts = [r, (r[0], s*575), (110, s*575), (110, s*700), (75, s*700), (75, wd[1]), wd]
        return pts if r == A else pts[::-1]
    o = lane(f"w{s}"); x = WC + o
    if tgt.startswith("ESC"):
        pts = [r, (r[0], s*520), (x, s*520), (x, wd[1] + s*(-18)), (wd[0], wd[1] + s*(-18)), wd]
    elif tgt.endswith("T"):
        pts = [r, (r[0], s*520), (x, s*520), (x, s*1900), (wd[0], s*1900), wd]
    elif tgt.startswith("LED"):
        yb_ = s*(816 - abs(o)*0.6)
        xj = -74 if wd[0] < 0 else 524
        pts = [r, (r[0], s*520), (x, s*520), (x, yb_), (xj, yb_), (wd[0], yb_), wd]
    elif tgt.endswith("1"):
        pts = [r, (r[0], s*520), (x, s*520), (x, wd[1]), wd]
    else:   # ruddervator: M8 4-pin at the rear boom joint, boom, tail joint CONN 4P at X 1775
        yb_ = s*(840 + abs(o)*0.6)
        pts = [r, (r[0], s*520), (x, s*520), (x, yb_), (524, yb_), (1775, yb_), (1775, s*900), (wd[0], s*900), wd]
    return pts if r == A else pts[::-1]

def plen(p): return sum(math.dist(a, b) for a, b in zip(p, p[1:]))

ORDER = {"bat": 0, "phase": 1, "v12": 2, "v5": 3, "fcpwr": 4, "pwm": 5, "can": 6, "data": 7}
raw = []
for f in sorted((ROOT / "harness").glob("*.yaml")):
    d = yaml.safe_load(open(f, encoding="utf-8"))
    cab = d.get("cables") or {}
    for conn in d.get("connections") or []:
        names = [list(x.keys())[0] if isinstance(x, dict) else x for x in conn]
        if len(names) != 3 or names[1] == "-->": continue
        a, cid, b = names
        c = cab.get(cid, {})
        raw.append((cid, f.stem, a, b, c))
raw.sort(key=lambda r: (ORDER[classify(r[0], r[4].get("notes", ""))], r[0]))
cables = []
for cid, fs, a, b, c in raw:
    da, db = dev_of(a), dev_of(b)
    sk = classify(cid, c.get("notes", ""))
    local = da == db
    pts = [] if local else route(da, db, sk, cid)
    L = plen(pts) if pts else 0
    cables.append(dict(id=cid, h=fs.replace("_system", ""), a=a, b=b, da=da, db=db, s=sk,
        g=str(c.get("gauge", "") or ""), n=c.get("wirecount", ""), note=c.get("notes", ""),
        p=[[round(x, 1), round(y, 1)] for x, y in pts], L=round(L), cut=0 if local else math.ceil((L*1.15 + 100)/10)*10))
for s in (1, -1):   # battery -> PDB, not yet in the harness
    sd = "R" if s > 0 else "L"
    pts = route(f"BATT_{sd}", "PDB", "bat", "")
    cables.append(dict(id=f"BATT_{sd}_PDB", h="(planned)", a=f"BATT_Bay_Receptacle_{sd}", b="PDB_J2BAT", da=f"BATT_{sd}",
        db="PDB", s="bat", g="8 AWG", n=2, note="Battery receptacle to PDB J2 - not yet defined in power_system.yaml",
        p=[[round(x, 1), round(y, 1)] for x, y in pts], L=round(plen(pts)), cut=math.ceil((plen(pts)*1.15+100)/10)*10, planned=True))

# ------------------------------------------------------------------ CAD -> svg paths
NICE = {"AV_FC_CubeOrangePlus_ADSB": "Cube Orange+", "AV_Radio_DoodleLabs_RM2450_Mini": "Mesh Rider Mini",
 "AV_GSM_DualTelet_Waveshare": "Waveshare 5G", "AV_GNSS_Sierra_PrecisionPoint_Pro": "GNSS", "AV_LiDAR_LightWare_GRF500": "GRF-500",
 "AV_Airspeed_Sierra_TrueSpeedV2": "TrueSpeed", "AV_Power_Switch_22mm": "Power switch", "AV_Jetson_OrinNX_DevKit": "Jetson Orin NX",
 "AV_PDB_AXL400": "AXL 400 PDB", "AV_BEC_KDE_UBECUVC": "KDE UBEC", "AV_ESC_APD_120F3": "APD 120F3 ESC",
 "AV_Camera_SIYI_A8mini": "SIYI A8 mini", "AV_LED_StrobeIT_Pro": "StrobeIT-Pro", "AV_LED_StrobeIT": "StrobeIT",
 "AV_Antenna_Whip": "Antenna", "COTS_Servo_Z1500H": "Z1500H servo", "COTS_Motor_VT8020PRO_120KV": "VT8020 PRO",
 "CON_DSUB25_Female": "DB-25 F", "CON_DSUB25_Male": "DB-25 M", "CON_XT90_Female": "XT90 F", "CON_XT90_Male": "XT90 M",
 "CON_M8_4pin_Female": "M8 4p F", "CON_M8_4pin_Male": "M8 4p M", "CON_M8_3pin_Female": "M8 3p F", "CON_M8_3pin_Male": "M8 3p M",
 "CON_Phase3_Bullet4mm_Female": "Phase 3p F", "CON_Phase3_Bullet4mm_Male": "Phase 3p M"}
def nice(key, layer):
    last = key.split("|")[0].split("+")[-1]
    base = re.sub(r" v\d+:\d+$|:\d+$", "", last)
    return NICE.get(base, key.split("|")[-1] if "|" in key else base)
cad = []
for o in CAD:
    d_ = " ".join("M" + " L".join(f"{y:g} {x:g}" for x, y in r) + "Z" for r in o["rings"])
    cad.append(dict(l=o["layer"], k=nice(o["key"], o["layer"]), d=d_, bb=o["bb"]))

data = dict(cad=cad, cables=cables, sys={k: {"c": v[0], "n": v[1]} for k, v in SYS.items()},
            dev={k: dict(x=v[0], y=v[1], z=v[2], n=v[3], cad=v[4], ld=LDIR.get(k, "e")) for k, v in D.items()},
            built=datetime.date.today().isoformat())
html = (Path(__file__).parent / "harness_topview_template.html.in").read_text(encoding="utf-8")
html = html.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
(OUT / "sage_harness_topview.html").write_text(html, encoding="utf-8")
with open(OUT / "harness_route_lengths.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["cable", "harness", "from", "to", "gauge", "wires", "system", "plan_route_mm", "est_cut_length_mm"])
    for c in sorted(cables, key=lambda c: c["id"]):
        w.writerow([c["id"], c["h"], c["a"], c["b"], c["g"], c["n"], SYS[c["s"]][1], c["L"] or "local", c["cut"] or "local"])
print("cables", len(cables), "html KB", round(len(html)/1024))
