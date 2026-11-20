---
layout: post
title: "Original Data for AI Search: a Benchmark and 23 Links"
description: "Part 9: publishing a reproducible PHP benchmark built to be cited, the two misleading first runs it took, and 23 in-text links between older posts."
date: 2026-11-20
tags: [seo, geo, internal-links, client-zero]
series: seo-client-zero
series_part: 9
tldr:
  - "AI answers and other writers cite numbers they can't get elsewhere. So I published a benchmark: Laravel 13 on PHP 8.3, 8.4 and 8.5, on three machines."
  - "My first runs were wrong in opposite directions: PHP 8.5 looked 3x slower, then 2-3x faster. Interleaved, repeated runs on three machines showed it was the machine, not PHP."
  - "The final method bakes the app into images, interleaves versions, pins CPU cores and reports medians. Anyone can re-run it on GitHub with one click."
  - "23 in-text links now connect 16 older posts. In-text links between posts went from 14 to 37."
faq:
  - q: "Why does original data help with AI search?"
    a: "AI assistants and search engines prefer to cite the source of a fact. A post that rewrites documentation competes with the documentation and usually loses. A post with numbers nobody else has measured is the source, so answers that use those numbers have a reason to link to it."
  - q: "How do you make a benchmark trustworthy?"
    a: "Hold everything constant except the thing you're testing, interleave the variants so slow moments hit all of them, repeat enough to report a median and a spread, run on more than one machine, and publish the harness and raw data so others can check. Then state the limits plainly."
---

This part adds two things to the site: a piece of original data, and links between older posts in the text itself. The data is a benchmark of [Laravel on PHP 8.3, 8.4 and 8.5](/posts/2026-11-20-laravel-php-83-84-85-benchmark/), published with its harness and raw results so anyone can check it. Getting numbers I'd stand behind took two failed attempts first.

## Why publish original data?

Because it's the content that gets cited. When an AI assistant answers "is PHP 8.5 faster than 8.4 for Laravel?", it looks for a source that measured it. A post that rewrites the release notes competes with the release notes. A post with numbers nobody else has is the source.

The benchmark post follows the [answer-first standard](/posts/2026-11-20-seo-client-zero-4-content-pipeline/):
- The finding comes first: about 2% between versions, and 2x between CPUs.
- The tables and method follow, then the limits, and FAQ answers that stand on their own.
- It's listed in `llms.txt`.
- The harness, the raw results and the GitHub Actions runs are public.

## What went wrong in the first runs?

Two things, in opposite directions.

**First, PHP 8.5 looked three times slower.** A full request took 8 ms on PHP 8.3 and 8.4, and 20-26 ms on 8.5. If I'd published that, it would have been a headline, and wrong. The app was mounted into Docker from the host, so every file and database read crossed Docker Desktop's file sharing. I moved the app into one image per PHP version, which a benchmark should do anyway. The next run still showed 8.5 at 28-31 ms against 11-14 ms for the others.

**Then PHP 8.5 looked two to three times faster.** Microbenchmarks of single operations (escaping, Carbon dates, model attributes) put 8.5 far ahead, and the same Blade render took 10.5 ms on 8.4 in one run and 3.7 ms in another.

I never pinned down a single cause. The laptop was doing other work at the same time, including another Docker build, and short runs one version at a time can't tell that apart from a PHP difference. What settled it was changing the method, not finding the culprit.

## What made the final numbers trustworthy?

Holding everything constant and repeating:

1. **The same app and data everywhere:** one Laravel 13.43 app with dependencies pinned by `composer.lock`, seeded with fixed random data, baked into the official `php:8.x-cli` images.
2. **Interleaved runs:** 8 rounds, each running every workload on every version in a shuffled order, so a slow moment hits all versions.
3. **Pinned CPU cores** for every container, and a warm-up before measuring.
4. **Medians and spreads:** 40 samples per workload and version, and the spread is published next to the median.
5. **Three machines:** two GitHub Actions runners with different AMD EPYC CPUs, plus the laptop. A difference that shows up on one machine only is reported as such, not as a finding.

The final answer was much less exciting than either false start. A full request on PHP 8.5 was 1.4-2.2% faster than on 8.3 on both servers. The CPU generation made a 2x difference. That's the useful finding: upgrade PHP for support dates, and look elsewhere for speed.

## How did the internal links change?

[Part 6](/posts/2026-11-20-seo-client-zero-6-internal-links/) added a related-posts block, which guarantees a way onward but carries little context. This time I added 23 links inside the text of 16 older posts. Each one sits on words that already name the other post's topic: "eager-loaded relationships" links to the N+1 post, and "consolidated `bootstrap/app.php` file" links to the Laravel 11 structure post. I didn't change any wording.

| Measure | Before | After |
|---|---|---|
| In-text links between posts | 14 | 37 |
| 2025 posts with an in-text link out | 1 of 21 | 17 of 21 |
| 2025 posts with an in-text link pointing to them | 2 of 21 | 18 of 21 |

Three posts have no natural anchor anywhere else, so linking to them would mean adding sentences, not just links. That's an editorial decision I've left open. The related-posts block still links them.

## Check this on your own site

1. **Find one question in your field with no measured answer,** and measure it. A small, honest benchmark beats a long opinion piece.
2. **Distrust your first result,** especially a dramatic one. Change one thing at a time and run it again.
3. **Publish the method, the raw data and the limits.** Data that others can check is data they can cite.
4. **Read your older posts for phrases that already name another post's topic,** and link those exact words.

## Next

The tasks I can do without input are done for now. What's next needs decisions or accounts: Search Console and Bing to measure search results, the offers that service pages will be built around, and a few settings changes on the domain.

## Sources

- [Benchmark harness and raw results](https://github.com/ciuc123/homelab/tree/main/benchmarks/laravel-php)
- [Docker Docs: bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)
- [Google: make your links crawlable (anchor text)](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)
