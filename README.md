# Karla's Agency — website (staging)

Static site for Karla's Agency, a local digital marketing agency.

## Pages
- `index.html` — Home
- `services.html` — All services in detail
- `industries.html` — Industries served
- `pricing.html` — Packages, comparison, add-ons, one-time projects
- `social.html` — Social media content examples (sample brands)
- `about.html` — About and how we work
- `checklist.html` — Interactive Google Business Profile checklist
- `contact.html` — Free marketing audit request

## Structure
- `src/` — page content (one file per page)
- `style.css`, `site.js` — shared styles and scripts
- `build.py` — wraps each page with the shared nav and footer and writes the finished site to `dist/`

Run `python3 build.py` after editing, then deploy the `dist/` folder (Cloudflare Pages: build output directory `dist`).

## Before launch
- Replace the placeholder email `hello@karlasagency.com` (in `build.py`, `site.js` and `src/`).
