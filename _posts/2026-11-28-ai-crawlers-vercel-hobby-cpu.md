---
layout: post
title: "AI Crawlers Were Eating My Vercel Hobby CPU"
description: "A crawler walked my job pages and pushed Vercel Hobby CPU over budget. How I found the bots, blocked them by JA4 fingerprint and kept Google with robots.txt."
date: 2026-11-28
tags: [vercel, nextjs, bots, robots-txt, free-tier]
tldr:
  - "On Vercel Hobby every signed-out render of a dynamic page costs function CPU, so a crawler walking 13,000 job pages is a CPU bill, not just traffic."
  - "One AWS IP fetched about 400 different job pages in ten minutes. A Vercel Firewall rule on its JA4 TLS fingerprint denied 6,900 of its requests in the next day, before any function ran."
  - "Hobby keeps one hour of request logs with no user agent; saving each hour with `vercel logs` and reading the Firewall's logged traffic together showed which pages still rendered and for whom."
  - "With the firewall on, about 340 job pages and 240 home pages a day still rendered for bots; AI and scraper crawlers such as ElevenlabsCrawler were among them."
  - "A separate robots.txt group gives those bots `Disallow: /` and leaves the job pages open to Google and Bing."
faq:
  - q: "Do requests blocked by the Vercel Firewall use function CPU?"
    a: "No. A custom rule with the Deny action refuses the request at Vercel's edge, before the function or the middleware runs, so it adds nothing to Fluid Active CPU. That is why blocking a crawler there is worth more than rejecting it in the app."
  - q: "What is a JA4 fingerprint?"
    a: "A short string that describes how a client opens a TLS connection: protocol, TLS version, whether it sent a server name, how many ciphers and extensions it offered, and which HTTP protocol it asked for. It stays the same when a crawler changes its IP or its user agent, and it is specific enough that one crawler's value doesn't match real browsers."
  - q: "Can robots.txt block AI crawlers without leaving Google?"
    a: "Yes. Give the AI bots a group of their own with `Disallow: /` and keep the `User-agent: *` group as it was. A crawler follows only the most specific group that names it, so Googlebot keeps the `*` rules. The flip side: a bot that matches its own group ignores everything in `*`, so that group must hold all the rules you want it to follow."
---

A crawler walking every job page of a server-rendered Next.js site costs real function CPU on Vercel Hobby, and Hobby gives you 4 hours a month. I stopped the one that ignored the rules with a **Vercel Firewall rule on its JA4 TLS fingerprint**, which refused 6,900 of its requests in a day before any function ran. The polite AI and scraper bots got their **own `Disallow: /` group in robots.txt**, so Google and Bing still see the job pages. Here is how I found them with Hobby's one hour of logs, and the counts from the night after.

This is the third post about the CPU budget of my side project, [Job Radar](https://jobs.ciuculescu.com). [The first](/posts/2026-11-24-sentry-uptime-vercel-hobby-cpu/) was a Sentry monitor loading the dashboard every minute, [the second](/posts/2026-11-26-vercel-hobby-pause-30-days/) the 30-day pause that followed.

## Why do crawlers cost CPU on Vercel Hobby?

Because every page they fetch is rendered on the server. Job Radar has about 13,000 public job pages at `/jobs/<id>`. Each one runs the Clerk middleware and a server render that reads the database, and signed-out pages are sent `private, no-store`, so the CDN caches none of them. A person reads a few pages. A crawler reads them all, one after the other.

The budget is tight. Hobby allows 4 hours of Fluid Active CPU over a rolling 30 days, and Vercel's one-time raise to 12 hours ends on December 26. From then on every day has to fit in 8 minutes, 7.2 with a margin. A quiet day was about 8.3.

## How do you find which bots hit a Vercel Hobby site?

Hobby keeps **one hour** of request logs, with the path, status and whether the page or the middleware ran, but **no user agent and no duration**. The Vercel Firewall's traffic view has the other half: IPs, JA4 fingerprints, AS names and user agents, but not what each request cost. I used both.

For the logs, a small script saved each hour before it expired. `vercel logs` returns at most 50 to 100 rows per call, so it asks in 2.5-minute slices:

```bash
for ((s = 3600; s > 0; s -= 150)); do
  from=$(date -u -d "@$((now - s))" +%Y-%m-%dT%H:%M:%SZ)
  to=$(date -u -d "@$((now - s + 150))" +%Y-%m-%dT%H:%M:%SZ)
  vercel logs --no-branch --since "$from" --until "$to" --limit 1000 --json --non-interactive >> "$out"
done
```

Even so, 17 slices during the crawl hit the row cap, so those busy hours are counted low. The quiet hours are complete.

On November 27 the logs showed one thing clearly: **about 400 job-page requests in ten minutes from one AWS IP, `216.73.216.238`, each a different `/jobs/<id>`**. In the first three hours of the sample, 276 of 581 function renders were job pages.

## What is a JA4 fingerprint, and why block on it?

JA4 describes how a client opens a TLS connection. The crawler's was `t13d1011h2_61a7ad8aa9b6_3fcd1a44f3e3`. The first part reads: TCP, TLS 1.3, a server name was sent (`d`), 10 cipher suites, 11 extensions, and it asked for HTTP/2 (`h2`). The two hashes after it cover the exact ciphers and extensions.

An IP changes, and blocking the whole AS would have hit Amazon, where my auth provider's webhooks may come from. A user agent is whatever the crawler says it is. The fingerprint comes from the TLS library the crawler runs, so it stays put, and it doesn't match ordinary browsers. On the evening of November 27 I set up the Firewall on production:

- the **AI Bots** managed ruleset, with AI Crawlers on **Deny**;
- **Bot Protection** on **Log**, to see what it would catch before letting it challenge anyone;
- a **custom rule** denying that JA4 on `/jobs/` paths;
- Hobby's one **rate-limit** rule, on `/jobs/`, answering 429.

A denied request never reaches the function, so it costs no CPU.

## Did the firewall rule work?

The next day the Firewall showed, for the past 24 hours:

| | Requests |
|---|---|
| Denied by the JA4 rule | 6,900 |
| Denied in total | 7,000 |
| Allowed | 6,600 |
| Logged by Bot Protection | 1,400 |

The crawler didn't give up. It kept asking at about the same pace all night, and got refused every time. Without the rule those would have been close to 7,000 job-page renders in one day.

The logged traffic showed what still got through. The same IP and JA4 appeared **592 times on `/`**, the home page, which my rule didn't cover because I had limited it to `/jobs/`. Below it in the list:

| Client | Logged requests | What it is |
|---|---|---|
| `ElevenlabsCrawler` (Amazon) | 357 | An AI crawler with a named user agent |
| A client on HostPapa, JA4 `t13d450900_d524c25c267f_9da38b6fd1bc` | 299 | `00` at the end of the first part: no ALPN, which browsers always send. A script, not a person |
| `breaknorm-jobs/1.0` (Hetzner) | 105 | A job aggregator |

The request logs from the 11 quiet hours, 21:00 to 08:00 UTC with the firewall on, give the cost side:

| Route | Renders in 11 hours | Per day at that pace |
|---|---|---|
| `/jobs/<id>`, signed out, each a different job | 157 | about 340 |
| `/`, signed out | 110 | about 240 |
| Everything else | 13 | about 30 |

157 renders of 157 different job pages in a night is a crawler, not a reader.

## Can robots.txt block AI crawlers but keep Google?

Yes, with a group of their own. I had considered `Disallow: /jobs/` for every bot, which would have stopped the job-page renders and also taken the pages out of search results. The counts pointed at AI and scraper bots, so only they lose access. In Next.js, `app/robots.ts`:

```ts
const BLOCKED_BOTS = [
  "GPTBot", "ClaudeBot", "anthropic-ai", "CCBot", "Bytespider", "PerplexityBot", "Amazonbot",
  "Meta-ExternalAgent", "Google-Extended", "Applebot-Extended", "ElevenlabsCrawler", "breaknorm-jobs",
];

export default function robots(): MetadataRoute.Robots {
  if (deployEnvironment() !== "production") return { rules: { userAgent: "*", disallow: "/" } };
  return {
    rules: [
      { userAgent: "*", allow: "/", disallow: PRIVATE_PATHS },
      { userAgent: BLOCKED_BOTS, disallow: "/" },
    ],
  };
}
```

One detail decides how to write the second group: **a crawler follows only the group that names it most specifically** (RFC 9309). A bot with a group of its own ignores the `*` group completely, so a group that only said `Disallow: /jobs/` would have opened the signed-in and private paths to those bots. `Disallow: /` sidesteps that, and it covers the home page too.

robots.txt only stops bots that read it. For the others the Firewall rule grew: I removed the `/jobs/` condition so the JA4 is denied on every path, added the HostPapa fingerprint with OR, and moved the rule above the rate limit, so these clients are refused before they count against it. Both changes went live on November 28.

## What's left?

- **The effect.** The day after a change is the earliest the Firewall can show it, and polite bots usually re-read robots.txt within a day. The next usage numbers will say whether a day now fits in 7.2 minutes.
- **The real fix is caching.** Signed-out pages render per request because the shared layout calls `auth()`. Moving that out lets the CDN serve them, and then no crawler costs CPU. That is a day or two of work, planned after December 15.
- **A bot-class log.** Hobby's logs have no user agent, so the app will log one class per signed-out job-page render (`googlebot`, `bingbot`, `ai`, `browser`, `other`), never the raw string. The next burst will then show who it is without the Firewall.

## Sources

- [Vercel Firewall](https://vercel.com/docs/vercel-firewall) and [custom rules](https://vercel.com/docs/vercel-firewall/vercel-waf/custom-rules)
- [Vercel: Hobby plan](https://vercel.com/docs/plans/hobby)
- [JA4+ fingerprinting (FoxIO)](https://github.com/FoxIO-LLC/ja4)
- [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309)
- [Next.js: robots.txt](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots)

*A crawler doesn't care what a page costs you, so the cheapest request is the one refused at the edge.*
