#!/usr/bin/env python3
"""
Protein Please — meal-box sleeve (belly band) generator.  SIMPLE layout.

Box: L 6.4in x W 4.5in x H 2.0in.
The sleeve is a closed loop around the girth perpendicular to the length:
    girth = 2*(W + H) = 2*(4.5 + 2.0) = 13.0in  (+ 0.5in glue flap)
Band width (extent along the 6.4in length) = 3.6in. Front panel = 4.5in x 3.6in.

Front face mirrors the approved reference poster: three plan points up top,
the big Protein Please wordmark, a pink "___ grams of protein" circle the chef
fills in by hand before shipping, the tagline, and the keep-refrigerated note.
Units: 100 user units per inch. Outline fonts before printing.
"""
import os, base64, re, math

HERE = os.path.dirname(os.path.abspath(__file__))
UPI = 100

# ---- palette (brand book) -----------------------------------------------
C = dict(
    green900="#13200E", green800="#1D2F17", green700="#284121",
    green600="#36562C", green500="#4A7039", green100="#DCE5D4",
    pink500="#DCA7C4", pink400="#E8BBD3", pink300="#EFCFDF",
    pink200="#F5E0EB", pink100="#FBF0F5",
    cream50="#FBF8EF", cream100="#F6F2E6", cream300="#E2DAC2",
    stone400="#B7B09B", stone600="#6E6A58",
    leaf="#3E8E4E", tomato="#D6462F", yolk="#E8B23A",
    hero="#2E5A1E",  # forest green of the reference wordmark
)
DISPLAY = "'Impact PP','Arial Narrow','Impact',sans-serif"
BODY = "'Hanken Grotesk','Helvetica Neue',Arial,sans-serif"
MONO = "'Space Mono','Courier New',monospace"

# ---- embed the brand display font ---------------------------------------
with open(os.path.join(HERE, "..", "assets", "impact.woff2"), "rb") as _f:
    _FONT_B64 = base64.b64encode(_f.read()).decode()
FONT_DEFS = ("<defs><style>@font-face{font-family:'Impact PP';font-weight:400 800;"
             "src:url(data:font/woff2;base64," + _FONT_B64 + ") format('woff2');}"
             "</style></defs>")

# ---- brand wordmark (from assets/logo-cream.svg), recoloured on the fly --
with open(os.path.join(HERE, "..", "assets", "logo-cream.svg")) as _f:
    _wm = _f.read()
WM_VB = (6946.0, 3745.0)
WM_PATHS = "".join(re.findall(r"<path[^>]*/>", _wm))  # paths keep their own transforms

def wordmark(x, y, h, color, anchor="start"):
    """Place the real Protein Please wordmark at height h; returns (svg, width)."""
    s = h / WM_VB[1]
    w = WM_VB[0] * s
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f})" '
            f'fill="{color}">{WM_PATHS}</g>', w)

# ---- geometry ------------------------------------------------------------
W, H, L = 4.5, 2.0, 6.4
BAND, GLUE, BLEED = 3.6, 0.5, 0.125
b = BLEED * UPI
P_TOP, P_SIDE, P_BOT, P_GLUE, BW = W*UPI, H*UPI, W*UPI, GLUE*UPI, BAND*UPI
X_TOP = b
X_FRONT = X_TOP + P_TOP
X_BOT = X_FRONT + P_SIDE
X_BACK = X_BOT + P_BOT
X_GLUE = X_BACK + P_SIDE
ART_W = X_GLUE + P_GLUE + b
ART_H = b + BW + b
FOLDS = [X_FRONT, X_BOT, X_BACK, X_GLUE]

# ---- QR ------------------------------------------------------------------
with open(os.path.join(HERE, "_qr-path.txt")) as f:
    QR_N = int(f.readline().strip())
    _qr_path = f.readline().strip()

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---- primitives ----------------------------------------------------------
def star(cx, cy, r, fill, sw=None):
    sw = sw or r * 0.34
    g = [f'<g stroke="{fill}" stroke-width="{sw:.2f}" stroke-linecap="round">']
    for a in (0, 60, 120):
        rad = math.radians(a); dx, dy = r*math.cos(rad), r*math.sin(rad)
        g.append(f'<line x1="{cx-dx:.1f}" y1="{cy-dy:.1f}" x2="{cx+dx:.1f}" y2="{cy+dy:.1f}"/>')
    g.append('</g>')
    return "".join(g)

def qr_block(cx, cy, size, dark, pad_fill="#FFFFFF", caption=None, cap_fill=None, cap_size=11):
    quiet = size*(4/(QR_N+8)); inner = size-2*quiet; s = inner/QR_N
    x0, y0 = cx-size/2, cy-size/2
    out = [f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{size:.2f}" height="{size:.2f}" rx="{size*0.05:.2f}" fill="{pad_fill}"/>',
           f'<g transform="translate({x0+quiet:.2f},{y0+quiet:.2f}) scale({s:.4f})"><path d="{_qr_path}" fill="{dark}"/></g>']
    if caption:
        out.append(f'<text x="{cx:.2f}" y="{y0+size+cap_size+7:.1f}" text-anchor="middle" '
                   f'font-family="{MONO}" font-size="{cap_size}" letter-spacing="1.2" '
                   f'fill="{cap_fill or dark}">{esc(caption)}</text>')
    return "\n".join(out)

# ---- the hand-written protein circle (chef fills in the number) ----------
def protein_circle(cx, cy, r):
    """Pink disc: blank top for the chef to write the grams, 'grams of protein' below."""
    g = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{C["pink300"]}"/>']
    g.append(f'<g transform="rotate(-12 {cx} {cy})">'
             f'<text x="{cx}" y="{cy+r*0.34:.1f}" font-family="{BODY}" font-weight="700" '
             f'font-size="{r*0.30:.1f}" fill="{C["green800"]}" text-anchor="middle">grams</text>'
             f'<text x="{cx}" y="{cy+r*0.63:.1f}" font-family="{BODY}" font-weight="700" '
             f'font-size="{r*0.30:.1f}" fill="{C["green800"]}" text-anchor="middle">of protein</text>'
             f'</g>')
    return "".join(g)

# =========================================================================
#  FRONT — the approved reference layout, adapted to the band
# =========================================================================
def hero_front():
    cx = P_TOP / 2
    g = [f'<rect width="{P_TOP}" height="{BW}" fill="{C["cream50"]}"/>']

    # --- wordmark (small) at the very top ---
    wm, ww = wordmark(cx, 26, 74, C["hero"], anchor="middle")
    g.append(wm)

    # --- the three plan points, centred, below ---
    pts = ["Veg & Non-Veg Meal Plans",
           "Thoughtfully Crafted, Protein-Rich Meals",
           "Real Ingredients. No Artificial Colours or Flavours"]
    fs = 12.5
    for i, ln in enumerate(pts):
        y = 150 + i * 22
        w = len(ln) * fs * 0.55          # approx text width for bullet placement
        g.append(star(cx - w/2 - 13, y - 4, 4.8, C["pink500"], 1.9))
        g.append(f'<text x="{cx}" y="{y}" font-family="{BODY}" font-weight="600" '
                 f'font-size="{fs}" fill="{C["green900"]}" text-anchor="middle">{esc(ln)}</text>')

    # --- pink "___ grams of protein" circle, low, chef writes the number ---
    g.append(protein_circle(cx, 262, 45))

    # --- keep-refrigerated / heating note ---
    g.append(f'<text x="{cx}" y="326" font-family="{BODY}" font-weight="700" font-size="13.5" '
             f'letter-spacing="0.3" fill="{C["green800"]}" text-anchor="middle">Keep refrigerated</text>')
    g.append(f'<text x="{cx}" y="347" font-family="{BODY}" font-weight="500" font-size="13" '
             f'fill="{C["stone600"]}" text-anchor="middle">Microwave for 12 minutes before consumption</text>')
    return "".join(g)

# =========================================================================
#  side panels — solid green, minimal
# =========================================================================
def side_panel(w, label):
    g = [f'<rect width="{w}" height="{BW}" fill="{C["green700"]}"/>']
    g.append(f'<text x="{w/2}" y="{BW/2}" font-family="{MONO}" font-weight="700" font-size="14" '
             f'letter-spacing="3" fill="{C["pink300"]}" text-anchor="middle" dominant-baseline="central" '
             f'transform="rotate(-90 {w/2} {BW/2})" style="text-transform:uppercase">{esc(label)}</text>')
    return "".join(g)

# =========================================================================
#  back panel (rotated 180 on the wrap) — clean, with the menu QR
# =========================================================================
def back_panel():
    cx = P_BOT / 2
    g = [f'<rect width="{P_BOT}" height="{BW}" fill="{C["cream50"]}"/>']
    wm, ww = wordmark(cx, 34, 66, C["hero"], anchor="middle")
    g.append(wm)
    g.append(f'<text x="{cx}" y="132" font-family="{BODY}" font-weight="600" font-size="15" '
             f'fill="{C["green900"]}" text-anchor="middle">So good you\'ll forget it\'s healthy</text>')
    g.append(qr_block(cx, 232, 96, C["green900"], caption="SCAN FOR THE MENU", cap_fill=C["stone600"], cap_size=10))
    g.append(f'<text x="{cx}" y="330" font-family="{MONO}" font-size="11" letter-spacing="1" '
             f'fill="{C["stone600"]}" text-anchor="middle">proteinplease.in</text>')
    return "".join(g)

def glue_flap():
    return (f'<rect width="{P_GLUE}" height="{BW}" fill="{C["cream300"]}" opacity="0.5"/>'
            f'<text x="{P_GLUE/2}" y="{BW/2}" font-family="{MONO}" font-size="9" fill="{C["stone600"]}" '
            f'text-anchor="middle" dominant-baseline="central" transform="rotate(-90 {P_GLUE/2} {BW/2})">GLUE FLAP</text>')

# =========================================================================
def build(out_name, title):
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ART_W/UPI:.3f}in" '
        f'height="{ART_H/UPI:.3f}in" viewBox="0 0 {ART_W:.1f} {ART_H:.1f}">',
        f'<title>{esc(title)}</title>', FONT_DEFS,
        f'<rect width="{ART_W:.1f}" height="{ART_H:.1f}" fill="{C["cream50"]}"/>',
        f'<g transform="translate({X_TOP},{b})">{hero_front()}</g>',
        f'<g transform="translate({X_FRONT},{b})">{side_panel(P_SIDE, "HIGH PROTEIN · REAL FOOD · THANE")}</g>',
        f'<g transform="translate({X_BOT},{b})">{back_panel()}</g>',
        f'<g transform="translate({X_BACK},{b})">{side_panel(P_SIDE, "SO GOOD YOU\'LL FORGET IT\'S HEALTHY")}</g>',
        f'<g transform="translate({X_GLUE},{b})">{glue_flap()}</g>']
    for fx in FOLDS:
        parts.append(f'<line x1="{fx}" y1="{b}" x2="{fx}" y2="{b+BW}" stroke="{C["yolk"]}" '
                     f'stroke-width="0.8" stroke-dasharray="5 4" opacity="0.9"/>')
    parts.append(f'<rect x="{b}" y="{b}" width="{P_TOP+2*P_SIDE+P_BOT+P_GLUE}" height="{BW}" '
                 f'fill="none" stroke="{C["green900"]}" stroke-width="0.6" opacity="0.4"/>')
    parts.append('</svg>')
    with open(os.path.join(HERE, out_name), "w") as f:
        f.write("\n".join(parts))
    return out_name

out = build("sleeve.svg", "Protein Please — sleeve")
print("wrote:", out)
print(f"artboard: {ART_W/UPI:.3f}in x {ART_H/UPI:.3f}in | front panel {W}in x {BAND}in")
