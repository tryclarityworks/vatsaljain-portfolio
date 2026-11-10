# Portfolio website

Personal portfolio for Vatsal Jain, developed with AI assistance. This source repository contains the static-site builder, content, template, checks and public assets. The private career workspace is maintained separately.

A concise, responsive personal portfolio for hiring teams. The homepage introduces Vatsal and previews selected projects. Dedicated Work, About, Notes & videos, and Contact pages organize six project stories, a biography and method, two notes, two public video links, work filters, and calendar/email/social links. Infnty is explicitly labeled under development. Content and personal photos are adapted from the user's Clarity Works website with explicit permission. Booking opens the verified Cal.com introductory-call page, with email retained as an alternative. There is no contact-form backend, account system, or database. Production pages use Vercel Web Analytics.

`content.json` holds the public `booking.url` and `booking.duration_minutes`. The navigation and contact section share these settings. The calendar is an ordinary link; no embedded widget or third-party calendar script loads on the portfolio. If `booking` is removed, those actions fall back to email.

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
- `media.json`: responsive image variants, dimensions, sizes, and local font paths.
- `templates/shell.html`: shared head, navigation, footer, and person metadata.
- `build.py`: generates the home page, project pages, note pages, 404, sitemap, and robots file.
- `static/`: styles, JS, portrait, favicon, and social graphic.
- `dist/`: generated deployable files, ignored by Git; rebuild after edits.
- `vercel.json`: the selected host's build, routing, and domain redirect configuration.
- `.vercelignore`: public build-source upload allowlist.

The build only reads these public sources. Private profile and career files are never copied. Source resumes are not offered as a public download; tailored applications should use the appropriate attachment privately.

## Design and assets

The [user-selected palette](https://coolors.co/bfbdc1-6d6a75-37323e-deb841-de9e36) remains the source of color tokens in `static/style.css`: dark plum for text and dark surfaces, gold for the primary action and contact field, amber for hover feedback, and gray tones for supporting surfaces. Dark text on gold preserves contrast. [DESIGN.md](DESIGN.md) records the implemented tokens and component behavior; [PRODUCT.md](PRODUCT.md) records audience and factual constraints.

The October 28 redesign pairs a larger portrait and personal introduction with project-led visual previews and clear paths through the multipage site. The Work page contains all six projects, while About, Notes & videos, and Contact each have a dedicated page. Existing case-study and note routes preserve the supporting evidence; original homepage fragment links still land on relevant sections. The public `home` block in `content.json` owns homepage-specific summaries; full project records remain the source for the case-study pages. Canadian citizenship is visible in the shared public work context and photo captions. Work-arrangement details use an accessible native disclosure near the contact action.

Typography uses self-hosted Manrope/DM Sans Latin WOFF2 fonts with system fallbacks. The shared head preloads both fonts and embeds the stylesheet, avoiding an external font/CSS request chain. Redistributed fonts retain SIL Open Font Licenses in `static/assets/fonts/`.

Project filtering is keyboard accessible and announces the visible count. Filters appear only after JavaScript initializes; all six projects remain readable without JavaScript. Directional icons are authored inline SVG, hidden from screen readers and keyboard focus, so mobile browsers cannot replace them with emoji glyphs. The portrait settling and ordered workflow-step entrances add brief orientation. Surface-specific focus rings remain legible around both gold and dark actions; video links use play icons and short summaries. Reduced motion removes travel and animated clipping, including when changed during the visit; content remains visible without JavaScript.

Two photos come from [Clarity Works](https://www.tryclarityworks.com/about); the video thumbnails link to Vatsal's own published videos. These assets are reused with the owner's permission. Photos/thumbnails use responsive AVIF sources and WebP fallbacks, with original JPEGs retained. Below-fold images load lazily, and intrinsic dimensions reserve their layout space. Workflow diagrams are simplified explanatory views, not product screenshots.

Optimized media/font filenames contain content hashes and receive immutable one-year cache headers. The deferred app script uses a content-hash query version for the same cache policy. Original images and social assets keep their existing URLs. When an image changes, regenerate its optimized variants and update `media.json` before rebuilding. Media generation is offline; the deployed Python build has no package installation or image-processing dependency.

Social metadata uses a 1200×630 PNG rendered from the editable `social.svg`. Verify rich previews on the target platform at public launch.

## Web Analytics

The shared HTML template includes Vercel's supported tracking snippet when `VERCEL_ENV=production`. It loads the deferred script at `/_vercel/insights/script.js` to count visitors and page views on every production page. Local and preview builds omit tracking. This static site uses the HTML integration, so no Next.js component, npm dependency, or JavaScript bundler is required. See [Vercel's setup guide](https://vercel.com/docs/analytics/quickstart).

Web Analytics must remain enabled in the existing Vercel project. Verify the script returns JavaScript and the browser's page-view request succeeds after deployment. Counts are available in that project's Analytics dashboard.

## Hosting

**Vercel** is the chosen production host for **vatsaljain.com**, using its standalone public GitHub source repository, `tryclarityworks/vatsaljain-portfolio`.

Import this repository into Vercel with root directory `.` and framework preset Other. Vercel reads `vercel.json`, builds with `python3 build.py && python3 check.py`, and serves only `dist/`. There are no Python packages to install; the standard build image provides Python. Production branch: `main`. Canonicals, sitemap, and social metadata default to `https://vatsaljain.com`; preview builds are marked noindex. No environment variables are required.

Attach `vatsaljain.com` and `www.vatsaljain.com` to the Vercel project, then use its returned DNS recommendations. Manage the primary-domain redirect in Vercel's Domains settings; do not add a reverse host redirect in `vercel.json`. The active domain configuration redirects the apex to `www`. Do not change mail or other unrelated DNS records.

The portfolio manager keeps private operations and deployment records outside this repository. Historical hosting identity, Vercel local state, credentials, and generated output are ignored. No registrar or DNS credentials are stored here.
