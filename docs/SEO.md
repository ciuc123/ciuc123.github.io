# SEO audit and plan: ciuculescu.com (2026-11-16)

Audit made from the repository only: the live site could not be fetched from the session that wrote this, so every point marked *(verify live)* needs a look at the deployed page, Google Search Console or PageSpeed Insights. The tasks are in `PLAN.md`; this file holds the findings and the reasoning.

## Current state

- Jekyll on GitHub Pages, `minima` theme (overridden layouts), plugins `jekyll-seo-tag`, `jekyll-sitemap`, `jekyll-feed`. Good base: titles, meta descriptions from excerpts, canonical URLs, Open Graph, JSON-LD and `sitemap.xml` / `robots.txt` come for free *if Jekyll actually builds the site* (see 1).
- 22 posts (2024-06 to 2025-11), mostly PHP 8.4 / Laravel 11 / testing / Docker / security, 500 to 1,800 words. No commits since 2025-12-02.
- Audience is mixed: hiring managers and SMB owners (services, availability) and developers (code-heavy posts).

## Findings, by priority

### Critical

1. **Deploy path is unclear and may serve unbuilt files.** `.github/workflows/static.yml` uploads the repository *as is* (`path: '.'`) to Pages on push to `master`, with no `jekyll build`. If Settings → Pages → Source is "GitHub Actions", the live site is raw Markdown and Liquid: no posts index, no sitemap, no SEO tags. If the source is "Deploy from a branch", GitHub builds Jekyll and this workflow is redundant (or fails). *(verify live: open `/posts/` and `/sitemap.xml`)*. Fix: replace it with the official Jekyll workflow (`actions/jekyll-build-pages`) or delete it and keep branch builds.
2. **Contact form sends nothing.** `assets/js/main.js` fakes a submit with `setTimeout` and an alert: every inquiry is lost while the visitor is told it was sent. Not SEO strictly, but it is the conversion point all SEO traffic leads to. Fix: Formspree / Basin / a MailerLite form (MailerLite is already loaded) or a plain `mailto:` until then.
3. **Non-site files may be published**: `README.md`, `AGENT_PROMPTS.md`, `generate-welcome-pdf.sh` (and now `PLAN.md`, `docs/`) have no front matter, so Jekyll copies them as static files. `AGENT_PROMPTS.md` exposes the content workflow. Fix: `exclude` in `_config.yml` (done with this plan).

### High

4. **Duplicate H1 on posts.** `_layouts/post.html` prints the title as `<h1>`; 5 posts also start with a `# ` heading (2025-09-15, -17, -23, -25, -27). Remove the in-body H1s.
5. **No per-post `description`.** `jekyll-seo-tag` falls back to the first paragraph, which is often a generic hook. Write 140 to 160 character descriptions with the main keyword, for every post.
6. **Titles too long.** The site title "Andrei Ciuculescu - Laravel & DevOps Specialist" is appended to every post title; with post titles of 60 to 103 characters, Google truncates almost all. Shorten post titles to ≤ 60, and set a short site `title` ("Andrei Ciuculescu") with the tagline in `description`.
7. **No social image.** No `image:` anywhere, so shares on LinkedIn (the main distribution channel) show no card picture. Add a default `image` in `_config.yml` (1200×630) and per-post images for the strongest posts.
8. **Weak or private pages indexed.** "Hello World" (18 words) is thin content; "How to remove git secrets" names a client repo (`lauragheorghica.ro`) and its front-matter date (2025-08-09) disagrees with its file name (2025-09-09). Delete or merge Hello World (keep its `welcome-email` tag elsewhere); anonymise and fix the date of the other.
9. **Nested `<main>` on posts** (`default.html` wraps `post.html`'s own `<main>`). Invalid HTML, confuses landmarks. Use `<article>` only.

### Medium

10. **No author / Person structured data.** Add `author` with `url`, `sameAs` (GitHub, LinkedIn) via `jekyll-seo-tag`'s `social:` block, and a `Person` + `ProfessionalService` JSON-LD on the home page (area served, Bucharest, services). Helps the name query "Andrei Ciuculescu" and E-E-A-T.
11. **No internal linking.** Posts don't link to each other or to services; the posts index is one long list with no tags. Add: related posts at the end of each post (by tag), tags on every post (only `welcome-email` exists today), a "Hire me" call to action in the post layout linking to `/contact/`.
12. **Topic clusters.** Group existing posts into 3 to 4 hubs, each with a pillar page linking to its posts: *Laravel performance* (queues, N+1, slim architecture, PHP 8.4 performance), *Laravel testing* (3 testing posts, PhpStorm/Xdebug), *PHP & Laravel security* (audit, APP_KEY RCE, Stripe, Docker security, git secrets), *Upgrades & migration* (Laravel 11 guide, PHP 8.4 ROI, property hooks). The two LinkedIn/Zapier posts and the WordPress themes post are off-topic for a Laravel consultant; keep them but don't build on them.
13. **Services page.** "Laravel Development", "DevOps", "Consulting" live only as cards on the home page. A `/services/` page (or one page each) targeting commercial queries ("Laravel developer for hire", "Laravel consultant Romania/EU", "Laravel upgrade service") is the page most likely to bring clients.
14. **Freshness.** Posts about "PHP 8.4" and "Laravel 11" are dated 2025; newer Laravel and PHP releases (Laravel 12, PHP 8.5) have shipped since. Update the best ones (add `last_modified_at`, with `jekyll-last-modified-at` or by hand) rather than writing new ones on the same topic.
15. **Performance** *(verify live with PageSpeed Insights)*: full Font Awesome 6.0.0 CSS (≈ 90 KB plus webfonts) for about 10 icons; Google Fonts Inter, 5 weights; PostHog and MailerLite scripts on every page; `favicon.ico` is 287 KB. Swap Font Awesome for inline SVGs, cut Inter to 2 to 3 weights or self-host, shrink the favicon.
16. **Consent.** PostHog and MailerLite load without a consent banner; for EU visitors that is a GDPR issue (and AdSense, prepared by `ads.txt`, would need a CMP). Add a light consent banner or switch PostHog to cookieless mode.

### Low

17. `lang`/`locale` fine; add `hreflang` only if Romanian pages are added.
18. Google Search Console and Bing Webmaster Tools: verify the domain, submit `sitemap.xml`, check Coverage and Core Web Vitals. *(owner)*
19. `jekyll-feed` exists; link the RSS feed visibly (footer) for developer readers.
20. 404 page missing (`404.html` with links to posts and contact).

## Measurement

Baseline before changes, then monthly: Search Console clicks / impressions / average position per page, indexed pages count, PageSpeed mobile score for `/` and one post, contact-form submissions (once the form works). Targets for 3 months after the fixes: every post indexed, branded query "Andrei Ciuculescu" at position 1 with sitelinks, first impressions on "Laravel consultant" type queries from the services page.
