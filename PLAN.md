# Plan: ciuculescu.com

All ongoing and planned work for this site lives here, and only here. Tasks are tagged `[Owner]` (needs Andrei: accounts, DNS, decisions, writing in his voice) or `[AI]` (an agent can do it from the repo). Tick a task when it is done; keep **Now** at five lines or fewer.

Background: `docs/SEO.md` (audit findings, numbered; tasks below cite them as SEO-n), `docs/DEV_SUBDOMAIN.md` (dev.ciuculescu.com).

## Now

1. [Owner] Check how Pages deploys and what dev.ciuculescu.com resolves to (first two tasks under **Site health**).
2. [Owner] Decide the site's direction: keep Jekyll, or continue the Next.js paid-library rebuild on the `dev` branch (**Next.js rebuild**).
3. [AI] Fix the deploy workflow and the contact form.
4. [AI] SEO quick wins (duplicate H1s, descriptions, titles, social image).
5. [Owner] Search Console set up, baseline numbers written down.

## Work in flight (unmerged branches, checked 2026-11-16)

None of these is merged into `master`. Decide for each: merge, finish, or delete the branch.

- [ ] [Owner] `dev`: Next.js rebuild, 14 commits, last 2026-03-21 (see **Next.js rebuild**).
- [ ] [Owner] `copilot/remove-page-title-issue`: removes the duplicate H1s (SEO-4) and adds `validate_posts.rb` plus a workflow; 2025-11-06. Merging it covers the H1 task below; check its workflow first.
- [ ] [Owner] `copilot/execute-agents-md`: finished post "Laravel Sanctum vs Passport API Authentication"; 2025-12-02. Review and publish.
- [ ] [Owner] `ideas/2026-07-06-from-monolith-to-microservices-solo-devs-guide-to-scaling-laravel`: draft post (114 lines). Review and publish.
- [ ] [Owner] `posts/advance`: draft post "Laravel Forge VPS zero-downtime" (file name says "downtine"); 2025-09-30.
- [ ] [Owner] `copilot/create-prompts-folder` and `copilot/remove-anthropic-api-key`: two overlapping content-generation systems (prompts, LinkedIn posts, GitHub Models); 2025-12-16. Keep at most one; `AGENT_PROMPTS.md` on `master` already covers the prompts.
- [ ] [Owner] Delete branches already merged into `master`: `add-laravel-queue-optimization-post`, `backup`, `copilot/create-blog-posts-with-php-laravel`, `copilot/find-wordpress-scheduling-themes`.

## Next.js rebuild (`dev` branch)

The `dev` branch's `plan/` folder holds the detailed tasks (`plan/tasks-tech/`, `plan/tasks-product/`, `plan/tasks-first-sale/`): turn the site into a paid "curated materials" library with Next.js on Vercel, Clerk, Supabase, Stripe and optional Resend / GA4 / S3. Done there: 010 Next.js skeleton, 015 upgrade to Next.js 16; 020 Clerk mostly done (SDK env docs and the manual sign-in test still open). Next: 030 Supabase schema, 040 Stripe checkout.

- [ ] [Owner] Decide: go on with the rebuild, or keep the Jekyll blog and drop it. If the rebuild goes ahead, prefer the Postgres/Drizzle + Clerk setup already running in Job Radar over adding Supabase.
- [ ] [Owner] If it goes ahead: create the Vercel project for `app-next/` on `dev` and map `dev.ciuculescu.com` with `noindex` (option 4 in `docs/DEV_SUBDOMAIN.md`).
- [ ] [AI] If it goes ahead: before switching `ciuculescu.com` to Next.js, keep every post URL (`/posts/:year-:month-:day-:title/`) or add 301 redirects, and carry over sitemap, RSS, canonical and structured data. Until then, keep Jekyll SEO work to the quick wins.

## Site health (do first)

- [ ] [Owner] Settings → Pages: note the source ("Deploy from a branch" or "GitHub Actions") here; open `/posts/` and `/sitemap.xml` live to confirm Jekyll is built (SEO-1).
- [ ] [Owner] Run the three checks in `docs/DEV_SUBDOMAIN.md` for `dev.ciuculescu.com` and write the result here. If it is a dangling GitHub Pages or Vercel record, delete it the same day.
- [ ] [Owner] Verify `ciuculescu.com` in GitHub (Settings → Pages → Verified domains) to block subdomain takeovers.
- [ ] [Owner] Decide on dev.ciuculescu.com: option 1 (no subdomain, local + PR previews; recommended), 2 (staging with noindex), 3 (developer hub) or 4 (Job Radar dev). See `docs/DEV_SUBDOMAIN.md`.
- [ ] [AI] Replace `.github/workflows/static.yml` (uploads the raw repo, no build) with the Jekyll build workflow, or delete it if branch builds are used (SEO-1).
- [ ] [Owner] Pick a form backend (Formspree, Basin, or a MailerLite form since MailerLite is already loaded) and create the endpoint.
- [ ] [AI] Wire `contactForm` to that endpoint; today `assets/js/main.js` only shows an alert and drops the message (SEO-2).
- [x] [AI] Exclude non-site files (`README.md`, `AGENT_PROMPTS.md`, `PLAN.md`, `docs/`, scripts) from the Jekyll build (SEO-3).

## SEO quick wins

- [ ] [AI] Remove the in-body `# ` H1 from the 5 posts that have one, or merge `copilot/remove-page-title-issue` which does it (SEO-4).
- [ ] [AI] Draft a 140 to 160 character `description:` for each post; [Owner] reviews (SEO-5).
- [ ] [AI] Shorten post titles to ≤ 60 characters (keep URLs unchanged) and the site `title` to "Andrei Ciuculescu" (SEO-6).
- [ ] [Owner] Provide or approve a default 1200×630 social image; [AI] wires `image:` in `_config.yml` (SEO-7).
- [ ] [AI] Delete "Hello World" (move its `welcome-email` role to a real post), anonymise the client repo name in the git-secrets post and fix its date (SEO-8).
- [ ] [AI] Remove the nested `<main>` in `_layouts/post.html` (SEO-9).
- [ ] [AI] Add a `404.html` and a visible RSS link in the footer (SEO-19, SEO-20).

## SEO foundations

- [ ] [Owner] Verify the domain in Google Search Console and Bing Webmaster Tools, submit `sitemap.xml`, write the baseline (clicks, impressions, indexed pages, PageSpeed mobile for `/` and one post) in this file.
- [ ] [AI] Author / Person / ProfessionalService structured data and `social:` links in `_config.yml` (SEO-10).
- [ ] [AI] Tags on every post, a tag index, related posts and a "Work with me" block in the post layout (SEO-11).
- [ ] [Owner] Approve the topic clusters in SEO-12 (performance, testing, security, upgrades).
- [ ] [AI] One pillar page per approved cluster, linking its posts, and links back from each post (SEO-12).
- [ ] [AI] Draft a `/services/` page targeting commercial queries; [Owner] sets scope, rates wording and availability (SEO-13).
- [ ] [AI] Performance: replace Font Awesome with inline SVGs, trim Inter weights, shrink `favicon.ico` (287 KB) (SEO-15).
- [ ] [Owner] Consent: decide between a consent banner and cookieless PostHog; [AI] implements (SEO-16).

## Content

- [ ] [Owner] Pick the 3 to 5 best-performing posts (from Search Console, once data exists) to refresh for current Laravel / PHP versions, with `last_modified_at` (SEO-14).
- [ ] [Owner] Resume a publishing cadence (e.g. 2 posts a month) inside the clusters; `AGENT_PROMPTS.md` holds the drafting prompts. No commits since 2025-12-02.
- [ ] [AI] Update `AGENT_PROMPTS.md` so new posts include `description`, tags, a ≤ 60 character title, no in-body H1 and links to the cluster pillar.
- [ ] [Owner] Regenerate the welcome-email PDF (`./generate-welcome-pdf.sh`) after the posts tagged `welcome-email` change.

## Monthly review

- [ ] [Owner] Search Console: clicks, impressions, position per page, indexing errors; note the numbers here with the date.
