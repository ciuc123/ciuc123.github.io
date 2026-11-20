---
layout: post
title: "My Site Scored 78/100 on the SEO Audit I Wrote"
description: "Part 2 of fixing my own site's SEO: a small Python audit that runs on every push and on any site from a GitHub issue, what it found, and the ratchet."
date: 2026-11-20
tags: [seo, python, github-actions, ci, client-zero]
series: seo-client-zero
series_part: 2
tldr:
  - "First score: 78/100, from 541 checks over 24 posts and 29 rendered pages; 119 failed."
  - "The audit is dependency-free Python and runs on every push and pull request, before anything is deployed."
  - "The same checks audit any live site from a GitHub issue, with a plain-language list of what to fix first."
  - "A ratchet keeps CI green on day one: failing rules start as warnings and become errors once fixed."
  - "Its tests caught two bugs in the live-site mode before it ever ran in CI."
---

In [part 1](/posts/2026-11-20-seo-client-zero-1-contact-form/) I found that my contact form had been faking success since launch. It survived because nothing ever checked it: it *looked* fine, so nobody looked closer.

That's the real lesson, and it applies to SEO as a whole. Titles creep past 60 characters, a post goes out without a description, someone links to a page that never existed. None of it throws an error. So before fixing anything else, I built the thing that checks: a small audit that runs on every push and every pull request, and that I can point at any client's live site.

Its first verdict on ciuculescu.com: **78 out of 100.**

## Why write an audit instead of using a crawler?

Because it runs before deploy, on every push, and checks rules specific to this site. There are excellent SEO crawlers, and for a one-off audit of a big site I'd still use one. I wanted something different:

- **It runs before deploy, not after.** It checks the built site in CI, so a broken link or a missing description is caught in the pull request, not by a visitor.
- **It checks the source too.** Front matter rules (title length, description, tags, dates) run on the Markdown, where the fix actually happens.
- **It checks things specific to this site.** Every post must end with a call to action, and every form must post to a real endpoint. That second one would have caught part 1's bug.
- **No dependencies.** Python's standard library only, so it runs anywhere with `python3`: CI, my laptop, a client's server.
- **The same checks work on any live site.** That's the version I'll use for client audits.

## What it checks

One tool, three modes:

```bash
python3 tools/seo_audit lint-content _posts             # source posts
python3 tools/seo_audit audit-site _site --posts _posts  # the built site
python3 tools/seo_audit audit-url https://example.com   # any live site, via its sitemap
```

| Area | Rules |
|---|---|
| Posts (front matter) | title ≤ 60 characters, description of 120–160 characters, at least one tag, date matches the filename, no future date, no stale year in the title, at least 300 words |
| Every page | one `<title>`, meta description of 50–160 characters, absolute canonical, exactly one `<h1>`, valid JSON-LD, `og:image`, `alt` on images, internal links that resolve |
| This site's own rules | every post has a call to action, every form has a real `action` |
| Whole site | `robots.txt` with a sitemap line, a valid sitemap whose URLs all exist, `llms.txt`, no private repo files published, no orphan pages |

Each rule applied to one page or post is one check. The score is simply the share of checks that pass. Reports come out three ways: a console summary, JSON, and Markdown that lands in the GitHub Actions job summary.

The stale-year rule shows the kind of detail that matters. "Laravel tips for 2024" on a post dated 2025 is stale; "PhpStorm 2025.1" is a version number. The rule only flags a year that isn't followed by `.digit`:

```python
_YEAR = re.compile(r"\b((?:19|20)\d{2})\b(?!\.\d)")  # "in 2024" yes, "PhpStorm 2025.1" no
```

## What it found

541 checks across 24 posts and 29 rendered pages. 422 passed, 119 failed:

| Finding | Pages or posts |
|---|---|
| No `og:image` (no picture when shared on LinkedIn, Slack, etc.) | 29 of 29 |
| No description in front matter | 22 of 24 |
| No tags | 18 of 24 |
| Title over 60 characters | 18 of 24 |
| Meta description too long or too short (up to 438 characters) | 17 of 29 |
| Two `<h1>` on the page, or none | 7 of 29 |
| Private repo files published (README.md, a shell script) | yes |
| No `llms.txt` | yes |
| Thin posts (8 and 25 words of prose) | 2 |
| A link to a page that never existed | 1 |

Some of these I knew about from the manual audit. Three I didn't:

- **A post links to its own "complete migration guide"** at a URL with the wrong date. The guide doesn't exist. Every reader who clicked got a 404.
- **Six posts have two `<h1>`s.** The layout renders the title as `<h1>`, and the posts start their body with a `# Heading` too. And the contact page has none at all.
- **Meta descriptions up to 438 characters.** With no `description` in front matter, the SEO plugin falls back to the first paragraph. Google cuts it at roughly 155–160 characters, and often writes its own instead.

All of them get fixed in later parts. This part is about making sure they're visible, and stay visible.

## The ratchet

If the audit failed the build on all 119 problems, CI would be red from day one and I'd learn to ignore it. If it only warned, nothing would stop new problems. So it uses a ratchet:

```json
{
  "base_url": "https://ciuculescu.com",
  "severity": {
    "og-image": "warning",
    "title-length": "warning",
    "description-present": "warning"
  }
}
```

Every rule is an **error** by default and fails the build. Rules that already failed on the baseline start as **warnings** in this config file. When a later task fixes a rule across the site, I delete its line, and from then on it's an error: the build blocks anything that breaks it again.

So the 13 rules that pass today (canonicals, valid structured data, a call to action on every post, real form actions, sitemap and robots.txt) are already enforced. The other 13 get promoted one by one as I fix them. The score can only go up.

## Testing the tester

An audit tool that's wrong is worse than none, because you trust it. It has 25 unit tests built on two fixture sites: a good one that passes every rule, and a bad one that breaks each rule at least once. The live-site mode is tested by serving the fixtures from a local HTTP server.

The tests caught two real bugs before the tool ever ran in CI:

1. **The sitemap on the wrong host.** If `robots.txt` names the sitemap on another host (`www.` vs. the bare domain, or staging), the live audit silently fell back to checking only the home page. It now tries that path on the audited host and then `/sitemap.xml`.
2. **Double counting.** A sitemap URL that returns 404 was also reported as an orphan page. One problem, two failures, and a lower score than deserved.

Then I ran the live-site mode against ciuculescu.com and compared it with the build audit. Same failures on the same pages, which is a good sign that both modes agree on what they're checking.

## CI, and one snag

A GitHub Actions workflow runs on every pull request and every push: unit tests, Jekyll build, then the audit of the built site and the posts. The Markdown report goes into the job summary, so the score is right there on the pull request.

The snag: the first run failed before the audit even started. GitHub's `ubuntu-latest` runner had moved to a newer Ubuntu, and its C compiler can't build `commonmarker` 0.23, an old dependency of the `github-pages` gem. I already built the site locally in the official `ruby:3.2` Docker image, so the job now runs in that same container. CI and my machine build the same way, which is what you want anyway.

## Auditing any site from a GitHub issue

The client mode needed a front door. I already run my client-site setup from a small control repo (`homelab`): open an issue with a form, a GitHub Actions workflow does the work and reports back on the issue. The audit now lives there too, with its own form:

1. Open an issue with the **SEO audit** form and the target site.
2. The workflow checks the request (only a public website; no IP addresses, internal names or anything that resolves to a private address), then runs the live-site audit over the pages in the site's sitemap.
3. A comment lands on the issue with the score and **what to fix first**: each problem with why it matters and how to fix it, in plain language, ordered by impact. Lost leads and broken links come before missing images.
4. The full report is committed to the repo, one file per site per day. The next audit of the same site shows the score change and, for each problem, how many pages were failing last time. That before/after is exactly the evidence a case study needs.

This site's CI uses the same tool, pinned to a tagged version of it, so the checks that gate my deploys are the ones I'd run for a client.

For ciuculescu.com the issue version gives **84/100**, higher than the 78 above, because a live audit sees only the rendered pages. It can't read the posts' source front matter, where most of the missing descriptions and tags show up.

## Check this on your own site

You don't need my tool for the most useful checks. Ten minutes in a browser:

1. **View source on your home page and one article.** Count the `<title>` and `<h1>` tags: one each.
2. **Read your meta description** in that source. Is it there, and is it under about 160 characters, or is it the first paragraph cut off?
3. **Look for `og:image`.** Without it, links to your site look bare on LinkedIn and in chat apps.
4. **Open `/robots.txt` and `/sitemap.xml`** on your domain. The sitemap should list your real pages, and robots.txt should point to it.
5. **Try `/README.md`, `/.env` and `/composer.json`** on your domain. Each should be a 404.
6. **Click the links in your three most-read articles.** Especially the ones to your own pages.

If you have a developer, ask them to put checks like these into the build. The point isn't the score, it's that a regression shows up as a failed build instead of a lost visitor. The source of this audit is public in [my homelab repository](https://github.com/ciuc123/homelab/tree/main/seo_audit).

## Next

Part 3 is the technical and identity foundation: a proper `robots.txt` and `llms.txt`, structured data that says who I am and what I do, an `og:image` for every page, and keeping private files out of the build. It also covers the two minutes this site was completely down while I was publishing part 1, and why.

*The audit doesn't make the site better. It makes it impossible to make it worse without noticing.*

## Sources

- [Google: control your snippets in search results (meta descriptions)](https://developers.google.com/search/docs/appearance/snippet)
- [Google: influencing your title links](https://developers.google.com/search/docs/appearance/title-link)
- [The Open Graph protocol (og:image)](https://ogp.me/)
- [Python: html.parser](https://docs.python.org/3/library/html.parser.html)
- [seo_audit source](https://github.com/ciuc123/homelab/tree/main/seo_audit)
