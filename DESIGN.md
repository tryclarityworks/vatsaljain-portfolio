---
name: Vatsal Jain Portfolio
description: A personal showcase of practical AI work, grounded in the person and the projects.
colors:
  palette-gray: "#BFBDC1"
  palette-muted: "#6D6A75"
  palette-ink: "#37323E"
  palette-gold: "#DEB841"
  palette-amber: "#DE9E36"
  paper: "#F4F3F5"
  surface: "#E9E8EB"
  surface-warm: "#F8EFD9"
typography:
  display:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "clamp(42px, 4.8vw, 68px)"
    fontWeight: 650
    lineHeight: 1.08
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "clamp(32px, 3.2vw, 44px)"
    fontWeight: 650
    lineHeight: 1.13
    letterSpacing: "-0.035em"
  title:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "24px"
    fontWeight: 650
    lineHeight: 1.13
    letterSpacing: "-0.035em"
  body:
    fontFamily: "DM Sans, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "DM Sans, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  square: "0px"
  avatar: "50%"
spacing:
  8: "8px"
  16: "16px"
  24: "24px"
  32: "32px"
  40: "40px"
  section: "112px"
components:
  button-primary:
    backgroundColor: "{colors.palette-gold}"
    textColor: "{colors.palette-ink}"
    rounded: "{rounded.square}"
    padding: "15px 20px"
  button-primary-hover:
    backgroundColor: "{colors.palette-amber}"
  button-inverse:
    backgroundColor: "{colors.palette-ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.square}"
    padding: "15px 20px"
  filter:
    backgroundColor: "transparent"
    textColor: "{colors.palette-ink}"
    rounded: "{rounded.square}"
    padding: "10px 12px"
  filter-selected:
    backgroundColor: "{colors.palette-ink}"
    textColor: "{colors.paper}"
  note:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.palette-ink}"
    rounded: "{rounded.square}"
    padding: "32px"
  tag:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.palette-ink}"
    rounded: "{rounded.square}"
    padding: "8px 12px"
  status:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.palette-ink}"
    rounded: "{rounded.square}"
    padding: "5px 10px"
---

# Design System: Vatsal Jain Portfolio

## Overview

**Creative North Star: "The Personal Project Bookshelf"**

A photographic, editorial portfolio pairs a direct personal introduction with a collection of specific work. Large plum, cool paper, and gold fields, simple typography, and generous space let the person and projects lead.

The design is flat and rectangular. Project representations use real descriptions and clearly labeled illustration, while approved photographs and original video thumbnails bring a human presence. Content is visible by default; short, optional motion adds orientation without becoming necessary to read or navigate.

**Key Characteristics:**

- A dark opening with a real portrait and selected work.
- Manrope headings and DM Sans text, both self-hosted.
- Square, flat fields and project-specific visual explanations.
- Accessible navigation, visible focus, and restrained motion.

Documented from the October 30, 2026 Hallmark refinement of the October 28 implementation in `static/style.css`, `static/app.js`, `build.py`, `templates/shell.html`, and `media.json`, checked against the final desktop and phone captures in `output/design/2026-10-28/redesign/final/`. The November 17 extension added output captures, a code gallery, and a tools directory. The November 18 refinement aligns the main layouts, brings Tools into the header, and adds repository cards and marks to the directory. Surface composition is recorded in `.impeccable/surfaces/templates-shell-html.md`.

## Colors

The user-pinned plum and gray palette is punctuated with gold and amber; light fields provide reading surfaces.

### Primary

- **Gold:** primary action, announcement, contact and case-workflow fields, selection, and video link mark.
- **Amber:** action hover and link underlines.

### Neutral

- **Plum ink:** dark header, opening, footer, selected filters, case facts and inverse actions; body text on light fields.
- **Cool paper:** body background and text on plum.
- **Cool surface:** note panels, tags, status markers, and filter hover.
- **Palette gray:** the Infnty illustrative field.
- **Muted plum gray:** scrollbar and portrait loading background.
- **Warm surface** supports tool marks and repository link hover states.

**The Gold Contrast Rule.** Gold actions carry dark ink text; pale text is reserved for dark fields.

## Typography

**Display Font:** Manrope, with Arial and sans-serif fallbacks. **Body Font:** DM Sans with the same fallbacks. Both are variable Latin WOFF2 files served locally and preloaded in the shared shell; preserve their licenses and manifest references.

The frontmatter records the opening display and shared heading, title, body, and label defaults. Page mastheads use a larger responsive display (`clamp(54px, 7vw, 96px)`); project titles and contact headings have their own scales. Headings use weight (650), tight tracking and balanced wrapping. Action labels are semibold. Case prose is capped at (72ch); long-form note prose uses (18px) with (1.85) line height until mobile.

## Layout

The centered content area is capped at 1280px. Side gutters are 40px, reducing to 32px, 24px, 20px, and 16px at 1100px, 899px, 620px, and 374px. Section spacing follows the same first three breakpoints. Major side-by-side layouts use a shared gap that scales from 24px to 64px.

Home aligns the introduction and portrait at the top. Selected work uses the full content width below, with three equal visual columns on desktop, rows with media and text on tablet, and stacked media and text on phones. Work uses a consistent media column across featured projects. The case-study and About reading sections use a shared heading-to-text column ratio, and notes keep the shared left edge with a narrower reading measure. Video thumbnails share one aspect ratio and column width. Contact aligns both columns at the top, then places the details below the heading and actions on narrow screens. At 620px and below the main layouts stack.

## Elevation & Depth

The interface uses flat tonal fields, image crops, and spacing instead of shadows, gradients, or blur. A visible focus outline (3px, 5px offset) uses `--focus`: plum ink on paper/gold and cool paper on dark fields. The ring contrasts with the surrounding surface rather than inheriting the button label color.

## Shapes

Fields, photos, controls, and media use square corners. The note signature uses a circular avatar as a specific exception. Directional arrows are inline SVG, generally (20px), and serve selected actions and workflow direction. Video thumbnails use a dedicated (24px) play glyph in a (48px) control mark, with a brief existing video summary below.

## Components

### Actions and navigation

Primary actions are gold with ink text; inverse actions are ink with paper text on gold. Both have a (48px) minimum height and use the padding in frontmatter. Hover changes a primary action to amber and inverse text to gold; links acquire amber underlines. The dark header contains the wordmark, Work, About, Tools, Notes, Contact, and a direct booking link. Current routes receive a gold underline. The header uses a compact wordmark between 461px and 620px. At 460px and below, the full wordmark sits above the navigation row. At 374px and below, the booking label shortens visually. The footer repeats navigation and external links.

### Project representations

Featured entries combine a linked visual field, title, maturity, description, contribution, and a case-study link. Outbound and GTM entries use captures of actual credential-free synthetic demo output. The signal diagram explains the 15-minute check and advisor review; the Infnty newsletter field explicitly labels itself illustrative. The compact work index uses simple rows on plum.

Filters are hidden until JavaScript enables them, so every project remains available without it. Buttons communicate selection with `aria-pressed`, and the result count is a polite live region. Notes use cool square panels; case facts, flow steps, status markers and tags use flat fields. The contact detail disclosure uses native `details` and `summary`.

### Code gallery and tools directory

The Work code gallery presents three equal-width output previews on desktop, then a text-only source entry across the width of the grid. The preview and its text sit side by side on tablets and stack on phones. Output previews use a 4:3 crop anchored at the top. Case-study output figures use their natural proportions with a width cap.

The Tools page uses four jump links and two prominent upstream repository cards with visible GitHub paths. Application and stack groups pair a short description with labeled tiles. Repository-backed stack tiles link to their upstream source. Tool labels stay visible beside locally served marks or initials. The cool background behind Applications spans the viewport, with its content aligned to the same edges as the other sections.

### Media and motion

Approved portrait photography, original public video thumbnails, and synthetic output captures use responsive AVIF and WebP sources with a fallback from `media.json`; video art retains its 16:9 presentation. `ASSETS.md` records the three output captures and their synthetic scope. The shared shell preloads the local fonts. Preserve hashed filenames and their manifest references.

With motion allowed, the portrait settles from scale (1.04) over (1.1s); project artifact elements enter over (.65s), staggered by (70ms). Hover feedback changes action contrast, underlines linked titles, and shifts directional icons; photographs and project illustrations remain still. The shared easing is `cubic-bezier(.16,1,.3,1)`. Reduced motion disables entrance and transition effects, and all content remains visible without JavaScript. Links, buttons, and summaries expose visible keyboard focus; the skip link appears on focus.

## Do's and Don'ts

### Do:

- **Do** use the pinned palette and keep dark text on gold actions.
- **Do** preserve approved photos, original video thumbnails, responsive media, and self-hosted fonts.
- **Do** label illustrative material and keep project representations tied to supported facts and maturity.
- **Do** maintain keyboard focus, semantic controls, reduced-motion support, and content visible without JavaScript.

### Don't:

- **Don't** present illustrations as actual product screenshots or imply unsupported outcomes.
- **Don't** use emoji arrows or external font imports.
- **Don't** use motion to conceal ordinary content or block navigation.
- **Don't** generalize the note avatar's circular crop to the rest of the interface.

## October 30 refinements

Hallmark was used for an audit and targeted polish within this locked design. The shared public work context restores Canadian citizenship on Home, About and Contact. Metadata uses distinct text elements rather than dot-joined lists, and tools remain supported named items. Image grid tracks use `minmax(0, ...)`, headings can wrap safely, and root horizontal overflow uses `clip`. Phone actions remain on one line. No new imagery, video, testimonial or project claim was invented. The Hallmark comparison and audit state stay private in `.hallmark/`.
