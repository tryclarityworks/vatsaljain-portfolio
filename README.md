# Portfolio website

An editorial, responsive static portfolio. Five project stories, two notes, an about section, work filters, and email/social links. Contact opens the visitor's email app; there is no contact-form backend, analytics, account system, or database.

## Edit and preview

```sh
python3 website/build.py
python3 website/check.py
node --check website/static/app.js
python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist
```

Open http://127.0.0.1:4173. The server can be stopped with Ctrl+C.

- `content.json`: all public biography, project, and note content.
- `templates/shell.html`: shared head, navigation, footer, and person metadata.
- `build.py`: generates the home page, project pages, note pages, 404, sitemap, and robots file.
- `static/`: styles, JS, portrait, favicon, and social graphic.
- `dist/`: generated deployable files; rebuild after edits.
- `.openai/hosting.json`: Sites identity and static output directory.

The build only reads these public sources. Private profile and career files are never copied. Source resumes are not offered as a public download; tailored applications should use the appropriate attachment privately.

## Design and assets

Warm paper, charcoal, blue accents, Manrope/DM Sans with system fallbacks, and an italic serif emphasis. Google Fonts is an external font request; the site remains readable without it. Portrait reused from Vatsal's public Clarity Works site: https://www.tryclarityworks.com/brand/vatsal.jpg. Workflow diagrams are simplified explanatory views, not product screenshots.

Social metadata uses a 1200×630 PNG rendered from the editable `social.svg`. Verify rich previews on the target platform at public launch.

## Hosting

Read [launch status](../operations/launch-status.md). Hosted changes must reuse the existing Site ID and the Sites skill's source-sync/package/deploy workflow. The Site starts private. No registrar or DNS credentials are stored here.
