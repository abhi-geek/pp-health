#!/usr/bin/env python3
"""
Protein Please — meal-box sleeve (belly band) generator.

Box: L 6.4in x W 4.5in x H 2.0in.
The sleeve is a closed loop around the girth perpendicular to the length:
    girth = 2*(W + H) = 2*(4.5 + 2.0) = 13.0in  (+ 0.5in glue flap)
Band width (extent along the 6.4in length) = 3.6in. Front panel = 4.5in x 3.6in.

Brand language matches the website: the soup Lucide mark, the real
"Protein Please" wordmark (assets/logo-cream.svg), and ✳ stars. No flowers.
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

# ---- soup Lucide mark (matches the site header) -------------------------
SOUP = ('<path d="M12 21a9 9 0 0 0 9-9H3a9 9 0 0 0 9 9Z"/><path d="M7 21h10"/>'
        '<path d="M19.5 12 22 6"/>'
        '<path d="M16.25 3c.27.1.8.53.75 1.36-.06.83-.93 1.2-1 2.02-.05.78.34 1.24.73 1.62"/>'
        '<path d="M11.25 3c.27.1.8.53.74 1.36-.05.83-.93 1.2-.98 2.02-.06.78.33 1.24.72 1.62"/>'
        '<path d="M6.25 3c.27.1.8.53.75 1.36-.06.83-.93 1.2-1 2.02-.05.78.34 1.24.74 1.62"/>')

def mark(x, y, size, dark=True):
    """The soup mark in a rounded tile (like the website logo mark)."""
    s = size / 48
    if dark:
        tile = f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size*13/48:.1f}" fill="{C["green800"]}" stroke="{C["green600"]}" stroke-width="1.5"/>'
        icol = C["cream50"]
    else:
        tile = f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size*13/48:.1f}" fill="{C["cream50"]}" stroke="{C["cream300"]}" stroke-width="1.5"/>'
        icol = C["green800"]
    icon = (f'<g transform="translate({x+12*s:.2f},{y+12*s:.2f}) scale({s:.4f})" '
            f'fill="none" stroke="{icol}" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round">{SOUP}</g>')
    return tile + icon

def soup_glyph(cx, cy, size, color, opacity=1.0, sw=2.0):
    """A standalone soup Lucide glyph (subtle brand motif)."""
    s = size / 24
    return (f'<g transform="translate({cx-size/2:.1f},{cy-size/2:.1f}) scale({s:.4f})" '
            f'fill="none" stroke="{color}" stroke-width="{sw/s:.3f}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="{opacity}">{SOUP}</g>')

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

def eyebrow(x, y, text, color, size=12, ls=3):
    return (star(x+6, y-4, 6, color, 2) +
            f'<text x="{x+18}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'letter-spacing="{ls}" fill="{color}" style="text-transform:uppercase">{esc(text)}</text>')

def pill(x, y, label, color, marker=False, fs=10.5, pad=11):
    w = pad*2 + len(label)*fs*0.62
    h = fs + 12
    inx = x + pad
    mk = ""
    if marker:
        mk = (f'<rect x="{x+8}" y="{y+h/2-4.5}" width="9" height="9" rx="2.5" fill="none" '
              f'stroke="{color}" stroke-width="1.6"/><circle cx="{x+12.5}" cy="{y+h/2}" r="2.4" fill="{color}"/>')
        inx = x + 24; w += 14
    txt = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" fill="none" '
           f'stroke="{color}" stroke-width="1.4"/>{mk}'
           f'<text x="{inx:.1f}" y="{y+h/2:.1f}" font-family="{BODY}" font-weight="700" '
           f'font-size="{fs}" letter-spacing="0.8" fill="{color}" dominant-baseline="central" '
           f'style="text-transform:uppercase">{esc(label)}</text>')
    return txt, w

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

# =========================================================================
#  HERO — named dish
# =========================================================================
def hero_named(name1, name2, desc1, desc2, instruction, best_before, macros, veg=True):
    g = [f'<rect width="{P_TOP}" height="{BW}" fill="{C["green800"]}"/>']
    g.append(f'<clipPath id="hc"><rect width="{P_TOP}" height="{BW}"/></clipPath>')
    # left strip: a couple of ✳ stars only (site motif, kept minimal)
    g.append(f'<g clip-path="url(#hc)">'
             + star(42, 150, 13, C["pink500"], 3)
             + star(56, 244, 8, C["green600"], 2.4) + '</g>')
    cx0, cy0, cw, ch = 84, 12, 354, 286
    g.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="14" fill="{C["cream50"]}"/>')
    tx = 104
    g.append(f'<text x="{tx}" y="60" font-family="{DISPLAY}" font-weight="700" font-size="42" '
             f'textLength="316" lengthAdjust="spacingAndGlyphs" letter-spacing="-0.5" '
             f'fill="{C["green900"]}" style="text-transform:uppercase">{esc(name1)}</text>')
    g.append(f'<text x="{tx}" y="102" font-family="{DISPLAY}" font-weight="700" font-size="42" '
             f'letter-spacing="-0.5" fill="{C["green900"]}" style="text-transform:uppercase">{esc(name2)}</text>')
    g.append(f'<text x="{tx}" y="130" font-family="{BODY}" font-weight="600" font-size="11.5" '
             f'letter-spacing="0.5" fill="{C["stone600"]}" style="text-transform:uppercase">{esc(desc1)}</text>')
    g.append(f'<text x="{tx}" y="146" font-family="{BODY}" font-weight="600" font-size="11.5" '
             f'letter-spacing="0.5" fill="{C["stone600"]}" style="text-transform:uppercase">{esc(desc2)}</text>')
    p1, w1 = pill(tx, 162, "VEG" if veg else "NON-VEG", C["leaf"] if veg else C["tomato"], marker=True)
    p2, _ = pill(tx+w1+10, 162, "HIGH PROTEIN", C["green700"])
    g.append(p1 + p2)
    iy = 206
    g.append(f'<text x="{tx}" y="{iy}" font-family="{MONO}" font-size="8.5" letter-spacing="1" '
             f'font-weight="700" fill="{C["green900"]}">INSTRUCTIONS</text>')
    for j, ln in enumerate(instruction):
        g.append(f'<text x="{tx}" y="{iy+15+j*14}" font-family="{BODY}" font-size="10.5" '
                 f'fill="{C["stone600"]}">{esc(ln)}</text>')
    bby = iy + 38
    g.append(f'<rect x="{tx}" y="{bby}" width="118" height="42" rx="7" fill="none" stroke="{C["green800"]}" stroke-width="1.5"/>')
    g.append(f'<text x="{tx+11}" y="{bby+16}" font-family="{MONO}" font-size="7.5" letter-spacing="0.8" fill="{C["stone600"]}">BEST BEFORE</text>')
    g.append(f'<text x="{tx+11}" y="{bby+34}" font-family="{DISPLAY}" font-weight="700" font-size="21" fill="{C["green900"]}">{esc(best_before)}</text>')
    mx0, my, cellw = 250, 208, 43
    for i, (lab, val) in enumerate(macros):
        cxm = mx0 + i*cellw
        if i:
            g.append(f'<line x1="{cxm-4}" y1="{my-4}" x2="{cxm-4}" y2="{my+50}" stroke="{C["cream300"]}" stroke-width="1"/>')
        g.append(f'<text x="{cxm}" y="{my+6}" font-family="{MONO}" font-size="8" letter-spacing="0.5" fill="{C["stone600"]}">{lab}</text>')
        g.append(f'<text x="{cxm}" y="{my+34}" font-family="{DISPLAY}" font-weight="700" font-size="23" fill="{C["green900"]}">{val}</text>')
    # brand bar — real logo mark + wordmark (kept clear of the bottom fold)
    y0 = 298; h = BW - y0
    g.append(f'<rect x="0" y="{y0}" width="{P_TOP}" height="{h}" fill="{C["green900"]}"/>')
    g.append(mark(18, 306, 34, dark=True))
    wm, ww = wordmark(62, 310, 26, C["cream50"])
    g.append(wm)
    g.append(f'<text x="{P_TOP-14}" y="{y0+h*0.44:.0f}" font-family="{BODY}" font-weight="700" '
             f'font-size="11" fill="{C["pink300"]}" text-anchor="end">HIGH-PROTEIN MEALS</text>')
    g.append(f'<text x="{P_TOP-14}" y="{y0+h*0.76:.0f}" font-family="{BODY}" font-size="10" '
             f'fill="{C["green100"]}" text-anchor="end">so good you\'ll forget it\'s healthy</text>')
    return "".join(g)

# =========================================================================
#  HERO — generic
# =========================================================================
def hero_generic():
    g = [f'<rect width="{P_TOP}" height="{BW}" fill="{C["green800"]}"/>']
    g.append(eyebrow(30, 46, "Fresh from our kitchen", C["pink300"]))
    # real wordmark, cream (matches the website logo)
    wm, ww = wordmark(30, 62, 120, C["cream50"])
    g.append(wm)
    g.append(star(ww + 46, 150, 16, C["pink300"], 5))
    note = ["Real ingredients, plenty of", "protein & a whole lot of love", "in every box. Eat well today."]
    for i, ln in enumerate(note):
        g.append(f'<text x="32" y="{212+i*22}" font-family="{BODY}" font-weight="600" '
                 f'font-size="15" fill="{C["green100"]}">{esc(ln)}</text>')
    g.append(f'<text x="32" y="{212+3*22+8}" font-family="{BODY}" font-style="italic" '
             f'font-weight="700" font-size="14.5" fill="{C["pink300"]}">— Shruti, Chef &amp; fellow Protein Paglu</text>')
    g.append(f'<text x="360" y="150" font-family="{MONO}" font-size="10" letter-spacing="1" '
             f'fill="{C["cream50"]}" text-anchor="middle">proteinplease.in</text>')
    g.append(qr_block(360, 236, 110, C["green900"], caption="SCAN FOR THE MENU", cap_fill=C["cream50"]))
    return "".join(g)

# =========================================================================
#  side panels
# =========================================================================
def side_panel(w, primary):
    g = [f'<rect width="{w}" height="{BW}" fill="{C["green700"]}"/>',
         star(w/2, 34, 8, C["pink500"], 2.4), star(w/2, BW-34, 8, C["pink500"], 2.4)]
    if primary:
        wm, ww = wordmark(0, 0, 92, C["cream50"])  # placed rotated below
        g.append(f'<g transform="translate({w/2},{BW/2}) rotate(-90) translate({-ww/2:.1f},-46)">{wm}</g>')
    else:
        g.append(f'<text x="{w/2}" y="{BW/2}" font-family="{MONO}" font-weight="700" font-size="14" '
                 f'letter-spacing="3" fill="{C["pink300"]}" text-anchor="middle" dominant-baseline="central" '
                 f'transform="rotate(-90 {w/2} {BW/2})" style="text-transform:uppercase">HIGH PROTEIN · REAL FOOD · THANE</text>')
    return "".join(g)

# =========================================================================
#  bottom panel (the "back") — now UPRIGHT
# =========================================================================
def bottom_panel():
    g = [f'<rect width="{P_BOT}" height="{BW}" fill="{C["cream50"]}"/>']
    g.append(star(46, 52, 10, C["pink500"], 2.6))
    g.append(star(P_BOT-46, BW-52, 10, C["pink500"], 2.6))
    cx = P_BOT/2
    wm, ww = wordmark(cx, 24, 40, C["green800"], anchor="middle")
    g.append(wm)
    g.append(f'<g transform="translate({cx-92},92)">' + eyebrow(0, 0, "A note from the chef", C["stone600"], 10, 2.2) + '</g>')
    g.append(f'<text x="{cx}" y="132" font-family="{DISPLAY}" font-weight="700" font-size="26" '
             f'fill="{C["green800"]}" text-anchor="middle">Thank you for letting me cook for you.</text>')
    g.append(f'<text x="{cx}" y="160" font-family="{BODY}" font-size="14" fill="{C["stone600"]}" '
             f'text-anchor="middle">Made fresh, with real ingredients and plenty of protein.</text>')
    g.append(f'<text x="{cx}" y="182" font-family="{BODY}" font-style="italic" font-weight="700" '
             f'font-size="14" fill="{C["green700"]}" text-anchor="middle">— Shruti</text>')
    g.append(qr_block(cx, 268, 88, C["green900"], caption="proteinplease.in", cap_fill=C["stone600"], cap_size=10))
    return "".join(g)

def glue_flap():
    return (f'<rect width="{P_GLUE}" height="{BW}" fill="{C["cream300"]}" opacity="0.5"/>'
            f'<text x="{P_GLUE/2}" y="{BW/2}" font-family="{MONO}" font-size="9" fill="{C["stone600"]}" '
            f'text-anchor="middle" dominant-baseline="central" transform="rotate(-90 {P_GLUE/2} {BW/2})">GLUE FLAP</text>')

# =========================================================================
def build(hero, out_name, title, back_primary=True):
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ART_W/UPI:.3f}in" '
        f'height="{ART_H/UPI:.3f}in" viewBox="0 0 {ART_W:.1f} {ART_H:.1f}">',
        f'<title>{esc(title)}</title>', FONT_DEFS,
        f'<rect width="{ART_W:.1f}" height="{ART_H:.1f}" fill="{C["green800"]}"/>',
        f'<g transform="translate({X_TOP},{b})">{hero}</g>',
        f'<g transform="translate({X_FRONT},{b})">{side_panel(P_SIDE, False)}</g>',
        f'<g transform="translate({X_BOT},{b})">{bottom_panel()}</g>',
        f'<g transform="translate({X_BACK},{b})">{side_panel(P_SIDE, back_primary)}</g>',
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

named = hero_named("PANEER POWER", "BOWL",
    "SPICED PANEER, BROWN RICE, CHARRED VEG", "& A COOL MINT-CURD DRIZZLE",
    ["Microwave 2–2.5 mins,", "or enjoy it cold."], "3 DAYS",
    [("CAL","480"),("PRO","38g"),("FAT","16g"),("CAR","42g")], veg=True)
p1 = build(named, "sleeve-paneer-power-bowl.svg", "Protein Please — Paneer Power Bowl sleeve")
p2 = build(hero_generic(), "sleeve-generic.svg", "Protein Please — generic sleeve")
print("wrote:", p1, "+", p2)
print(f"artboard: {ART_W/UPI:.3f}in x {ART_H/UPI:.3f}in | front panel {W}in x {BAND}in")
