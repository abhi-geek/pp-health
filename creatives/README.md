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
**TOP/front → tray side → BOTTOM (chef note + QR, rotated 180°) → tray side → glue flap.**
Fold lines are the dashed gold guides; the thin outline is the trim edge.

## Files
| File | What |
|---|---|
| `sleeve-paneer-power-bowl.svg` | Named-dish sleeve (flagship layout: dish name, description, VEG / HIGH PROTEIN badges, instructions, best-before, macros, brand bar). Master vector. |
| `sleeve-generic.svg` | Generic sleeve — no dish name. Big Protein Please branding, a warm note from the chef, and the QR. Use on any box. |
| `sleeve-*.png` | ~288 DPI raster previews (rendered from the SVGs). |
| `qr-proteinplease.svg` / `.png` | Standalone QR → **https://www.proteinplease.in** (error-correction H). |
| `_build_sleeves.py`, `_qr-path.txt` | Generator + QR data. Re-run `python3 _build_sleeves.py` to rebuild the SVGs. |

## QR
Encodes `https://www.proteinplease.in`, high error-correction (~30%), verified to
decode with OpenCV on every artboard. It appears on the underside of the named
sleeve and prominently on the generic sleeve. Keep it ≥ 0.8 in on the final print.

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
