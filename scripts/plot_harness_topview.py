"""Plot every SAGE harness cable on the aircraft top view (plan view).

Reads harness/*.yaml (WireViz), places each connector at its device location on the SAGE
airframe (aircraft axes from the Fusion master: X aft, Y right, origin at the wing-root LE in
plan, mm) and routes each cable along fixed wireways. Outputs (docs/harness_layout/):
  sage_harness_topview.png/.svg/.pdf     whole aircraft
  sage_harness_fuselage_detail.png/.svg  fuselage + wing roots
  harness_route_lengths.csv / .md        estimated route and cut length per cable

Airframe outline: built from the SAGE CAD design-log dimensions (SAGE_Master v99), not exported
from Fusion. Device positions marked (est) in POS are estimates to be confirmed in the CAD.
Usage: python scripts/plot_harness_topview.py
"""
import csv, math, glob
from pathlib import Path
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "harness_layout"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- device positions (x aft, y right), zone ----------------
DEV = {
 # nose avionics bay (63_Avionics_Nose)
 "JETSON": ((-330, 60), "nose", "Jetson Orin NX"),
 "CUBE": ((-190, 0), "nose", "Cube Orange+"),
 "MESH": ((-250, -150), "nose", "Mesh Rider Mini"),
 "WAV1": ((-345, 195), "nose", "5G dongle 1"),
 "WAV2": ((-255, 195), "nose", "5G dongle 2"),
 "U2T": ((-265, 105), "nose", "USB-TTL"),
 "GNSS": ((-125, -85), "nose", "GNSS (under RF window)"),
 "ARSP": ((-520, 95), "nose", "Airspeed TrueSpeed V2"),
 "LIDAR": ((-420, -120), "nose", "GRF-500 LiDAR"),
 "CANSPL": ((-115, 110), "nose", "CAN splitter"),
 "SWBTN": ((-150, 235), "nose", "Power pushbutton"),
 "CAM": ((-505, 0), "nose", "SIYI A8 mini"),
 "CAMXT30": ((-450, 35), "nose", "A8 XT30"),
 # aft bay (64_Avionics_Aft)
 "PDB": ((500, 0), "aft", "AXL 400 PDB"),
 "UBEC12": ((600, 90), "aft", "KDE UBEC 12 V"),
 "UBEC5": ((600, -90), "aft", "KDE UBEC 5 V"),
 "ESCFWD": ((720, 0), "aft", "APD 120F3 pusher ESC"),
 "MOTFWD": ((1040, 0), "aftx", "VT4130 pusher"),
}
for s, side in ((1, "R"), (-1, "L")):
    front, rear = ("1", "4") if s > 0 else ("3", "2")
    DEV[f"SPLIT_{side}"] = ((166, s*500), f"root{side}", f"DB-25 {side}")
    DEV[f"XT90F_{side}"] = ((151, s*500), f"root{side}", "XT90 (fwd motor)")
    DEV[f"XT90A_{side}"] = ((264, s*500), f"root{side}", "XT90 (aft motor)")
    DEV[f"ESC{front}"] = ((50, s*730), f"wing{side}", f"ESC VTOL{front}")
    DEV[f"ESC{rear}"] = ((50, s*930), f"wing{side}", f"ESC VTOL{rear}")
    DEV[f"MOT{front}"] = ((-640, s*830), f"wing{side}", f"VTOL{front}")
    DEV[f"MOT{rear}"] = ((962, s*830), f"wing{side}", f"VTOL{rear}")
    DEV[f"SRV{side}1"] = ((330, s*1300), f"wing{side}", f"Servo {side}1 aileron (est)")
    DEV[f"SRV{side}2"] = ((1720, s*1000), f"wing{side}", f"Servo {side}2 ruddervator (est)")
    DEV[f"LED{side}1"] = ((-640, s*878), f"wing{side}", f"LED {side}1 fwd mount")
    DEV[f"LED{side}2"] = ((962, s*878), f"wing{side}", f"LED {side}2 aft mount")
    DEV[f"LED{side}T"] = ((130, s*1955), f"wing{side}", f"LED {side}T winglet")

def connector_device(c):
    import re
    m = re.match
    if c.startswith("JET_") or c in ("A8M_RJ45", "RF_RJ45") or re.match(r"WAV\d_EXT_M", c): return "JETSON"
    if c.startswith("FC_"): return "CUBE"
    if c.startswith("RF_") and c != "RF_UBEC_HP": return "MESH"
    if c == "RF_UBEC_HP": return "UBEC5"
    if re.match(r"WAV1", c): return "WAV1"
    if re.match(r"WAV2", c): return "WAV2"
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
    if c.startswith("ESC_FWD") or c.startswith("CAP_FWD"): return "ESCFWD"
    if c == "MOT_FWD": return "MOTFWD"
    if c == "ESC_FWD_IN": return "ESCFWD"
    m = re.match(r"XT90_VTOL(\d)_[FM]", c)
    if m:
        n = m.group(1); side = "R" if n in "14" else "L"
        return f"XT90F_{side}" if n in "13" else f"XT90A_{side}"
    m = re.match(r"SPLIT_([LR])_", c)
    if m: return f"SPLIT_{m.group(1)}"
    m = re.match(r"(?:ESC|CAP)_VTOL(\d)", c)
    if m: return f"ESC{m.group(1)}"
    m = re.match(r"MOT_VTOL(\d)", c)
    if m: return f"MOT{m.group(1)}"
    m = re.match(r"SRV_([LR])(\d)", c)
    if m: return f"SRV{m.group(1)}{m.group(2)}"
    m = re.match(r"LED_([LR])(\d|T)", c)
    if m: return f"LED{m.group(1)}{m.group(2)}"
    raise KeyError(c)

# ---------------- system classification ----------------
SYS = {  # key: (colour, lane, label)
 "bat":   ("#c62828", 0, "Battery / motor power (10-16 AWG)"),
 "phase": ("#424242", 0, "Motor phases"),
 "v12":   ("#ef6c00", 1, "12 V UBEC distribution"),
 "v5":    ("#f9a825", 2, "5 V UBEC distribution"),
 "pwm":   ("#1565c0", 3, "PWM / DShot / LED signal"),
 "can":   ("#7b1fa2", 4, "CAN (DroneCAN servos, GNSS, airspeed)"),
 "data":  ("#2e7d32", 5, "UART / Ethernet / USB data"),
 "fcpwr": ("#ad1457", 6, "PDB -> Cube power / switch"),
}
def classify(cid, note, a, b):
    n = (note or "").lower()
    if "phase" in n: return "phase"
    if "capacitor" in n: return "bat"
    if cid in ("W_PWR_01", "W_PWR_02") or "power, pdb" in n or "power, wing split" in n or "forward esc power" in n: return "bat"
    if cid in ("W_FC_01", "W_PWR_03"): return "fcpwr"
    if "can" in n.split() or "can pair" in n or "can_h" in n or cid in ("W_FC_02", "W_FC_03", "W_FC_05"): return "can"
    if "12 v" in n or "jetson xt30" in n or "camera xt30" in n or "a8-mini power" in n or ("servo" in n and "power" in n and "12" in n): return "v12"
    if cid in ("W_ACT_10", "W_ACT_12", "W_ACT_19", "W_ACT_21"): return "v12"
    if "5 v ubec" in n: return "v5"
    if "led" in n and "pwm" not in n and "wing plug to led" in n: return "v5"
    if "pwm" in n or "esc signal" in n or "signal: t, s" in n or "signal and ground" in n: return "pwm"
    return "data"

# ---------------- routing ----------------
L = 13  # lane pitch, mm
def route(cid, da, db, sysk):
    (pa, za, _), (pb, zb, _) = DEV[da], DEV[db]
    lane = SYS[sysk][1]
    o = lane * L
    def side(z): return 1 if z.endswith("R") else -1
    zs = {za, zb}
    # same bay: L-shape
    if za == zb and za in ("nose", "aft"):
        return [pa, (pa[0], pb[1]), pb]
    if zs <= {"aft", "aftx"}:
        return [pa, (pa[0], pb[1]+o*0), pb]
    # nose <-> aft along the crown wireway (over the payload box)
    if zs == {"nose", "aft"} or zs == {"nose", "aftx"}:
        n, a = (pa, pb) if za == "nose" else (pb, pa)
        y = -45 + o
        pts = [n, (n[0], y), (-90, y), (430, y), (430, a[1]), a]
        return pts if za == "nose" else pts[::-1]
    # wing-root split on fuselage side
    root = [z for z in zs if z.startswith("root")]
    if root and ("nose" in zs or "aft" in zs):
        s = side(root[0])
        r, f = (pa, pb) if za.startswith("root") else (pb, pa)
        if f[0] < 0:   # from nose: fwd of the battery, through the wing-root LE bay
            y1 = s*(60 + o)
            pts = [f, (f[0], y1), (35 + o, y1), (35 + o, s*455), (r[0], s*455), r]
        else:          # from aft bay: aft of the batteries, behind the rear spar region
            y1 = s*(150 + o)
            pts = [f, (430 - o, f[1]), (430 - o, y1), (310 + o, y1), (310 + o, s*440 + s*o*0.3), (r[0], s*440 + s*o*0.3), r]
        return pts if f is pa else pts[::-1]
    # wing side
    wz = [z for z in zs if z.startswith("wing")]
    if wz:
        s = side(wz[0])
        a, b = pa, pb
        if za.startswith("wing") and zb.startswith("wing"):   # ESC -> motor phases
            esc, mot = (a, b) if da.startswith("ESC") else (b, a)
            if mot[0] < 0:
                return [esc, (25, esc[1]), (25, s*812), (mot[0], s*812), mot]
            return [esc, (80, esc[1]), (80, s*848), (mot[0], s*848), mot]
        r, w = (a, b) if za.startswith("root") else (b, a)
        dw = db if zb.startswith("wing") else da
        x0 = 200 + o
        if dw.startswith("ESC"):
            if sysk == "bat":   # XT90 -> ESC input, in front of the main spar
                xb = 95 if r[0] < 200 else 115
                pts = [r, (r[0], s*(560 if r[0] < 200 else 600)), (xb, s*(560 if r[0] < 200 else 600)), (xb, w[1]), w]
            else:
                pts = [r, (x0, r[1]), (x0, w[1] - s*25), (w[0], w[1] - s*25), w]
        elif dw.startswith("LED") and dw.endswith("T"):
            pts = [r, (x0, r[1]), (x0, w[1]), w]
        elif dw.startswith("LED"):
            yb = s*(795 - o*0.5)
            xj = 10 if w[0] < 0 else 440
            pts = [r, (x0, r[1]), (x0, yb), (xj, yb), (w[0], yb), w]
        elif dw.endswith("1"):   # aileron servo
            pts = [r, (x0, r[1]), (x0, w[1]), w]
        else:                    # ruddervator servo via rear boom joint + boom
            yb = s*(800 - o*0.5)
            pts = [r, (x0, r[1]), (x0, yb), (440, yb), (w[0], yb), w]
        return pts if r is pa else pts[::-1]
    return [pa, pb]

def plen(pts):
    return sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))

# ---------------- read harness ----------------
cables = []
for f in sorted((ROOT / "harness").glob("*.yaml")):
    d = yaml.safe_load(open(f, encoding="utf-8"))
    cab = d.get("cables") or {}
    for conn in d.get("connections") or []:
        names = [list(x.keys())[0] if isinstance(x, dict) else x for x in conn]
        if len(names) != 3 or names[1] == "-->": continue
        a, cid, b = names
        c = cab.get(cid, {})
        da, db = connector_device(a), connector_device(b)
        sk = classify(cid, c.get("notes", ""), a, b)
        pts = route(cid, da, db, sk)
        cables.append(dict(id=cid, file=f.stem, a=a, b=b, da=da, db=db, sys=sk,
                           gauge=c.get("gauge", ""), wires=c.get("wirecount", ""),
                           note=c.get("notes", ""), pts=pts, local=(da == db)))

# ---------------- airframe outline (from the CAD design log) ----------------
def hw(x):
    if x < -560 or x > 1000: return None
    if x < -150: base = 360 * max(0.0, 1 - ((-150 - x) / 410) ** 2.2) ** (1 / 2.2)
    elif x <= 360: base = 360
    else: base = 360 - 295 * (1 - math.cos(math.pi * (x - 360) / 640)) / 2
    if 60 <= x <= 280: b = 1
    elif -200 < x < 60: b = (1 - math.cos(math.pi * (x + 200) / 260)) / 2
    elif 280 < x < 500: b = (1 + math.cos(math.pi * (x - 280) / 220)) / 2
    else: b = 0
    return base + 28 * b

def P(x, y): return (y, -x)   # plot coords: Y right, nose up

def draw_airframe(ax, detail=False):
    oml = dict(fc="#eceff1", ec="#37474f", lw=1.1, zorder=1)
    # wing
    ys = [-1900 + i * 20 for i in range(191)]
    le = [(59.5 * abs(y) / 1900, y) for y in ys]
    te = [(59.5 * abs(y) / 1900 + 400 - 10 * abs(y) / 1900, y) for y in ys][::-1]
    ax.add_patch(Polygon([P(*p) for p in le + te], **oml))
    for s in (1, -1):
        ax.add_patch(Polygon([P(59.5, s*1900), P(449.5, s*1900), P(410, s*2100), P(210, s*2100)], **oml))
        # aileron (est)
        ail = [(59.5*y/1900 + 0.75*(400-10*y/1900), s*y) for y in (1150, 1750)]
        ail += [(59.5*y/1900 + 400 - 10*y/1900, s*y) for y in (1750, 1150)]
        ax.add_patch(Polygon([P(*p) for p in ail], fc="#cfd8dc", ec="#78909c", lw=0.7, ls="--", zorder=1.1))
        # tail (inverted V, plan projection)
        root_le, root_te, tip_y = 1410, 1850, 800 + 750 * math.cos(math.radians(35))
        tip_le = root_le + 750 * math.tan(math.radians(18)) * math.cos(math.radians(35))
        ax.add_patch(Polygon([P(root_le, s*800), P(root_te, s*800), P(tip_le + 400, s*tip_y), P(tip_le, s*tip_y)], **oml))
        ax.add_patch(Polygon([P(root_te - 0.3*440, s*800), P(root_te, s*800), P(tip_le + 400, s*tip_y), P(tip_le + 0.7*400, s*tip_y)],
                             fc="#cfd8dc", ec="#78909c", lw=0.7, ls="--", zorder=1.1))
        # boom + nacelle
        ax.add_patch(Rectangle(P(-660, s*830 - 22.5)[::1] if False else (s*830 - 22.5, -1850), 45, 2510, fc="#b0bec5", ec="#455a64", lw=0.8, zorder=1.2))
        ax.add_patch(Rectangle((s*830 - 35, -440), 70, 430, fc="#cfd8dc", ec="#455a64", lw=0.8, zorder=1.25))
        for mx in (-640, 962):
            ax.add_patch(Circle(P(mx, s*830), 44, fc="#90a4ae", ec="#263238", lw=0.8, zorder=1.3))
            ax.add_patch(Circle(P(mx, s*830), 381, fc="none", ec="#90a4ae", lw=0.7, ls=(0, (4, 4)), zorder=1.0))
        # wing split + boom joints
        ax.plot(*zip(P(-20, s*500), P(430, s*500)), color="#d32f2f", lw=1.2, ls="-.", zorder=1.4)
        for xj, col in ((10, "#fbc02d"), (440, "#8e24aa")):
            ax.plot(*zip(P(xj, s*800), P(xj, s*860)), color=col, lw=3, zorder=1.4)
        # battery cartridges
        ax.add_patch(Rectangle((min(s*255, s*365), -235), 110, 148, fc="#ffe0b2", ec="#e65100", lw=0.8, zorder=2.1))
        ax.text(s*310, -161, "BATT\n12S 25Ah", ha="center", va="center", fontsize=5 if not detail else 7, color="#bf360c", zorder=2.2)
    # fuselage
    xs = [-560 + i * 5 for i in range(313)]
    pts = [P(x, hw(x)) for x in xs] + [P(x, -hw(x)) for x in xs[::-1]]
    ax.add_patch(Polygon(pts, fc="#f5f5f5", ec="#263238", lw=1.3, zorder=2))
    # payload box, bays
    ax.add_patch(Rectangle((-250, -411), 500, 500, fc="none", ec="#757575", lw=0.8, ls="--", zorder=2.05))
    ax.text(0, -270, "Payload bay 500x500 (5 kg)", ha="center", fontsize=6 if not detail else 8, color="#616161", zorder=2.06)
    ax.add_patch(Rectangle((-215, 110), 430, 415, fc="#e3f2fd", ec="#90caf9", lw=0.6, zorder=2.03))
    ax.add_patch(Rectangle((-180, -770), 360, 335, fc="#e8f5e9", ec="#a5d6a7", lw=0.6, zorder=2.03))
    ax.text(0, 130, "Nose avionics bay", ha="center", va="bottom", fontsize=6 if not detail else 8, color="#1565c0", zorder=2.06)
    ax.text(0, -760, "Aft avionics bay", ha="center", va="bottom", fontsize=6 if not detail else 8, color="#2e7d32", zorder=2.06)
    ax.plot(*zip(P(1060, -229), P(1060, 229)), color="#78909c", lw=2.5, zorder=1.5)
    ax.plot(0, 0, marker="+", color="k", ms=8, zorder=6)

def offset(pts, k):
    return pts  # lanes already built into the routes

def draw_cables(ax, lw_scale=1.0):
    for c in cables:
        if c["local"]: continue
        col = SYS[c["sys"]][0]
        g = str(c["gauge"])
        lw = 2.6 if g.startswith("10") else 1.8 if g.startswith("16") else 1.1 if g.startswith("22") else 0.8
        if c["sys"] == "phase": lw = 2.2
        xy = [P(*p) for p in c["pts"]]
        ax.plot(*zip(*xy), color=col, lw=lw * lw_scale, alpha=0.9, solid_joinstyle="round", zorder=3)
    # battery -> PDB J2 (not yet in harness)
    for s in (1, -1):
        pts = [(73, s*273), (73, s*200), (430, s*200), (430, s*20), (500, s*20)]
        ax.plot(*zip(*[P(*p) for p in pts]), color="#c62828", lw=2.4 * lw_scale, ls=(0, (3, 2)), alpha=0.6, zorder=2.9)

def draw_devices(ax, which, fs=6):
    for k, ((x, y), z, name) in DEV.items():
        if which == "detail" and (abs(y) > 560 or x > 1100): continue
        ax.plot(*P(x, y), marker="s", ms=4 if which != "detail" else 6, mfc="white", mec="#212121", mew=0.9, zorder=5)
        if which == "overall" and z in ("nose", "aft"): continue
        dx, ha = (14, "left") if y >= 0 else (-14, "right")
        if which == "detail" and z.startswith("root"):
            dx, ha = (18, "left") if y > 0 else (-18, "right")
        ax.annotate(name, P(x, y), xytext=(dx / 4, 2), textcoords="offset points", ha=ha, va="bottom",
                    fontsize=fs, color="#212121", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))

def legend(ax, loc):
    h = [Line2D([0], [0], color=v[0], lw=2.2, label=v[2]) for v in SYS.values()]
    h.append(Line2D([0], [0], color="#c62828", lw=2.2, ls=(0, (3, 2)), alpha=0.6, label="Battery -> PDB J2 (not yet in harness)"))
    h.append(Line2D([0], [0], color="#d32f2f", lw=1.2, ls="-.", label="Wing split Y +/-500 (DB-25 + 2 x XT90)"))
    h.append(Line2D([0], [0], color="#fbc02d", lw=3, label="Front boom joint X 10"))
    h.append(Line2D([0], [0], color="#8e24aa", lw=3, label="Rear boom joint X 440"))
    ax.legend(handles=h, loc=loc, fontsize=7, frameon=True, framealpha=0.95)

NOTE = ("Top view, nose up, Y right. Airframe drawn from the SAGE CAD design log (SAGE_Master v99) dimensions; "
        "device positions marked (est) and wireway lanes are layout proposals.\n"
        "Fuselage cables cross the payload bay on the crown (above the box); wing-root runs pass above the battery bays. "
        "Cable IDs and endpoints from sagewire/harness/*.yaml.")

# ---------------- overall ----------------
fig, ax = plt.subplots(figsize=(22, 14))
draw_airframe(ax)
draw_cables(ax)
draw_devices(ax, "overall", fs=6.5)
for lab, (x, y) in {"NOSE AVIONICS\nJetson, Cube, Mesh Rider,\n5G, GNSS, LiDAR, airspeed, A8": (-330, -40),
                    "AFT BAY\nPDB, UBEC 12 V / 5 V,\npusher ESC": (610, 0)}.items():
    ax.annotate(lab, P(x, y), xytext=((-1550, 280) if x < 0 else (-1600, -700)),
                fontsize=8, ha="center", arrowprops=dict(arrowstyle="-", color="#546e7a", lw=0.7),
                bbox=dict(boxstyle="round", fc="white", ec="#90a4ae"))
ax.set_xlim(-2250, 2250); ax.set_ylim(-2150, 780)
ax.set_aspect("equal"); ax.set_xlabel("Y (mm, right +)"); ax.set_ylabel("-X (mm, nose up)")
ax.grid(color="#eeeeee", lw=0.5, zorder=0)
ax.set_title("SAGE eVTOL - wiring harness routing on the top view (all systems)", fontsize=14, fontweight="bold")
ax.text(-2230, -2130, NOTE, fontsize=7, va="bottom", color="#424242")
legend(ax, "upper right")
fig.tight_layout()
for ext in ("png", "svg", "pdf"):
    fig.savefig(OUT / f"sage_harness_topview.{ext}", dpi=200)
plt.close(fig)

# ---------------- fuselage detail ----------------
fig, ax = plt.subplots(figsize=(16, 17))
draw_airframe(ax, detail=True)
draw_cables(ax, lw_scale=1.5)
draw_devices(ax, "detail", fs=8)
# cable id tags at mid-run (fuselage side only)
for c in cables:
    if c["local"]: continue
    pts = c["pts"]
    if all(abs(p[1]) > 560 for p in pts): continue
    segs = [(math.dist(p, q), p, q) for p, q in zip(pts, pts[1:]) if abs(p[1]) <= 520 and abs(q[1]) <= 520 and -600 < p[0] < 1060]
    if not segs: continue
    _, p, q = max(segs)
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    ax.text(*P(*m), c["id"].replace("W_", ""), fontsize=4.6, color=SYS[c["sys"]][0], ha="center", va="center",
            zorder=7, bbox=dict(boxstyle="round,pad=0.08", fc="white", ec="none", alpha=0.8))
ax.set_xlim(-620, 620); ax.set_ylim(-1100, 620)
ax.set_aspect("equal"); ax.grid(color="#eeeeee", lw=0.5, zorder=0)
ax.set_xlabel("Y (mm, right +)"); ax.set_ylabel("-X (mm, nose up)")
ax.set_title("SAGE - fuselage harness detail (nose bay, crown wireway, aft bay, wing-root splits)", fontsize=13, fontweight="bold")
legend(ax, "lower left")
fig.tight_layout()
for ext in ("png", "svg"):
    fig.savefig(OUT / f"sage_harness_fuselage_detail.{ext}", dpi=200)
plt.close(fig)

# ---------------- lengths ----------------
rows = []
for c in cables:
    pl = plen(c["pts"])
    cut = 0 if c["local"] else math.ceil((pl * 1.15 + 100) / 10) * 10
    rows.append([c["id"], c["file"], c["a"], c["b"], c["gauge"], c["wires"], SYS[c["sys"]][2],
                 "local (at device)" if c["local"] else round(pl), "short, fit on assembly" if c["local"] else cut])
rows.sort(key=lambda r: r[0])
with open(OUT / "harness_route_lengths.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["cable", "harness", "from", "to", "gauge", "wires", "system", "plan_route_mm", "est_cut_length_mm"])
    w.writerows(rows)
with open(OUT / "harness_route_lengths.md", "w", encoding="utf-8") as f:
    f.write("# SAGE harness - estimated route lengths\n\n")
    f.write("Plan-view route length along the wireways in `sage_harness_topview.png`. Estimated cut length = route x 1.15 "
            "(height changes, bends, tie-down) + 100 mm (terminations and service loops), rounded up to 10 mm. "
            "Replace with measured lengths from the CAD harness once routed in Fusion.\n\n")
    f.write("| Cable | Harness | From | To | Gauge | Wires | Plan route (mm) | Est. cut length (mm) |\n|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        f.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[7]} | {r[8]} |\n")
print(len(cables), "cables;", sum(1 for c in cables if c["local"]), "local")
