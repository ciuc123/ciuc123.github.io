---
layout: post
title: "From 5 to 25: Linking My Blog Posts to Each Other"
description: "Part 6: 24 of 28 posts linked to no other post. A related-posts block ranked by shared tags fixed that, plus one link that had sent readers to a 404."
date: 2026-11-20
tags: [seo, internal-links, jekyll, client-zero]
series: seo-client-zero
series_part: 6
tldr:
  - "Before: only 5 of 28 posts were linked from another post, and 24 posts linked to no other post at all."
  - "After: 25 of 29 posts are linked from at least one other post, and every post links to three others."
  - "Related posts are ranked by how many topic tags they share, in about 30 lines of Liquid. No plugin, no JavaScript."
  - "One call to action had pointed readers to a guide that never existed. It now links to the real one."
faq:
  - q: "How many internal links should a blog post have?"
    a: "There's no magic number. A useful floor is that every post links to a few related posts and is linked from at least one, so neither readers nor crawlers hit a dead end. Beyond that, link where it genuinely helps the reader with the next question, ideally in the text itself."
  - q: "Is a related-posts block as good as links in the text?"
    a: "No. A link inside a sentence carries context: the words around it tell readers and search engines why the other page matters. A related-posts block is a floor that guarantees every post has a way onward. The better step is adding contextual links by hand to the posts that matter most."
---

Every post on this site now ends with three related posts, chosen by the topics they share. Before this change, 24 of 28 posts didn't link to a single other post. A reader who finished one had nowhere to go but back, and a crawler had little to go on about which posts belong together.

## Why do internal links matter?

Because they are how both readers and search engines move through a site. Google says it plainly: it uses links "as a signal when determining the relevancy of pages and to find new pages". A post that nothing links to depends on the sitemap and the posts list to be found, and it tells no one what it relates to.

For readers, it's simpler. Someone who just read about N+1 queries is the most likely person to want the post about testing strategies. If the page doesn't offer it, they leave.

## How bad was it?

I counted links between posts inside the article body (the content, series box and related posts, not the site navigation):

| Measure | Before | After |
|---|---|---|
| Posts linked from at least one other post | 5 of 28 | 25 of 29 |
| Posts with no link to another post | 24 | 0 |
| Average links from a post to other posts | 0.5 | 3.7 |

The five that were linked were the parts of this series, which link to each other through the series box. Everything older stood alone.

## How are related posts chosen?

By shared topic tags, in a Liquid include with no plugin and no JavaScript. Tags were cleaned up in [part 5](/posts/2026-11-20-seo-client-zero-5-metadata/), which is what makes this work at all:

1. Count how many topic tags each other post shares with this one.
2. Take posts sharing three or more tags first, then two, then one, newest first within each level.
3. If that gives fewer than three, fill up with the newest posts on the site's core topic (Laravel).
4. Skip tags that don't describe a topic (like `welcome-email`), and skip posts from the same series, because the series box already links those.

The core of it:

```liquid
{% raw %}
{%- for level in (1..3) reversed -%}
  {%- for p in site.posts -%}
    {%- if related.size >= 3 -%}{%- break -%}{%- endif -%}
    {%- assign shared = 0 -%}
    {%- for t in p.tags -%}
      {%- if my_tags contains t -%}{%- assign shared = shared | plus: 1 -%}{%- endif -%}
    {%- endfor -%}
    {%- if shared >= level -%}{%- assign related = related | push: p -%}{%- endif -%}
  {%- endfor -%}
{%- endfor -%}
{% endraw %}
```

The results look like what a human would pick: the N+1 query post now suggests the queue optimization, testing strategies and PhpStorm testing posts, and the PHP 8.4 posts point to each other.

## What was the broken link?

The Laravel 11 architecture post ended with "Get the complete Laravel 11 migration guide", linking to a URL dated 2024 that never existed on this site. Every reader who clicked the post's main call to action got a 404. The audit from [part 2](/posts/2026-11-20-seo-client-zero-2-audit-tool/) found it on its first run.

There is a real Laravel 11 migration guide on this site, written a few weeks before that post. The link now goes there. With that fixed, broken internal links are a build-breaking error, so the next one can't ship.

## What isn't solved yet?

Three things, honestly:

- **Four posts are still linked from no other post:** two very short ones waiting for a decision about their future, the one off-topic WordPress roundup, and a post about AI agents in Laravel whose only shared tag is the very common `laravel`. All four are still reachable from the posts list.
- **The fallback is lopsided.** Posts with no close match fall back to the newest Laravel posts, so three posts now receive 11-15 of these links each. It's better than nothing, and the fix is better tags or hand-picked links, not a cleverer algorithm.
- **These aren't contextual links.** A link inside a sentence carries much more meaning than a list at the end. Adding those by hand, and linking posts to service pages once those exist, is the next level.

With the broken link fixed, the live audit of the site passes all 431 of its checks. The full audit, which also lints every post's source, passes 712 of 714: the two short posts are the remaining warnings.

## Check this on your own site

1. **Pick three posts and scroll to the end.** Is there a way onward, or only the footer?
2. **Count incoming links for your best post.** If nothing else on the site links to it, it's carrying itself.
3. **Click the calls to action in your older posts.** Links to "the complete guide" are where 404s hide.
4. **Look at your tags.** If a related-posts feature suggests strange posts, the tags are usually the problem, not the feature.
5. **Add three contextual links** from your most-read post to the posts that answer the reader's next question.

## Next

Part 7 is page speed: the site still loads all of Font Awesome and a web font from third-party servers for a handful of icons, which is the first thing to measure and cut.

## Sources

- [Google: make your links crawlable](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)
- [Google: SEO starter guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Jekyll: variables (site.posts, site.tags)](https://jekyllrb.com/docs/variables/)
- [Liquid template language](https://shopify.github.io/liquid/)
