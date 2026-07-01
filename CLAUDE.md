# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the **landing/marketing website** for **Monomail** — an open-source, monochrome (black-and-white) Android email client for Gmail and Outlook, built with Jetpack Compose and Material 3 Expressive.

The Android app source code lives in a separate repository (`shrivatsav-0/monomail` on GitHub). This repo is **only the static marketing site**.

## Commands

| Command | Action |
|---|---|
| `npm run dev` | Start Astro dev server at `localhost:4321` |
| `npm run build` | Build static site to `dist/` |
| `npm run preview` | Preview the production build locally |

Built with **Bun** on Windows — `bun install`, `bun run dev`, `bun run build` all work interchangeably.

## Tech Stack (site)

- **Astro 5** — static site generation, zero JS by default
- **Pure CSS** — no framework, monochrome design system with CSS custom properties
- **TypeScript** via `astro/tsconfigs/strict`
- Deploy target: `https://monomail.millosaurs.me`

## Project Structure

```
src/
├── pages/
│   ├── index.astro       # Main landing page — composes all sections
│   ├── pp.astro           # Privacy Policy page (legal layout)
│   └── tos.astro          # Terms of Service page (legal layout)
├── layouts/
│   └── BaseLayout.astro   # HTML shell: SEO/OG tags, fonts, PWA meta, <slot />
├── components/
│   ├── Nav.astro           # Fixed top nav with logo, links, GitHub + Download CTAs
│   ├── Hero.astro          # Hero section: tagline, CTA buttons, phone mockup
│   ├── WhatsNew.astro      # v1.5.4 changelog cards (push notifications, rich compose, etc.)
│   ├── Screenshots.astro   # 8 phone screenshots grid
│   ├── Features.astro      # Feature cards grid + checklist
│   ├── OpenSource.astro    # Open-source pitch with GitHub-style card
│   ├── Download.astro      # Download APK CTA + flavour differences notice
│   ├── Community.astro     # Discord community CTA
│   ├── Support.astro       # UPI QR + Ko-fi support cards
│   └── Footer.astro        # Footer with links to legal pages
└── styles/
    └── global.css          # Entire stylesheet: ~2200 lines, pure CSS monochrome theme
```

### Architecture notes

- **Single Astro layout** (`BaseLayout.astro`) wraps all pages with SEO/Open Graph meta tags, Google Fonts, and PWA-compatible mobile meta.
- **Landing page** (`index.astro`) composes components in order. Each component is a self-contained `<section>` with inline SVGs for icons.
- **Legal pages** (`pp.astro`, `tos.astro`) share the `page-legal` CSS class and reuse Nav, Community, Support, and Footer.
- **No client-side JavaScript.** The site is completely static — all interactivity is pure CSS (hover states, scroll behavior, backdrop blur on nav).
- **Assets** live in `public/imgs/ui/` (phone screenshots, 9 files) and `public/imgs/` (qr-code, leaf logo, social share preview).
- **Images also exist in `imgs/`** at the project root — these are the same source files referenced by the old single-page HTML version (`index.html`). The Astro site uses copies in `public/imgs/`.

## Design System (CSS)

- `--black`, `--white`, `--surface`, `--muted`, `--border` — full palette
- `--r-card: 28px`, `--r-phone: 44px` — border radius tokens
- Google Fonts: Google Sans Display / Google Sans / Roboto
- Monochrome-only: no colour except brand SVGs

## Deploy

- Build: `npm run build` outputs to `dist/`
- Deploy the `dist/` directory to any static host
- Site URL: `https://monomail.millosaurs.me`
