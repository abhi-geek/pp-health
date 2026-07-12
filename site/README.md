# Protein Please — website

A single-page site to get people excited about the brand and collect early-access interest via a Google Form. Built pre-launch for the Thane tryout batches.

## The one thing you need to do: wire up the Google Form

1. Open `index.html`.
2. Scroll to the very bottom, to the `<script>` block.
3. Change this line:
   ```js
   const GOOGLE_FORM_URL = "#";
   ```
   to your live form link, e.g.
   ```js
   const GOOGLE_FORM_URL = "https://forms.gle/your-form-id";
   ```

That's it — every "Get early access / Save my spot / Grab early access" button on the page now points to your form (and opens it in a new tab). Until you set it, those buttons just scroll to the sign-up section.

## Publishing it (proteinplease.in)

The site is plain HTML/CSS — no build step. Upload the whole `site/` folder to any static host:

- **Netlify / Vercel / Cloudflare Pages** — drag-and-drop the `site` folder, then point `proteinplease.in` at it.
- **GitHub Pages** — push `site/` and enable Pages.

Keep the `assets/` folder next to `index.html`.

## What's in `assets/`

- `logo.svg` / `.png` — primary wordmark (green), the master logo
- `logo-pink.svg`, `logo-cream.svg`, `logo-mono.svg` — variants for dark/green backgrounds
- `logo-on-cream.png`, `logo-on-green.png` — ready-to-use with a background
- `logo-mark.svg` / `logo-mark-dark.svg` — the soup-bowl logo-mark (light / dark tile), used as the site mark and favicon
- `impact.woff2` — the Impact display font, self-hosted
- `favicon.png`, `favicon-32.png` — browser tab icon (soup-bowl mark)
- `hero-banner.jpg` — wide hero strip; `founder-real.jpg` — branded-box photo in the chef's note
- `og-image.jpg` — social share preview (WhatsApp / Instagram link / etc.)
- `meal-*.jpg` — product photos

## Editing copy

All text lives directly in `index.html` — search for the words you want to change. The founder note (signed by Shruti) is in the section marked `<!-- FOUNDER NOTE -->`.

## Notes

- Colours, type and voice all follow the brand book.
- The brand book HTML was also updated so its display font is **Impact** (a backup of the original is saved as `Protein Please brand book.ORIGINAL.html` in the `brand-book` folder).
