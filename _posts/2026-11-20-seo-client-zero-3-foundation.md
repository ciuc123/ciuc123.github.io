---
layout: post
title: "The Two Minutes My Site Served a 404 for Every Page"
description: "Part 3: fixing the foundation of my own site: a deploy race that took it down, structured data, llms.txt, robots.txt, share images and a real 404 page."
date: 2026-11-20
tags: [seo, geo, structured-data, github-pages, client-zero]
series: seo-client-zero
series_part: 3
---

While I was publishing [part 1](/posts/2026-11-20-seo-client-zero-1-contact-form/) of this series, ciuculescu.com went down. Not slow: every page, the home page included, returned GitHub's "404 File not found" for about two minutes, then came back on its own.

The cause had been sitting in the repository for months, and my baseline audit had even flagged it as a risk. This part is about that, and about the rest of the foundation: the things search engines and AI assistants read before they read a single word of content.

## The deploy race

The site is built by GitHub Pages from the `master` branch. In June 2025 I had also added a GitHub Actions workflow that deployed **the raw repository** to Pages on every push. Two deploys ran for every push, and whichever finished last won.

Usually that was the real Jekyll build. That time it was the raw upload. The raw repository has `index.md`, not `index.html`, so every URL returned 404 until the next build replaced it. The same raw upload also served files that were never meant to be public, like the repo's README and a tool's cache file.

The fix was one line in a commit: delete the workflow. GitHub's own Jekyll build is now the only way the site gets deployed. The lesson is older than this site: **two things that can each deploy production will eventually both do it.**

## Private files

Even without the raw deploy, the Jekyll build was publishing three files it shouldn't have: the repository's `README.md`, a shell script, and a long document of internal prompts I use for drafting content. Jekyll copies any file without front matter as-is, and nobody had told it to skip these.

They're excluded now, and the audit from [part 2](/posts/2026-11-20-seo-client-zero-2-audit-tool/) treats a published private file as a build-breaking error.

## Telling machines who's behind the site

Search engines and AI assistants try to connect a page to an entity: a person or a business they can describe, trust and cite. Before this task, the only structured data on the site said "a WebSite, author: Andrei Ciuculescu" and nothing else. No job, no location, no links to profiles that would prove it's the same person.

Now every page carries one JSON-LD graph with stable identifiers:

```json
{
  "@type": "Person",
  "@id": "https://ciuculescu.com/#person",
  "name": "Andrei Ciuculescu",
  "jobTitle": "Laravel Backend & DevOps Specialist",
  "address": { "@type": "PostalAddress", "addressLocality": "Bucharest", "addressCountry": "RO" },
  "knowsAbout": ["Laravel", "PHP", "DevOps", "CI/CD", "Docker", "..."],
  "sameAs": ["https://www.linkedin.com/in/andrei-ciuculescu/", "https://github.com/ciuc123"],
  "worksFor": { "@id": "https://ciuculescu.com/#business" }
}
```

Next to it is a `ProfessionalService` with the three services and what each includes, and on every post a `BlogPosting` whose author is simply `{"@id": "https://ciuculescu.com/#person"}`. One definition of who I am, and everything points at it.

All of it comes from a single data file. The author box at the end of each post (see below this article) reads the same file, so the structured data and what a reader sees can't drift apart. That's also the version that works for clients: fill in one file, get consistent markup everywhere.

## llms.txt

`/llms.txt` is a short Markdown file for AI tools: who I am, the services, how to get in touch, and ten articles with a one-line summary each. It's a proposal, not a standard, and I can't point to an AI assistant that has confirmed it reads the file. It took ten minutes, and any tool that does read it gets a clean summary instead of having to guess from the navigation.

The summaries describe what each post covers and nothing more. If an assistant quotes them, they should be true.

## robots.txt that says what I mean

Before, `robots.txt` was generated and said only where the sitemap is. Now it explicitly allows everything, names the AI crawlers it welcomes (OpenAI's, Anthropic's and Perplexity's crawlers and agents, Bing, Common Crawl, and Google's and Apple's AI-use tokens), and keeps the sitemap line.

That's a choice, and it's worth making on purpose. For a freelancer who wants to be recommended by AI assistants, blocking their crawlers is self-defeating. A publisher might reasonably block **training** crawlers while allowing the **search** ones that send visitors. So I added a rule to the audit that fails only when a site blocks search engines or AI answer crawlers, not when it opts out of training.

## Share images

No page had an `og:image`, so a link to this site on LinkedIn or in a chat app showed up as plain text. Every page now has a default 1200×630 image. I made it as an HTML page in the site's colors and saved a screenshot of it with a headless browser, which is faster to change than an image file in a design tool.

## A real 404 page

Missing pages used to show GitHub's generic 404. Now they get a page with links home, to all posts and to contact, plus the five most recent posts. A wrong link from somewhere else no longer has to mean a lost visitor.

The audit checks this in two ways. On the built site, there must be a 404 page that links somewhere. On a live site, it requests a page that can't exist and expects status **404**. Some sites answer missing pages with status 200 and a "not found" message (a *soft 404*), and search engines then index those as real pages. That check found a bug in my own tool on its first run: the live mode was discarding the body of any 404 response, so every custom 404 page looked empty to it.

## The rest

- **An author box** on every post: name, one line of credentials, links to the About page, LinkedIn and GitHub. There's no photo yet, just initials. A photo is on my list.
- **A date mismatch fixed without moving a URL.** One post's file name said September 9, its front matter said August 9, and the live URL used August 9. I renamed the file to match, so the URL stays exactly where links already point.

## Result

| Check | Before | After |
|---|---|---|
| Audit score (same rules as part 2) | 78/100 | 84/100 |
| Pages with a share image | 0 of 29 | all |
| Structured data about the person and business | name only | Person + ProfessionalService with profiles, services, location |
| Posts whose author is a linked entity | 0 | all |
| Private files published | 3 | 0 |
| `llms.txt` | missing | yes |
| 404 page | GitHub default | custom, with links |
| Rules enforced in CI | 13 | 22 |

The last row is the ratchet: five rules fixed in this task moved from warning to error, and the audit gained four new ones (entity, article author, 404 page, AI crawlers), all passing. None of them can quietly regress now.

## Check this on your own site

1. **Count your deploy paths.** Look at everything that can publish your site (CI workflows, hosting settings, plugins). If there are two, remove one.
2. **Try `/README.md`, `/.env` and `/composer.json`** on your domain. All should be 404.
3. **Paste your home page into Google's Rich Results Test** and look for an Organization or Person with links to your profiles.
4. **Share your home page in a private chat** with yourself. If there's no image, add an `og:image`.
5. **Open `/robots.txt`.** Make sure it says what you mean about search engines and AI crawlers, not what a plugin decided.
6. **Visit a page that doesn't exist.** Is it helpful? Then check its status code (in your browser's developer tools, Network tab): it must be 404, not 200.

## Next

Part 4 is about content: an intake pipeline for ideas and drafts, and a post standard built for answer engines (a short summary up top, questions as headings, FAQ markup), shown on the first post that goes through it.

*Most of this work is invisible to readers. That's the point: it's what lets the visible part be found.*
