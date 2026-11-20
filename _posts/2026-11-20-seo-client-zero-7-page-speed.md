---
layout: post
title: "Cutting 1 MB Pages to 320 KB, and Why the Score Didn't Move"
description: "Part 7: replacing Font Awesome and Google Fonts cut first paint from 1.8 s to 1.0 s and removed every third-party render blocker. The real weight is a popup."
date: 2026-11-20
tags: [seo, performance, jekyll, client-zero]
series: seo-client-zero
series_part: 7
tldr:
  - "Five icons were pulling in all of Font Awesome: 243 KB of CSS and fonts that blocked rendering. They're now inline SVG."
  - "Inter is self-hosted (48 KB) instead of loaded from Google Fonts, and the site script no longer blocks rendering."
  - "Mobile Lighthouse, median of 3 runs: first paint 1.8 s to 1.0 s on the home page, render-blocking third-party files 2 to 0, page weight at load about 1 MB to 320 KB."
  - "The performance score stayed in the 90s: the remaining cost is analytics JavaScript, and a newsletter popup that adds about 550 KB five seconds after load."
faq:
  - q: "Should I self-host Google Fonts?"
    a: "For one or two font families, usually yes. You skip the connection to two extra servers, the font CSS no longer blocks rendering, and you control caching. Download the woff2 files you actually use, declare them with @font-face and font-display swap, and preload the main one. Keep the font's license file next to it."
  - q: "Is Font Awesome bad for performance?"
    a: "Not by itself, but loading the full kit for a handful of icons is. Here the CSS and two icon fonts came to 243 KB, and the CSS blocked rendering for almost a second in Lighthouse's mobile test. If a site uses fewer than a dozen icons, inline SVGs cost a few hundred bytes each and block nothing."
---

Every page on this site now weighs about 320 KB when it finishes loading, instead of about 1 MB, and the home page paints in 1.0 seconds instead of 1.8 on a simulated mobile connection. No third-party file blocks rendering anymore. The Lighthouse performance score, though, barely changed, and the biggest download on the site is still there. This part is about both.

## What was slowing the pages down?

Four files blocked rendering on every page, and two of them came from other servers:

| Render-blocking file | Lighthouse estimated delay |
|---|---|
| Font Awesome CSS (cdnjs) | 0.94 s |
| Google Fonts CSS for Inter | 0.89 s |
| `main.js` (the site's own) | 0.54 s |
| `main.css` (the site's own) | 0.21 s |

Font Awesome was there for five icons: GitHub, LinkedIn, Laravel, a server and a cog, used in ten places across the header, footer, home and contact pages. For those five it downloaded 243 KB of CSS and icon fonts on every page.

## What did I change?

Three things, in [one pull request](https://github.com/ciuc123/ciuc123.github.io/pull/21):

1. **Inline SVG icons.** A small include outputs each icon as SVG markup: brand logos from Simple Icons (CC0), the server and cog from Lucide (ISC license). They inherit the text color and size like the font icons did.
2. **Self-hosted Inter.** Two woff2 files, Latin (48 KB) and Latin Extended (81 KB, downloaded only when a page uses those characters), with `font-display: swap` and a preload for the Latin file. The license file sits next to them.
3. **A deferred script.** `main.js` moved to `<head>` with `defer`, so the browser downloads it in parallel and runs it after parsing instead of stopping for it.

Screenshots before and after matched except for the server and cog icons, which are now outlines instead of solid shapes. A follow-up shrank `favicon.ico` from 287 KB (seven sizes up to 256 px) to 9 KB (three sizes): browsers use the SVG favicon, and the large frames were never shown anywhere.

## What did Lighthouse measure?

Lighthouse 12.6, mobile preset, three runs per page against the live site, before and after the change. Medians:

| Page | Metric | Before | After |
|---|---|---|---|
| Home | First contentful paint | 1.8 s | 1.0 s |
| Home | Largest contentful paint | 1.8 s | 1.5 s |
| Home | Total blocking time | 230 ms | 330 ms |
| Home | Performance score | 95 | 92 |
| Home | Page weight / requests | 1,012 KB / 27 | 319 KB / 14 |
| N+1 post | First contentful paint | 1.7 s | 1.0 s |
| N+1 post | Largest contentful paint | 1.7 s | 1.8 s |
| N+1 post | Performance score | 96 | 96 |
| N+1 post | Page weight / requests | 893 KB / 26 | 323 KB / 14 |

Page rendering got faster: first paint is 0.7-0.8 s earlier on both pages, and only `main.css` still blocks rendering, for about 0.17 s. The scores didn't move, because on this site they're dominated by total blocking time, and that's JavaScript. PostHog's analytics library alone used about 400 ms of main-thread time on the home page. Across three runs, blocking time varies more than the change I made.

## Where did the other 700 KB go?

Mostly, it didn't go anywhere. It moved out of Lighthouse's view. The site has a MailerLite newsletter popup that appears five seconds after the page loads. Before, the page was slow enough that the popup's download started inside Lighthouse's measurement window. Now the page finishes first and Lighthouse stops measuring before the popup arrives.

So I measured a real visit in a headless browser with a mobile profile, counting every request in every frame:

| Time after opening the home page | Downloaded |
|---|---|
| At load | 202 KB |
| 5 seconds | 300 KB |
| 10 seconds | 827 KB |

The popup brings Google reCAPTCHA (about 450 KB), MailerLite's own fonts and scripts, and a logo: about 550 KB in total. It shows once a month per visitor, so a returning reader doesn't pay it again, but a first-time visitor on a phone does. That's not visible in a Lighthouse report, and it's the single biggest download on the site.

## What's left to do?

In order of size:

1. **The popup's reCAPTCHA (about 450 KB).** MailerLite lets you turn reCAPTCHA off for a popup, and spam can be handled with a honeypot field like the contact form uses. The better step is replacing the popup with an inline signup form posted through the same kind of serverless function as the contact form. Both are newsletter decisions, so they're on my list rather than done.
2. **Analytics JavaScript (188 KB, about 400 ms of CPU).** PostHog loads surveys and dead-click tracking that this site doesn't use. Turning those off is a config change. Loading analytics after the first interaction would remove most of the blocking time.
3. **`main.css`.** It's 5 KB and still blocks rendering for about 0.17 s. Inlining the CSS needed for the first screen would remove that, but on a 5 KB file it's the smallest item on this list.

## Check this on your own site

1. **Run Lighthouse three times, not once.** My home page scored 62, 95 and 96 on three runs of the same code. One run tells you very little.
2. **Read the render-blocking list.** Every third-party CSS file on it is a server your page waits for before showing anything.
3. **Count your icons.** If you load an icon font for fewer than a dozen icons, inline SVG is smaller and blocks nothing.
4. **Measure for longer than the page load.** Open your site in a private window, wait 10 seconds, then check the network panel's total. Popups, chat widgets and consent banners often arrive after Lighthouse stops looking.
5. **Check your favicon's size.** Mine was the largest file the site served itself.

## Next

Part 8 is the cleanup of thin content: deleting the placeholder first post, rewriting the oldest how-to so it's actually correct, and what I found when I checked which URLs on my domain I didn't create myself.

## Sources

- [Chrome for Developers: eliminate render-blocking resources](https://developer.chrome.com/docs/lighthouse/performance/render-blocking-resources)
- [Chrome for Developers: Lighthouse performance scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring)
- [MDN: font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display)
- [MailerLite: how to use reCAPTCHA](https://www.mailerlite.com/help/how-to-use-recaptcha)
- [PostHog JS configuration](https://posthog.com/docs/libraries/js/config)
- [Simple Icons](https://simpleicons.org/) and [Lucide](https://lucide.dev/)
