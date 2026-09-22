# SEO — Technical Foundation Checklist

This lane aims to make **core content retrievable and understandable by target crawlers**.
Google renders JavaScript, but search and AI crawlers do not all support the same features.
Initial HTML improves compatibility and reliability. CSR alone does not prove a page is unindexable.

## 1. Content exposure

- [ ] Request representative URLs (home, listing, detail) without login; save status, final URL, and body.
      Record login, consent, or bot challenges as restrictions on access to the actual content.
- [ ] Inspect robots.txt, robots meta, and `X-Robots-Tag` together. robots.txt blocking does not
      guarantee exclusion from the index; a crawler may not read `noindex` on a blocked URL.
- [ ] Compare body, links, metadata, and JSON-LD in `curl -sL <url>` HTML and the rendered DOM.
      Investigate resource blocks, JS errors, and interaction-dependent loading; consider SSR/SSG where useful.
- [ ] With Search Console access, check URL Inspection's indexed status and live rendered result.
      Browser visibility is not proof of Google indexing; record indexing as unverified without access.
- [ ] ⚠️ **CSR bailout trap**: even in SSR frameworks, certain hooks/APIs can silently drop
      a whole page to client rendering. Compare initial HTML and rendered output before and after deployment.

Sources: [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics),
[robots.txt limitations](https://developers.google.com/search/docs/crawling-indexing/robots/intro).

## 2. Sitemap

- [ ] sitemap.xml exists + referenced from robots.txt
- [ ] Include canonical detail URLs intended for search (products, articles, items), not only listing pages.
- [ ] Split files to stay within 50K URLs and 50MB uncompressed per sitemap (sitemap index + parts).
- [ ] Update canonical URLs for new content types and `lastmod` reflecting actual changes.
      A sitemap helps discovery; it is a hint and does not guarantee indexing.

Source: [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).

## 3. Meta

- [ ] Titles should describe the page accurately and concisely, without unnecessary keyword repetition.
- [ ] Descriptions summarize that page's value. Fixed character counts are not indexing pass criteria.
- [ ] Distinguish titles and descriptions by page; Google may rewrite the displayed text.
- [ ] OG image: the face of every share. Dynamic generation per page type is ideal

Sources: [Title links](https://developers.google.com/search/docs/appearance/title-link),
[Search snippets](https://developers.google.com/search/docs/appearance/snippet).

## 4. Structured data (JSON-LD)

- [ ] Schema matching the page type: Article, Product, FAQPage, BreadcrumbList, Organization
- [ ] Structured data must accurately represent user-visible content. Do not invent facts or reviews.
- [ ] Link the same entity with consistent `@id` and properties; avoid conflicting organization facts across pages.
- [ ] On request, generate or update JSON-LD using values verified on the page; do not invent unverified values.
- [ ] Before publishing, check JSON syntax and Schema Markup Validator; use Rich Results Test for supported types.
      Recheck the live URL after publishing. Valid syntax and schema do not guarantee rich result appearance.

Source: [Google structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

## 5. URL & response hygiene

- [ ] canonical: parameter variants and duplicate paths point to one canonical URL
- [ ] Multilingual? hreflang must cross-reference (one-sided tags are void)
- [ ] Missing pages return 404, not 200 — soft 404s burn crawl budget
- [ ] ⚠️ **Baked-404 trap**: in ISR/CDN cache layers, a transient failure's 404 can get
      baked for hours. On data-fetch failure, throw (retry) instead of returning 404 —
      "doesn't exist" and "couldn't fetch" are different things
- [ ] Redirect chains: 1 hop max

## 6. Measured Core Web Vitals & performance

- [ ] Obtain mobile and desktop PageSpeed Insights (PSI) results for representative URLs.
      Record report URL, retrieval date, device, and scope (URL or origin).
- [ ] **Field data**: record CrUX's trailing 28-day, 75th-percentile LCP, INP, and CLS separately.
      If PSI falls back to origin data, do not present it as a measurement of that individual page.
- [ ] Good thresholds: **LCP ≤ 2.5s / INP ≤ 200ms / CLS ≤ 0.1**. Separate each metric from the tool's overall verdict.
      Label missing values `no data` and unperformed checks `not measured`; never invent scores.
- [ ] **Lab data**: separately record PSI/Lighthouse conditions, LCP, CLS, TBT, and diagnostics.
      TBT in a Lighthouse navigation run is not INP; a performance score alone does not prove a CWV pass.
- [ ] Prioritize using evidence: LCP element/loading delay, long JS tasks (INP), and unreserved image/ad space (CLS).
      Compare lab runs under matching conditions after fixes; note that 28-day field aggregates include older visits.
- [ ] Use WebP/AVIF and explicit image width/height (CLS). Avoid lazy-loading the actual LCP image;
      adjust preload/priority only where needed, rather than preloading every image and font.
- [ ] Losslessly optimize logos/icons — shipping a multi-hundred-KB logo on every page wastes bandwidth.

Sources: [Web Vitals metrics](https://web.dev/articles/vitals),
[PSI data and assessment](https://developers.google.com/speed/docs/insights/v5/about),
[Field vs. lab data](https://web.dev/articles/lab-and-field-data-differences).

## 7. Mobile & rendering parity

- [ ] Inspect mobile viewport, horizontal overflow, text legibility, touch interactions, and content-obscuring overlays.
- [ ] Compare core content, titles, robots directives, and structured data on mobile and desktop.
      Layouts may differ. Check whether loading primary content requires a click or scroll-triggered network request.
- [ ] Check access to required mobile CSS, JS, and images. For separate mobile URLs, verify
      corresponding URLs, redirects, and canonical/alternate relationships.

Source: [Google mobile-first indexing](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing).

## 8. HTTPS & safe content delivery

- [ ] Check HTTPS certificate validity, hostname match, certificate errors, and HTTP→HTTPS redirects.
      Internal links, canonicals, and sitemaps should also use the intended HTTPS URLs.
- [ ] Inspect browser console/network output for mixed content and blocked resources.
      Record missing content or broken functionality caused by HTTP scripts, styles, or iframes.
- [ ] Record observed security headers and resource blocks caused by policies such as CSP.
      A missing header alone does not prove an indexing failure. This is not a penetration test or security certification.

Source: [web.dev mixed content](https://web.dev/articles/what-is-mixed-content).

## 9. Index acceleration

- [ ] IndexNow: ping new/updated pages at publish time (consumed by Bing, Naver, Yandex)
- [ ] Google doesn't support IndexNow — win with sitemap `lastmod` accuracy instead
- [ ] Publishing at volume? Build the ping into the publishing pipeline — manual pings
      always stop happening

## 10. Audit evidence

Report `URL | check | observed fact/evidence | status (pass/issue/unverified/not measured) | impact | fix | recheck`.
Missing access, tools, or data is not itself a site defect. Do not claim to have used unavailable tools;
distinguish completed public checks from checks that were not performed.
