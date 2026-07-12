# Protein Please — website

A single-page site to get people excited about the brand and collect early-access interest via a Google Form. Built pre-launch for the Thane tryout batches.

## Structure

The website lives at the **repo root** so GitHub Pages serves it directly:

```
index.html        ← the whole site
assets/           ← logos, fonts, photos, icons, favicon
_source/          ← working files (brand book, raw photos) — NOT published
```

`_source/` starts with an underscore, so GitHub Pages (Jekyll) ignores it — the confidential brand book and raw photos stay in the repo but never appear on the live site.

## The Google Form

Already wired to `https://forms.gle/ppdi67NRiSnXVDnN9`. To change it, edit `GOOGLE_FORM_URL` in the `<script>` at the bottom of `index.html` — every early-access button uses it automatically.

## Publishing (GitHub Pages → proteinplease.in)

1. In the repo: **Settings → Pages**.
2. Set **Source: Deploy from a branch**, **Branch: `main`**, **Folder: `/ (root)`**.
3. Save. The site goes live at `https://<user>.github.io/pp-health/`.
4. For `proteinplease.in`: add a custom domain in the same Pages settings and point your DNS at GitHub.

No build step — it's plain HTML/CSS, so it also drag-and-drops onto Netlify / Vercel / Cloudflare Pages.

## What's in `assets/`

- `logo.svg` / `.png` — primary wordmark (green), the master logo
- `logo-pink.svg`, `logo-cream.svg`, `logo-mono.svg` — variants for dark/green backgrounds
- `logo-on-cream.png`, `logo-on-green.png` — ready-to-use with a background
- `logo-mark.svg` / `logo-mark-dark.svg` — the soup-bowl logo-mark (light / dark tile), used as the site mark and favicon
- `impact.woff2` — the Impact display font, self-hosted
- `favicon.png`, `favicon-32.png` — browser tab icon (soup-bowl mark)
- `hero-side.jpg` — square hero photo; `founder-real.jpg` — branded-box photo in the chef's note
- `og-image.jpg` — social share preview (WhatsApp / Instagram link / etc.)
- `meal-*.jpg` — product photos

## Editing copy

All text lives directly in `index.html` — search for the words you want to change. The founder note (signed by Shruti) is in the section marked `<!-- FOUNDER NOTE -->`.

## Notes

- Colours, type and voice all follow the brand book.
- The brand book HTML was also updated so its display font is **Impact** (a backup of the original is saved as `Protein Please brand book.ORIGINAL.html` in `_source/brand-book/`).
