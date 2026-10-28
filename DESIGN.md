---
name: Vatsal Jain Portfolio
description: A personal showcase of practical AI systems and the person behind them.
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
    fontSize: "clamp(64px, 8.5vw, 120px)"
    fontWeight: 650
    lineHeight: 1.05
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "clamp(30px, 3vw, 36px)"
    fontWeight: 650
    lineHeight: 1.15
    letterSpacing: "-0.035em"
  title:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "24px"
    fontWeight: 650
    lineHeight: 1.15
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
  48: "48px"
  section: "104px"
components:
  button-primary:
    backgroundColor: "{colors.palette-gold}"
    textColor: "{colors.palette-ink}"
    rounded: "{rounded.square}"
    padding: "14px 20px"
  button-primary-hover:
    backgroundColor: "{colors.palette-amber}"
  button-inverse:
    backgroundColor: "{colors.palette-ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.square}"
    padding: "14px 20px"
  button-inverse-hover:
    backgroundColor: "{colors.palette-ink}"
    textColor: "{colors.palette-gold}"
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
    padding: "28px"
  tag:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.square}"
    padding: "8px 12px"
  status:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.square}"
    padding: "5px 10px"
---

# Design System: Vatsal Jain Portfolio

## Overview

**Creative North Star: "The Speaking Folio"**

A personal showcase with a confident name, approved photographs, and plain geometric explanations of real workflows. Plum, cool paper, and gold give the work contrast without decorative surface effects.

The system is flat and open: hierarchy comes from scale, spacing, image crops, and tonal fields. Motion introduces the name and portrait once, then sequences workflow steps; ordinary headings and prose remain static.

**Key Characteristics:**

- Oversized Manrope display with readable DM Sans text.
- Square media and flat plum, paper, and gold fields.
- Workflow geometry and real photographs as the visual material.
- Visible content by default, with optional introduction and workflow motion.

Extracted from the completed October 27, 2026 implementation: `static/style.css`, `static/app.js`, `build.py`, `templates/shell.html`, and `dist/index.html`. The desktop, tablet, and mobile captures in `.impeccable/review/` record its rendered expression. Surface-specific composition stays in `.impeccable/surfaces/templates-shell-html.md`.

## Colors

The user-selected palette pairs plum and gray neutrals with gold and amber accents; the implementation adds light fields for legibility.

### Primary

- **Gold** (`palette-gold`): primary actions, the signal preview, contact field, selection, and video-link mark.
- **Amber** (`palette-amber`): action hover, link underline, and the monogram dot.

### Neutral

- **Plum Ink** (`palette-ink`): body text, dark preview fields, selected filters, and inverse actions.
- **Cool Paper** (`paper`): page background and text on dark ink.
- **Cool Surface** (`surface`): note panels, outbound grouping, case facts, and unselected-filter hover.
- **Warm Surface** (`surface-warm`): signal inputs and case-study workflow fields.
- **Muted Plum Gray** (`palette-muted`): native scrollbar color. Body copy remains ink.
- **Palette Gray** (`palette-gray`): pinned palette primitive retained in the source; no active component assignment.

**The Gold Contrast Rule.** Gold actions carry dark ink text; pale text is reserved for ink fields.

## Typography

**Display Font:** Manrope, with Arial and sans-serif fallbacks. **Body Font:** DM Sans, with the same fallbacks. Both are self-hosted Latin WOFF2 variable fonts, preloaded by the shared shell.

Display, headline, title, body, and label values live in the frontmatter. The large name has tighter tracking and leading than section headings. Titles use the headline weight; labels remain sentence case without tracking or a separate mono face. Action labels increase to semibold (600).

The display name becomes (64px) at the tablet breakpoint and a mobile clamp (`clamp(54px,15.8vw,92px)`) below (620px). Body text becomes (16px) there. Story titles use their own smaller responsive display; long note prose uses (18px) with (1.85) leading until mobile. Homepage descriptions stay near (46–54ch); case prose reaches (72ch).

## Layout

The centered container caps at (1280px). Its side gutter is (40px), then (32px), (24px), (20px), and (16px) at maximum widths of (1100px), (800px), (620px), and (360px). Section spacing follows (104px), (80px), (72px), then (64px).

Work uses a six-column grid: substantial previews span three columns, the wide outbound row spans six, and compact entries span two. Below (620px), projects, biography, videos, and notes form single columns. The hero retains a compact portrait alongside its introductory text on mobile, with the name above both. Two-column video and note grids use a (32px) desktop gap, reducing to (24px) on tablet. Case-study prose pairs a narrow heading column with a wider text column, then stacks on mobile. Filtered results use one column and an updated live count.

## Elevation & Depth

No shadows, gradients, blur, or decorative border vocabulary ships. Grouping comes from cool and warm tonal fields, image crops, and spacing. Keyboard focus is an intentional functional outline (3px ink, 5px offset).

**The Flat Surface Rule.** Use tonal fields and space for grouping; do not add decorative borders, gradients, blur, or shadows.

## Shapes

Controls, panels, diagrams, photographs, and video thumbnails have square corners. The only circular exception is the small author avatar on retained note pages. Workflow arrows are inline SVG with a (1.5) stroke, normally (20px); they express direction or a link, never act as ornamental glyphs.

## Components

### Buttons and links

Gold actions use dark ink text; the contact field uses an inverse ink action with paper text. Both have the primary button padding in the frontmatter, a (48px) minimum height, and semibold labels. Text links remain open, with (44px) minimum height. Hover changes the gold action to amber; link hover adds an amber underline. Hover-capable users without a reduced-motion preference also receive a small upward movement and arrow shift. All links, buttons, and summaries share the visible focus outline.

The Cal.com action is an ordinary external link, not an embedded scheduling interface.

### Navigation

A plain, non-sticky row pairs the monogram and name with sentence-case links. Navigation links have (44px) minimum height; the name beside the monogram hides on mobile while the links remain visible. There is no drawer, floating pill, blur, or navigation panel.

### Project filters and metadata

Borderless square filter buttons use ink on paper at rest, a cool field on hover, and paper on ink when selected. Selection is represented by `aria-pressed`; the result count is a polite live region. Filters are hidden until JavaScript enables them, leaving all projects available otherwise. Technology tags and the retained status marker use flat cool fields with their distinct frontmatter padding; homepage maturity and contribution text remains unboxed.

### Workflow previews

Large gold and ink fields hold semantic text nodes, square records, and directional SVG connectors. They explain a workflow rather than imitate an app interface. Their entire preview links to the corresponding case study; the visible text supplies the accessible name. The outbound preview uses a cool field and a dark human-approval block. Workflow direction adapts to available width.

Steps enter once in reading order with (70ms) stagger. The arrival lasts (.65s); only workflow steps receive JavaScript entrance assignments. Name and portrait introduce on load for (.85s) and (1.2s). All use the source easing `cubic-bezier(.16,1,.3,1)`. Content is visible initially, and reduced-motion settings disable these entrances and hover movement.

### Media, notes, and case studies

Approved photographs use deliberate cover crops. Original video thumbnails retain a (16:9) presentation and a small square gold link mark; they open the public videos without autoplay. Notes are simple cool panels, with a title, arrow, and topic. Case facts, workflow nodes, and technology tags repeat the same flat grouping. No input, modal, or form component exists in this implementation.

## Do's and Don'ts

### Do:

- **Do** use approved photographs and original video thumbnails; preserve responsive assets and self-hosted fonts.
- **Do** keep workflow previews diagrammatic and readable, with visible text supplying their link names.
- **Do** preserve square corners, visible keyboard focus, and content that remains visible without JavaScript.
- **Do** limit entrance motion to the name, portrait, and workflow steps; honor reduced motion.

### Don't:

- **Don't** turn diagrams into invented product screenshots or imply unsupported results.
- **Don't** add ornamental borders, gradients, shadows, rounded cards, or a floating navigation shell.
- **Don't** use emoji arrows, external font imports, or scroll-driven hiding of ordinary content.
- **Don't** treat the retained circular note avatar as a general corner treatment.
