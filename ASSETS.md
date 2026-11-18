# Output capture provenance

Added November 17, 2026. All three captures were produced in installed Google Chrome at 1280×960 from actual local HTML output. They are synthetic-data demonstrations, not live customer/product screenshots.

| Asset | Source | What is shown |
| --- | --- | --- |
| `static/assets/outbound-demo.png` | `tryclarityworks/outbound-orchestration-demo`, `examples/report.html` | Actual six-row fixture run, rendered drafts, one local staging and zero emails sent. The report is a new showcase presentation of existing fixture output. |
| `static/assets/gtm-demo.png` | `tryclarityworks/gtm-intelligence-demo`, `examples/report.html` | Fictional accounts with separate fit, coverage and review states. The demo adapts an earlier scoring module from the private local app; it is not the full app. |
| `static/assets/newsletter-demo.png` | `tryclarityworks/newsletter-pipeline-demo`, `examples/newsletter.html` | Actual newsletter HTML from invented article/model fixtures. No live news, model request or delivery. |

Responsive AVIF/WebP variants at 480, 800 and 1280 pixels are mapped in media.json. Filenames contain the first 12 SHA-256 hex characters of their exact bytes, matching the immutable optimized-asset cache policy. Resizing/encoding used Pillow; there is no image-generation prompt. The original PNGs carry a description of their source and synthetic status.

Original approved portraits and video thumbnails retain their earlier provenance in README.md. Existing fonts retain their SIL Open Font Licenses.

## Tools directory marks

- The monochrome marks use paths from [Simple Icons at revision 17cd4ee](https://github.com/simple-icons/simple-icons/tree/17cd4ee07612198a1d8777a060d4100423762a8b/icons) and the portfolio's ink color.
- The [Scrapling repository mark](https://github.com/D4Vinci/Scrapling/blob/2998c9ebba52ef6116f0a483c7d2f21908250024/docs/assets/logo.png) and [Apify organization mark](https://github.com/apify) are resized to square WebP assets.
- Tools without a sourced mark use initials. Visible labels identify every tool for sighted visitors and assistive technology. Marks are served from the same origin using hashed filenames.
