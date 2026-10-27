# The Energy Gazette: Venezuela Edition

Website for The Energy Gazette, served at **abaxgrid.com/energygazette** (GitHub Pages, custom domain set on `abaxgrid.github.io`).

A publication of AbaxGrid · Proactivados, S.A. · Founder & Editor: Danny Peña.

## What is here

| Path | What it is |
|---|---|
| `index.html` | The whole site: latest issues, timeline, fiscal take calculator, archive, reference desk, next issue, editor page, map drawer, news and facts tickers, EN/ES/PT switch, dark theme only |
| `maps/venezuela.json` | Map data for the Venezuela chapter (Natural Earth 10m, simplified lon/lat arrays) |
| `assets/portrait.png` | Editor portrait |
| `i18n/es.json`, `i18n/pt.json` | Spanish and Portuguese (pt-BR) dictionaries. Keys are the English strings as shown on the page. English is the default; the page carries its own copy of both dictionaries inline, so after editing a file here ask Claude to sync it into `index.html` |
| `en/`, `es/`, `pt/` | Share links with their own WhatsApp/social preview (`assets/share-eg-*.jpg`); each opens the site in that language |
| `tools/build_deploy.py` | Rebuilds `index.html` and the share pages from the page source |
| `tools/mapkit/` | Builder and geography checks for map chapters (`build_region.py`, `verify.py`, one config per chapter) |
| `issues/` | Edition PDFs (to upload, see below) |
| `.nojekyll` | Tells GitHub Pages to serve files as they are |

## Files still to upload

The page already links to these. Upload them with exactly these names or the links will 404.

**`issues/`**
- `issue-04-procurement-signal.pdf` (Issue No. 4, executive brief)
- `issue-03-gold-rush.pdf` (Issue No. 3, magazine sample)
- `issue-02-full.pdf`, `issue-02-brief.pdf` (Issue No. 2)
- `issue-01-full.pdf`, `issue-01-carousel.pdf` (Issue No. 1)
- `special-anatomy-oil-mou-brief.pdf` (Special, Anatomy of an Oil MoU)
- `special-national-added-value.pdf` (Special, National Added Value FAQ)
- `briefing-operators-tracker.pdf` (Briefing, Who's Operating in Venezuela)

**`tools/`** (in the repo: `operators-tracker.html`, `supply-chain-eras.html`)
- `ofac-licensing.html` and `relationship-matrix.pdf` are not built yet; the page shows them as "on request". When they exist, add them here and switch their cards back to direct links.

## Updating the tickers

- **News:** the `<li>` items inside `#tk-track` in `index.html`.
- **Prices and results calendar:** the JSON block `<script type="application/json" id="eg-markets">`. Change `asOf`, the prices and daily changes, and the calendar dates. Past dates drop off the ticker automatically.
