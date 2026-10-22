# Portfolio website

An editorial, responsive static portfolio. Five project stories, two notes, an about section, a four-step working method, two public video links, work filters, and email/social links. Content and personal photos are adapted from the user's Clarity Works website with explicit permission. Contact opens the visitor's email app; there is no contact-form backend, account system, or database. Production pages use Vercel Web Analytics.

## Edit and preview

```sh
# Run from this repository's root (website/ in the portfolio manager).
python3 build.py
python3 check.py
node --check static/app.js
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4173. The server can be stopped with Ctrl+C.

- `content.json`: all public biography, project, and note content.
- `templates/shell.html`: shared head, navigation, footer, and person metadata.
- `build.py`: generates the home page, project pages, note pages, 404, sitemap, and robots file.
- `static/`: styles, JS, portrait, favicon, and social graphic.
- `dist/`: generated deployable files, ignored by Git; rebuild after edits.
- `vercel.json`: the selected host's build, routing, and domain redirect configuration.
- `.vercelignore`: public build-source upload allowlist.

The build only reads these public sources. Private profile and career files are never copied. Source resumes are not offered as a public download; tailored applications should use the appropriate attachment privately.

## Design and assets

The [user-selected palette](https://coolors.co/bfbdc1-6d6a75-37323e-deb841-de9e36) sets the color tokens in `static/style.css`: gray `#BFBDC1` for borders, muted gray `#6D6A75` for supporting text, dark plum `#37323E` for text and the contact panel, gold `#DEB841` for buttons and emphasis, and amber `#DE9E36` for hover states and decorative accents. Pale gray and gold tints provide page and diagram surfaces. Buttons use dark text, and supporting text switches to dark plum on the gray panels to preserve contrast.

Typography uses Manrope/DM Sans with system fallbacks and an italic serif emphasis. Google Fonts is an external font request; the site remains readable without it. Two photos come from [Clarity Works](https://www.tryclarityworks.com/about); the video thumbnails link to Vatsal's own published videos. These assets are reused with the owner's permission. Workflow diagrams are simplified explanatory views, not product screenshots.

Social metadata uses a 1200×630 PNG rendered from the editable `social.svg`. Verify rich previews on the target platform at public launch.

## Web Analytics

The shared HTML template includes Vercel's supported tracking snippet when `VERCEL_ENV=production`. It loads the deferred script at `/_vercel/insights/script.js` to count visitors and page views on every production page. Local and preview builds omit tracking. This static site uses the HTML integration, so no Next.js component, npm dependency, or JavaScript bundler is required. See [Vercel's setup guide](https://vercel.com/docs/analytics/quickstart).

Web Analytics must remain enabled in the existing Vercel project. Verify the script returns JavaScript and the browser's page-view request succeeds after deployment. Counts are available in that project's Analytics dashboard.

## Hosting

**Vercel** is the chosen production host for **vatsaljain.com**, using a dedicated private GitHub repository, `tryclarityworks/vatsaljain-portfolio`.

Import this repository into Vercel with root directory `.` and framework preset Other. Vercel reads `vercel.json`, builds with `python3 build.py && python3 check.py`, and serves only `dist/`. There are no Python packages to install; the standard build image provides Python. Production branch: `main`. Canonicals, sitemap, and social metadata default to `https://vatsaljain.com`; preview builds are marked noindex. No environment variables are required.

Attach `vatsaljain.com` and `www.vatsaljain.com` to the Vercel project, then use its returned DNS recommendations. Manage the primary-domain redirect in Vercel's Domains settings; do not add a reverse host redirect in `vercel.json`. The active domain configuration redirects the apex to `www`. Do not change mail or other unrelated DNS records.

The portfolio manager keeps private operations and deployment records outside this repository. Historical hosting identity, Vercel local state, credentials, and generated output are ignored. No registrar or DNS credentials are stored here.
