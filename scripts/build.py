#!/usr/bin/env python3
"""Build the Covered Bridge Home Loans website blocks.

Design: David's "Mortgage Lender" GHL template layout (light content
sections with dark feature bands), in Covered Bridge Brands colors, logo
and type. The previous all-dark design is kept on the git branch
archive/v1-dark-design.

Writes GHL-ready fragments (no <html>/<head>/<body>):
  sections/home-loans-header.html   shared header  (root .cbhl-header)
  sections/home-loans-footer.html   shared footer  (root .cbhl-footer)
  pages/home-loans-*.html           the nine page bodies (one root each)

and review copies with the header and footer around each page:
  preview/index.html, preview/loan-options/index.html, ...
Serve preview/ from its own folder (python3 -m http.server) so the
site's /route links work. Never paste preview files into GHL.

Settings: config/site.json (application link, optional GHL Media image
links). Run:  python3 scripts/build.py
"""
import base64
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads(Path(os.environ.get("HL_CONFIG", ROOT / "config/site.json")).read_text(encoding="utf-8"))
OUT = Path(os.environ.get("HL_OUT", ROOT))

APPLICATION_URL = CONFIG.get("applicationUrl", "").strip()
assert APPLICATION_URL == "" or (APPLICATION_URL.startswith("https://") and "'" not in APPLICATION_URL), APPLICATION_URL

# ---------------------------------------------------------------------------
# Images: a GHL Media link from config/site.json, else embedded from assets/web
# ---------------------------------------------------------------------------
IMAGES = {
    # key: (file in assets/web, width, height, alt text)
    "logo": ("cbb-logo.webp", 480, 100, ""),
    "hero": ("home-loans-hero.webp", 1600, 900,
             "A two-story home with warm light glowing in its windows at sunset."),
    "resources": ("home-loans-resources.webp", 1100, 733,
                  "A small wooden model house beside a set of house keys, a notebook and a pen on a wooden table."),
    "consultation": ("home-loans-consultation.webp", 1100, 733,
                     "Two people talking with an advisor across a table as she reviews paperwork with them."),
    "couplePlanning": ("home-loans-couple-planning.webp", 600, 750,
                       "A couple sitting on a sofa, looking at a tablet together."),
    "advisor": ("home-loans-advisor.webp", 600, 750,
                "A man in a blazer reviewing papers in a folder at a desk."),
    "familyMoving": ("home-loans-family-moving.webp", 600, 750,
                     "Two parents and a young child unpacking a moving box in a bright, empty room."),
}


def img_src(key):
    url = (CONFIG.get("images") or {}).get(key, "").strip()
    if url:
        assert url.startswith("https://") and '"' not in url, url
        return url
    data = (ROOT / "assets/web" / IMAGES[key][0]).read_bytes()
    return "data:image/webp;base64," + base64.b64encode(data).decode()


def img(key, cls="", eager=False):
    _, w, h, alt = IMAGES[key]
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="%IMG:{key}%" alt="{alt}" width="{w}" height="{h}" {loading} decoding="async">'


CTA_LABEL = "Talk About Your Home Loan"
DISCLAIMER = ("Loan options, eligibility, down payments and terms depend on the applicable program and "
              "individual circumstances. All loans are subject to credit and underwriting approval. "
              "Website information is not a commitment to lend.")

# ---------------------------------------------------------------------------
# Design tokens. %R is replaced by each block's root class.
# ---------------------------------------------------------------------------
TOKENS = """
    --hl-black: #0D0D0D;
    --hl-charcoal: #121619;
    --hl-gold: #D2A34C;
    --hl-gold-hover: #EAC266;
    --hl-gold-text: #87631A;          /* gold for small text on light backgrounds */
    --hl-warm: #F2F0EB;               /* text on dark */
    --hl-warm-muted: #C9C4B6;         /* secondary text on dark */
    --hl-light: #FAF8F4;              /* light content background */
    --hl-band: #F1EDE5;               /* slightly deeper light band */
    --hl-white: #FFFFFF;
    --hl-ink: #242424;                /* body text on light */
    --hl-ink-muted: #57534B;          /* secondary text on light */
    --hl-line: #E4DCCD;               /* borders on light */
    --hl-line-dark: rgba(210, 163, 76, 0.22);
    --hl-serif: 'Playfair Display', Georgia, 'Times New Roman', serif;
    --hl-sans: 'Inter', -apple-system, system-ui, 'Segoe UI', Roboto, sans-serif;
    --hl-gutter: clamp(20px, 4vw, 48px);
"""

CSS = {}

CSS["base"] = """
  .%R {""" + TOKENS + """
    display: block;
    width: 100%;
    margin: 0;
    padding: 0;
    background: var(--hl-light);
    color: var(--hl-ink);
    font-family: var(--hl-sans);
    font-size: 17px;
    line-height: 1.7;
    text-align: left;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
  }
  .%R,
  .%R *,
  .%R *::before,
  .%R *::after {
    box-sizing: border-box;
  }
  .%R [hidden] { display: none !important; }
  .%R img { max-width: 100%; }

  /* ---------- Sections ---------- */
  .%R .%R__s {
    position: relative;
    margin: 0;
    padding: clamp(64px, 8vw, 112px) var(--hl-gutter);
    background: var(--hl-light);
    scroll-margin-top: 92px; /* clears the fixed header */
  }
  .%R .%R__s--white { background: var(--hl-white); }
  .%R .%R__s--band { background: var(--hl-band); }
  .%R .%R__s--dark {
    background: var(--hl-charcoal);
    color: var(--hl-warm);
    overflow: hidden;
  }
  .%R .%R__s--tight {
    padding-top: clamp(48px, 6vw, 72px);
    padding-bottom: clamp(48px, 6vw, 72px);
  }
  .%R .%R__in {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 1180px;
    margin: 0 auto;
  }
  .%R .%R__narrow { max-width: 760px; }
  .%R .%R__center { text-align: center; }
  .%R .%R__center .%R__eyebrow { justify-content: center; }
  .%R .%R__center .%R__lede,
  .%R .%R__center .%R__h1 { margin-left: auto; margin-right: auto; }
  .%R .%R__head {
    max-width: 720px;
    margin: 0 0 clamp(36px, 5vw, 56px);
  }
  .%R .%R__head.%R__center { margin-left: auto; margin-right: auto; }

  /* ---------- Type ---------- */
  .%R .%R__eyebrow {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0 0 14px;
    padding: 0;
    font-family: var(--hl-sans);
    font-size: 0.8125rem;
    font-weight: 600;
    line-height: 1.5;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--hl-gold-text);
  }
  .%R .%R__eyebrow svg {
    flex: 0 0 auto;
    width: 20px;
    height: 12px;
  }
  .%R .%R__s--dark .%R__eyebrow { color: var(--hl-gold); }
  .%R .%R__h1 {
    margin: 0 0 20px;
    padding: 0;
    font-family: var(--hl-serif);
    font-size: clamp(2.375rem, 2.8vw + 1.1rem, 3.75rem);
    font-weight: 600;
    line-height: 1.1;
    letter-spacing: -0.01em;
    text-transform: none;
    color: var(--hl-ink);
  }
  .%R .%R__h2 {
    margin: 0 0 16px;
    padding: 0;
    font-family: var(--hl-serif);
    font-size: clamp(1.875rem, 1.6vw + 1.2rem, 2.625rem);
    font-weight: 600;
    line-height: 1.18;
    letter-spacing: -0.005em;
    text-transform: none;
    color: var(--hl-ink);
  }
  .%R .%R__h3 {
    margin: 0 0 8px;
    padding: 0;
    font-family: var(--hl-sans);
    font-size: 1.1875rem;
    font-weight: 600;
    line-height: 1.35;
    letter-spacing: 0;
    text-transform: none;
    color: var(--hl-ink);
  }
  .%R .%R__s--dark .%R__h1,
  .%R .%R__s--dark .%R__h2,
  .%R .%R__s--dark .%R__h3 { color: var(--hl-warm); }
  .%R .%R__gold { color: var(--hl-gold); }
  .%R .%R__lede {
    max-width: 38em;
    margin: 0;
    padding: 0;
    font-size: clamp(1.0625rem, 0.3vw + 1rem, 1.1875rem);
    line-height: 1.7;
    color: var(--hl-ink-muted);
  }
  .%R .%R__p {
    margin: 0 0 16px;
    padding: 0;
    font-size: 1.0625rem;
    line-height: 1.75;
    color: var(--hl-ink-muted);
  }
  .%R .%R__p:last-child { margin-bottom: 0; }
  .%R .%R__p--sm { font-size: 1rem; line-height: 1.7; }
  .%R .%R__s--dark .%R__lede,
  .%R .%R__s--dark .%R__p { color: var(--hl-warm-muted); }
  .%R .%R__p a,
  .%R .%R__lede a {
    color: var(--hl-gold-text);
    font-weight: 600;
    text-decoration: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 3px;
  }
  .%R .%R__s--dark .%R__p a { color: var(--hl-gold-hover); }

  /* ---------- Buttons and links ---------- */
  .%R .%R__actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 16px 28px;
    margin: clamp(28px, 3.4vw, 36px) 0 0;
  }
  .%R .%R__center .%R__actions,
  .%R .%R__actions.%R__center { justify-content: center; }
  .%R .%R__btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    min-height: 52px;
    margin: 0;
    padding: 0 28px;
    border: 0;
    border-radius: 999px;
    background: var(--hl-gold);
    color: #0D0D0D;
    font-family: var(--hl-sans);
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.2;
    letter-spacing: 0.01em;
    text-align: center;
    text-decoration: none;
    text-transform: none;
    cursor: pointer;
    transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
  }
  .%R .%R__btn svg {
    width: 17px;
    height: 17px;
    flex: 0 0 17px;
  }
  .%R .%R__btn:hover {
    background: var(--hl-gold-hover);
    color: #0D0D0D;
    transform: translateY(-1px);
    box-shadow: 0 10px 26px rgba(210, 163, 76, 0.3);
  }
  .%R .%R__btn--sm {
    min-height: 44px;
    padding: 0 22px;
    font-size: 0.9375rem;
  }
  .%R .%R__link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 0 0 3px;
    border-bottom: 1px solid currentColor;
    font-family: var(--hl-sans);
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.4;
    color: var(--hl-gold-text);
    text-decoration: none;
    transition: color 0.2s ease;
  }
  .%R .%R__link svg {
    width: 16px;
    height: 16px;
    flex: 0 0 16px;
    transition: transform 0.2s ease;
  }
  .%R .%R__link:hover { color: var(--hl-ink); }
  .%R .%R__link:hover svg { transform: translateX(3px); }
  .%R .%R__s--dark .%R__link { color: var(--hl-gold); }
  .%R .%R__s--dark .%R__link:hover { color: var(--hl-gold-hover); }
  .%R a:focus-visible,
  .%R summary:focus-visible {
    outline: 2px solid var(--hl-gold);
    outline-offset: 4px;
    border-radius: 4px;
  }
  .%R .%R__s--dark a:focus-visible { outline-color: var(--hl-gold-hover); }
  .%R .%R__sr {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  /* ---------- Decorative gold linework (dark bands) ---------- */
  .%R .%R__lines {
    position: absolute;
    z-index: 0;
    width: clamp(260px, 34vw, 520px);
    height: auto;
    color: var(--hl-gold);
    opacity: 0.22;
    pointer-events: none;
  }
  .%R .%R__lines--br { right: -40px; bottom: -40px; }
  .%R .%R__lines--bl { left: -60px; bottom: -60px; transform: scaleX(-1); }

  /* ---------- Dark call-to-action band ---------- */
  .%R .%R__cta { text-align: center; }
  .%R .%R__cta .%R__in { max-width: 760px; }
  .%R .%R__cta .%R__actions { justify-content: center; }
  .%R .%R__cta .%R__lede { margin: 0 auto; }

  @media (max-width: 1240px) {
    .%R .%R__s { scroll-margin-top: 80px; }
  }
  @media (max-width: 480px) {
    .%R .%R__actions .%R__btn { width: 100%; }
  }
  @media (prefers-reduced-motion: reduce) {
    .%R .%R__btn,
    .%R .%R__link,
    .%R .%R__link svg { transition: none; }
    .%R .%R__btn:hover,
    .%R .%R__link:hover svg { transform: none; }
  }
"""

CSS["hero"] = """
  /* ---------- Home hero (photo, copy over the darker left side) ---------- */
  .%R .%R__hero {
    position: relative;
    display: flex;
    align-items: center;
    min-height: clamp(600px, 88vh, 800px);
    margin: 0;
    padding: clamp(80px, 9vw, 120px) var(--hl-gutter) clamp(150px, 15vw, 210px);
    background: var(--hl-black);
    color: var(--hl-warm);
    overflow: hidden;
  }
  .%R .%R__hero-img {
    position: absolute;
    inset: 0;
    display: block;
    width: 100%;
    max-width: none;
    height: 100%;
    object-fit: cover;
    object-position: 66% 50%;
  }
  .%R .%R__hero-shade {
    position: absolute;
    inset: 0;
    background:
      linear-gradient(90deg, rgba(13, 13, 13, 0.9) 0%, rgba(13, 13, 13, 0.74) 32%, rgba(13, 13, 13, 0.28) 58%, rgba(13, 13, 13, 0) 76%),
      linear-gradient(180deg, rgba(13, 13, 13, 0.35) 0%, rgba(13, 13, 13, 0) 22%);
  }
  .%R .%R__hero-copy { max-width: 600px; }
  .%R .%R__hero .%R__h1 {
    font-size: clamp(2.75rem, 3.8vw + 1rem, 4.5rem);
    color: var(--hl-warm);
    text-shadow: 0 2px 24px rgba(0, 0, 0, 0.35);
  }
  .%R .%R__hero .%R__lede { color: rgba(242, 240, 235, 0.92); }
  .%R .%R__hero .%R__eyebrow { color: var(--hl-gold); }
  .%R .%R__hero .%R__link { color: var(--hl-warm); }
  .%R .%R__hero .%R__link:hover { color: var(--hl-gold-hover); }
  .%R .%R__hero a:focus-visible { outline-color: var(--hl-gold-hover); }
  /* Tablet and phone: the photo becomes a band above the copy. */
  @media (max-width: 900px) {
    .%R .%R__hero {
      display: block;
      min-height: 0;
      padding: 0 0 clamp(96px, 16vw, 128px);
    }
    .%R .%R__hero-img {
      position: relative;
      inset: auto;
      height: clamp(260px, 60vw, 460px);
      object-position: 74% 45%;
    }
    .%R .%R__hero-shade {
      inset: 0 0 auto 0;
      height: clamp(260px, 60vw, 460px);
      background: linear-gradient(180deg, rgba(13, 13, 13, 0) 50%, rgba(13, 13, 13, 0.6) 80%, #0D0D0D 100%);
    }
    .%R .%R__hero .%R__in {
      margin-top: clamp(-52px, -6vw, -24px);
      padding: 0 var(--hl-gutter);
    }
    .%R .%R__hero .%R__h1 { text-shadow: none; }
  }

  /* ---------- Overlapping question panel (stays in normal flow) ---------- */
  .%R .%R__panel-band {
    position: relative;
    z-index: 2;
    margin: 0;
    padding: 0 var(--hl-gutter) clamp(48px, 6vw, 72px);
    background: var(--hl-band);
  }
  .%R .%R__panel {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    max-width: 1000px;
    margin: calc(-1 * clamp(80px, 9vw, 120px)) auto 0;
    padding: clamp(28px, 4vw, 44px) 0;
    border-radius: 18px;
    background: var(--hl-charcoal);
    box-shadow: 0 24px 60px rgba(13, 13, 13, 0.28);
    color: var(--hl-warm);
  }
  .%R .%R__panel-col { padding: 0 clamp(24px, 4vw, 52px); }
  .%R .%R__panel-col + .%R__panel-col { border-left: 1px solid var(--hl-line-dark); }
  .%R .%R__panel .%R__h2 {
    margin-bottom: 8px;
    font-size: clamp(1.375rem, 0.8vw + 1.1rem, 1.75rem);
    color: var(--hl-warm);
  }
  .%R .%R__panel .%R__p { margin-bottom: 18px; color: var(--hl-warm-muted); }
  .%R .%R__panel .%R__link { color: var(--hl-gold); }
  .%R .%R__panel .%R__link:hover { color: var(--hl-gold-hover); }
  .%R .%R__panel a:focus-visible { outline-color: var(--hl-gold-hover); }
  @media (max-width: 760px) {
    .%R .%R__panel {
      grid-template-columns: minmax(0, 1fr);
      margin-top: calc(-1 * clamp(64px, 14vw, 88px));
      padding: 0;
    }
    .%R .%R__panel-col { padding: 28px 24px; }
    .%R .%R__panel-col + .%R__panel-col {
      border-left: 0;
      border-top: 1px solid var(--hl-line-dark);
    }
  }
"""

CSS["comp"] = """
  /* ---------- Copy beside an overlapping photo composition ---------- */
  .%R .%R__split {
    display: grid;
    grid-template-columns: minmax(0, 5fr) minmax(0, 6fr);
    gap: clamp(40px, 6vw, 96px);
    align-items: center;
  }
  .%R .%R__comp {
    position: relative;
    width: 100%;
    max-width: 520px;
    aspect-ratio: 1 / 1.05;
    margin: 0 auto;
  }
  .%R .%R__comp img {
    position: absolute;
    display: block;
    height: auto;
    aspect-ratio: 4 / 5;
    object-fit: cover;
    border-radius: 8px;
    background: var(--hl-band);
  }
  .%R .%R__comp-a {
    left: 0;
    top: 8%;
    width: 58%;
    box-shadow: 0 18px 40px rgba(13, 13, 13, 0.14);
  }
  .%R .%R__comp-b {
    right: 0;
    bottom: 0;
    width: 54%;
    border: 6px solid var(--hl-white);
    box-shadow: 0 18px 40px rgba(13, 13, 13, 0.18);
  }
  .%R .%R__comp--process .%R__comp-a { top: 0; width: 60%; }
  .%R .%R__comp--process .%R__comp-b { width: 50%; bottom: 2%; }
  .%R .%R__comp--landscape .%R__comp-b {
    width: 64%;
    bottom: 4%;
    aspect-ratio: 4 / 3;
    border-color: var(--hl-band);
  }
  .%R .%R__comp-badge {
    position: absolute;
    z-index: 2;
    top: 0;
    left: 42%;
    width: 32%;
    margin: 0;
    padding: 14px 14px 16px;
    border-radius: 6px;
    background: var(--hl-gold);
    color: #0D0D0D;
    font-family: var(--hl-sans);
    font-size: 0.75rem;
    font-weight: 700;
    line-height: 1.4;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    box-shadow: 0 12px 28px rgba(13, 13, 13, 0.18);
  }
  @media (max-width: 900px) {
    .%R .%R__split { grid-template-columns: minmax(0, 1fr); }
  }
  /* Phones: the overlap becomes two side-by-side photos. */
  @media (max-width: 560px) {
    .%R .%R__comp {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 12px;
      max-width: none;
      aspect-ratio: auto;
    }
    .%R .%R__comp img,
    .%R .%R__comp--process .%R__comp-a,
    .%R .%R__comp--process .%R__comp-b,
    .%R .%R__comp--landscape .%R__comp-b {
      position: static;
      width: 100%;
      aspect-ratio: 4 / 5;
      border: 0;
    }
    .%R .%R__comp-b { margin-top: 32px; }
    .%R .%R__comp-badge {
      position: static;
      order: -1;
      grid-column: 1 / -1;
      width: auto;
      text-align: center;
    }
  }
"""

CSS["benefits"] = """
  /* ---------- Dark band: icon circles, divider, two columns ---------- */
  .%R .%R__icons {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 24px;
    max-width: 900px;
    margin: clamp(32px, 4vw, 48px) auto 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__icons li {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
    margin: 0;
    text-align: center;
    font-size: 1.0625rem;
    font-weight: 600;
    color: var(--hl-warm);
  }
  .%R .%R__icons li::marker { content: none; }
  .%R .%R__icon {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    justify-content: center;
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: var(--hl-gold);
    color: #0D0D0D;
  }
  .%R .%R__icon svg { width: 34px; height: 34px; }
  .%R .%R__divider {
    max-width: 900px;
    height: 1px;
    margin: clamp(40px, 5vw, 56px) auto;
    border: 0;
    background: rgba(242, 240, 235, 0.25);
  }
  .%R .%R__benefit-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: clamp(36px, 6vw, 88px);
    max-width: 1000px;
    margin: 0 auto;
  }
  .%R .%R__checks {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__checks > li {
    display: grid;
    grid-template-columns: 24px minmax(0, 1fr);
    gap: 14px;
    margin: 0 0 22px;
  }
  .%R .%R__checks > li:last-child { margin-bottom: 0; }
  .%R .%R__checks > li::marker { content: none; }
  .%R .%R__checks svg {
    width: 24px;
    height: 24px;
    margin-top: 2px;
    color: var(--hl-gold);
  }
  .%R .%R__checks .%R__h3 { margin-bottom: 4px; font-size: 1.125rem; }
  .%R .%R__value-title {
    display: block;
    margin: 0 0 6px;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--hl-warm);
  }
  .%R .%R__value-text {
    display: block;
    max-width: 22em;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.65;
    color: var(--hl-warm-muted);
  }
  @media (max-width: 760px) {
    .%R .%R__icons { grid-template-columns: minmax(0, 1fr); gap: 22px; }
    .%R .%R__icons li { flex-direction: row; align-items: flex-start; text-align: left; }
    .%R .%R__icons li > span:only-of-type { align-self: center; }
    .%R .%R__icon { width: 56px; height: 56px; }
    .%R .%R__icon svg { width: 28px; height: 28px; }
    .%R .%R__benefit-grid { grid-template-columns: minmax(0, 1fr); }
  }
"""

CSS["cards"] = """
  /* ---------- Cards ---------- */
  .%R .%R__cards-head {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: clamp(20px, 5vw, 72px);
    align-items: end;
    margin: 0 0 clamp(36px, 5vw, 52px);
  }
  .%R .%R__cards-head .%R__h2 { margin-bottom: 0; }
  .%R .%R__cards {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: clamp(16px, 2vw, 24px);
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__card {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin: 0;
    padding: clamp(26px, 3vw, 34px);
    border: 1px solid var(--hl-line);
    border-radius: 10px;
    background:
      linear-gradient(118deg, rgba(255, 255, 255, 0) 0 56%, rgba(255, 255, 255, 0.65) 56% 100%),
      #F3EFE7;
  }
  .%R .%R__card::marker { content: none; }
  .%R .%R__card-tab {
    display: inline-block;
    margin: 0 0 16px;
    padding: 9px 16px;
    border-radius: 4px;
    background: var(--hl-charcoal);
    color: var(--hl-warm);
    font-family: var(--hl-sans);
    font-size: 1.0625rem;
    font-weight: 600;
    line-height: 1.3;
  }
  .%R .%R__card .%R__p { flex: 1 1 auto; margin-bottom: 22px; }
  .%R .%R__cards--plain .%R__card { background: var(--hl-white); }
  .%R .%R__cards--plain .%R__card .%R__p { margin-bottom: 0; }
  @media (max-width: 960px) {
    .%R .%R__cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  @media (max-width: 760px) {
    .%R .%R__cards-head { grid-template-columns: minmax(0, 1fr); }
  }
  @media (max-width: 620px) {
    .%R .%R__cards { grid-template-columns: minmax(0, 1fr); }
  }
"""

CSS["steps"] = """
  /* ---------- Numbered steps ---------- */
  .%R .%R__steps {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__step {
    display: grid;
    grid-template-columns: 58px minmax(0, 1fr);
    gap: 20px;
    align-items: start;
    margin: 0 0 26px;
  }
  .%R .%R__step:last-child { margin-bottom: 0; }
  .%R .%R__step::marker { content: none; }
  .%R .%R__num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 58px;
    height: 58px;
    border-radius: 8px;
    background: var(--hl-white);
    box-shadow: 0 8px 22px rgba(13, 13, 13, 0.1);
    font-family: var(--hl-serif);
    font-size: 1.75rem;
    font-weight: 700;
    line-height: 1;
    color: var(--hl-gold-text);
  }
  .%R .%R__s--white .%R__num { background: var(--hl-light); }
  .%R .%R__step .%R__h3 { margin: 4px 0; }
  .%R .%R__step .%R__link { margin-top: 12px; }
  .%R .%R__steps--large .%R__step {
    margin-bottom: clamp(26px, 3.4vw, 36px);
    padding-bottom: clamp(26px, 3.4vw, 36px);
    border-bottom: 1px solid var(--hl-line);
  }
  .%R .%R__steps--large .%R__step:last-child { margin-bottom: 0; padding-bottom: 0; border-bottom: 0; }
  .%R .%R__steps--large .%R__h3 {
    font-family: var(--hl-serif);
    font-size: clamp(1.3125rem, 0.6vw + 1.1rem, 1.5625rem);
  }
"""

CSS["resource"] = """
  /* ---------- Resource links ---------- */
  .%R .%R__res {
    display: grid;
    grid-template-columns: minmax(0, 5fr) minmax(0, 6fr);
    gap: clamp(28px, 5vw, 72px);
    align-items: center;
  }
  .%R .%R__tiles {
    display: grid;
    gap: 14px;
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__tiles li { margin: 0; }
  .%R .%R__tiles li::marker { content: none; }
  .%R .%R__tile {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 22px 24px;
    border: 1px solid var(--hl-line);
    border-left: 4px solid var(--hl-gold);
    border-radius: 8px;
    background: var(--hl-white);
    color: var(--hl-ink);
    font-family: var(--hl-serif);
    font-size: 1.3125rem;
    font-weight: 600;
    line-height: 1.3;
    text-decoration: none;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
  }
  .%R .%R__tile svg {
    width: 20px;
    height: 20px;
    flex: 0 0 20px;
    color: var(--hl-gold-text);
    transition: transform 0.2s ease;
  }
  .%R .%R__tile:hover {
    border-color: var(--hl-gold);
    box-shadow: 0 10px 26px rgba(13, 13, 13, 0.08);
  }
  .%R .%R__tile:hover svg { transform: translateX(3px); }
  @media (max-width: 760px) {
    .%R .%R__res { grid-template-columns: minmax(0, 1fr); }
  }
  @media (prefers-reduced-motion: reduce) {
    .%R .%R__tile,
    .%R .%R__tile svg { transition: none; }
    .%R .%R__tile:hover svg { transform: none; }
  }
"""

CSS["faq"] = """
  /* ---------- FAQ accordion (native details/summary: keyboard and touch ready) ---------- */
  .%R .%R__faq {
    max-width: 880px;
    margin: 0 auto;
  }
  .%R .%R__faq details {
    margin: 0 0 12px;
    border: 1px solid var(--hl-gold);
    border-radius: 8px;
    background: var(--hl-white);
  }
  .%R .%R__faq summary {
    position: relative;
    display: block;
    padding: 18px 56px 18px 22px;
    font-family: var(--hl-sans);
    font-size: 1.0625rem;
    font-weight: 600;
    line-height: 1.45;
    color: var(--hl-ink);
    list-style: none;
    cursor: pointer;
    transition: color 0.2s ease;
  }
  .%R .%R__faq summary::-webkit-details-marker { display: none; }
  .%R .%R__faq summary::before,
  .%R .%R__faq summary::after {
    content: "";
    position: absolute;
    top: 50%;
    right: 22px;
    width: 14px;
    height: 2px;
    margin-top: -1px;
    background: var(--hl-ink);
    transition: transform 0.2s ease;
  }
  .%R .%R__faq summary::after { transform: rotate(90deg); }
  .%R .%R__faq details[open] summary { color: var(--hl-gold-text); }
  .%R .%R__faq details[open] summary::before { background: var(--hl-gold-text); }
  .%R .%R__faq details[open] summary::after { transform: rotate(0deg); background: var(--hl-gold-text); }
  .%R .%R__faq summary:hover { color: var(--hl-gold-text); }
  .%R .%R__faq summary:focus-visible { outline-offset: 2px; }
  .%R .%R__faq-body { padding: 0 22px 20px; }
  .%R .%R__faq-body .%R__p { max-width: 70ch; font-size: 1rem; }
  @media (prefers-reduced-motion: reduce) {
    .%R .%R__faq summary,
    .%R .%R__faq summary::before,
    .%R .%R__faq summary::after { transition: none; }
  }
"""

CSS["banner"] = """
  /* ---------- Inner-page banner (shorter than the Home hero) ---------- */
  .%R .%R__banner {
    position: relative;
    margin: 0;
    padding: clamp(56px, 7vw, 96px) var(--hl-gutter);
    background:
      radial-gradient(45% 80% at 100% 0%, rgba(210, 163, 76, 0.14), rgba(210, 163, 76, 0) 65%),
      var(--hl-band);
    border-bottom: 1px solid var(--hl-line);
    overflow: hidden;
  }
  .%R .%R__banner--dark {
    background:
      radial-gradient(45% 80% at 100% 0%, rgba(210, 163, 76, 0.16), rgba(210, 163, 76, 0) 65%),
      var(--hl-charcoal);
    border-bottom: 0;
    color: var(--hl-warm);
  }
  .%R .%R__banner--dark .%R__h1 { color: var(--hl-warm); }
  .%R .%R__banner--dark .%R__lede { color: var(--hl-warm-muted); }
  .%R .%R__banner--dark .%R__eyebrow { color: var(--hl-gold); }
  .%R .%R__banner .%R__h1 { max-width: 18em; }
  .%R .%R__banner-grid {
    display: grid;
    grid-template-columns: minmax(0, 6fr) minmax(0, 5fr);
    gap: clamp(36px, 6vw, 88px);
    align-items: center;
  }
  @media (max-width: 900px) {
    .%R .%R__banner-grid { grid-template-columns: minmax(0, 1fr); }
  }
"""

CSS["photo"] = """
  /* ---------- Single photo with a gold offset frame ---------- */
  .%R .%R__photo {
    position: relative;
    margin: 0 16px 16px 0;
  }
  .%R .%R__photo::before {
    content: "";
    position: absolute;
    inset: 16px -16px -16px 16px;
    border: 2px solid var(--hl-gold);
    border-radius: 10px;
    pointer-events: none;
  }
  .%R .%R__photo img {
    position: relative;
    z-index: 1;
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 4 / 3;
    object-fit: cover;
    border-radius: 10px;
    background: var(--hl-band);
  }
  .%R .%R__photo--tall img { aspect-ratio: 4 / 5; }
  @media (max-width: 900px) {
    .%R .%R__photo img { aspect-ratio: 16 / 10; }
    .%R .%R__photo--tall img { aspect-ratio: 16 / 11; object-position: 50% 28%; }
  }
"""

CSS["rows"] = """
  /* ---------- Program sections ---------- */
  .%R .%R__program {
    display: grid;
    grid-template-columns: minmax(0, 4fr) minmax(0, 7fr);
    gap: clamp(16px, 5vw, 72px);
    align-items: start;
  }
  .%R .%R__program-num {
    display: block;
    margin: 0 0 6px;
    font-family: var(--hl-serif);
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--hl-gold-text);
  }
  .%R .%R__program .%R__h2 {
    margin: 0;
    padding-left: 18px;
    border-left: 3px solid var(--hl-gold);
    font-size: clamp(1.625rem, 1vw + 1.25rem, 2.125rem);
  }
  .%R .%R__program .%R__p { font-size: 1.125rem; }
  @media (max-width: 760px) {
    .%R .%R__program { grid-template-columns: minmax(0, 1fr); }
  }
"""

CSS["gloss"] = """
  /* ---------- Glossary ---------- */
  .%R .%R__gloss {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0 clamp(32px, 5vw, 72px);
    margin: 0;
    padding: 0;
  }
  .%R .%R__gloss > div {
    margin: 0;
    padding: 24px 0;
    border-top: 1px solid var(--hl-line);
  }
  .%R .%R__gloss dt {
    margin: 0 0 6px;
    font-family: var(--hl-serif);
    font-size: 1.3125rem;
    font-weight: 600;
    line-height: 1.3;
    color: var(--hl-ink);
  }
  .%R .%R__gloss dd {
    margin: 0;
    font-size: 1rem;
    line-height: 1.7;
    color: var(--hl-ink-muted);
  }
  @media (max-width: 760px) {
    .%R .%R__gloss { grid-template-columns: minmax(0, 1fr); }
  }
"""

CSS["lists"] = """
  /* ---------- Point lists, notes, callouts ---------- */
  .%R .%R__points {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__points > li {
    display: grid;
    grid-template-columns: 24px minmax(0, 1fr);
    gap: 14px;
    align-items: start;
    margin: 0;
    padding: 16px 0;
    border-top: 1px solid var(--hl-line);
    font-size: 1.0625rem;
    line-height: 1.6;
    color: var(--hl-ink);
  }
  .%R .%R__points > li:last-child { border-bottom: 1px solid var(--hl-line); }
  .%R .%R__points > li::marker { content: none; }
  .%R .%R__points svg {
    width: 24px;
    height: 24px;
    margin-top: 1px;
    color: var(--hl-gold-text);
  }
  .%R .%R__note {
    max-width: 72ch;
    margin: clamp(22px, 3vw, 30px) 0 0;
    font-size: 0.9375rem;
    line-height: 1.65;
    color: var(--hl-ink-muted);
  }
  .%R .%R__callout {
    display: grid;
    grid-template-columns: 28px minmax(0, 1fr);
    gap: 16px;
    max-width: 880px;
    margin: clamp(32px, 4vw, 44px) 0 0;
    padding: 22px 26px;
    border: 1px solid var(--hl-line);
    border-left: 4px solid var(--hl-gold);
    border-radius: 8px;
    background: var(--hl-light);
  }
  .%R .%R__callout svg { width: 28px; height: 28px; color: var(--hl-gold-text); }
  .%R .%R__callout .%R__h3 { margin-bottom: 4px; }
"""

CSS["contact"] = """
  /* ---------- Contact ---------- */
  .%R .%R__contact {
    display: grid;
    grid-template-columns: minmax(0, 5fr) minmax(0, 6fr);
    gap: clamp(40px, 6vw, 88px);
    align-items: start;
  }
  /* The GHL form goes inside .%R__form. While it's empty the box is
     hidden, so visitors never see an empty panel. */
  .%R .%R__form {
    margin: 26px 0 0;
    padding: clamp(20px, 3vw, 30px);
    border: 1px solid var(--hl-line);
    border-top: 4px solid var(--hl-gold);
    border-radius: 10px;
    background: var(--hl-white);
    box-shadow: 0 16px 40px rgba(13, 13, 13, 0.06);
  }
  .%R .%R__form:empty { display: none; }
  .%R .%R__form iframe {
    display: block;
    width: 100%;
    max-width: 100%;
    border: 0;
  }
  .%R .%R__notices {
    margin: 26px 0 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__notices > li {
    display: grid;
    grid-template-columns: 22px minmax(0, 1fr);
    gap: 12px;
    margin: 0;
    padding: 14px 0;
    border-top: 1px solid var(--hl-line);
    font-size: 0.9375rem;
    line-height: 1.6;
    color: var(--hl-ink-muted);
  }
  .%R .%R__notices > li::marker { content: none; }
  .%R .%R__notices svg { width: 22px; height: 22px; color: var(--hl-gold-text); }
  .%R .%R__notices a {
    color: var(--hl-gold-text);
    font-weight: 600;
    text-decoration: underline;
    text-underline-offset: 3px;
  }
  .%R .%R__apply {
    margin: 26px 0 0;
    padding: 22px 0 0;
    border-top: 1px solid var(--hl-line);
  }
  .%R .%R__apply .%R__actions { margin-top: 14px; }
  @media (max-width: 900px) {
    .%R .%R__contact { grid-template-columns: minmax(0, 1fr); }
  }
"""

CSS["legal"] = """
  /* ---------- Legal draft ---------- */
  .%R .%R__legal { max-width: 820px; }
  .%R .%R__status {
    margin: 22px 0 0;
    padding: 14px 18px;
    border: 1px solid var(--hl-gold);
    border-left: 4px solid var(--hl-gold);
    border-radius: 6px;
    background: var(--hl-white);
    font-size: 0.9375rem;
    font-weight: 600;
    line-height: 1.6;
    color: var(--hl-ink);
  }
  .%R .%R__legal-sec {
    margin: 0;
    padding: clamp(26px, 3.2vw, 34px) 0;
    border-top: 1px solid var(--hl-line);
  }
  .%R .%R__legal-sec:first-child { padding-top: 0; border-top: 0; }
  .%R .%R__legal-sec .%R__h2 {
    margin-bottom: 10px;
    font-size: clamp(1.375rem, 0.7vw + 1.1rem, 1.75rem);
  }
  .%R .%R__legal-num { margin-right: 8px; color: var(--hl-gold-text); }
  .%R .%R__review {
    margin: 12px 0 0;
    padding: 14px 18px;
    border: 1px dashed var(--hl-gold-text);
    border-radius: 6px;
    background: #FFFDF7;
    font-size: 0.9375rem;
    line-height: 1.6;
    color: var(--hl-ink);
  }
  .%R .%R__review strong { color: var(--hl-gold-text); }
  .%R .%R__review ul { margin: 8px 0 0; padding: 0 0 0 20px; }
  .%R .%R__review li { margin: 4px 0; }
"""

CSS["stages"] = """
  /* ---------- Photo beside the detailed stages ---------- */
  .%R .%R__stage-grid {
    display: grid;
    grid-template-columns: minmax(0, 4fr) minmax(0, 7fr);
    gap: clamp(40px, 6vw, 88px);
    align-items: start;
  }
  .%R .%R__stage-grid--even { grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); }
  .%R .%R__stage-media {
    position: sticky;
    top: 110px;
  }
  @media (max-width: 900px) {
    .%R .%R__stage-grid,
    .%R .%R__stage-grid--even { grid-template-columns: minmax(0, 1fr); }
    .%R .%R__stage-media { position: static; }
  }
"""

# ---------------------------------------------------------------------------
# Icons and small shared pieces (SVG line icons, stroke = currentColor)
# ---------------------------------------------------------------------------
def svg(paths, box="0 0 24 24", sw="1.6"):
    return (f'<svg viewBox="{box}" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths}</svg>')


ROOF = svg('<path d="M1.5 11 10 2.5l8.5 8.5"/>', "0 0 20 12")
ARROW = svg('<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>', sw="2")
HOUSE = svg('<path d="M3.5 11 12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>')
CHECK = svg('<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.6 2.6L16 9.5"/>')
SHIELD = svg('<path d="M12 3 4.5 6v5.5c0 4.6 3.1 8.2 7.5 9.5 4.4-1.3 7.5-4.9 7.5-9.5V6L12 3z"/><path d="m9 12 2 2 4-4"/>')
INFO = svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 8h.01"/>')
ICON_PURCHASE = svg('<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v10h13V10"/><circle cx="12" cy="13.5" r="2"/><path d="M12 15.5V18"/>')
ICON_REFI = svg('<path d="M20 12a8 8 0 0 1-13.6 5.7"/><path d="M4 12a8 8 0 0 1 13.6-5.7"/><path d="M17.5 2.8v3.6h-3.6"/><path d="M6.5 21.2v-3.6h3.6"/>')
ICON_OPTIONS = svg('<rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M8 8h8"/><path d="M8 12h8"/><path d="M8 16h5"/>')
ICON_TALK = svg('<path d="M20 15a2 2 0 0 1-2 2H8l-4 3.5V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2z"/><path d="M8 9h8"/><path d="M8 12.5h5"/>')
ICON_PERSON = svg('<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5"/>')
ICON_DECIDE = svg('<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.6 2.6L16 9.5"/>')


def lines_svg(cls):
    """Subtle flowing gold linework for dark bands (decorative)."""
    paths = []
    for i in range(9):
        o = i * 9
        paths.append(f'<path d="M0 {300 - o} C 120 {200 - o}, 220 {320 - o * 0.5:g}, 340 {170 - o} '
                     f'S 520 {60 - o * 0.3:g}, 600 {20 + o * 0.4:g}"/>')
    return (f'<svg class="{cls}" viewBox="0 0 600 320" fill="none" stroke="currentColor" stroke-width="1" '
            f'aria-hidden="true" focusable="false">{"".join(paths)}</svg>')


def eyebrow(text):
    return f'<p class="%R__eyebrow">{ROOF}<span>{text}</span></p>'


def link(href, text):
    return f'<a class="%R__link" href="{href}">{text}{ARROW}</a>'


def btn(href, text, small=False, label=None):
    sz = " %R__btn--sm" if small else ""
    aria = f' aria-label="{label}"' if label else ""
    return f'<a class="%R__btn{sz}" href="{href}"{aria}>{text}{ARROW}</a>'


def points(items, indent="        "):
    lis = "\n".join(f"{indent}  <li>{HOUSE}<span>{t}</span></li>" for t in items)
    return f'{indent}<ul class="%R__points">\n{lis}\n{indent}</ul>'


def cta(title_id, headline, text=None, label=CTA_LABEL, href="/contact"):
    lede = f'\n      <p class="%R__lede">{text}</p>' if text else ""
    return f"""  <section class="%R__s %R__s--dark %R__cta" aria-labelledby="%R-{title_id}">
    {lines_svg("%R__lines %R__lines--br")}
    <div class="%R__in">
      <h2 class="%R__h2" id="%R-{title_id}">{headline}</h2>{lede}
      <div class="%R__actions">
        {btn(href, label)}
      </div>
    </div>
  </section>"""


def banner(title_id, eyebrow_text, h1, lede, dark=False, media=None, center=False):
    cls = " %R__banner--dark" if dark else ""
    lines = f"\n    {lines_svg('%R__lines %R__lines--br')}" if dark else ""
    copy = f"""<div{' class="%R__center"' if center else ''}>
        {eyebrow(eyebrow_text)}
        <h1 class="%R__h1" id="%R-{title_id}">{h1}</h1>
        <p class="%R__lede">{lede}</p>
      </div>"""
    if media:
        inner = f"""<div class="%R__in %R__banner-grid">
      {copy}
      {media}
    </div>"""
    else:
        inner = f"""<div class="%R__in">
      {copy}
    </div>"""
    return f"""  <section class="%R__banner{cls}" aria-labelledby="%R-{title_id}">{lines}
    {inner}
  </section>"""


def photo(key, tall=False, eager=False):
    t = " %R__photo--tall" if tall else ""
    return f'<figure class="%R__photo{t}">{img(key, eager=eager)}</figure>'


def faq_items(items, first_open=False):
    out = []
    for i, (q, a) in enumerate(items):
        op = " open" if first_open and i == 0 else ""
        out.append(f"""        <details{op}>
          <summary>{q}</summary>
          <div class="%R__faq-body">
            <p class="%R__p">{a}</p>
          </div>
        </details>""")
    return "\n".join(out)


def step_list(items, extra_cls="", small=True):
    p_cls = "%R__p %R__p--sm" if small else "%R__p"
    lis = "\n".join(f"""          <li class="%R__step">
            <span class="%R__num" aria-hidden="true">{i}</span>
            <div>
              <h3 class="%R__h3"><span class="%R__sr">Step {i}: </span>{t}</h3>
              <p class="{p_cls}">{d}</p>{extra}
            </div>
          </li>""" for i, (t, d, extra) in enumerate(items, 1))
    return f'        <ol class="%R__steps{extra_cls}">\n{lis}\n        </ol>'


APPLY_SCRIPT = """<script>
  (function () {
    /* ==========================================================
       HOME_LOAN_APPLICATION_URL — the online mortgage application.
       Not confirmed yet. While it's '', every application link on
       this page stays hidden (no broken buttons). When the
       destination is approved, paste its full https:// address
       between the quotes (or set applicationUrl in
       config/site.json and rebuild).
       ========================================================== */
    var HOME_LOAN_APPLICATION_URL = '%APPLICATION_URL%';

    var url = String(HOME_LOAN_APPLICATION_URL || '').trim();
    if (!/^https:\\/\\/[^\\s"'<>]+$/i.test(url)) return;
    var els = document.querySelectorAll('.%R [data-hl-apply]');
    Array.prototype.forEach.call(els, function (el) {
      var a = el.matches('a') ? el : el.querySelector('a[data-hl-apply-link]');
      if (a) a.setAttribute('href', url);
      el.hidden = false;
    });
  })();
</script>"""

# ---------------------------------------------------------------------------
# Shared content (approved copy)
# ---------------------------------------------------------------------------
# slug, full name, card name, Loan Options text, Home card text
PROGRAMS = [
    ("conventional", "Conventional Loans", "Conventional",
     "Conventional financing may be available for eligible primary residences, second homes and investment properties. Down-payment options, mortgage insurance and other requirements depend on the specific program and borrower.",
     "Financing options for eligible homebuyers and property types."),
    ("fha", "FHA Loans", "FHA",
     "FHA loans are government-insured mortgages that may be suitable for a range of borrowers, including some first-time homebuyers. Credit, down-payment and property requirements apply.",
     "Government-insured financing that may suit a range of borrowers."),
    ("va", "VA Loans", "VA",
     "VA loan options are available to eligible veterans, service members and qualifying surviving spouses. Eligibility, entitlement and the specific transaction determine the available options.",
     "Options for eligible veterans, service members and qualifying surviving spouses."),
    ("usda", "USDA Loans", "USDA",
     "USDA financing may be available to eligible borrowers purchasing qualifying properties in eligible areas. Household income, property location and program requirements apply.",
     "Options for eligible borrowers and properties in qualifying areas."),
    ("refinancing", "Refinancing", "Refinancing",
     "Refinancing replaces an existing mortgage with a new loan. Whether it makes sense depends on your goals, available terms, costs and how long you expect to keep the loan.",
     "Discuss whether replacing your existing mortgage may fit your goals."),
    ("down-payment-assistance", "Down Payment Assistance", "Down Payment Assistance",
     "Some eligible buyers may have access to assistance programs. Availability, funding, income limits, location and other conditions vary. Ask which programs may apply to your situation.",
     "Ask about assistance programs that may be available to eligible buyers."),
]

FAQS = [
    ("How do I know which loan is right for me?",
     "The appropriate options depend on your finances, goals, property and program eligibility. Start with a conversation rather than choosing a program based on one advertised feature."),
    ("Do I have to be a first-time buyer?",
     "No. The available options include financing for eligible first-time and repeat buyers, as well as refinancing."),
    ("How much will I need for a down payment?",
     "That depends on the program, property, borrower and transaction. Ask the team to explain the options and other upfront costs relevant to your situation."),
    ("Is down payment assistance available?",
     "Assistance may be available through qualifying programs, but funding, eligibility and availability vary. Ask which options may apply."),
    ("What credit score do I need?",
     "Requirements differ by program and individual circumstances. A credit score alone does not establish approval or determine every available option."),
    ("What documents should I prepare?",
     'Common requests include identification, income documentation and account statements. Requirements differ for employed, self-employed and fixed-income borrowers. See <a href="/homebuyer-resources">Homebuyer Resources</a> for general examples.'),
    ("How long does the mortgage process take?",
     "Timing depends on the transaction, document completeness, property requirements, underwriting and closing conditions. The team can discuss the expected process for your situation."),
    ("Are an appraisal and a home inspection the same?",
     "No. An appraisal assesses value for financing purposes. A home inspection evaluates aspects of a property&rsquo;s condition. Ask which requirements apply to your transaction."),
    ("What is included in a mortgage payment?",
     "Depending on the loan, payments may include principal, interest, property taxes, homeowners insurance and mortgage insurance. The exact structure varies."),
    ("Can I refinance my current mortgage?",
     "Potential options depend on your existing loan, finances, property, goals and available terms. Consider costs and potential benefits before proceeding."),
    ("Does contacting you mean I am approved?",
     "No. A website inquiry starts a conversation. Approval requires the appropriate application, review and underwriting."),
    ("How do I get started?",
     'Use the <a href="/contact">Contact page</a> to share your questions and request a conversation.'),
]
FAQ = dict(FAQS)

PAGES = []


def page(**kw):
    PAGES.append(kw)


# ===========================================================================
# 1. Home (template section order)
# ===========================================================================
cards = "\n".join(f"""        <li class="%R__card">
          <h3 class="%R__card-tab">{short}</h3>
          <p class="%R__p %R__p--sm">{summary}</p>
          {btn("/loan-options#" + slug, "Learn More", small=True, label="Learn more about " + name)}
        </li>""" for slug, name, short, _, summary in PROGRAMS)

home_faqs = faq_items([
    ("Which loan option might fit my circumstances?", FAQ["How do I know which loan is right for me?"]),
    ("How much will I need for a down payment?", FAQ["How much will I need for a down payment?"]),
    ("What documents should I prepare?", FAQ["What documents should I prepare?"]),
    ("How long does the mortgage process take?", FAQ["How long does the mortgage process take?"]),
], first_open=True)

page(
    file="home-loans-home.html", route="/", root="cbhl-home",
    title="Covered Bridge Home Loans | Home Purchase &amp; Refinancing Guidance",
    meta="Explore home purchase and refinancing options with Covered Bridge Home Loans, including Conventional, FHA, VA and USDA loans, with guidance through the mortgage process.",
    css=["base", "hero", "comp", "benefits", "cards", "steps", "resource", "faq"],
    body=f"""  <!-- A. Photographic hero -->
  <section class="%R__hero" aria-labelledby="%R-title">
    {img("hero", "%R__hero-img", eager=True)}
    <div class="%R__hero-shade" aria-hidden="true"></div>
    <div class="%R__in">
      <div class="%R__hero-copy">
        {eyebrow("Home Purchase &amp; Refinancing")}
        <h1 class="%R__h1" id="%R-title">Your next chapter starts at home.</h1>
        <p class="%R__lede">Whether you&rsquo;re buying your first home, planning your next move or exploring refinancing, Covered Bridge Home Loans helps you understand your options and take the next step with confidence.</p>
        <div class="%R__actions">
          {btn("/contact", CTA_LABEL)}
          {link("/loan-options", "Explore Loan Options")}
        </div>
      </div>
    </div>
  </section>

  <!-- B. Overlapping question panel -->
  <section class="%R__panel-band" aria-label="Get started">
    <div class="%R__panel">
      <div class="%R__panel-col">
        <h2 class="%R__h2">Questions about your next move?</h2>
        <p class="%R__p %R__p--sm">Start with a conversation about buying, refinancing or understanding your home-loan options.</p>
        {link("/contact", "Ask the Team")}
      </div>
      <div class="%R__panel-col">
        <h2 class="%R__h2">Explore your options.</h2>
        <p class="%R__p %R__p--sm">Find a starting point that fits your plans.</p>
        {btn("/loan-options", "View Loan Options", small=True)}
      </div>
    </div>
  </section>

  <!-- C. Introduction with overlapping photos -->
  <section class="%R__s %R__s--white" aria-labelledby="%R-who">
    <div class="%R__in %R__split">
      <div class="%R__comp">
        {img("couplePlanning", "%R__comp-a")}
        {img("advisor", "%R__comp-b")}
        <p class="%R__comp-badge" aria-hidden="true">Guidance for your next chapter</p>
      </div>
      <div>
        {eyebrow("Who We Are")}
        <h2 class="%R__h2" id="%R-who">Home financing starts with understanding your plans.</h2>
        <p class="%R__p">A home loan is a personal decision. Covered Bridge Home Loans helps you explore potential options, prepare the requested information and understand the next steps in the mortgage process.</p>
        <div class="%R__actions">
          {btn("/about", "About Covered Bridge Home Loans")}
        </div>
      </div>
    </div>
  </section>

  <!-- D. Dark benefits band -->
  <section class="%R__s %R__s--dark" aria-labelledby="%R-benefits">
    {lines_svg("%R__lines %R__lines--bl")}
    {lines_svg("%R__lines %R__lines--br")}
    <div class="%R__in">
      <div class="%R__center">
        {eyebrow("A Clearer Path Forward")}
        <h2 class="%R__h2" id="%R-benefits">Support for your <span class="%R__gold">homeownership</span> journey.</h2>
      </div>
      <ul class="%R__icons">
        <li><span class="%R__icon">{ICON_PURCHASE}</span><span>Home Purchase</span></li>
        <li><span class="%R__icon">{ICON_REFI}</span><span>Refinancing</span></li>
        <li><span class="%R__icon">{ICON_OPTIONS}</span><span>Loan Options</span></li>
      </ul>
      <hr class="%R__divider">
      <div class="%R__benefit-grid">
        <ul class="%R__checks">
          <li>{CHECK}<div><h3 class="%R__h3">Clear Communication</h3><p class="%R__p %R__p--sm">Understand the questions, information and next steps relevant to your situation.</p></div></li>
          <li>{CHECK}<div><h3 class="%R__h3">Individual Circumstances</h3><p class="%R__p %R__p--sm">Discuss financing in the context of your goals, finances and property.</p></div></li>
          <li>{CHECK}<div><h3 class="%R__h3">Informed Decisions</h3><p class="%R__p %R__p--sm">Take time to understand the terms, costs and responsibilities before moving forward.</p></div></li>
        </ul>
        <div>
          <h3 class="%R__h2">Start with your goals.</h3>
          <p class="%R__p">Whether you are preparing for a purchase or considering a refinance, begin by explaining what you want to accomplish.</p>
          {link("/how-it-works", "See How It Works")}
        </div>
      </div>
    </div>
  </section>

  <!-- E. Loan-option cards -->
  <section class="%R__s" aria-labelledby="%R-options">
    <div class="%R__in">
      <div class="%R__cards-head">
        <div>
          {eyebrow("Loan Options")}
          <h2 class="%R__h2" id="%R-options">Different paths. One important decision.</h2>
        </div>
        <p class="%R__p">Explore the main program categories, then discuss which options may fit your circumstances.</p>
      </div>
      <ul class="%R__cards">
{cards}
      </ul>
    </div>
  </section>

  <!-- F. Overlapping photos and numbered process -->
  <section class="%R__s %R__s--white" aria-labelledby="%R-how">
    <div class="%R__in %R__split">
      <div class="%R__comp %R__comp--process">
        {img("familyMoving", "%R__comp-a")}
        {img("advisor", "%R__comp-b")}
      </div>
      <div>
        {eyebrow("How It Works")}
        <h2 class="%R__h2" id="%R-how">Know what comes next.</h2>
{step_list([
    ("Start a conversation", "Discuss your purchase or refinance goals and initial questions.", ""),
    ("Prepare and apply", "Use the designated application process and gather the information requested for your situation.", ""),
    ("Move through review", "Understand the processing, underwriting and closing steps that apply to your transaction.", ""),
])}
        <div class="%R__actions">
          {link("/how-it-works", "Explore the Full Process")}
        </div>
      </div>
    </div>
  </section>

  <!-- G. Resources: prepare with confidence -->
  <section class="%R__s %R__s--band %R__s--tight" aria-labelledby="%R-prepare">
    <div class="%R__in %R__res">
      <div>
        <h2 class="%R__h2" id="%R-prepare">Prepare with confidence.</h2>
        <p class="%R__p">Explore common mortgage questions and the documents that may be requested for your situation.</p>
      </div>
      <ul class="%R__tiles">
        <li><a class="%R__tile" href="/homebuyer-resources">Homebuyer Resources{ARROW}</a></li>
        <li><a class="%R__tile" href="/faqs">Frequently Asked Questions{ARROW}</a></li>
      </ul>
    </div>
  </section>

  <!-- H. FAQ preview -->
  <section class="%R__s %R__s--white" aria-labelledby="%R-faq">
    <div class="%R__in">
      <div class="%R__head %R__center">
        {eyebrow("FAQs")}
        <h2 class="%R__h2" id="%R-faq">Frequently asked questions</h2>
      </div>
      <div class="%R__faq">
{home_faqs}
      </div>
      <div class="%R__actions %R__center">
        {link("/faqs", "View All FAQs")}
      </div>
    </div>
  </section>""",
)

# ===========================================================================
# 2. Loan Options
# ===========================================================================
programs = "\n\n".join(f"""  <section class="%R__s{' %R__s--white' if i % 2 else ''} %R__s--tight" id="{slug}" aria-labelledby="%R-{slug}">
    <div class="%R__in %R__program">
      <div>
        <span class="%R__program-num" aria-hidden="true">{i + 1:02d}</span>
        <h2 class="%R__h2" id="%R-{slug}">{name}</h2>
      </div>
      <p class="%R__p">{text}</p>
    </div>
  </section>""" for i, (slug, name, _, text, _) in enumerate(PROGRAMS))

page(
    file="home-loans-loan-options.html", route="/loan-options", root="cbhl-loans",
    title="Loan Options | Covered Bridge Home Loans",
    meta="Learn about Conventional, FHA, VA and USDA loans, refinancing and down payment assistance, then discuss which options may fit with the Covered Bridge Home Loans team.",
    css=["base", "banner", "photo", "rows"],
    body=f"""{banner("title", "Loan Options", "Understand your home-loan options.",
       "The right starting point depends on your goals, finances, property and eligibility. Explore the main program categories, then discuss the details with the team.",
       media=photo("resources", eager=True))}

{programs}

{cta("start", "Not sure where to start?", "You do not need to choose a program before speaking with the team. Start by explaining your plans and asking which options may fit.", label="Discuss Your Options")}""",
)

# ===========================================================================
# 3. How It Works
# ===========================================================================
APPLY_LINK = '\n              <p hidden data-hl-apply><a class="%R__link" data-hl-apply-link>Start your application' + ARROW + '</a></p>'

page(
    file="home-loans-how-it-works.html", route="/how-it-works", root="cbhl-how",
    title="How the Home Loan Process Works | Covered Bridge Home Loans",
    meta="Understand the main stages of a home loan, from your first conversation and application to documents, review and closing, so you can prepare for each step.",
    css=["base", "banner", "photo", "steps", "lists", "stages"],
    apply=True,
    body=f"""{banner("title", "How It Works", "Know what comes next.",
       "Every home-loan situation is different, but understanding the main stages can help you prepare.", dark=True)}

  <section class="%R__s %R__s--white" aria-labelledby="%R-stages">
    <div class="%R__in %R__stage-grid">
      <div class="%R__stage-media">
        {photo("advisor", tall=True)}
      </div>
      <div>
        {eyebrow("The Main Stages")}
        <h2 class="%R__h2" id="%R-stages">From first conversation to closing</h2>
{step_list([
    ("Discuss your plans", "Talk about your purchase or refinance goals, timing and financial circumstances.", ""),
    ("Complete the appropriate application", "When you are ready, use the designated application process and provide the requested information. An inquiry alone is not a completed mortgage application or approval.", APPLY_LINK),
    ("Prepare your documents", "Gather the income, asset, identification and property information requested for your situation.", ""),
    ("Move through review", "Depending on your transaction, the process may include disclosures, processing, property valuation, underwriting and requests for additional information.", ""),
    ("Prepare for closing", "If the loan is approved and closing conditions are satisfied, review the final documents and complete the required closing steps.", ""),
], extra_cls=" %R__steps--large", small=False)}
      </div>
    </div>
  </section>

  <section class="%R__s" aria-labelledby="%R-moving">
    <div class="%R__in %R__stage-grid %R__stage-grid--even">
      <div>
        {eyebrow("Along the Way")}
        <h2 class="%R__h2" id="%R-moving">Keep the process moving</h2>
      </div>
{points([
    "Respond to document requests promptly.",
    "Ask about anything you do not understand.",
    "Discuss significant financial changes with your loan professional while the loan is in progress.",
], indent="      ")}
    </div>
  </section>

{cta("closing", "Start with your questions.")}""",
)

# ===========================================================================
# 4. Homebuyer Resources
# ===========================================================================
GLOSSARY = [
    ("Down Payment", "The portion of the purchase price paid upfront rather than financed through the mortgage."),
    ("Earnest Money", "A deposit made as part of a purchase agreement. Its treatment depends on the contract and closing arrangements."),
    ("Appraisal", "An assessment of property value used in the financing process. It serves a different purpose from a home inspection."),
    ("Mortgage Insurance", "Insurance required with some loan arrangements. Its cost and cancellation rules depend on the loan type and applicable requirements."),
    ("Escrow", "An arrangement used with some mortgages to collect funds for expenses such as property taxes and homeowners insurance."),
    ("Closing Costs", "Transaction expenses associated with completing a purchase or refinance. Ask for an explanation of the costs relevant to your loan."),
]
gloss = "\n".join(f"""        <div>
          <dt>{t}</dt>
          <dd>{d}</dd>
        </div>""" for t, d in GLOSSARY)

DOCS = [
    ("Employed / W-2 Borrowers",
     "Common requests may include identification, recent pay statements, W-2 forms and account statements for funds used in the transaction."),
    ("Self-Employed Borrowers",
     "Common requests may include identification, tax returns, business or income documentation and relevant account statements."),
    ("Retired / Fixed-Income Borrowers",
     "Common requests may include identification, pension or Social Security award information and relevant account statements."),
]
docs = "\n".join(f"""        <li class="%R__card">
          <h3 class="%R__card-tab">{t}</h3>
          <p class="%R__p %R__p--sm">{d}</p>
        </li>""" for t, d in DOCS)

page(
    file="home-loans-resources.html", route="/homebuyer-resources", root="cbhl-res",
    title="Homebuyer Resources | Covered Bridge Home Loans",
    meta="Commonly requested mortgage documents, plain-language mortgage terms and questions worth asking before your home-loan conversation.",
    css=["base", "banner", "photo", "cards", "gloss", "lists"],
    body=f"""{banner("title", "Homebuyer Resources", "A little preparation goes a long way.",
       "Use these starting points to organize your questions and prepare for a conversation about your mortgage.",
       media=photo("resources", eager=True))}

  <section class="%R__s %R__s--white" aria-labelledby="%R-docs">
    <div class="%R__in">
      <div class="%R__head">
        {eyebrow("Documents")}
        <h2 class="%R__h2" id="%R-docs">Documents commonly requested</h2>
        <p class="%R__p">The exact documents depend on your circumstances and the loan program. Your loan professional will explain what is needed.</p>
      </div>
      <ul class="%R__cards %R__cards--plain">
{docs}
      </ul>
      <p class="%R__note">These are general examples, not a complete application checklist. Additional documents may be requested.</p>
      <div class="%R__callout" role="note">
        {SHIELD}
        <div>
          <h3 class="%R__h3">Security note</h3>
          <p class="%R__p %R__p--sm">Do not send identification, tax returns, bank statements or other sensitive documents through a general website inquiry. Use the designated document-submission process when instructed.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="%R__s" aria-labelledby="%R-terms">
    <div class="%R__in">
      <div class="%R__head">
        {eyebrow("Terms")}
        <h2 class="%R__h2" id="%R-terms">Mortgage terms in plain language</h2>
      </div>
      <dl class="%R__gloss">
{gloss}
      </dl>
    </div>
  </section>

  <section class="%R__s %R__s--white" aria-labelledby="%R-questions">
    <div class="%R__in %R__narrow">
      {eyebrow("Your Conversation")}
      <h2 class="%R__h2" id="%R-questions">Questions worth asking</h2>
{points([
    "Which programs might fit my circumstances?",
    "What upfront funds should I prepare?",
    "What costs and mortgage-insurance requirements apply?",
    "Which documents are needed?",
    "What could affect the timeline?",
    "What should I understand before accepting the loan terms?",
], indent="      ")}
    </div>
  </section>

{cta("closing", "Have a question about your situation?", label="Ask the Team")}""",
)

# ===========================================================================
# 5. FAQs
# ===========================================================================
page(
    file="home-loans-faqs.html", route="/faqs", root="cbhl-faq",
    title="Home Loan FAQs | Covered Bridge Home Loans",
    meta="Answers to common questions about loan options, down payments, credit, documents, timing, appraisals, mortgage payments and refinancing.",
    css=["base", "banner", "faq"],
    body=f"""{banner("title", "FAQs", "Your home-loan questions, answered.",
       "Clear starting points for your homebuying or refinancing conversation.", center=True)}

  <section class="%R__s %R__s--white" aria-label="Frequently asked questions">
    <div class="%R__in">
      <div class="%R__faq">
{faq_items(FAQS)}
      </div>
    </div>
  </section>

{cta("closing", "Still have questions?")}""",
)

# ===========================================================================
# 6. About
# ===========================================================================
page(
    file="home-loans-about.html", route="/about", root="cbhl-about",
    title="About | Covered Bridge Home Loans",
    meta="Covered Bridge Home Loans helps individuals and families explore mortgage options for buying or refinancing a home. Part of Covered Bridge Brands.",
    css=["base", "comp", "benefits"],
    body=f"""  <section class="%R__s %R__s--band" aria-labelledby="%R-title">
    <div class="%R__in %R__split">
      <div class="%R__comp %R__comp--landscape">
        {img("couplePlanning", "%R__comp-a", eager=True)}
        {img("consultation", "%R__comp-b")}
      </div>
      <div>
        {eyebrow("About")}
        <h1 class="%R__h1" id="%R-title">Guidance for one of life&rsquo;s important decisions.</h1>
        <p class="%R__lede">Covered Bridge Home Loans helps individuals and families explore mortgage options for buying or refinancing a home.</p>
      </div>
    </div>
  </section>

  <section class="%R__s %R__s--white" aria-labelledby="%R-approach">
    <div class="%R__in %R__narrow">
      {eyebrow("Our Approach")}
      <h2 class="%R__h2" id="%R-approach">Your home. Your plans. A clearer next step.</h2>
      <p class="%R__p">A home loan is a personal decision. Your circumstances, questions and priorities matter.</p>
      <p class="%R__p">Our focus is on helping you understand potential options, prepare the requested information and navigate the next steps in the mortgage process.</p>
      <p class="%R__p">Whether you are starting your first home search or considering a refinance, begin with a conversation about what you want to accomplish.</p>
    </div>
  </section>

  <section class="%R__s %R__s--dark" aria-labelledby="%R-values">
    {lines_svg("%R__lines %R__lines--bl")}
    <div class="%R__in">
      <div class="%R__center">
        {eyebrow("What We Value")}
        <h2 class="%R__h2" id="%R-values">What matters along the way</h2>
      </div>
      <ul class="%R__icons">
        <li><span class="%R__icon">{ICON_TALK}</span><span><span class="%R__value-title">Clear Communication</span><span class="%R__value-text">Understand the questions, information and next steps relevant to your situation.</span></span></li>
        <li><span class="%R__icon">{ICON_PERSON}</span><span><span class="%R__value-title">Individual Circumstances</span><span class="%R__value-text">Discuss financing in the context of your goals, finances and property.</span></span></li>
        <li><span class="%R__icon">{ICON_DECIDE}</span><span><span class="%R__value-title">Informed Decisions</span><span class="%R__value-text">Take time to understand the terms, costs and responsibilities before moving forward.</span></span></li>
      </ul>
    </div>
  </section>

  <section class="%R__s" aria-labelledby="%R-family">
    <div class="%R__in %R__narrow %R__center">
      {eyebrow("Our Family of Brands")}
      <h2 class="%R__h2" id="%R-family">Part of Covered Bridge Brands</h2>
      <p class="%R__p">Covered Bridge Home Loans is part of the Covered Bridge Brands family.</p>
      <div class="%R__actions">
        {link("https://coveredbridgebrands.com/", "Visit Covered Bridge Brands")}
      </div>
    </div>
  </section>

{cta("closing", "Tell us about your next chapter.")}""",
)

# ===========================================================================
# 7. Contact
# ===========================================================================
page(
    file="home-loans-contact.html", route="/contact", root="cbhl-contact",
    title="Contact | Covered Bridge Home Loans",
    meta="Buying, refinancing or simply exploring? Share your questions and start a conversation with Covered Bridge Home Loans.",
    css=["base", "banner", "photo", "contact"],
    apply=True,
    body=f"""{banner("title", "Contact", "Let&rsquo;s talk about your home-loan plans.",
       "Buying, refinancing or simply exploring? Share a few initial details and your questions.")}

  <section class="%R__s %R__s--white" aria-labelledby="%R-inquiry">
    <div class="%R__in %R__contact">
      <div>
        {photo("consultation")}
      </div>
      <div>
        {eyebrow("Inquiry")}
        <h2 class="%R__h2" id="%R-inquiry">Start a Conversation</h2>
        <p class="%R__p">Tell us what you are planning so the team can help you understand the appropriate next step.</p>
        <div class="%R__form" aria-label="Inquiry form"><!--
          >>> GHL FORM EMBED GOES HERE (integration dependency) <<<
          Paste the native Covered Bridge Home Loans GHL form's embed code
          between this comment and the closing </div>. While this box is
          empty it is hidden, so visitors never see an empty panel.

          Intended fields:
            Full name (required) · Email (required) · Phone (optional)
            What can we help with? (required): Buying a Home / Refinancing /
              Exploring Loan Options / General Question
            Property state, if known (optional) · Brief message (optional)
          Do NOT collect: SSN, date of birth, credit score, income or account
          details, identification files, tax returns or bank statements.
          Add any required communication-consent wording in the GHL form
          itself; no credit-check authorization, bundled marketing consent
          or SMS enrollment.
        --></div>
        <ul class="%R__notices">
          <li>{SHIELD}<span>Please do not include sensitive financial or identification information. This form is for general inquiries and is not a mortgage application.</span></li>
          <li>{INFO}<span>See our <a href="/privacy-policy">Privacy Policy</a> for information about how inquiry details are handled.</span></li>
        </ul>
        <div class="%R__apply" hidden data-hl-apply>
          <h3 class="%R__h3">Ready to apply?</h3>
          <p class="%R__p %R__p--sm">If you&rsquo;re ready to begin a mortgage application, use the online application.</p>
          <div class="%R__actions">
            <a class="%R__btn %R__btn--sm" data-hl-apply-link>Start Your Application{ARROW}</a>
          </div>
        </div>
      </div>
    </div>
  </section>""",
)

# ===========================================================================
# 8–9. Legal drafts
# ===========================================================================
def legal_sections(items):
    out = []
    for i, (title, text, review) in enumerate(items, 1):
        body = f'\n        <p class="%R__p">{text}</p>' if text else ""
        if isinstance(review, list):
            lis = "".join(f"<li>{r}</li>" for r in review)
            rv = f'\n        <div class="%R__review"><strong>Review:</strong><ul>{lis}</ul></div>'
        elif review:
            rv = f'\n        <p class="%R__review"><strong>Review:</strong> {review}</p>'
        else:
            rv = ""
        out.append(f"""      <section class="%R__legal-sec" aria-labelledby="%R-s{i}">
        <h2 class="%R__h2" id="%R-s{i}"><span class="%R__legal-num">{i}.</span>{title}</h2>{body}{rv}
      </section>""")
    return "\n".join(out)


PRIVACY = [
    ("Website operator", "",
     "Confirm the responsible legal entity, trading name and privacy contact. Do not replace a registered entity name solely because the website branding changes."),
    ("Information collected",
     "The planned general inquiry form requests contact details and a brief description of the visitor&rsquo;s home-loan questions.",
     "Confirm final form fields, logs and other collection methods."),
    ("How information is used",
     "Proposed purposes include responding to inquiries and managing related communications.",
     "Confirm actual purposes and any separately authorized marketing activity."),
    ("Providers and sharing", "",
     "Identify relevant CRM, website and service providers and explain any sharing with mortgage/application providers."),
    ("Separate mortgage applications", "",
     "Identify the designated application provider and the policies/disclosures applicable to that separate process."),
    ("Cookies and analytics", "",
     "Confirm which technologies are actually enabled."),
    ("Retention and protection", "",
     "Confirm retention practices and accurately describe safeguards. Do not promise absolute security."),
    ("Requests and communication preferences", "",
     "Supply the correct contact channel and applicable procedures."),
    ("External links",
     "External websites and application services may have their own privacy policies.", ""),
    ("Effective date and contact", "",
     "Supply the approved effective date, responsible entity and contact information."),
]

TERMS = [
    ("Website purpose",
     "This website provides general information about home-loan options and a way to make an inquiry.", ""),
    ("No approval or commitment",
     "Website information and inquiry submissions do not constitute a mortgage approval, financing offer, rate lock or commitment to lend.", ""),
    ("Program information",
     "Loan options, eligibility, down payments, costs and terms depend on the applicable program and individual circumstances. All loans are subject to credit and underwriting approval.", ""),
    ("Applications and agreements",
     "Any mortgage application, financing offer or transaction is governed by its applicable documents, disclosures and agreements.", ""),
    ("General information",
     "Website content is general information and does not replace advice appropriate to your individual legal, tax or financial circumstances.", ""),
    ("Information submitted",
     "Provide accurate inquiry information and do not submit information you are not authorized to share. Do not include sensitive financial or identification details in a general inquiry.", ""),
    ("Appropriate use",
     "Do not misuse the website, disrupt its operation or attempt unauthorized access.", ""),
    ("External services",
     "External websites and application services may have separate terms and policies.", ""),
    ("Privacy",
     'Please review our <a href="/privacy-policy">Privacy Policy</a> for information about the website&rsquo;s data practices.', ""),
    ("Content ownership and legal details", "",
     ["Confirm the responsible legal entity.",
      "Confirm authorized use of branding and third-party content.",
      "Add approved contact details and effective date.",
      "Obtain any necessary additional legal provisions."]),
]

LEGAL_COMMENT = """<!-- LEGAL DRAFT: not ready to publish. The review notes below are
     intentionally visible while this page is a draft. Replace each
     one with approved wording (or remove it) after legal review, and
     remove the draft status line when the page is approved. -->"""


def legal_page(title, status, sections, opening=""):
    open_p = f'\n      <p class="%R__lede">{opening}</p>' if opening else ""
    return f"""  {LEGAL_COMMENT}
  <section class="%R__banner" aria-labelledby="%R-title">
    <div class="%R__in %R__legal">
      {eyebrow("Legal")}
      <h1 class="%R__h1" id="%R-title">{title}</h1>{open_p}
      <p class="%R__status" role="note">{status}</p>
    </div>
  </section>

  <div class="%R__s %R__s--white">
    <div class="%R__in %R__legal">
{legal_sections(sections)}
    </div>
  </div>"""


page(
    file="home-loans-privacy-policy-draft.html", route="/privacy-policy", root="cbhl-privacy",
    title="Privacy Policy | Covered Bridge Home Loans",
    meta="Privacy Policy for the Covered Bridge Home Loans website and its general inquiry process.",
    css=["base", "banner", "legal"],
    body=legal_page("Privacy Policy",
                    "Draft &mdash; business identity and data practices require confirmation before publication.",
                    PRIVACY,
                    "This draft identifies the privacy information to be confirmed for the Covered Bridge Home Loans website and its general inquiry process."),
)

page(
    file="home-loans-terms-draft.html", route="/terms", root="cbhl-terms",
    title="Terms of Use | Covered Bridge Home Loans",
    meta="Terms of Use for the Covered Bridge Home Loans website.",
    css=["base", "banner", "legal"],
    body=legal_page("Terms of Use",
                    "Draft &mdash; legal identity and applicable terms require confirmation before publication.",
                    TERMS),
)

# ===========================================================================
# Shared header
# ===========================================================================
NAV = [("/", "Home"), ("/about", "About"), ("/loan-options", "Loan Options"), ("/how-it-works", "How It Works"),
       ("/homebuyer-resources", "Resources"), ("/faqs", "FAQs"), ("/contact", "Contact")]
HEADER_BP = 1240

HEADER = """<!-- ============================================================
     COVERED BRIDGE HOME LOANS — SHARED HEADER
     Paste once into a GHL Custom HTML/JavaScript element inside a
     GLOBAL SECTION at the top of the site, and add that global
     section to every page (don't paste a copy per page).
     Styles are scoped to .%R; the script only touches .%R.

     Slim dark bar pinned with position: fixed (sticky doesn't survive
     GHL's element wrappers); the outer box reserves the bar's height.
     Logo: the Covered Bridge Brands logo, embedded unless
     config/site.json supplies a GHL Media link.
     ============================================================ -->
<style>
  .%R {""" + TOKENS + """
    --%R-h: 76px;
    position: relative;
    display: block;
    width: 100%;
    height: var(--%R-h);
    margin: 0;
    padding: 0;
    background: var(--hl-black);
    font-family: var(--hl-sans);
  }
  .%R,
  .%R *,
  .%R *::before,
  .%R *::after {
    box-sizing: border-box;
  }
  .%R .%R__bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    margin: 0;
    padding: 0 clamp(16px, 3vw, 40px);
    background: var(--hl-black);
    border-bottom: 1px solid rgba(210, 163, 76, 0.35);
    transition: box-shadow 0.25s ease;
  }
  .%R.is-scrolled .%R__bar { box-shadow: 0 8px 28px rgba(0, 0, 0, 0.45); }
  .%R .%R__inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    max-width: 1280px;
    height: var(--%R-h);
    margin: 0 auto;
  }

  /* ---- Identity ---- */
  .%R .%R__brand {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 0 1 auto;
    min-width: 0;
    text-decoration: none;
  }
  .%R .%R__logo {
    display: block;
    width: auto;
    height: 34px;
    border: 0;
  }
  .%R .%R__rule {
    flex: 0 0 1px;
    width: 1px;
    height: 32px;
    background: rgba(210, 163, 76, 0.45);
  }
  .%R .%R__name {
    display: flex;
    flex-direction: column;
    line-height: 1.15;
    white-space: nowrap;
  }
  .%R .%R__name-top {
    font-size: 0.625rem;
    font-weight: 600;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--hl-gold);
  }
  .%R .%R__name-main {
    font-family: var(--hl-serif);
    font-size: 1.1875rem;
    font-weight: 600;
    color: var(--hl-warm);
  }
  .%R .%R__brand:focus-visible {
    outline: 2px solid var(--hl-gold-hover);
    outline-offset: 4px;
  }

  /* ---- Navigation ---- */
  .%R .%R__nav {
    display: flex;
    align-items: center;
    gap: clamp(18px, 2vw, 28px);
  }
  .%R .%R__list {
    display: flex;
    align-items: center;
    gap: clamp(14px, 1.6vw, 24px);
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__item { margin: 0; padding: 0; }
  .%R .%R__item::marker { content: none; }
  .%R .%R__link {
    position: relative;
    display: inline-block;
    padding: 8px 0;
    font-size: 0.9375rem;
    font-weight: 500;
    line-height: 1.2;
    white-space: nowrap;
    color: var(--hl-warm);
    text-decoration: none;
    transition: color 0.2s ease;
  }
  .%R .%R__link::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: -2px;
    height: 2px;
    background: var(--hl-gold);
    transform: scaleX(0);
    transform-origin: left center;
    transition: transform 0.25s ease;
  }
  .%R .%R__link:hover,
  .%R .%R__link[aria-current="page"] { color: var(--hl-gold); }
  .%R .%R__link:hover::after,
  .%R .%R__link[aria-current="page"]::after { transform: scaleX(1); }
  .%R .%R__cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 44px;
    padding: 0 22px;
    border-radius: 999px;
    background: var(--hl-gold);
    color: #0D0D0D;
    font-size: 0.9375rem;
    font-weight: 600;
    line-height: 1.2;
    white-space: nowrap;
    text-decoration: none;
    transition: background-color 0.2s ease;
  }
  .%R .%R__cta:hover { background: var(--hl-gold-hover); color: #0D0D0D; }
  .%R .%R__link:focus-visible,
  .%R .%R__cta:focus-visible {
    outline: 2px solid var(--hl-gold-hover);
    outline-offset: 4px;
  }

  /* ---- Menu button ---- */
  .%R .%R__toggle {
    display: none;
    flex: 0 0 auto;
    flex-direction: column;
    justify-content: center;
    align-items: stretch;
    gap: 6px;
    width: 46px;
    height: 46px;
    margin: 0;
    padding: 0 11px;
    border: 1px solid rgba(210, 163, 76, 0.55);
    border-radius: 6px;
    background: transparent;
    cursor: pointer;
    -webkit-appearance: none;
    appearance: none;
  }
  .%R .%R__toggle:focus-visible {
    outline: 2px solid var(--hl-gold-hover);
    outline-offset: 3px;
  }
  .%R .%R__toggle-line {
    display: block;
    width: 100%;
    height: 1.5px;
    background: var(--hl-gold);
    transition: transform 0.25s ease, opacity 0.2s ease;
  }
  .%R.is-open .%R__toggle-line:nth-child(1) { transform: translateY(7.5px) rotate(45deg); }
  .%R.is-open .%R__toggle-line:nth-child(2) { opacity: 0; }
  .%R.is-open .%R__toggle-line:nth-child(3) { transform: translateY(-7.5px) rotate(-45deg); }
  .%R .%R__sr {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  @media (max-width: %BPpx) {
    .%R { --%R-h: 68px; }
    .%R .%R__toggle { display: flex; }
    .%R .%R__nav {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      display: block;
      max-height: 0;
      overflow: hidden;
      visibility: hidden;
      background: var(--hl-black);
      border-bottom: 1px solid rgba(210, 163, 76, 0);
      transition: max-height 0.35s ease, visibility 0s linear 0.35s, border-color 0.35s ease;
    }
    .%R.is-open .%R__nav {
      max-height: calc(100vh - var(--%R-h));
      overflow-y: auto;
      visibility: visible;
      border-bottom-color: rgba(210, 163, 76, 0.45);
      box-shadow: 0 18px 36px rgba(0, 0, 0, 0.5);
      transition: max-height 0.35s ease, visibility 0s linear 0s, border-color 0.35s ease;
    }
    .%R .%R__list {
      flex-direction: column;
      align-items: stretch;
      gap: 0;
      padding: 6px clamp(16px, 4vw, 40px) 0;
    }
    .%R .%R__link {
      display: block;
      padding: 15px 0;
      border-bottom: 1px solid rgba(210, 163, 76, 0.15);
      font-size: 1.0625rem;
    }
    .%R .%R__link::after { right: auto; bottom: 9px; width: 28px; }
    .%R .%R__cta {
      display: flex;
      min-height: 52px;
      margin: 18px clamp(16px, 4vw, 40px) 22px;
      font-size: 1rem;
    }
  }
  @media (max-width: 560px) {
    .%R .%R__logo,
    .%R .%R__rule { display: none; }
  }
  @media (prefers-reduced-motion: reduce) {
    .%R .%R__bar,
    .%R .%R__link,
    .%R .%R__link::after,
    .%R .%R__toggle-line,
    .%R .%R__nav,
    .%R .%R__cta { transition: none; }
  }
</style>

<div class="%R">
  <header class="%R__bar">
    <div class="%R__inner">
      <a class="%R__brand" href="/" aria-label="Covered Bridge Home Loans home">
        <img class="%R__logo" src="%IMG:logo%" alt="" width="480" height="100" decoding="async">
        <span class="%R__rule" aria-hidden="true"></span>
        <span class="%R__name" aria-hidden="true">
          <span class="%R__name-top">Covered Bridge</span>
          <span class="%R__name-main">Home Loans</span>
        </span>
      </a>

      <button class="%R__toggle" type="button" aria-expanded="false" aria-controls="%R-nav">
        <span class="%R__toggle-line" aria-hidden="true"></span>
        <span class="%R__toggle-line" aria-hidden="true"></span>
        <span class="%R__toggle-line" aria-hidden="true"></span>
        <span class="%R__sr">Open menu</span>
      </button>

      <nav class="%R__nav" id="%R-nav" aria-label="Main">
        <ul class="%R__list">
%NAV%
        </ul>
        <a class="%R__cta" href="/contact">""" + CTA_LABEL + """</a>
      </nav>
    </div>
  </header>
</div>

<script>
  (function () {
    var roots = document.querySelectorAll('.%R:not([data-ready])');
    Array.prototype.forEach.call(roots, function (root) {
      root.setAttribute('data-ready', '');
      var toggle = root.querySelector('.%R__toggle');
      var label = root.querySelector('.%R__sr');
      var links = root.querySelectorAll('.%R__nav a');
      var desktop = window.matchMedia('(min-width: %BP1px)');

      /* Current page: gold link + aria-current, matched from the URL */
      var clean = function (p) { return (p || '/').replace(/\\/+$/, '') || '/'; };
      var here = clean(window.location.pathname);
      Array.prototype.forEach.call(root.querySelectorAll('.%R__link'), function (a) {
        if (clean(a.getAttribute('href')) === here) a.setAttribute('aria-current', 'page');
      });

      var setOpen = function (open) {
        root.classList.toggle('is-open', open);
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        label.textContent = open ? 'Close menu' : 'Open menu';
      };
      toggle.addEventListener('click', function () {
        setOpen(!root.classList.contains('is-open'));
      });
      Array.prototype.forEach.call(links, function (a) {
        a.addEventListener('click', function () { setOpen(false); });
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && root.classList.contains('is-open')) {
          setOpen(false);
          toggle.focus();
        }
      });
      document.addEventListener('click', function (e) {
        if (root.classList.contains('is-open') && !root.contains(e.target)) setOpen(false);
      });
      var onBreakpoint = function () { if (desktop.matches) setOpen(false); };
      if (desktop.addEventListener) desktop.addEventListener('change', onBreakpoint);
      else if (desktop.addListener) desktop.addListener(onBreakpoint);

      var onScroll = function () { root.classList.toggle('is-scrolled', window.scrollY > 8); };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    });
  })();
</script>
"""

# ===========================================================================
# Shared footer
# ===========================================================================
FOOTER_RES = [("/homebuyer-resources", "Homebuyer Resources"), ("/faqs", "FAQs"),
              ("/privacy-policy", "Privacy Policy"), ("/terms", "Terms of Use")]

FOOTER = """<!-- ============================================================
     COVERED BRIDGE HOME LOANS — SHARED FOOTER
     Paste once into a GHL Custom HTML/JavaScript element inside a
     GLOBAL SECTION at the bottom of the site, and add that global
     section to every page. Styles are scoped to .%R.
     It carries the site-wide loan disclaimer.

     >>> LEGAL DISCLOSURE REQUIRED BEFORE PUBLISHING <<<
     The disclosure area below (.%R__legal) is intentionally empty and
     hidden. Before the site goes live, add the approved legal entity
     name, NMLS number and any other required disclosures (e.g. Equal
     Housing Opportunity statement/logo, state licensing) there.
     Source pages identify "Boxcar Mortgage, LLC DBA Valor Home Loans,
     NMLS #1969375" as the source business. Do NOT relabel that entity
     or its registration as Covered Bridge Home Loans without
     confirmation. The site is not ready to publish until this is done.
     ============================================================ -->
<style>
  .%R {""" + TOKENS + """
    display: block;
    width: 100%;
    margin: 0;
    padding: clamp(56px, 7vw, 84px) var(--hl-gutter) 26px;
    background: var(--hl-black);
    color: var(--hl-warm);
    font-family: var(--hl-sans);
    font-size: 16px;
    line-height: 1.6;
    text-align: left;
  }
  .%R,
  .%R *,
  .%R *::before,
  .%R *::after {
    box-sizing: border-box;
  }
  .%R .%R__in {
    max-width: 1180px;
    margin: 0 auto;
  }
  .%R .%R__grid {
    display: grid;
    grid-template-columns: minmax(0, 5fr) minmax(0, 3fr) minmax(0, 4fr);
    gap: clamp(32px, 5vw, 72px);
  }
  .%R .%R__logo {
    display: block;
    width: auto;
    height: 40px;
    margin: 0 0 18px;
  }
  .%R .%R__name {
    margin: 0 0 8px;
    font-family: var(--hl-serif);
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1.25;
    color: var(--hl-warm);
  }
  .%R .%R__desc {
    max-width: 30em;
    margin: 0 0 18px;
    font-size: 0.9375rem;
    line-height: 1.65;
    color: var(--hl-warm-muted);
  }
  .%R .%R__family {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9375rem;
    font-weight: 600;
    color: var(--hl-gold);
    text-decoration: none;
  }
  .%R .%R__family svg { width: 15px; height: 15px; }
  .%R .%R__family:hover { color: var(--hl-gold-hover); }
  .%R .%R__heading {
    display: inline-block;
    margin: 4px 0 18px;
    padding: 0 0 6px;
    border-bottom: 2px solid var(--hl-gold);
    font-family: var(--hl-sans);
    font-size: 1rem;
    font-weight: 600;
    color: var(--hl-warm);
  }
  .%R .%R__links {
    display: grid;
    gap: 10px;
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__links li { margin: 0; }
  .%R .%R__links li::marker { content: none; }
  .%R .%R__links a {
    font-size: 0.9375rem;
    line-height: 1.5;
    color: var(--hl-warm);
    text-decoration: none;
  }
  .%R .%R__links a:hover { color: var(--hl-gold); }
  .%R .%R__cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 46px;
    margin: 24px 0 0;
    padding: 0 22px;
    border-radius: 999px;
    background: var(--hl-gold);
    color: #0D0D0D;
    font-size: 0.9375rem;
    font-weight: 600;
    text-decoration: none;
  }
  .%R .%R__cta:hover { background: var(--hl-gold-hover); color: #0D0D0D; }
  .%R a:focus-visible {
    outline: 2px solid var(--hl-gold-hover);
    outline-offset: 4px;
    border-radius: 3px;
  }
  .%R .%R__fine {
    margin: clamp(36px, 4vw, 48px) 0 0;
    padding: 22px 0 0;
    border-top: 1px solid rgba(210, 163, 76, 0.2);
    font-size: 0.8125rem;
    line-height: 1.65;
    color: #B8B3A5;
  }
  .%R .%R__fine p { margin: 0 0 8px; }
  .%R .%R__fine p:last-child { margin-bottom: 0; }
  /* Legal disclosure: hidden until approved wording is added. */
  .%R .%R__legal:empty { display: none; }
  .%R .%R__legal p { margin: 0 0 8px; }
  .%R .%R__bottom {
    margin: 22px 0 0;
    padding: 18px 0 0;
    border-top: 1px solid rgba(210, 163, 76, 0.2);
    font-size: 0.8125rem;
    color: #B8B3A5;
  }
  .%R .%R__bottom p { margin: 0; }
  @media (max-width: 900px) {
    .%R .%R__grid { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
    .%R .%R__brand { grid-column: 1 / -1; }
  }
  @media (max-width: 520px) {
    .%R .%R__grid { grid-template-columns: minmax(0, 1fr); }
  }
</style>

<footer class="%R">
  <div class="%R__in">
    <div class="%R__grid">
      <div class="%R__brand">
        <img class="%R__logo" src="%IMG:logo%" alt="Covered Bridge Brands" width="480" height="100" loading="lazy" decoding="async">
        <p class="%R__name">Covered Bridge Home Loans</p>
        <p class="%R__desc">Guidance for your home purchase or refinance.</p>
        <a class="%R__family" href="https://coveredbridgebrands.com/">Part of Covered Bridge Brands""" + ARROW + """</a>
      </div>
      <nav aria-label="Footer">
        <p class="%R__heading">Navigation</p>
        <ul class="%R__links">
%NAV%
        </ul>
      </nav>
      <div>
        <p class="%R__heading">Helpful Resources</p>
        <ul class="%R__links">
%RES%
        </ul>
        <a class="%R__cta" href="/contact">""" + CTA_LABEL + """</a>
      </div>
    </div>
    <div class="%R__fine">
      <p>""" + DISCLAIMER + """</p>
      <div class="%R__legal"><!--
        LEGAL DISCLOSURE (required before publishing): add the approved
        entity name, NMLS ID and other required disclosures here as
        <p>…</p> lines, replacing this comment. See the note at the top.
      --></div>
    </div>
    <div class="%R__bottom">
      <p>&copy; <span data-year>2026</span> Covered Bridge Home Loans. All rights reserved.</p>
    </div>
  </div>
</footer>

<script>
  (function () {
    var y = document.querySelectorAll('.%R [data-year]');
    Array.prototype.forEach.call(y, function (el) { el.textContent = String(new Date().getFullYear()); });
  })();
</script>
"""


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def render(text, root):
    for key in IMAGES:
        token = f"%IMG:{key}%"
        if token in text:
            text = text.replace(token, img_src(key))
    return text.replace("%R", root)


def build_header():
    nav = "\n".join(f'          <li class="%R__item"><a class="%R__link" href="{h}">{t}</a></li>' for h, t in NAV)
    text = HEADER.replace("%NAV%", nav).replace("%BP1", str(HEADER_BP + 1)).replace("%BP", str(HEADER_BP))
    return render(text, "cbhl-header")


def build_footer():
    nav = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t in NAV)
    res = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t in FOOTER_RES)
    return render(FOOTER.replace("%NAV%", nav).replace("%RES%", res), "cbhl-footer")


def build_page(p):
    css = "".join(CSS[k] for k in p["css"])
    name = p["title"].split(" | ")[0].replace("&amp;", "&").upper()
    head = f"""<!-- ============================================================
     COVERED BRIDGE HOME LOANS — {name} PAGE BODY
     Route: {p['route']}
     SEO title: {p['title'].replace('&amp;', '&')}
     Meta description: {p['meta']}

     Paste into one GHL Custom HTML/JavaScript element on this page,
     between the shared header and footer global sections. Section:
     full width, 0 padding, no background. Styles are scoped to .%R.
     ============================================================ -->"""
    script = ""
    if p.get("apply"):
        script = "\n\n" + APPLY_SCRIPT.replace("%APPLICATION_URL%", APPLICATION_URL)
    html = f"""{head}
<style>{css}</style>

<div class="%R">

{p['body']}

</div>{script}
"""
    return render(html, p["root"])


def preview(header, body, footer, title):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<!-- Preview only: GHL loads the fonts itself. Don't paste this file into GHL. -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap">
<style>body {{ margin: 0; background: #FAF8F4; }}</style>
</head>
<body>
{header}
{body}
{footer}
</body>
</html>
"""


def main():
    header, footer = build_header(), build_footer()
    for d in ("sections", "pages", "preview"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    (OUT / "sections/home-loans-header.html").write_text(header, encoding="utf-8")
    (OUT / "sections/home-loans-footer.html").write_text(footer, encoding="utf-8")
    for p in PAGES:
        body = build_page(p)
        assert "%R" not in body and "%IMG" not in body and "%APPLICATION" not in body, p["file"]
        import re
        low = re.sub(r"data:image/[a-z]+;base64,[A-Za-z0-9+/=]+", "", body).lower()
        for banned in ("trulli", "mapscore", "covered bridge capital", "coming soon", "scout", "floify",
                       "valor", "testimonial", "apply now"):
            assert banned not in low, (p["file"], banned)
        (OUT / "pages" / p["file"]).write_text(body, encoding="utf-8")
        route_dir = OUT / "preview" / p["route"].strip("/")
        route_dir.mkdir(parents=True, exist_ok=True)
        (route_dir / "index.html").write_text(
            preview(header, body, footer, p["title"].replace("&amp;", "&")), encoding="utf-8")
        print(f"{p['file']:40s} {p['route']:22s} {len(body) // 1024:4d} KB")
    print(f"{'header / footer':40s} {'':22s} {len(header) // 1024:4d} / {len(footer) // 1024} KB")


if __name__ == "__main__":
    main()
