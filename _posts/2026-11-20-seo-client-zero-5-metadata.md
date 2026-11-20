---
layout: post
title: "Fixing the Metadata of 23 Old Posts in One Pull Request"
description: "Part 5: written descriptions, shorter titles, tags and one h1 per page across every older post. What changed, one script gotcha, and the score: 94 to 99."
date: 2026-11-20
tags: [seo, metadata, jekyll, client-zero]
series: seo-client-zero
series_part: 5
tldr:
  - "22 of 24 older posts had no description, so search results showed auto-excerpts of up to 438 characters."
  - "18 titles were longer than 60 characters, the longest 101. All now fit, with the same meaning and unchanged URLs."
  - "Six audit rules (titles, descriptions, tags, one h1, stale years) moved from warning to build-breaking error."
  - "Live audit: 94 to 99 out of 100. 416 of 417 checks pass; the last one is a broken link."
faq:
  - q: "Should every page have exactly one h1?"
    a: "It's the safe default. MDN recommends one h1 per page with headings nested without skipping levels, which helps screen-reader users and makes the page's topic unambiguous. Search engines can cope with more than one, but a single h1 that matches the title costs nothing and removes the doubt."
  - q: "Do shorter titles change a post's URL?"
    a: "Not on a Jekyll site with date-and-slug permalinks. The URL comes from the file name, and the title only fills the title tag, the heading and the share cards. I shortened 18 titles without touching a single file name, so no links broke and no redirects were needed."
---

Every older post on this site now has a written meta description, tags, a title of 60 characters or fewer, and exactly one `<h1>`. It took one pull request, and the audit from [part 2](/posts/2026-11-20-seo-client-zero-2-audit-tool/) now fails the build if any of it regresses.

This is the least glamorous part of the series and probably the one with the most direct effect on clicks, because it's what people see in search results before they decide to visit.

## What was wrong with the old metadata?

Almost everything a search result is made of. Out of 24 older posts:

| Problem | Posts |
|---|---|
| No `description` in front matter | 22 |
| Title over 60 characters (longest: 101) | 18 |
| No tags | 18 |
| Two `<h1>` headings (title repeated as `#` in the body) | 5 |
| A past year in the title ("…in 2024" on a 2025 post) | 1 |

Without a description, the SEO plugin used the first paragraph as the meta description. Some of those ran to 438 characters, and some were 36 characters of a sentence fragment. Search results show roughly the first 155-160 characters, and search engines often write their own snippet when the page's is unusable.

Two pages that aren't posts had the opposite heading problem: the contact page and the posts list had no `<h1>` at all.

## How did I write 22 descriptions?

By hand, from each post's actual sections, not by generating marketing copy. Each description says what the reader gets, in 120-160 characters:

> Detect N+1 queries in Laravel, fix them with eager loading, and write PHPUnit tests that fail when a page starts running too many queries again.

The rule I held myself to: a description may only promise what the post delivers. If a post covers three things, the description names those three things. It's the same rule as the [answer-first standard](/posts/2026-11-20-seo-client-zero-4-content-pipeline/): a search snippet is an answer, and it should be a true one.

## How do you shorten titles without breaking anything?

Keep the meaning and the key terms, cut the filler, and don't touch the file name. On this site the URL is built from the file's date and slug, so a new title changes the page's `<title>`, its heading and its share cards, and nothing else. No links break and no redirects are needed.

| Before | After |
|---|---|
| Optimizing Laravel Testing Workflows with PhpStorm 2025.1: A Developer's Guide to Faster Debug Cycles (101) | Faster Laravel Testing and Debugging with PhpStorm 2025.1 (57) |
| Supercharge Your Laravel Development: PhpStorm 2025.1 with Seamless Xdebug Docker Integration (93) | PhpStorm 2025.1 + Xdebug in Docker for Laravel (46) |
| Stripe Payment Security: Essential Best Practices for Laravel Applications in 2024 (82) | Stripe Payment Security Best Practices for Laravel (50) |

Sixty characters isn't a number Google publishes. It's my rule of thumb for a title that fits a results line without being cut off, and the audit enforces it.

## What went wrong along the way?

One thing almost did. Several posts carry a `welcome-email` tag, and a shell script that builds a welcome PDF finds them with a plain `grep '^tags:.*welcome-email'`. If I had rewritten tags as a multi-line YAML list, that grep would have silently stopped matching and the PDF would have lost those posts. So tags stay on one line, and the `welcome-email` tags stayed where they were.

The other surprise was in my own tool. After the fix, 684 of 687 checks passed, and the audit printed **100/100**, because 99.56 rounds up. A perfect score with three open problems is a lie told by rounding, so the tool now caps the score at 99 while anything fails.

## Why one h1, and how?

Because the `<h1>` should name what the page is about, once. [MDN's guidance](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/Heading_Elements) is to prefer a single `<h1>` per page with headings nested without skipping levels, which matters most for people using screen readers.

Five posts started their body with the title again as a Markdown `#` heading, so the page had two. I moved every heading in those posts down one level, skipping code blocks, where a `#` is a shell comment, not a heading. The contact page's "Get in Touch" became the page's `<h1>` with its old styling, and the posts list got a "Posts" heading. While I was there, the post titles on that list were plain browser-blue links with no styling at all, and now they match the rest of the site.

## Result

| Check | Before | After |
|---|---|---|
| Posts with a written description | 2 of 24 | all |
| Titles of 60 characters or fewer | 6 of 24 | all |
| Posts with tags | 6 of 24 | all |
| Pages with exactly one `<h1>` | 22 of 29 | all |
| Audit rules that fail the build (of 37) | 29 | 35 |
| Live audit score | 94/100 | 99/100 |

What I can't show yet is the effect on clicks: that needs Search Console data, which I haven't connected. The before state is recorded, so the comparison can come later.

Two problems are left. One post links to a guide that doesn't exist, which belongs to the internal-linking work. Two very short posts need a decision about whether to expand, merge or hide them, which is an editorial call I'm leaving open for now.

## Check this on your own site

1. **Search for `site:yourdomain.com`** and read your own results as a stranger. Are the snippets sentences you wrote, or random first paragraphs?
2. **List your page titles** (any crawler or a quick script) and sort by length. Fix everything over about 60 characters first.
3. **Before changing a title, check what builds the URL.** If the URL comes from the title (some CMS setups), plan redirects.
4. **Grep your repo for anything that parses your content** before you reformat it: scripts, feeds, email builders.
5. **Count the `<h1>` tags** on your templates, not just your articles. Contact and listing pages are the usual misses.

## Next

Part 6 is internal linking: connecting related posts, fixing that last broken link, and making sure no post is a dead end.

## Sources

- [MDN: heading elements (one h1 per page)](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/Heading_Elements)
- [Google: control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)
- [Google: influencing your title links](https://developers.google.com/search/docs/appearance/title-link)
- [Jekyll: permalinks](https://jekyllrb.com/docs/permalinks/)
