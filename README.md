# Covered Bridge Home Loans — Website (GoHighLevel)

The standalone website for Covered Bridge Home Loans, built for the Covered Bridge Home Loans GHL sub-account (formerly the Valor sub-account). It is separate from the main Covered Bridge Brands site, its Home Loans teaser page, Covered Bridge Capital and MapScore.

> **Not ready to publish.** See [Before publishing](#before-publishing): the legal disclosure, contact form, final domain and legal-page review are still open.

## Files and routes

| Page | Route | Paste this file | Images |
|---|---|---|---|
| Home | `/` | `pages/home-loans-home.html` | House at sunset (hero) |
| Loan Options | `/loan-options` | `pages/home-loans-loan-options.html` | House and keys |
| How It Works | `/how-it-works` | `pages/home-loans-how-it-works.html` | Consultation |
| Homebuyer Resources | `/homebuyer-resources` | `pages/home-loans-resources.html` | House and keys |
| FAQs | `/faqs` | `pages/home-loans-faqs.html` | none |
| About | `/about` | `pages/home-loans-about.html` | Consultation |
| Contact | `/contact` | `pages/home-loans-contact.html` | none |
| Privacy Policy (draft) | `/privacy-policy` | `pages/home-loans-privacy-policy-draft.html` | none |
| Terms of Use (draft) | `/terms` | `pages/home-loans-terms-draft.html` | none |
| Shared header | every page | `sections/home-loans-header.html` | CBB logo |
| Shared footer | every page | `sections/home-loans-footer.html` | none |

Every file is a GHL-ready fragment: no `<html>`, `<head>` or `<body>`, styles scoped to the block's own root class (`.cbhl-header`, `.cbhl-footer`, `.cbhl-home`, `.cbhl-loans`, `.cbhl-how`, `.cbhl-res`, `.cbhl-faq`, `.cbhl-about`, `.cbhl-contact`, `.cbhl-privacy`, `.cbhl-terms`). Internal links are root-relative (`/contact`), so they work on whatever domain the site gets.

`preview/` holds review copies of each page with the header and footer around it. Don't paste them into GHL. To view them, serve the folder: `cd preview && python3 -m http.server`, then open http://localhost:8000/.

## GHL placement

1. **Header and footer (once).** In the Home Loans sub-account's website builder, create a **Global Section** containing one full-width Custom HTML/JavaScript element with `sections/home-loans-header.html`, and another with `sections/home-loans-footer.html`. Add the header global section to the top and the footer global section to the bottom of every page. Don't paste copies on individual pages; edits to a global section update every page.
2. **Each page.** Create the page at its route, then add one full-width section (0 padding, no background) with one Custom HTML/JavaScript element, and paste the page file. Order on every page: header global section → page element → footer global section.
3. **Page settings.** Set the SEO title and meta description from the table below. Each file's top comment repeats them.
4. **Fonts.** Choose Playfair Display and Inter in the site's typography settings. Without them the blocks fall back to Georgia and the system sans-serif.
5. **Contact form.** When the native form exists, paste its embed code inside the `__form` box on the Contact page (marked `GHL FORM EMBED GOES HERE`). The box is hidden while it's empty.

Images are embedded in the blocks, so they show as soon as they're pasted. To make the blocks smaller, upload `assets/web/*.webp` to the sub-account's Media library, put the links in `config/site.json` under `images`, and run the build.

## SEO

| Page | Title | Meta description |
|---|---|---|
| Home | Covered Bridge Home Loans \| Home Purchase & Refinancing Guidance | Explore home purchase and refinancing options with Covered Bridge Home Loans, including Conventional, FHA, VA and USDA loans, with guidance through the mortgage process. |
| Loan Options | Loan Options \| Covered Bridge Home Loans | Learn about Conventional, FHA, VA and USDA loans, refinancing and down payment assistance, then discuss which options may fit with the Covered Bridge Home Loans team. |
| How It Works | How the Home Loan Process Works \| Covered Bridge Home Loans | Understand the main stages of a home loan, from your first conversation and application to documents, review and closing, so you can prepare for each step. |
| Homebuyer Resources | Homebuyer Resources \| Covered Bridge Home Loans | Commonly requested mortgage documents, plain-language mortgage terms and questions worth asking before your home-loan conversation. |
| FAQs | Home Loan FAQs \| Covered Bridge Home Loans | Answers to common questions about loan options, down payments, credit, documents, timing, appraisals, mortgage payments and refinancing. |
| About | About \| Covered Bridge Home Loans | Covered Bridge Home Loans helps individuals and families explore mortgage options for buying or refinancing a home. Part of Covered Bridge Brands. |
| Contact | Contact \| Covered Bridge Home Loans | Buying, refinancing or simply exploring? Share your questions and start a conversation with Covered Bridge Home Loans. |
| Privacy Policy | Privacy Policy \| Covered Bridge Home Loans | Privacy Policy for the Covered Bridge Home Loans website and its general inquiry process. |
| Terms of Use | Terms of Use \| Covered Bridge Home Loans | Terms of Use for the Covered Bridge Home Loans website. |

## Application link

`HOME_LOAN_APPLICATION_URL` controls the online application buttons (Contact page and How It Works step 2). It is empty because the destination isn't confirmed, so those buttons are hidden and no broken link appears. To turn them on, set `applicationUrl` in `config/site.json` to the full `https://` address and run the build (or edit the value at the bottom of those two page blocks).

## Before publishing

1. **Final domain.** Not supplied. Links are root-relative, so no code change is needed; connect the domain in GHL.
2. **Contact form.** Paste the native Covered Bridge Home Loans GHL form into the Contact page's form box. Intended fields and the information it must not collect are listed in the comment there. Until then the Contact page has no way to send an inquiry.
3. **Application destination.** Decide the online application link (the source site used both Scout and Floify) and set `applicationUrl`.
4. **Business contact details.** No phone, email or address appears anywhere; supply confirmed details if they should be shown.
5. **Legal entity, NMLS and other required disclosures.** Add the approved wording to the footer's legal disclosure area (`__legal`, marked in the footer comment); it's hidden while empty. Source pages identify "Boxcar Mortgage, LLC DBA Valor Home Loans, NMLS #1969375"; don't relabel that entity or registration as Covered Bridge Home Loans without confirmation. Add any Equal Housing statement or logo only with the correct asset and requirements.
6. **Legal pages.** Privacy Policy and Terms of Use are drafts with visible review notes. Complete the review, replace the notes with approved wording, and remove the draft status line.

## Images

| File | Source (kept unchanged in `assets/originals/`) | Used on |
|---|---|---|
| `assets/web/hero-house-sunset.webp` (1600 × 900) | `house-at-sunset.webp` | Home hero: copy over the dark left side on desktop; on tablet and phone the photo becomes a band above the copy, cropped to keep the house |
| `assets/web/house-and-keys.webp` (1200 × 800) | `wooden-house-and-keys.webp` | Loan Options hero, Homebuyer Resources |
| `assets/web/consultation.webp` (1200 × 800) | `consultation.webp` | How It Works hero, About hero |
| `assets/web/cbb-logo.webp` (480 × 100) | `cbb-logo.png` (Covered Bridge Brands logo) | Header |

The photos are illustrative; the copy doesn't identify the people as staff or customers or the house as a financed property.

## Editing

All wording, layout and styles live in `scripts/build.py`; settings in `config/site.json`. After any change run:

```
python3 scripts/build.py
```

It rebuilds `sections/`, `pages/` and `preview/`, and refuses to write a page that mentions Capital, MapScore, Trulli, Scout, Floify or "Coming Soon".
