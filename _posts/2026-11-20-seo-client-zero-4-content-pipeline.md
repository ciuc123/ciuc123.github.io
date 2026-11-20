---
layout: post
title: "Writing for Answer Engines: a Post Standard Enforced in CI"
description: "Part 4: an intake pipeline from idea to post, an answer-first standard for search snippets and AI assistants, and a build that fails when a post skips it."
date: 2026-11-20
tags: [seo, geo, content, client-zero]
series: seo-client-zero
series_part: 4
tldr:
  - "Every post now starts as an inbox note, becomes a brief with a required proof, then a draft, then a post."
  - "The standard: an answer in the first sentences, 3-5 key takeaways, question headings, real code or data, and a Sources section."
  - "CI enforces it: seo_audit 0.4.0 fails the build if a new post lacks takeaways, a question heading or Sources."
  - "The first post through the pipeline needed proof, so I ran a 3-way runner experiment, and it overturned my first explanation."
faq:
  - q: "What does answer-first writing mean?"
    a: "The first sentences under the title, and the first 40 to 60 words under each heading, answer the question completely on their own. Detail, code and caveats come after. Search engines can then lift that paragraph as a snippet, and AI assistants can quote it without the rest of the page."
  - q: "Is FAQ structured data still worth adding?"
    a: "Google has shown FAQ rich results only for well-known government and health sites since August 2023, so don't expect the expandable answers in Google's results. The markup still describes the questions and answers precisely, which other search engines and AI tools can read, and it costs nothing once the layout generates it."
  - q: "Why put a brief before the draft?"
    a: "Because the brief has a gate: no named reader, no real question or no proof means no post. Proof is the expensive part, a measured number, a real case or code that ran, and it's what makes a post worth citing. Finding out a post has none before writing it saves the writing."
---

Every new post on this site now goes through the same pipeline and the same standard, and the build fails if a post skips the standard. The standard is simple: answer the question first, show proof, make each section quotable on its own, and cite sources.

It's the content side of the work in [part 3](/posts/2026-11-20-seo-client-zero-3-foundation/): that part told machines who's behind the site, and this one makes what's on it easy to find, quote and trust.

## Why write for answer engines at all?

Because more and more of the people who might read a post never see the page. They get an answer from a search snippet, Google's AI overview, ChatGPT, Claude or Perplexity, and those systems pick passages that answer a question cleanly. A post that buries its answer under three paragraphs of scene-setting loses to one that leads with it, even if the second one is shorter.

That doesn't mean writing for robots. The same shape is what a busy CTO wants: the answer up top, proof after, and the option to stop reading once they have what they came for.

## What does the pipeline look like?

Four folders, each with a clear purpose:

```
content/inbox/  →  content/briefs/  →  _drafts/  →  _posts/
   (raw)            (who/why/proof)     (writing)    (CI lint)
```

1. **Inbox:** anything goes. A client question, a bug I fixed, a voice note. Questions real people asked and problems I actually solved are the best inputs.
2. **Brief:** the reader, the question as they'd type it, 3-5 related questions, the service it supports, and the **proof**: a measurement, a real case, code that ran. The brief has a gate: no proof, no post.
3. **Draft:** written from a template, in Jekyll's drafts folder, so it isn't published.
4. **Post:** moved into `_posts/` on a branch. The pull request runs the build and the audit. Errors block the merge.

`content/` isn't published, and the prompt I use with an AI writing assistant was rewritten around the same rules. The old prompt asked for "relevant statistics", which is an invitation to make numbers up. The new one says every number comes from the brief's proof or a cited source, or it doesn't appear.

## What is the post standard?

Five rules, from the template every draft starts from:

- **Answer first.** The opening sentences answer the main question. Each `##` section answers its own question in the first 40-60 words.
- **Key takeaways.** 3-5 concrete facts in the front matter (`tldr`), rendered as the box at the top of this post.
- **Question headings.** At least one heading phrased as the question people ask.
- **Proof, not adjectives.** Versions, numbers with units, commands with their output, code that ran.
- **Sources.** A `## Sources` section at the end for every claim that isn't first-hand.

An optional FAQ (`faq` in the front matter) is rendered as a visible section and as FAQPage structured data. Google has limited FAQ rich results to government and health sites since 2023, so this is for clarity and for other readers of the markup, not for a Google feature.

## How does CI enforce it?

The audit from [part 2](/posts/2026-11-20-seo-client-zero-2-audit-tool/) gained four rules in version 0.4.0. For posts dated on or after a cutoff in the site's config, it checks:

| Rule | Fails when |
|---|---|
| `post-tldr` | fewer than 3 or more than 5 takeaways |
| `question-heading` | no `##`/`###` heading ends with a question mark |
| `sources-section` | no `## Sources` (or References) section |
| `faq-entries` | an FAQ question doesn't end in `?`, or its answer is under 20 words |

Posts from before the cutoff are exempt, so CI didn't go red over the older posts. The first three parts of this series were published the same day as the cutoff, so I brought them up to the standard instead: they now have takeaways, a question heading and sources too. A generic check came along as well: any page with FAQPage markup must have questions with real answers. That one also runs in client audits.

## What happened to the first post through the pipeline?

The pipeline's first post was about a CI failure from part 2: the `github-pages` gem stopped installing on GitHub's new `ubuntu-latest` runner. My explanation at the time was simple: "the new runner image breaks it".

The brief wouldn't accept that without proof. So I ran the same bundle on three runner and Ruby combinations, and the result didn't match my explanation. Ubuntu 26.04 with Ruby 3.3 worked. Ubuntu 24.04 with Ruby 3.2 worked. Only Ruby 3.2 on Ubuntu 26.04 failed, because of how Ruby 3.2's headers meet GCC 15, which compiles C as C23 by default.

The post I published, [github-pages Gem Fails on Ubuntu 26.04: Ruby 3.2 + GCC 15](/posts/2026-11-20-github-pages-gem-ruby-32-gcc-15/), says that, shows the table, and gives three fixes that each passed on real runners. Without the gate it would have said something plausible and partly wrong. That's the whole argument for the brief in one example.

## Result

| Measure | Before | After |
|---|---|---|
| Posts with key takeaways | 0 | 5 (every post since the cutoff) |
| Posts with a Sources section | 0 | 5 |
| New posts that pass the standard | not checked | 5 of 5, enforced in CI |
| FAQ markup on the site | none | 2 posts, valid |
| Live audit score | 93/100 | 94/100 |

## Check this on your own posts

1. **Read the first two sentences of your three most-read posts.** Do they answer the question in the title? If a stranger stopped reading there, would they have the answer?
2. **Look at your headings.** Is at least one phrased the way a customer would ask the question?
3. **Find every number in one post.** Can you say where each came from? If not, cite it or cut it.
4. **Add a Sources section** to the post that makes the most claims.
5. **Write one brief before your next post:** the reader, the question, and the proof. If you can't name the proof, that's the post you shouldn't write yet.

## Next

Part 5 was going to be measurement: Search Console, Bing Webmaster Tools and a monthly check of what AI assistants say when asked about Laravel help. It needs account access I haven't set up yet, so the next parts are the ones I can do now: a metadata pass over all the older posts, internal links between them, and page speed.

## Sources

- [Google Search Central: changes to HowTo and FAQ rich results (August 2023)](https://developers.google.com/search/blog/2023/08/howto-faq-changes)
- [Google: control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)
- [schema.org: FAQPage](https://schema.org/FAQPage)
- [Jekyll: working with drafts](https://jekyllrb.com/docs/posts/#drafts)
- [seo_audit source and rules](https://github.com/ciuc123/homelab/tree/main/seo_audit)

*A standard nobody checks is a suggestion. This one fails the build.*
