---
layout: post
title: "Vercel Hobby Paused My Projects for 30 Days. Then It Didn't"
description: "I fixed the cause of my Vercel Hobby CPU overuse, and Vercel still paused every project for 30 days. How the pause works, how I got it lifted, my backup host."
date: 2026-11-26
tags: [vercel, nextjs, devops, free-tier, cloud-run]
tldr:
  - "Vercel Hobby counts usage over a rolling 30 days; there is no reset date, so a fix does not bring you back under the limit the next day."
  - "Crossing the Fluid Active CPU limit paused the whole team, five projects, for 30 days (Nov 25 to Dec 25), and every URL answered 402 DEPLOYMENT_DISABLED."
  - "The pause did not lift when usage dropped to near zero the next day."
  - "The support agent at vercel.com/help gave the one-time unblock each Hobby team gets, the same day I asked, after I explained the cause and the fix."
  - "That unblock can't be used twice, so I'm preparing Google Cloud Run as a backup host: free at this load, and billed rather than paused."
faq:
  - q: "What happens when a Vercel Hobby team goes over a usage limit?"
    a: "Vercel pauses the team. In my case the dashboard said the team exceeded the Hobby fair use limits for Fluid Active CPU and that the pause would end 30 days later. Every project in the team stopped serving: each URL, including static files, answered HTTP 402 with DEPLOYMENT_DISABLED."
  - q: "Does a Vercel Hobby pause end when usage goes back down?"
    a: "Not in my case. My usage was close to zero the day after the pause, and the dashboard still showed an end date 30 days after the day the limit was crossed. The options it offered were Upgrade to Pro or waiting; support was the third."
  - q: "Can Vercel support lift a Hobby pause early?"
    a: "Once. The support agent at vercel.com/help can grant a one-time unblock per Hobby team. I explained the cause, the fix and the current usage, and the team was serving again the same day. Other users report that a second unblock is refused, so treat it as a single spare."
---

When a Vercel Hobby team goes over a limit, Vercel pauses **every project in the team for 30 days**, counted from the day the limit was crossed, and fixing the cause doesn't shorten it. Mine was paused on 2026-11-25, a day after I found and removed what used the CPU. One message to Vercel's support agent got it lifted on 11-26. Here is what the pause looked like, the message that worked and the backup host I'm preparing, because that unblock only works once.

This follows [A Sentry Uptime Monitor Ate My Vercel Hobby CPU](/posts/2026-11-24-sentry-uptime-vercel-hobby-cpu/): an uptime monitor Sentry created by itself loaded the dashboard of my side project, [Job Radar](https://jobs.ciuculescu.com), every 60 seconds for nine days.

## Does the Vercel Hobby usage window reset on a fixed date?

No. The Hobby allowance for Fluid Active CPU is 4 hours over a **rolling 30 days**, so each day you are judged on the last 30. In the first post I wrote that the window reset the next day. It didn't. A day in the window drops out after 30 days, not on a set date. The days that crossed the line came after the fix. Reading the usage chart, 11-24 used about 1h05m and 11-25 about 27m. 11-24 still had the monitor until I repointed it, plus a production release with its smoke tests. Those two days took the total past 4 hours.

## What does a paused Vercel Hobby team look like?

The dashboard showed a red banner:

> **Deployments Paused.** Paused since Nov 25, 2026 for Fluid Active CPU. Your team exceeded the Hobby fair use limits. This pause ends on Dec 25, 2026.

It wasn't only deployments. Every project in the team stopped serving: Job Radar's production and dev sites, and four other projects that had used almost nothing. Every URL I tried, including a health endpoint and `robots.txt`, gave the same answer:

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://jobs.ciuculescu.com/api/health
# 402
curl -s https://jobs.ciuculescu.com/api/health
# Payment required
# DEPLOYMENT_DISABLED
```

Things kept running around the dead site. The production build of a merge made that evening showed as Ready in `vercel ls` and could not be reached. The twice-daily job fetch on GitHub Actions kept writing to the database, and its emails linked to the dead site. My post-deploy smoke tests were skipped, so nothing alerted me. I only noticed it in the dashboard.

## How do you get a paused Vercel Hobby team back?

Three ways: upgrade to Pro, wait out the 30 days, or ask the **support agent at [vercel.com/help](https://vercel.com/help)** for the one-time unblock each Hobby team gets. There is no support email address, and the community forum can't help with account pauses. I asked for the unblock. The message was short and factual:

- the team, the project and the date of the pause, and that every URL returns `402 DEPLOYMENT_DISABLED`;
- the cause, with numbers: an auto-created monitor, every 60 seconds since Nov 15, 8,959 checks, about 20 of 25 CPU minutes in 12 hours on one route;
- what I'd changed: the monitor repointed to `/api/health` every 20 minutes, `robots.txt` and `nofollow` on an expensive redirect, a 404 path that no longer renders a page, a daily usage check;
- that the usage chart was already near zero, and a usage screenshot attached;
- the question to answer if the unblock wasn't possible: does the pause end by itself on Dec 25?

Both sites answered 200 again the same day. The catch is in the name: it is **one-time**. People on Vercel's community forum report that a second request was refused. The next pause would last the full 30 days.

## Where can a Next.js app go as a backup host?

I compared five options against the real app: Next 16 App Router with a Node `proxy.ts`, `after()`, server actions, Neon over HTTP, Clerk, Sentry, Cloudflare DNS, deploy scripts on GitHub Actions. Its normal load is a few CPU minutes a day.

| Option | Cost at this load | Main catch |
|---|---|---|
| **Google Cloud Run** | Likely $0: 180,000 vCPU-seconds and 2 million requests free a month | Cold starts after idle; you write the Dockerfile and the deploy job |
| Fly.io | About $2 to $5 a month | No free tier |
| Netlify | 300 free credits a month; functions cost 10 credits per GB-hour | Billed on duration × memory, so time spent waiting on the database counts, and running out of credits can pause you the same way |
| Coolify on a Hetzner VPS | A flat few euros a month | You run and patch the server |
| Railway or Render | $5 to $7 a month | Pricing reports disagree; check the live pages |

Cloudflare Workers was out: the free plan allows 10 ms of CPU per request, and the OpenNext adapter doesn't support Node middleware, which `proxy.ts` is in Next 16.

I picked **Cloud Run**. It's free at this load, it bills extra use instead of pausing the service, and it fits deploy scripts that already run on GitHub Actions. You pick the region, so it can sit next to the database. The plan is a standby production copy with its own URL: build with `output: "standalone"` into a container, deploy it with `gcloud run deploy`, and switch the Cloudflare DNS record over if Vercel goes dark again. To get there I first have to remove what assumes Vercel: the deploy script that waits for Vercel's GitHub deployment status, a database migration that runs inside the Vercel build, `VERCEL_ENV` checks and the Vercel analytics scripts.

## What would I do differently?

- **Read "30 days" as rolling.** After a fix, the days before it stay in the total for a month. Hold back deploys, smoke tests and scans that cost function time until the chart shows real headroom, not until a date.
- **Alert on the site being down, not only on errors.** A 402 from the platform never reaches the app's error reporting. An external uptime check on production would have emailed me.
- **Keep the unblock as a spare, and have a second host ready.** Moving DNS takes minutes, while waiting out a pause takes 30 days.

## Sources

- [Vercel: Hobby plan](https://vercel.com/docs/plans/hobby) and [fair use guidelines](https://vercel.com/docs/limits/fair-use-guidelines)
- [Vercel KB: Why is my account deployment blocked](https://vercel.com/kb/guide/why-is-my-account-deployment-blocked)
- [Vercel community: What to do when your team is paused or blocked](https://community.vercel.com/t/what-to-do-when-your-team-is-paused-or-blocked/45069)
- [Vercel community: still paused after the one-time unblock was used](https://community.vercel.com/t/hobby-team-still-paused-after-one-time-unblock-was-used-and-usage-returned-within-limits/51328)
- [Google Cloud Run pricing](https://cloud.google.com/run/pricing)
- [Netlify: credit-based pricing plans](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/)
- [Cloudflare Workers limits](https://developers.cloudflare.com/workers/platform/limits) and [OpenNext on Cloudflare](https://developers.cloudflare.com/workers/framework-guides/web-apps/opennext/)
- [Fly.io pricing](https://fly.io/docs/about/pricing/)

*The fix took an hour and the pause would have taken a month, so a backup host is cheaper than another wait.*
