# Protein Please — creatives

Print-ready meal-box **sleeve (belly-band)** artwork.

## Box & sleeve geometry
Box: **L 6.4 in × W 4.5 in × H 2.0 in.**

The sleeve is a closed loop around the box girth (perpendicular to the 6.4 in
length), so it slides on like a belly band and leaves ~1.4 in of the tray
visible above and below it — just like the reference.

| Spec | Value |
|---|---|
| Loop / wrap circumference | 2 × (W + H) = **13.0 in** |
| Glue flap | **0.5 in** |
| Total flat length (trim) | **13.5 in** |
| Band width (along the length) | **3.6 in** |
| Front (top-face) panel | **4.5 in × 3.6 in** |
| Bleed | **0.125 in** all sides → artboard 13.75 in × 3.85 in |

Panel order across the flat wrap (left → right):
**TOP/front → tray side → BOTTOM (back: wordmark + menu QR, rotated 180°) → tray side → glue flap.**
Fold lines are the dashed gold guides; the thin outline is the trim edge.

## Front layout (approved)
A single, deliberately **simple** front, top → bottom:
- the **Protein Please** wordmark (small) in forest green,
- the tagline *“So good you'll forget it's healthy”*,
- the three plan points (Veg & Non-Veg / Thoughtfully Crafted / Real Ingredients),
- a pink **"grams of protein"** circle with blank space above — **the chef writes the
  protein number by hand before shipping**, and
- the **Keep refrigerated / Microwave for 12 minutes** note.

Sides are solid green with a vertical line each (`HIGH PROTEIN · REAL FOOD · THANE`
and `SO GOOD YOU'LL FORGET IT'S HEALTHY`); the back carries the wordmark + menu QR.

## Files
| File | What |
|---|---|
| `sleeve.svg` | The sleeve — master vector. Simple approved front (see above); solid-green sides; cream back with the menu QR. |
| `sleeve.png` | 300 DPI raster preview (4125 × 1155 px), rendered from the SVG. |
| `qr-proteinplease.svg` / `.png` | Standalone QR → **https://proteinplease.in/** (error-correction H). |
| `_build_sleeves.py`, `_qr-path.txt` | Generator + QR data. Re-run `python3 _build_sleeves.py` to rebuild the SVG, then render the PNG (below). |
| `archive/` | Previous, un-approved sleeve designs (generic + paneer-power-bowl) and their old generator, kept for reference. |

Render the PNG after building:
```
python3 _build_sleeves.py
cairosvg sleeve.svg -o sleeve.png --output-width 4125   # 300 DPI
```

## QR
Encodes `https://proteinplease.in/`, high error-correction (~30%), verified to
decode with OpenCV. It appears on the back panel as **SCAN FOR THE MENU**. Keep it
≥ 0.8 in on the final print.

## Fonts
The brand display face (**Impact PP**, from `../assets/impact.woff2`) is embedded
directly in the SVGs, so they render correctly in any browser or Illustrator.
Body/labels use **Hanken Grotesk** and **Space Mono** (the site's fonts).
**Before sending to print, outline all fonts** (or supply the font files) so the
printer doesn't substitute them.

## Colours (brand book)
Greens `#13200E → #4A7039`, pinks `#EFCFDF / #E8BBD3 / #DCA7C4`,
creams `#FBF8EF / #F6F2E6`, leaf `#3E8E4E`.

## To change the dish / macros
Edit the `hero_named(...)` call at the bottom of `_build_sleeves.py` (name lines,
description, instructions, best-before, macros, veg flag) and re-run it.
