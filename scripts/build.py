#!/usr/bin/env python3
"""Build the Covered Bridge Home Loans website blocks.

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
IMAGE_FILES = {
    "logo": "cbb-logo.webp",
    "heroHouse": "hero-house-sunset.webp",
    "houseKeys": "house-and-keys.webp",
    "consultation": "consultation.webp",
}


def img(key):
    url = (CONFIG.get("images") or {}).get(key, "").strip()
    if url:
        assert url.startswith("https://") and '"' not in url, url
        return url
    data = (ROOT / "assets/web" / IMAGE_FILES[key]).read_bytes()
    return "data:image/webp;base64," + base64.b64encode(data).decode()


ALT = {
    "heroHouse": "A two-story home with warm light glowing in its windows at sunset.",
    "houseKeys": "A small wooden model house beside a set of house keys, a notebook and a pen on a wooden table.",
    "consultation": "Two people talking with an advisor across a table as she reviews paperwork with them.",
}

DISCLAIMER = ("Loan options, eligibility, down payments and terms depend on the applicable program and "
              "individual circumstances. All loans are subject to credit and underwriting approval. "
              "Website information is not a commitment to lend.")

CTA_LABEL = "Talk About Your Home Loan"

# ---------------------------------------------------------------------------
# Shared tokens. %R is replaced by each block's root class.
# ---------------------------------------------------------------------------
TOKENS = """
    --hl-bg: #0D0D0D;
    --hl-surface: #121619;
    --hl-surface-2: #171B1E;
    --hl-gold: #D2A34C;
    --hl-gold-hover: #EAC266;
    --hl-text: #F2F0EB;
    --hl-muted: #BFBAAB;
    --hl-line: rgba(210, 163, 76, 0.2);
    --hl-line-strong: rgba(210, 163, 76, 0.5);
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
    background: var(--hl-bg);
    color: var(--hl-text);
    font-family: var(--hl-sans);
    font-size: 16px;
    line-height: 1.6;
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
  .%R [hidden] {
    display: none !important;
  }

  /* ---------- Layout ---------- */
  .%R .%R__section {
    position: relative;
    margin: 0;
    padding: clamp(64px, 8vw, 112px) var(--hl-gutter);
    scroll-margin-top: 100px; /* clears the fixed header */
  }
  .%R .%R__section--surface {
    background: var(--hl-surface);
  }
  .%R .%R__section + .%R__section:not(.%R__section--surface) {
    border-top: 1px solid rgba(210, 163, 76, 0.12);
  }
  .%R .%R__inner {
    width: 100%;
    max-width: 1180px;
    margin: 0 auto;
  }
  .%R .%R__narrow {
    max-width: 760px;
  }
  .%R .%R__header {
    max-width: 720px;
    margin: 0 0 clamp(36px, 5vw, 56px);
  }

  /* ---------- Type ---------- */
  .%R .%R__eyebrow {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0 0 18px;
    padding: 0;
    font-family: var(--hl-sans);
    font-size: 0.8125rem;
    font-weight: 500;
    line-height: 1.5;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--hl-gold);
  }
  .%R .%R__eyebrow svg {
    flex: 0 0 auto;
    width: 20px;
    height: 12px;
  }
  .%R .%R__h1 {
    margin: 0 0 22px;
    padding: 0;
    font-family: var(--hl-serif);
    font-size: clamp(2.5rem, 3.4vw + 1rem, 4.25rem);
    font-weight: 600;
    line-height: 1.08;
    letter-spacing: -0.01em;
    text-transform: none;
    color: var(--hl-text);
  }
  .%R .%R__h2 {
    margin: 0 0 16px;
    padding: 0;
    font-family: var(--hl-serif);
    font-size: clamp(1.875rem, 1.7vw + 1.2rem, 2.75rem);
    font-weight: 600;
    line-height: 1.15;
    letter-spacing: -0.005em;
    text-transform: none;
    color: var(--hl-text);
  }
  .%R .%R__h3 {
    margin: 0 0 8px;
    padding: 0;
    font-family: var(--hl-sans);
    font-size: 1.125rem;
    font-weight: 600;
    line-height: 1.4;
    letter-spacing: 0;
    text-transform: none;
    color: var(--hl-text);
  }
  .%R .%R__lede {
    max-width: 38em;
    margin: 0;
    padding: 0;
    font-size: clamp(1.0625rem, 0.35vw + 0.98rem, 1.1875rem);
    line-height: 1.7;
    color: rgba(242, 240, 235, 0.9);
  }
  .%R .%R__p {
    margin: 0 0 16px;
    padding: 0;
    font-size: 1.0625rem;
    line-height: 1.75;
    color: var(--hl-muted);
  }
  .%R .%R__p:last-child {
    margin-bottom: 0;
  }
  .%R .%R__p--sm {
    font-size: 1rem;
    line-height: 1.7;
  }
  .%R .%R__p a,
  .%R .%R__lede a {
    color: var(--hl-gold-hover);
    text-decoration: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 3px;
  }
  .%R .%R__p a:hover,
  .%R .%R__lede a:hover {
    color: var(--hl-text);
  }

  /* ---------- Buttons and links ---------- */
  .%R .%R__actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 14px 16px;
    margin: clamp(30px, 3.6vw, 38px) 0 0;
  }
  .%R .%R__btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    min-height: 54px;
    margin: 0;
    padding: 0 28px;
    border: 1px solid transparent;
    border-radius: 3px;
    font-family: var(--hl-sans);
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.2;
    letter-spacing: 0.01em;
    text-align: center;
    text-decoration: none;
    text-transform: none;
    cursor: pointer;
    transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
  }
  .%R .%R__btn--gold {
    background: var(--hl-gold);
    color: #0D0D0D;
  }
  .%R .%R__btn--gold:hover {
    background: var(--hl-gold-hover);
    color: #0D0D0D;
    transform: translateY(-1px);
    box-shadow: 0 10px 28px rgba(210, 163, 76, 0.25);
  }
  .%R .%R__btn--outline {
    background: rgba(13, 13, 13, 0.35);
    border-color: rgba(210, 163, 76, 0.65);
    color: var(--hl-text);
  }
  .%R .%R__btn--outline:hover {
    border-color: var(--hl-gold-hover);
    color: var(--hl-gold-hover);
  }
  .%R .%R__link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 0 0 3px;
    border-bottom: 1px solid rgba(210, 163, 76, 0.45);
    font-family: var(--hl-sans);
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.4;
    color: var(--hl-gold);
    text-decoration: none;
    transition: color 0.2s ease, border-color 0.2s ease;
  }
  .%R .%R__link svg {
    width: 16px;
    height: 16px;
    flex: 0 0 16px;
    transition: transform 0.2s ease;
  }
  .%R .%R__link:hover {
    color: var(--hl-gold-hover);
    border-color: var(--hl-gold-hover);
  }
  .%R .%R__link:hover svg {
    transform: translateX(3px);
  }
  .%R a:focus-visible,
  .%R summary:focus-visible {
    outline: 2px solid var(--hl-gold-hover);
    outline-offset: 4px;
    border-radius: 2px;
  }

  /* ---------- Closing call to action ---------- */
  .%R .%R__cta {
    text-align: center;
    background:
      radial-gradient(50% 80% at 50% 0%, rgba(210, 163, 76, 0.12), rgba(210, 163, 76, 0) 70%),
      var(--hl-surface);
    border-top: 1px solid var(--hl-line);
  }
  .%R .%R__cta .%R__inner {
    max-width: 760px;
  }
  .%R .%R__cta .%R__eyebrow,
  .%R .%R__cta .%R__actions {
    justify-content: center;
  }
  .%R .%R__cta .%R__lede {
    margin: 0 auto;
  }

  /* ---------- Loan disclaimer ---------- */
  .%R .%R__disclaimer {
    margin: 0;
    padding: 28px var(--hl-gutter) 32px;
    background: var(--hl-bg);
    border-top: 1px solid rgba(210, 163, 76, 0.14);
  }
  .%R .%R__disclaimer p {
    max-width: 1180px;
    margin: 0 auto;
    font-size: 0.875rem;
    line-height: 1.65;
    color: var(--hl-muted);
  }

  @media (max-width: 1180px) {
    .%R .%R__section {
      scroll-margin-top: 84px;
    }
  }
  @media (max-width: 480px) {
    .%R .%R__actions {
      flex-direction: column;
      align-items: stretch;
    }
    .%R .%R__btn {
      width: 100%;
      padding: 0 20px;
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .%R .%R__btn,
    .%R .%R__link,
    .%R .%R__link svg {
      transition: none;
    }
    .%R .%R__btn--gold:hover,
    .%R .%R__link:hover svg {
      transform: none;
    }
  }
"""

CSS["hero"] = """
  /* ---------- Home hero: photo with the copy over its darker left side ---------- */
  .%R .%R__hero {
    position: relative;
    display: flex;
    align-items: center;
    min-height: clamp(580px, 84vh, 780px);
    margin: 0;
    padding: clamp(96px, 10vw, 140px) var(--hl-gutter);
    background: var(--hl-bg);
    overflow: hidden;
  }
  .%R .%R__hero-img {
    position: absolute;
    inset: 0;
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: 68% 50%;
  }
  .%R .%R__hero-shade {
    position: absolute;
    inset: 0;
    background:
      linear-gradient(90deg, rgba(13, 13, 13, 0.92) 0%, rgba(13, 13, 13, 0.8) 30%, rgba(13, 13, 13, 0.35) 55%, rgba(13, 13, 13, 0) 72%),
      linear-gradient(180deg, rgba(13, 13, 13, 0) 70%, rgba(13, 13, 13, 0.85) 100%);
  }
  .%R .%R__hero .%R__inner {
    position: relative;
    z-index: 1;
  }
  .%R .%R__hero-copy {
    max-width: 580px;
  }
  .%R .%R__hero .%R__h1 {
    font-size: clamp(2.75rem, 4vw + 1rem, 4.75rem);
    text-shadow: 0 2px 24px rgba(0, 0, 0, 0.35);
  }
  /* Tablet and phone: the photo becomes a band above the copy so the
     house and the text both stay readable. */
  @media (max-width: 900px) {
    .%R .%R__hero {
      display: block;
      min-height: 0;
      padding: 0 0 clamp(56px, 9vw, 80px);
    }
    .%R .%R__hero-img {
      position: relative;
      inset: auto;
      height: clamp(260px, 62vw, 480px);
      object-position: 74% 45%;
    }
    .%R .%R__hero-shade {
      inset: 0 0 auto 0;
      height: clamp(260px, 62vw, 480px);
      background: linear-gradient(180deg, rgba(13, 13, 13, 0) 50%, rgba(13, 13, 13, 0.6) 80%, #0D0D0D 100%);
    }
    .%R .%R__hero .%R__inner {
      margin-top: clamp(-56px, -6vw, -28px);
      padding: 0 var(--hl-gutter);
    }
    .%R .%R__hero .%R__h1 {
      text-shadow: none;
    }
  }
"""

CSS["phero"] = """
  /* ---------- Page hero ---------- */
  .%R .%R__phero {
    position: relative;
    margin: 0;
    padding: clamp(72px, 9vw, 128px) var(--hl-gutter) clamp(64px, 8vw, 104px);
    background:
      radial-gradient(55% 75% at 88% 0%, rgba(210, 163, 76, 0.12), rgba(210, 163, 76, 0) 65%),
      linear-gradient(180deg, #0D0D0D 0%, #101316 100%);
    border-bottom: 1px solid var(--hl-line);
  }
  .%R .%R__phero-grid {
    display: grid;
    grid-template-columns: minmax(0, 6fr) minmax(0, 5fr);
    gap: clamp(40px, 6vw, 96px);
    align-items: center;
  }
  .%R .%R__phero-copy {
    max-width: 640px;
  }
  @media (max-width: 900px) {
    .%R .%R__phero-grid {
      grid-template-columns: minmax(0, 1fr);
    }
  }
"""

CSS["figure"] = """
  /* ---------- Framed photo ---------- */
  .%R .%R__figure {
    position: relative;
    margin: 0 14px 14px 0;
    padding: 0;
  }
  .%R .%R__figure::before {
    content: "";
    position: absolute;
    inset: 14px -14px -14px 14px;
    border: 1px solid rgba(210, 163, 76, 0.45);
    border-radius: 4px;
    pointer-events: none;
  }
  .%R .%R__figure img {
    position: relative;
    z-index: 1;
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 4 / 3;
    object-fit: cover;
    border-radius: 4px;
    background: var(--hl-surface);
  }
  @media (max-width: 900px) {
    .%R .%R__figure img {
      aspect-ratio: 16 / 10;
    }
  }
"""

CSS["cols"] = """
  /* ---------- Three columns ---------- */
  .%R .%R__cols {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: clamp(28px, 4vw, 56px);
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__col {
    display: flex;
    flex-direction: column;
    margin: 0;
    padding: 28px 0 0;
    border-top: 1px solid var(--hl-line-strong);
  }
  .%R .%R__col::marker {
    content: none;
  }
  .%R .%R__col .%R__p {
    flex: 1 1 auto;
  }
  .%R .%R__col .%R__link {
    align-self: flex-start;
    margin-top: 18px;
  }
  @media (max-width: 900px) {
    .%R .%R__cols {
      grid-template-columns: minmax(0, 1fr);
    }
  }
"""

CSS["grid2"] = """
  /* ---------- Two-column list ---------- */
  .%R .%R__grid2 {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0 clamp(32px, 5vw, 72px);
    margin: 0;
    padding: 0;
    list-style: none;
    border-bottom: 1px solid var(--hl-line);
  }
  .%R .%R__grid2 > li,
  .%R .%R__grid2 > div {
    margin: 0;
    padding: 26px 0;
    border-top: 1px solid var(--hl-line);
  }
  .%R .%R__grid2 > li::marker {
    content: none;
  }
  .%R .%R__below {
    margin: clamp(28px, 3.4vw, 36px) 0 0;
  }
  @media (max-width: 760px) {
    .%R .%R__grid2 {
      grid-template-columns: minmax(0, 1fr);
    }
  }
"""

CSS["split"] = """
  /* ---------- Copy beside a list or photo ---------- */
  .%R .%R__split {
    display: grid;
    grid-template-columns: minmax(0, 5fr) minmax(0, 6fr);
    gap: clamp(36px, 6vw, 96px);
    align-items: start;
  }
  .%R .%R__split--center {
    align-items: center;
  }
  .%R .%R__split .%R__link {
    margin-top: 22px;
  }
  @media (max-width: 900px) {
    .%R .%R__split {
      grid-template-columns: minmax(0, 1fr);
    }
  }
"""

CSS["points"] = """
  /* ---------- Points with a small house mark ---------- */
  .%R .%R__points {
    margin: 0;
    padding: 0;
    list-style: none;
    border-bottom: 1px solid var(--hl-line);
  }
  .%R .%R__points > li {
    display: grid;
    grid-template-columns: 22px minmax(0, 1fr);
    gap: 16px;
    align-items: start;
    margin: 0;
    padding: 20px 0;
    border-top: 1px solid var(--hl-line);
    font-size: 1.0625rem;
    line-height: 1.6;
    color: var(--hl-text);
  }
  .%R .%R__points > li::marker {
    content: none;
  }
  .%R .%R__points svg {
    width: 22px;
    height: 22px;
    margin-top: 2px;
    color: var(--hl-gold);
  }
"""

CSS["steps"] = """
  /* ---------- Numbered stages ---------- */
  .%R .%R__steps {
    max-width: 880px;
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__step {
    position: relative;
    display: grid;
    grid-template-columns: clamp(52px, 6vw, 72px) minmax(0, 1fr);
    gap: clamp(16px, 3vw, 32px);
    margin: 0;
    padding: 0 0 clamp(32px, 4vw, 44px);
  }
  .%R .%R__step::marker {
    content: none;
  }
  .%R .%R__step::before {
    content: "";
    position: absolute;
    top: 58px;
    bottom: 10px;
    left: calc(clamp(52px, 6vw, 72px) / 2);
    width: 1px;
    background: var(--hl-line-strong);
  }
  .%R .%R__step:last-child {
    padding-bottom: 0;
  }
  .%R .%R__step:last-child::before {
    content: none;
  }
  .%R .%R__step-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(52px, 6vw, 72px);
    height: clamp(52px, 6vw, 72px);
    border: 1px solid var(--hl-line-strong);
    border-radius: 50%;
    font-family: var(--hl-serif);
    font-size: clamp(1.375rem, 1vw + 1rem, 1.75rem);
    font-weight: 600;
    line-height: 1;
    color: var(--hl-gold);
  }
  .%R .%R__step-body {
    padding-top: clamp(10px, 1.4vw, 18px);
  }
  .%R .%R__step .%R__h3 {
    font-family: var(--hl-serif);
    font-size: clamp(1.375rem, 0.8vw + 1.1rem, 1.625rem);
  }
  .%R .%R__step .%R__link {
    margin-top: 14px;
  }
"""

CSS["rows"] = """
  /* ---------- Program rows ---------- */
  .%R .%R__rows {
    margin: 0;
    padding: 0;
    list-style: none;
    border-bottom: 1px solid var(--hl-line);
  }
  .%R .%R__row {
    display: grid;
    grid-template-columns: minmax(0, 4fr) minmax(0, 7fr);
    gap: clamp(14px, 5vw, 72px);
    margin: 0;
    padding: clamp(28px, 3.4vw, 40px) 0;
    border-top: 1px solid var(--hl-line);
    scroll-margin-top: 100px;
  }
  .%R .%R__row::marker {
    content: none;
  }
  .%R .%R__row .%R__h2 {
    margin: 0;
    font-size: clamp(1.5rem, 1vw + 1.15rem, 2rem);
  }
  @media (max-width: 760px) {
    .%R .%R__row {
      grid-template-columns: minmax(0, 1fr);
    }
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
    border-bottom: 1px solid var(--hl-line);
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
    color: var(--hl-gold);
  }
  .%R .%R__gloss dd {
    margin: 0;
    font-size: 1rem;
    line-height: 1.7;
    color: var(--hl-muted);
  }
  @media (max-width: 760px) {
    .%R .%R__gloss {
      grid-template-columns: minmax(0, 1fr);
    }
  }
"""

CSS["callout"] = """
  /* ---------- Callouts and notes ---------- */
  .%R .%R__note {
    max-width: 72ch;
    margin: clamp(24px, 3vw, 32px) 0 0;
    font-size: 0.9375rem;
    line-height: 1.65;
    color: var(--hl-muted);
  }
  .%R .%R__callout {
    display: grid;
    grid-template-columns: 26px minmax(0, 1fr);
    gap: 16px;
    max-width: 880px;
    margin: 0;
    padding: 24px 28px;
    border: 1px solid var(--hl-line);
    border-left: 3px solid var(--hl-gold);
    border-radius: 3px;
    background: rgba(210, 163, 76, 0.06);
  }
  .%R .%R__callout--spaced {
    margin-top: clamp(32px, 4vw, 44px);
  }
  .%R .%R__callout svg {
    width: 26px;
    height: 26px;
    color: var(--hl-gold);
  }
  .%R .%R__callout .%R__h3 {
    margin-bottom: 6px;
  }
"""

CSS["faq"] = """
  /* ---------- Questions (native disclosure: keyboard and touch ready) ---------- */
  .%R .%R__faq {
    max-width: 880px;
    margin: 0;
    border-bottom: 1px solid var(--hl-line);
  }
  .%R .%R__faq details {
    margin: 0;
    border-top: 1px solid var(--hl-line);
  }
  .%R .%R__faq summary {
    position: relative;
    display: block;
    padding: 24px 48px 24px 0;
    font-family: var(--hl-serif);
    font-size: clamp(1.125rem, 0.5vw + 1rem, 1.375rem);
    font-weight: 600;
    line-height: 1.4;
    color: var(--hl-text);
    list-style: none;
    cursor: pointer;
    transition: color 0.2s ease;
  }
  .%R .%R__faq summary::-webkit-details-marker {
    display: none;
  }
  .%R .%R__faq summary::before,
  .%R .%R__faq summary::after {
    content: "";
    position: absolute;
    top: 50%;
    right: 6px;
    width: 16px;
    height: 1.5px;
    background: var(--hl-gold);
    transition: transform 0.2s ease;
  }
  .%R .%R__faq summary::after {
    transform: rotate(90deg);
  }
  .%R .%R__faq details[open] summary::after {
    transform: rotate(0deg);
  }
  .%R .%R__faq summary:hover {
    color: var(--hl-gold-hover);
  }
  .%R .%R__faq-body {
    max-width: 70ch;
    padding: 0 0 26px;
  }
  @media (prefers-reduced-motion: reduce) {
    .%R .%R__faq summary,
    .%R .%R__faq summary::after {
      transition: none;
    }
  }
"""

CSS["contact"] = """
  /* ---------- Inquiry area ---------- */
  .%R .%R__contact {
    display: flex;
    flex-wrap: wrap;
    gap: clamp(36px, 6vw, 88px);
    align-items: flex-start;
  }
  .%R .%R__contact-copy {
    flex: 1 1 340px;
    max-width: 560px;
  }
  /* The GHL form goes inside .%R__form. While it's empty the panel
     collapses, so visitors never see an empty box. */
  .%R .%R__form {
    flex: 1.4 1 420px;
    min-width: 0;
    padding: clamp(20px, 3vw, 32px);
    border: 1px solid var(--hl-line);
    border-radius: 4px;
    background: var(--hl-surface-2);
  }
  .%R .%R__form:empty {
    display: none;
  }
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
    grid-template-columns: 20px minmax(0, 1fr);
    gap: 12px;
    margin: 0;
    padding: 14px 0;
    border-top: 1px solid var(--hl-line);
    font-size: 0.9375rem;
    line-height: 1.6;
    color: var(--hl-muted);
  }
  .%R .%R__notices > li::marker {
    content: none;
  }
  .%R .%R__notices svg {
    width: 20px;
    height: 20px;
    margin-top: 1px;
    color: var(--hl-gold);
  }
  .%R .%R__notices a {
    color: var(--hl-gold-hover);
    text-decoration: underline;
    text-underline-offset: 3px;
  }
  .%R .%R__apply {
    margin: 30px 0 0;
    padding: 24px 0 0;
    border-top: 1px solid var(--hl-line);
  }
  .%R .%R__apply .%R__actions {
    margin-top: 16px;
  }
"""

CSS["legal"] = """
  /* ---------- Legal draft ---------- */
  .%R .%R__legal {
    max-width: 820px;
  }
  .%R .%R__status {
    margin: 24px 0 0;
    padding: 16px 20px;
    border: 1px solid var(--hl-line-strong);
    border-left: 3px solid var(--hl-gold);
    border-radius: 3px;
    background: rgba(210, 163, 76, 0.08);
    font-size: 0.9375rem;
    font-weight: 600;
    line-height: 1.6;
    color: var(--hl-text);
  }
  .%R .%R__legal-sec {
    margin: 0;
    padding: clamp(28px, 3.4vw, 36px) 0;
    border-top: 1px solid var(--hl-line);
  }
  .%R .%R__legal-sec .%R__h2 {
    font-size: clamp(1.375rem, 0.8vw + 1.1rem, 1.75rem);
    margin-bottom: 12px;
  }
  .%R .%R__legal-num {
    margin-right: 8px;
    color: var(--hl-gold);
  }
  .%R .%R__review {
    margin: 12px 0 0;
    padding: 14px 18px;
    border: 1px dashed rgba(210, 163, 76, 0.55);
    border-radius: 3px;
    font-size: 0.9375rem;
    line-height: 1.6;
    color: rgba(242, 240, 235, 0.88);
  }
  .%R .%R__review strong {
    color: var(--hl-gold);
  }
  .%R .%R__review ul {
    margin: 8px 0 0;
    padding: 0 0 0 20px;
  }
  .%R .%R__review li {
    margin: 4px 0;
  }
"""

# ---------------------------------------------------------------------------
# Small shared pieces
# ---------------------------------------------------------------------------
ROOF = ('<svg viewBox="0 0 20 12" fill="none" stroke="currentColor" stroke-width="1.5" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
        '<path d="M1.5 11 10 2.5l8.5 8.5"/></svg>')
HOUSE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
         '<path d="M3.5 11 12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/></svg>')
SHIELD = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
          '<path d="M12 3 4.5 6v5.5c0 4.6 3.1 8.2 7.5 9.5 4.4-1.3 7.5-4.9 7.5-9.5V6L12 3z"/><path d="m9 12 2 2 4-4"/></svg>')
INFO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
        '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 8h.01"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
         '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>')


def eyebrow(text):
    return f'<p class="%R__eyebrow">{ROOF}<span>{text}</span></p>'


def link(href, text):
    return f'<a class="%R__link" href="{href}">{text}{ARROW}</a>'


def btn(href, text, kind="gold"):
    return f'<a class="%R__btn %R__btn--{kind}" href="{href}">{text}</a>'


def points(items):
    lis = "\n".join(f"          <li>{HOUSE}<span>{t}</span></li>" for t in items)
    return f'        <ul class="%R__points">\n{lis}\n        </ul>'


def cta(title_id, headline, text=None, label=CTA_LABEL, href="/contact"):
    lede = f'\n      <p class="%R__lede">{text}</p>' if text else ""
    return f"""  <section class="%R__section %R__cta" aria-labelledby="%R-{title_id}">
    <div class="%R__inner">
      <h2 class="%R__h2" id="%R-{title_id}">{headline}</h2>{lede}
      <div class="%R__actions">
        {btn(href, label)}
      </div>
    </div>
  </section>"""


def disclaimer():
    return f"""  <aside class="%R__disclaimer" aria-label="Loan disclaimer">
    <p>{DISCLAIMER}</p>
  </aside>"""


def figure(key, eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="%R__figure"><img src="%IMG:{key}%" alt="{ALT[key]}" width="1200" height="800" '
            f'{loading} decoding="async"></figure>')


def phero(title_id, eyebrow_text, h1, lede, image=None):
    media = f"\n      {figure(image, eager=True)}" if image else ""
    return f"""  <section class="%R__phero" aria-labelledby="%R-{title_id}">
    <div class="%R__inner %R__phero-grid">
      <div class="%R__phero-copy">
        {eyebrow(eyebrow_text)}
        <h1 class="%R__h1" id="%R-{title_id}">{h1}</h1>
        <p class="%R__lede">{lede}</p>
      </div>{media}
    </div>
  </section>"""


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
    var root = document.querySelectorAll('.%R [data-hl-apply]');
    Array.prototype.forEach.call(root, function (el) {
      var a = el.matches('a') ? el : el.querySelector('a[data-hl-apply-link]');
      if (a) a.setAttribute('href', url);
      el.hidden = false;
    });
  })();
</script>"""

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
PAGES = []


def page(**kw):
    PAGES.append(kw)


# ---------- 1. Home ----------
page(
    file="home-loans-home.html", route="/", root="cbhl-home",
    title="Covered Bridge Home Loans | Home Purchase &amp; Refinancing Guidance",
    meta="Explore home purchase and refinancing options with Covered Bridge Home Loans, including Conventional, FHA, VA and USDA loans, with guidance through the mortgage process.",
    css=["base", "hero", "cols", "grid2", "split", "points"],
    body=f"""  <section class="%R__hero" aria-labelledby="%R-title">
    <img class="%R__hero-img" src="%IMG:heroHouse%" alt="{ALT['heroHouse']}" width="1600" height="900" fetchpriority="high" decoding="async">
    <div class="%R__hero-shade" aria-hidden="true"></div>
    <div class="%R__inner">
      <div class="%R__hero-copy">
        {eyebrow("Home Purchase &amp; Refinancing")}
        <h1 class="%R__h1" id="%R-title">Your next chapter starts at home.</h1>
        <p class="%R__lede">Whether you&rsquo;re buying your first home, planning your next move or exploring refinancing, Covered Bridge Home Loans helps you understand your options and take the next step with confidence.</p>
        <div class="%R__actions">
          {btn("/contact", CTA_LABEL)}
          {btn("/loan-options", "Explore Loan Options", "outline")}
        </div>
      </div>
    </div>
  </section>

  <section class="%R__section" aria-labelledby="%R-paths">
    <div class="%R__inner">
      <header class="%R__header">
        {eyebrow("Where You Are")}
        <h2 class="%R__h2" id="%R-paths">What brings you here?</h2>
      </header>
      <ul class="%R__cols">
        <li class="%R__col">
          <h3 class="%R__h3">Buying Your First Home</h3>
          <p class="%R__p %R__p--sm">Get a clearer picture of your financing options and what to prepare before moving forward.</p>
          {link("/contact", "Talk about buying your first home")}
        </li>
        <li class="%R__col">
          <h3 class="%R__h3">Making Your Next Move</h3>
          <p class="%R__p %R__p--sm">Explore home financing as your needs, plans or circumstances change.</p>
          {link("/contact", "Talk about your next move")}
        </li>
        <li class="%R__col">
          <h3 class="%R__h3">Considering Refinancing</h3>
          <p class="%R__p %R__p--sm">Discuss whether refinancing may fit your goals and what factors to consider.</p>
          {link("/contact", "Talk about refinancing")}
        </li>
      </ul>
    </div>
  </section>

  <section class="%R__section %R__section--surface" aria-labelledby="%R-programs">
    <div class="%R__inner">
      <header class="%R__header">
        {eyebrow("Loan Options")}
        <h2 class="%R__h2" id="%R-programs">Explore your loan options</h2>
        <p class="%R__p">Different borrowers and properties may call for different programs.</p>
      </header>
      <ul class="%R__grid2">
        <li>
          <h3 class="%R__h3">Conventional</h3>
          <p class="%R__p %R__p--sm">Financing options for eligible homebuyers and property types.</p>
        </li>
        <li>
          <h3 class="%R__h3">FHA</h3>
          <p class="%R__p %R__p--sm">Government-insured financing that may suit a range of borrowers, including some first-time buyers.</p>
        </li>
        <li>
          <h3 class="%R__h3">VA</h3>
          <p class="%R__p %R__p--sm">Options for eligible veterans, service members and qualifying surviving spouses.</p>
        </li>
        <li>
          <h3 class="%R__h3">USDA</h3>
          <p class="%R__p %R__p--sm">Options for eligible borrowers and properties in qualifying areas.</p>
        </li>
      </ul>
      <p class="%R__below">{link("/loan-options", "Compare Loan Options")}</p>
    </div>
  </section>

  <section class="%R__section" aria-labelledby="%R-guidance">
    <div class="%R__inner %R__split">
      <div>
        {eyebrow("The Process")}
        <h2 class="%R__h2" id="%R-guidance">Guidance through the process</h2>
        <p class="%R__p">A home loan involves more than choosing a program. Understanding the paperwork, questions and next steps can help you move through the process with greater clarity.</p>
        {link("/how-it-works", "See How It Works")}
      </div>
{points([
    "Discuss your goals and circumstances.",
    "Understand the information and documents needed.",
    "Stay informed as your loan progresses.",
])}
    </div>
  </section>

{cta("closing", "Let&rsquo;s talk about your next move.", "Start with a conversation about your homebuying or refinancing plans.")}

{disclaimer()}""",
)

# ---------- 2. Loan Options ----------
PROGRAMS = [
    ("conventional", "Conventional Loans",
     "Conventional financing may be available for eligible primary residences, second homes and investment properties. Down-payment options, mortgage insurance and other requirements depend on the specific program and borrower."),
    ("fha", "FHA Loans",
     "FHA loans are government-insured mortgages that may be suitable for a range of borrowers, including some first-time homebuyers. Credit, down-payment and property requirements apply."),
    ("va", "VA Loans",
     "VA loan options are available to eligible veterans, service members and qualifying surviving spouses. Eligibility, entitlement and the specific transaction determine the available options."),
    ("usda", "USDA Loans",
     "USDA financing may be available to eligible borrowers purchasing qualifying properties in eligible areas. Household income, property location and program requirements apply."),
    ("refinancing", "Refinancing",
     "Refinancing replaces an existing mortgage with a new loan. Whether it makes sense depends on your goals, available terms, costs and how long you expect to keep the loan."),
    ("down-payment-assistance", "Down Payment Assistance",
     "Some eligible buyers may have access to assistance programs. Availability, funding, income limits, location and other conditions vary. Ask which programs may apply to your situation."),
]
rows = "\n".join(f"""        <li class="%R__row" id="{slug}">
          <h2 class="%R__h2">{name}</h2>
          <p class="%R__p">{text}</p>
        </li>""" for slug, name, text in PROGRAMS)

page(
    file="home-loans-loan-options.html", route="/loan-options", root="cbhl-loans",
    title="Loan Options | Covered Bridge Home Loans",
    meta="Learn about Conventional, FHA, VA and USDA loans, refinancing and down payment assistance, then discuss which options may fit with the Covered Bridge Home Loans team.",
    css=["base", "phero", "figure", "rows"],
    body=f"""{phero("title", "Loan Options", "Understand your home-loan options.",
       "The right starting point depends on your goals, finances, property and eligibility. Explore the main program categories, then discuss the details with the team.",
       image="houseKeys")}

  <section class="%R__section" aria-label="Loan programs">
    <div class="%R__inner">
      <ul class="%R__rows">
{rows}
      </ul>
    </div>
  </section>

{cta("start", "Not sure where to start?", "You do not need to choose a program before speaking with the team. Start by explaining your plans and asking which options may fit.", label="Discuss Your Options")}

{disclaimer()}""",
)

# ---------- 3. How It Works ----------
STEPS = [
    ("Discuss your plans",
     "Talk about your purchase or refinance goals, timing and financial circumstances.", ""),
    ("Complete the appropriate application",
     "When you are ready, use the designated application process and provide the requested information. An inquiry alone is not a completed mortgage application or approval.",
     '\n              <p hidden data-hl-apply><a class="%R__link" data-hl-apply-link>Start your application' + ARROW + '</a></p>'),
    ("Prepare your documents",
     "Gather the income, asset, identification and property information requested for your situation.", ""),
    ("Move through review",
     "Depending on your transaction, the process may include disclosures, processing, property valuation, underwriting and requests for additional information.", ""),
    ("Prepare for closing",
     "If the loan is approved and closing conditions are satisfied, review the final documents and complete the required closing steps.", ""),
]
steps = "\n".join(f"""        <li class="%R__step">
          <span class="%R__step-num" aria-hidden="true">{i}</span>
          <div class="%R__step-body">
            <h3 class="%R__h3"><span class="%R__sr">Step {i}: </span>{t}</h3>
            <p class="%R__p">{p}</p>{extra}
          </div>
        </li>""" for i, (t, p, extra) in enumerate(STEPS, 1))

SR_CSS = """
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
"""
CSS["base"] += SR_CSS

page(
    file="home-loans-how-it-works.html", route="/how-it-works", root="cbhl-how",
    title="How the Home Loan Process Works | Covered Bridge Home Loans",
    meta="Understand the main stages of a home loan, from your first conversation and application to documents, review and closing, so you can prepare for each step.",
    css=["base", "phero", "figure", "steps", "split", "points"],
    apply=True,
    body=f"""{phero("title", "How It Works", "Know what comes next.",
       "Every home-loan situation is different, but understanding the main stages can help you prepare.",
       image="consultation")}

  <section class="%R__section" aria-labelledby="%R-stages">
    <div class="%R__inner">
      <header class="%R__header">
        {eyebrow("The Main Stages")}
        <h2 class="%R__h2" id="%R-stages">From first conversation to closing</h2>
      </header>
      <ol class="%R__steps">
{steps}
      </ol>
    </div>
  </section>

  <section class="%R__section %R__section--surface" aria-labelledby="%R-moving">
    <div class="%R__inner %R__split">
      <div>
        {eyebrow("Along the Way")}
        <h2 class="%R__h2" id="%R-moving">Keep the process moving</h2>
      </div>
{points([
    "Respond to document requests promptly.",
    "Ask about anything you do not understand.",
    "Discuss significant financial changes with your loan professional while the loan is in progress.",
])}
    </div>
  </section>

{cta("closing", "Start with your questions.")}

{disclaimer()}""",
)

# ---------- 4. Homebuyer Resources ----------
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

page(
    file="home-loans-resources.html", route="/homebuyer-resources", root="cbhl-res",
    title="Homebuyer Resources | Covered Bridge Home Loans",
    meta="Commonly requested mortgage documents, plain-language mortgage terms and questions worth asking before your home-loan conversation.",
    css=["base", "phero", "figure", "cols", "gloss", "split", "points", "callout"],
    body=f"""{phero("title", "Homebuyer Resources", "A little preparation goes a long way.",
       "Use these starting points to organize your questions and prepare for a conversation about your mortgage.")}

  <section class="%R__section" aria-labelledby="%R-docs">
    <div class="%R__inner">
      <header class="%R__header">
        {eyebrow("Documents")}
        <h2 class="%R__h2" id="%R-docs">Documents commonly requested</h2>
        <p class="%R__p">The exact documents depend on your circumstances and the loan program. Your loan professional will explain what is needed.</p>
      </header>
      <ul class="%R__cols">
        <li class="%R__col">
          <h3 class="%R__h3">Employed / W-2 Borrowers</h3>
          <p class="%R__p %R__p--sm">Common requests may include identification, recent pay statements, W-2 forms and account statements for funds used in the transaction.</p>
        </li>
        <li class="%R__col">
          <h3 class="%R__h3">Self-Employed Borrowers</h3>
          <p class="%R__p %R__p--sm">Common requests may include identification, tax returns, business or income documentation and relevant account statements.</p>
        </li>
        <li class="%R__col">
          <h3 class="%R__h3">Retired / Fixed-Income Borrowers</h3>
          <p class="%R__p %R__p--sm">Common requests may include identification, pension or Social Security award information and relevant account statements.</p>
        </li>
      </ul>
      <p class="%R__note">These are general examples, not a complete application checklist. Additional documents may be requested.</p>
      <div class="%R__callout %R__callout--spaced" role="note">
        {SHIELD}
        <div>
          <h3 class="%R__h3">Security note</h3>
          <p class="%R__p %R__p--sm">Do not send identification, tax returns, bank statements or other sensitive documents through a general website inquiry. Use the designated document-submission process when instructed.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="%R__section %R__section--surface" aria-labelledby="%R-terms">
    <div class="%R__inner">
      <header class="%R__header">
        {eyebrow("Terms")}
        <h2 class="%R__h2" id="%R-terms">Mortgage terms in plain language</h2>
      </header>
      <dl class="%R__gloss">
{gloss}
      </dl>
    </div>
  </section>

  <section class="%R__section" aria-labelledby="%R-questions">
    <div class="%R__inner %R__split %R__split--center">
      <div>
        {eyebrow("Your Conversation")}
        <h2 class="%R__h2" id="%R-questions">Questions worth asking</h2>
{points([
    "Which programs might fit my circumstances?",
    "What upfront funds should I prepare?",
    "What costs and mortgage-insurance requirements apply?",
    "Which documents are needed?",
    "What could affect the timeline?",
    "What should I understand before accepting the loan terms?",
])}
      </div>
      {figure("houseKeys")}
    </div>
  </section>

{cta("closing", "Have a question about your situation?", label="Ask the Team")}

{disclaimer()}""",
)

# ---------- 5. FAQs ----------
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
faqs = "\n".join(f"""        <details>
          <summary>{q}</summary>
          <div class="%R__faq-body">
            <p class="%R__p">{a}</p>
          </div>
        </details>""" for q, a in FAQS)

page(
    file="home-loans-faqs.html", route="/faqs", root="cbhl-faq",
    title="Home Loan FAQs | Covered Bridge Home Loans",
    meta="Answers to common questions about loan options, down payments, credit, documents, timing, appraisals, mortgage payments and refinancing.",
    css=["base", "phero", "faq"],
    body=f"""{phero("title", "FAQs", "Your home-loan questions, answered.",
       "Clear starting points for your homebuying or refinancing conversation.")}

  <section class="%R__section" aria-label="Frequently asked questions">
    <div class="%R__inner">
      <div class="%R__faq">
{faqs}
      </div>
    </div>
  </section>

{cta("closing", "Still have questions?")}

{disclaimer()}""",
)

# ---------- 6. About ----------
page(
    file="home-loans-about.html", route="/about", root="cbhl-about",
    title="About | Covered Bridge Home Loans",
    meta="Covered Bridge Home Loans helps individuals and families explore mortgage options for buying or refinancing a home. Part of Covered Bridge Brands.",
    css=["base", "phero", "figure", "cols"],
    body=f"""{phero("title", "About", "Guidance for one of life&rsquo;s important decisions.",
       "Covered Bridge Home Loans helps individuals and families explore mortgage options for buying or refinancing a home.",
       image="consultation")}

  <section class="%R__section" aria-labelledby="%R-approach">
    <div class="%R__inner %R__narrow">
      {eyebrow("Our Approach")}
      <h2 class="%R__h2" id="%R-approach">Your home. Your plans. A clearer next step.</h2>
      <p class="%R__p">A home loan is a personal decision. Your circumstances, questions and priorities matter.</p>
      <p class="%R__p">Our focus is on helping you understand potential options, prepare the requested information and navigate the next steps in the mortgage process.</p>
      <p class="%R__p">Whether you are starting your first home search or considering a refinance, begin with a conversation about what you want to accomplish.</p>
    </div>
  </section>

  <section class="%R__section %R__section--surface" aria-labelledby="%R-values">
    <div class="%R__inner">
      <header class="%R__header">
        {eyebrow("What We Value")}
        <h2 class="%R__h2" id="%R-values">What matters along the way</h2>
      </header>
      <ul class="%R__cols">
        <li class="%R__col">
          <h3 class="%R__h3">Clear Communication</h3>
          <p class="%R__p %R__p--sm">Understand the questions, information and next steps relevant to your situation.</p>
        </li>
        <li class="%R__col">
          <h3 class="%R__h3">Individual Circumstances</h3>
          <p class="%R__p %R__p--sm">Discuss financing in the context of your goals, finances and property.</p>
        </li>
        <li class="%R__col">
          <h3 class="%R__h3">Informed Decisions</h3>
          <p class="%R__p %R__p--sm">Take time to understand the terms, costs and responsibilities before moving forward.</p>
        </li>
      </ul>
    </div>
  </section>

  <section class="%R__section" aria-labelledby="%R-family">
    <div class="%R__inner %R__narrow">
      {eyebrow("Our Family of Brands")}
      <h2 class="%R__h2" id="%R-family">Part of Covered Bridge Brands</h2>
      <p class="%R__p">Covered Bridge Home Loans is part of the Covered Bridge Brands family.</p>
      <p class="%R__p">{link("https://coveredbridgebrands.com/", "Visit Covered Bridge Brands")}</p>
    </div>
  </section>

{cta("closing", "Tell us about your next chapter.")}""",
)

# ---------- 7. Contact ----------
page(
    file="home-loans-contact.html", route="/contact", root="cbhl-contact",
    title="Contact | Covered Bridge Home Loans",
    meta="Buying, refinancing or simply exploring? Share your questions and start a conversation with Covered Bridge Home Loans.",
    css=["base", "phero", "contact"],
    apply=True,
    body=f"""{phero("title", "Contact", "Let&rsquo;s talk about your home-loan plans.",
       "Buying, refinancing or simply exploring? Share a few initial details and your questions.")}

  <section class="%R__section" aria-labelledby="%R-inquiry">
    <div class="%R__inner %R__contact">
      <div class="%R__contact-copy">
        {eyebrow("Inquiry")}
        <h2 class="%R__h2" id="%R-inquiry">Start a Conversation</h2>
        <p class="%R__p">Tell us what you are planning so the team can help you understand the appropriate next step.</p>
        <ul class="%R__notices">
          <li>{SHIELD}<span>Please do not include sensitive financial or identification information. This form is for general inquiries and is not a mortgage application.</span></li>
          <li>{INFO}<span>See our <a href="/privacy-policy">Privacy Policy</a> for information about how inquiry details are handled.</span></li>
        </ul>
        <div class="%R__apply" hidden data-hl-apply>
          <h3 class="%R__h3">Ready to apply?</h3>
          <p class="%R__p %R__p--sm">If you&rsquo;re ready to begin a mortgage application, use the online application.</p>
          <div class="%R__actions">
            <a class="%R__btn %R__btn--outline" data-hl-apply-link>Start Your Application</a>
          </div>
        </div>
      </div>
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
    </div>
  </section>

{disclaimer()}""",
)

# ---------- 8. Privacy Policy (draft) ----------
def legal_sections(items):
    out = []
    for i, (title, text, review) in enumerate(items, 1):
        body = f'\n        <p class="%R__p">{text}</p>' if text else ""
        if review:
            if isinstance(review, list):
                lis = "".join(f"<li>{r}</li>" for r in review)
                rv = f'\n        <div class="%R__review"><strong>Review:</strong><ul>{lis}</ul></div>'
            else:
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

LEGAL_COMMENT = """<!-- LEGAL DRAFT: not ready to publish. The review notes below are
     intentionally visible while this page is a draft. Replace each
     one with approved wording (or remove it) after legal review, and
     remove the draft status line when the page is approved. -->"""

page(
    file="home-loans-privacy-policy-draft.html", route="/privacy-policy", root="cbhl-privacy",
    title="Privacy Policy | Covered Bridge Home Loans",
    meta="Privacy Policy for the Covered Bridge Home Loans website and its general inquiry process.",
    css=["base", "phero", "legal"],
    body=f"""  {LEGAL_COMMENT}
  <section class="%R__phero" aria-labelledby="%R-title">
    <div class="%R__inner %R__legal">
      {eyebrow("Legal")}
      <h1 class="%R__h1" id="%R-title">Privacy Policy</h1>
      <p class="%R__lede">This draft identifies the privacy information to be confirmed for the Covered Bridge Home Loans website and its general inquiry process.</p>
      <p class="%R__status" role="note">Draft &mdash; business identity and data practices require confirmation before publication.</p>
    </div>
  </section>

  <div class="%R__section">
    <div class="%R__inner %R__legal">
{legal_sections(PRIVACY)}
    </div>
  </div>""",
)

# ---------- 9. Terms of Use (draft) ----------
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

page(
    file="home-loans-terms-draft.html", route="/terms", root="cbhl-terms",
    title="Terms of Use | Covered Bridge Home Loans",
    meta="Terms of Use for the Covered Bridge Home Loans website.",
    css=["base", "phero", "legal"],
    body=f"""  {LEGAL_COMMENT}
  <section class="%R__phero" aria-labelledby="%R-title">
    <div class="%R__inner %R__legal">
      {eyebrow("Legal")}
      <h1 class="%R__h1" id="%R-title">Terms of Use</h1>
      <p class="%R__status" role="note">Draft &mdash; legal identity and applicable terms require confirmation before publication.</p>
    </div>
  </section>

  <div class="%R__section">
    <div class="%R__inner %R__legal">
{legal_sections(TERMS)}
    </div>
  </div>""",
)

# ---------------------------------------------------------------------------
# Shared header and footer
# ---------------------------------------------------------------------------
NAV = [("/loan-options", "Loan Options"), ("/how-it-works", "How It Works"),
       ("/homebuyer-resources", "Homebuyer Resources"), ("/about", "About")]
HEADER_BP = 1140

HEADER = """<!-- ============================================================
     COVERED BRIDGE HOME LOANS — SHARED HEADER
     Paste once into a GHL Custom HTML/JavaScript element inside a
     GLOBAL SECTION at the top of the site, and add that global
     section to every page (don't paste a copy per page).
     Styles are scoped to .%R; the script only touches .%R.

     Pinned to the top with position: fixed (sticky doesn't survive
     GHL's element wrappers); the outer box reserves the bar's height.
     Logo: the Covered Bridge Brands logo, embedded unless
     config/site.json supplies a GHL Media link.
     ============================================================ -->
<style>
  .%R {""" + TOKENS + """
    --%R-h: 84px;
    position: relative;
    display: block;
    width: 100%;
    height: calc(var(--%R-h) + 1px);
    margin: 0;
    padding: 0;
    background: var(--hl-bg);
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
    padding: 0 clamp(16px, 3.4vw, 48px);
    background: rgba(13, 13, 13, 0.97);
    border-bottom: 1px solid rgba(210, 163, 76, 0.4);
    transition: box-shadow 0.25s ease;
  }
  .%R.is-scrolled .%R__bar {
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.55);
  }
  .%R .%R__inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    max-width: 1280px;
    height: var(--%R-h);
    margin: 0 auto;
  }

  /* ---- Identity: CBB logo + Covered Bridge Home Loans ---- */
  .%R .%R__brand {
    display: flex;
    align-items: center;
    gap: 14px;
    flex: 0 1 auto;
    min-width: 0;
    text-decoration: none;
  }
  .%R .%R__logo {
    display: block;
    width: auto;
    height: 38px;
    border: 0;
  }
  .%R .%R__divider {
    flex: 0 0 1px;
    width: 1px;
    height: 36px;
    background: rgba(210, 163, 76, 0.45);
  }
  .%R .%R__name {
    display: flex;
    flex-direction: column;
    line-height: 1.15;
    white-space: nowrap;
  }
  .%R .%R__name-top {
    font-family: var(--hl-sans);
    font-size: 0.6875rem;
    font-weight: 600;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--hl-gold);
  }
  .%R .%R__name-main {
    font-family: var(--hl-serif);
    font-size: 1.3125rem;
    font-weight: 600;
    color: var(--hl-text);
  }
  .%R .%R__brand:focus-visible {
    outline: 2px solid var(--hl-gold-hover);
    outline-offset: 4px;
  }

  /* ---- Navigation ---- */
  .%R .%R__nav {
    display: flex;
    align-items: center;
    gap: clamp(20px, 2.2vw, 32px);
  }
  .%R .%R__list {
    display: flex;
    align-items: center;
    gap: clamp(18px, 2vw, 30px);
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__item {
    margin: 0;
    padding: 0;
  }
  .%R .%R__item::marker {
    content: none;
  }
  .%R .%R__link {
    position: relative;
    display: inline-block;
    padding: 8px 0;
    font-family: var(--hl-sans);
    font-size: 0.9375rem;
    font-weight: 400;
    line-height: 1.2;
    white-space: nowrap;
    color: var(--hl-text);
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
  .%R .%R__link[aria-current="page"] {
    color: var(--hl-gold);
  }
  .%R .%R__link:hover::after,
  .%R .%R__link[aria-current="page"]::after {
    transform: scaleX(1);
  }
  .%R .%R__cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 46px;
    padding: 0 22px;
    border-radius: 3px;
    background: var(--hl-gold);
    color: #0D0D0D;
    font-family: var(--hl-sans);
    font-size: 0.9375rem;
    font-weight: 600;
    line-height: 1.2;
    white-space: nowrap;
    text-decoration: none;
    transition: background-color 0.2s ease;
  }
  .%R .%R__cta:hover {
    background: var(--hl-gold-hover);
    color: #0D0D0D;
  }
  .%R .%R__link:focus-visible,
  .%R .%R__cta:focus-visible {
    outline: 2px solid var(--hl-gold-hover);
    outline-offset: 4px;
  }

  /* ---- Menu button (smaller screens) ---- */
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
    border-radius: 3px;
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
  .%R.is-open .%R__toggle-line:nth-child(1) {
    transform: translateY(7.5px) rotate(45deg);
  }
  .%R.is-open .%R__toggle-line:nth-child(2) {
    opacity: 0;
  }
  .%R.is-open .%R__toggle-line:nth-child(3) {
    transform: translateY(-7.5px) rotate(-45deg);
  }
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
    .%R {
      --%R-h: 72px;
    }
    .%R .%R__toggle {
      display: flex;
    }
    .%R .%R__nav {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      display: block;
      max-height: 0;
      overflow: hidden;
      visibility: hidden;
      background: var(--hl-bg);
      border-bottom: 1px solid rgba(210, 163, 76, 0);
      transition: max-height 0.35s ease, visibility 0s linear 0.35s, border-color 0.35s ease;
    }
    .%R.is-open .%R__nav {
      max-height: calc(100vh - var(--%R-h));
      overflow-y: auto;
      visibility: visible;
      border-bottom-color: rgba(210, 163, 76, 0.45);
      box-shadow: 0 18px 36px rgba(0, 0, 0, 0.6);
      transition: max-height 0.35s ease, visibility 0s linear 0s, border-color 0.35s ease;
    }
    .%R .%R__list {
      flex-direction: column;
      align-items: stretch;
      gap: 0;
      padding: 8px clamp(16px, 4vw, 48px) 0;
    }
    .%R .%R__link {
      display: block;
      padding: 16px 0;
      border-bottom: 1px solid rgba(210, 163, 76, 0.15);
      font-size: 1.0625rem;
    }
    .%R .%R__link::after {
      right: auto;
      bottom: 10px;
      width: 28px;
    }
    .%R .%R__cta {
      display: flex;
      min-height: 52px;
      margin: 20px clamp(16px, 4vw, 48px) 24px;
      font-size: 1rem;
    }
  }
  @media (max-width: 560px) {
    .%R .%R__logo,
    .%R .%R__divider {
      display: none;
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .%R .%R__bar,
    .%R .%R__link,
    .%R .%R__link::after,
    .%R .%R__toggle-line,
    .%R .%R__nav,
    .%R .%R__cta {
      transition: none;
    }
  }
</style>

<div class="%R">
  <header class="%R__bar">
    <div class="%R__inner">
      <a class="%R__brand" href="/" aria-label="Covered Bridge Home Loans home">
        <img class="%R__logo" src="%IMG:logo%" alt="" width="480" height="100" decoding="async">
        <span class="%R__divider" aria-hidden="true"></span>
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

FOOTER_LINKS = [("/", "Home"), ("/loan-options", "Loan Options"), ("/how-it-works", "How It Works"),
                ("/homebuyer-resources", "Homebuyer Resources"), ("/faqs", "FAQs"), ("/about", "About"),
                ("/contact", "Contact")]

FOOTER = """<!-- ============================================================
     COVERED BRIDGE HOME LOANS — SHARED FOOTER
     Paste once into a GHL Custom HTML/JavaScript element inside a
     GLOBAL SECTION at the bottom of the site, and add that global
     section to every page. Styles are scoped to .%R.

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
    padding: clamp(56px, 7vw, 88px) var(--hl-gutter) 28px;
    background: #0A0A0A;
    border-top: 1px solid rgba(210, 163, 76, 0.3);
    color: var(--hl-text);
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
  .%R .%R__inner {
    max-width: 1180px;
    margin: 0 auto;
  }
  .%R .%R__grid {
    display: grid;
    grid-template-columns: minmax(0, 5fr) minmax(0, 4fr) minmax(0, 3fr);
    gap: clamp(32px, 5vw, 72px);
  }
  .%R .%R__name {
    margin: 0 0 8px;
    padding: 0;
    font-family: var(--hl-serif);
    font-size: 1.625rem;
    font-weight: 600;
    line-height: 1.25;
    color: var(--hl-text);
  }
  .%R .%R__tagline {
    margin: 0 0 22px;
    padding: 0;
    font-size: 1rem;
    line-height: 1.6;
    color: var(--hl-muted);
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
  .%R .%R__family svg {
    width: 15px;
    height: 15px;
  }
  .%R .%R__family:hover {
    color: var(--hl-gold-hover);
  }
  .%R .%R__heading {
    margin: 4px 0 14px;
    padding: 0;
    font-family: var(--hl-sans);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--hl-gold);
  }
  .%R .%R__links {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, max-content));
    gap: 10px 32px;
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .%R .%R__links--single {
    grid-template-columns: minmax(0, max-content);
  }
  .%R .%R__links li {
    margin: 0;
  }
  .%R .%R__links li::marker {
    content: none;
  }
  .%R .%R__links a {
    font-size: 0.9375rem;
    line-height: 1.5;
    color: var(--hl-text);
    text-decoration: none;
  }
  .%R .%R__links a:hover {
    color: var(--hl-gold);
  }
  .%R a:focus-visible {
    outline: 2px solid var(--hl-gold-hover);
    outline-offset: 4px;
    border-radius: 2px;
  }
  /* Legal disclosure: hidden until approved wording is added. */
  .%R .%R__legal {
    margin: clamp(36px, 4vw, 48px) 0 0;
    padding: 22px 0 0;
    border-top: 1px solid rgba(210, 163, 76, 0.18);
    font-size: 0.8125rem;
    line-height: 1.65;
    color: var(--hl-muted);
  }
  .%R .%R__legal:empty {
    display: none;
  }
  .%R .%R__legal p {
    margin: 0 0 8px;
  }
  .%R .%R__bottom {
    margin: clamp(36px, 4vw, 48px) 0 0;
    padding: 22px 0 0;
    border-top: 1px solid rgba(210, 163, 76, 0.18);
    font-size: 0.8125rem;
    line-height: 1.6;
    color: var(--hl-muted);
  }
  .%R .%R__legal:not(:empty) + .%R__bottom {
    margin-top: 16px;
    padding-top: 0;
    border-top: 0;
  }
  .%R .%R__bottom p {
    margin: 0;
  }
  @media (max-width: 900px) {
    .%R .%R__grid {
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    }
    .%R .%R__brand {
      grid-column: 1 / -1;
    }
  }
  @media (max-width: 520px) {
    .%R .%R__grid {
      grid-template-columns: minmax(0, 1fr);
    }
  }
</style>

<footer class="%R">
  <div class="%R__inner">
    <div class="%R__grid">
      <div class="%R__brand">
        <p class="%R__name">Covered Bridge Home Loans</p>
        <p class="%R__tagline">Guidance for your home purchase or refinance.</p>
        <a class="%R__family" href="https://coveredbridgebrands.com/">Part of Covered Bridge Brands""" + ARROW + """</a>
      </div>
      <nav aria-label="Footer">
        <p class="%R__heading">Explore</p>
        <ul class="%R__links">
%LINKS%
        </ul>
      </nav>
      <nav aria-label="Legal">
        <p class="%R__heading">Legal</p>
        <ul class="%R__links %R__links--single">
          <li><a href="/privacy-policy">Privacy Policy</a></li>
          <li><a href="/terms">Terms of Use</a></li>
        </ul>
      </nav>
    </div>
    <div class="%R__legal"><!--
      LEGAL DISCLOSURE (required before publishing): add the approved
      entity name, NMLS ID and other required disclosures here as
      <p>…</p> lines, replacing this comment. See the note at the top.
    --></div>
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


def render(text, root):
    for key in IMAGE_FILES:
        token = f"%IMG:{key}%"
        if token in text:
            text = text.replace(token, img(key))
    return text.replace("%R", root)


def build_header():
    nav = "\n".join(f'          <li class="%R__item"><a class="%R__link" href="{h}">{t}</a></li>' for h, t in NAV)
    text = HEADER.replace("%NAV%", nav).replace("%BP1", str(HEADER_BP + 1)).replace("%BP", str(HEADER_BP))
    return render(text, "cbhl-header")


def build_footer():
    links = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t in FOOTER_LINKS)
    return render(FOOTER.replace("%LINKS%", links), "cbhl-footer")


def build_page(p):
    css = "".join(CSS[k] for k in p["css"])
    head = f"""<!-- ============================================================
     COVERED BRIDGE HOME LOANS — {p['title'].split(' | ')[0].upper().replace('&AMP;', '&')} PAGE BODY
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400;600&display=swap">
<style>body {{ margin: 0; background: #0D0D0D; }}</style>
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
        low = body.lower()
        for banned in ("trulli", "mapscore", "covered bridge capital", "coming soon", "scout", "floify"):
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
