---
layout: post
title: "A Sentry Uptime Monitor Ate My Vercel Hobby CPU"
description: "My Vercel Hobby project hit 3h 55m of its 4h Fluid Active CPU. The cause was a Sentry uptime monitor I never created. How I found it, fixed it and guard it now."
date: 2026-11-24
last_modified_at: 2026-11-26
tags: [vercel, sentry, neon, nextjs, devops, free-tier]
tldr:
  - "Vercel Hobby includes 4 hours of Fluid Active CPU per 30 days; my side project reached 3h 55m with one day to go."
  - "Sentry had auto-created an uptime monitor on 2026-11-15 that loaded my dev site's dashboard every 60 seconds: 8,959 checks in nine days."
  - "Vercel's Observability → Functions page found the route (/ used 20 of about 25 CPU minutes in 12 hours); Firewall → Bot Management named the caller."
  - "The fix: repoint the monitor at a cheap /api/health endpoint every 20 minutes, add robots.txt and nofollow to an expensive redirect route."
  - "Next: a usage guard that compares each free quota with a baseline ending at 90% every day and turns checks down at 20% over."
faq:
  - q: "Does Sentry create uptime monitors automatically?"
    a: "Yes. Sentry can detect the hostnames your app reports errors from and create an uptime monitor for one of them. Mine checked a server-rendered page every 60 seconds. You can edit, disable or delete it under Monitors → Uptime; Sentry's assistant told me there is no organization switch to turn the detection off."
  - q: "How do I see Vercel usage on the Hobby plan from the API?"
    a: "The documented usage commands are Pro only: vercel usage returned 404 and /v1/usage said Pro or Enterprise. The dashboard's own /v2/usage endpoint answered on Hobby with daily invocations and function GB-hours, but not Fluid Active CPU. It is undocumented, so treat it as something that can change."
  - q: "How long does Vercel keep runtime logs on Hobby?"
    a: "About one hour in my case: vercel logs --since 24h only returned entries from the last hour, and older ranges came back empty. Look at the logs while the problem is happening, or use Observability, which keeps longer history per route."
---

**Update, November 26, 2026:** the window did not reset the next day. Vercel counts a rolling 30 days, and it paused every project in the team for 30 days anyway. How that went and how I got it lifted: [Vercel Hobby Paused My Projects for 30 Days. Then It Didn't](/posts/2026-11-26-vercel-hobby-pause-30-days/).

My Vercel Hobby account showed **3h 55m of 4h Fluid Active CPU used**, with the 30-day window resetting the next day. The cause was not traffic. It was a Sentry uptime monitor that Sentry created by itself, loading a server-rendered dashboard on my dev site once a minute for nine days. Here is how I found it with one hour of logs, what I changed, and the guard I'm building so I don't find the next one on a dashboard again.

The project is [Job Radar](https://jobs.ciuculescu.com), a Next.js App Router side project on Vercel Hobby, with Neon Postgres, Clerk and Sentry, all on free plans.

## What used the Vercel Hobby CPU?

A Sentry uptime monitor on the dev deployment's home page, every 60 seconds. The home page renders the whole job dashboard (auth, database reads, a list of jobs), about 1.1 seconds of CPU each time. 1,440 renders a day is roughly 25 CPU minutes, against an allowance of 4 hours a month. The daily bars on the Usage page went from a few minutes to 10 to 17 minutes a day in mid-November, and to 25 and 39 minutes on the last two days.

## How do you find it when Hobby keeps an hour of logs?

Three places, in this order.

**1. Runtime logs, for the pattern.** The CLI pulls them as JSON, but on Hobby only the last hour came back:

```bash
vercel logs --no-branch --since 24h --limit 1000 --json > logs.jsonl
# older ranges, e.g. --since 2026-11-23T00:00:00Z --until 2026-11-23T12:00:00Z, returned nothing
```

Grouping that hour by host and path showed the pattern at once: `GET /` on `dev.jobs.ciuculescu.com` at :10 past every minute, 57 times in the hour. The logs have no user agent, so they don't say who.

**2. Observability → Functions, for the cost.** For the last 12 hours, all environments:

| Route | Invocations | Active CPU |
|---|---|---|
| `/` | 1.1K | 20m |
| `/jobs/[id]` | 1.4K | 2m |
| `/r/[jobId]` | 1.3K | 1m |
| `/settings` | 128 | 27s |

One route, 20 of about 25 minutes. The job pages and the `/r/` redirect were crawlers: cheap per request, but nothing told them to stay away.

**3. Firewall → Bot Management, for the caller.** The past hour's verified bots: `sentry-uptime-monitoring-bot` 60, `googlebot` 30, `amazonbot` 23. Sixty an hour is once a minute.

## Does Sentry create uptime monitors by itself?

Yes. I never made one. Sentry's API showed it:

```bash
sentry api "organizations/<org>/detectors/?query=type:uptime_domain_failure" --json
# "name": "Uptime Monitoring for https://dev.jobs.ciuculescu.com"
# "dateCreated": "2026-11-15T03:12:10Z", "intervalSeconds": 60, "mode": 3  (auto-detected)
```

Its page in Sentry counted **8,959 checks from Nov 15 to Nov 24**, each about 3 seconds against the dev dashboard. When I asked Sentry's assistant how to turn uptime auto-detection off, the answer was that there is no organization-wide switch: delete the monitor (it won't be re-created) or disable it.

## How do you point it somewhere cheap?

I kept the monitor but made it useful: production, a health endpoint, every 20 minutes. One API call:

```bash
sentry api "projects/<org>/<project>/uptime/<monitor-id>/" --method PUT --data '{
  "name": "Production health",
  "url": "https://jobs.ciuculescu.com/api/health",
  "intervalSeconds": 1200,
  "timeoutMs": 10000,
  "downtimeThreshold": 2,
  "recoveryThreshold": 1
}'
# mode changes from 3 (auto-detected) to 1 (manual), so Sentry stops managing it
```

`/api/health` does three small reads (migration count, featured list count, source status) and costs about 0.3 s of CPU. Every 20 minutes is 72 calls a day, about 20 seconds of CPU. I didn't go shorter, because a check every few minutes would also keep the Neon database from ever suspending, and Neon's free compute hours are a quota too.

## How do you keep crawlers off expensive routes in Next.js?

`/r/<jobId>` is the Apply link: two or three database reads, a click count, then a redirect to the employer. A crawler gets nothing from it. There was no `robots.txt` at all, so I added `app/robots.ts`, built once per environment:

```typescript
import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  // dev and preview deployments: nothing is crawled
  if (process.env.VERCEL_ENV !== "production") return { rules: { userAgent: "*", disallow: "/" } };
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/r/", "/api/", "/admin", "/settings", "/network", "/cv", "/onboarding"],
    },
  };
}
```

Plus `rel="nofollow noreferrer"` on the Apply links, and `.txt` added to the static-file exclusions of the Clerk proxy matcher so `robots.txt` never runs middleware. Polite crawlers follow it; the uptime monitor would not have, which is why the monitor fix came first.

One more small leak turned up in the same hour: `/favicon.ico` didn't exist, so every request rendered the 404 page as a function. The proxy skips `.ico`, so the root layout's Clerk `auth()` threw, and the error alert fired on each one. A favicon file and a `catch` around that one `auth()` call (a missing session there only hides a banner) closed it.

## How do you see Vercel usage from the API on Hobby?

Partly. What I tried:

| Call | Hobby result |
|---|---|
| `vercel usage` | `Costs not found (404)` |
| `GET /v1/usage` | "only available to Teams on the Pro or Enterprise plan" |
| `POST /v2/observability/query` (CPU per route) | 402, needs Observability Plus |
| `GET /v2/usage?type=requests` | **works**: daily invocations, GB-hours, transfer, per project |

So Fluid Active CPU itself is not readable. Over the 30-day window my account used 11.2 function GB-hours for 235 CPU minutes, about 21 CPU minutes per GB-hour, and the daily ratio stayed between 20 and 30. That is good enough to estimate CPU from GB-hours and correct the factor once a month from the Usage page. `/v2/usage` is the dashboard's own endpoint and undocumented, so a tool that reads it has to fail loudly when it changes.

Neon is easier: `neonctl projects get <id>` returns `data_transfer_bytes`, `compute_time_seconds` and the consumption period, and reading them doesn't wake the database. That check showed the next limit coming: production at 4.16 of 5 GB transfer with a week of the month left.

## How do you stop finding this on a dashboard?

Nothing watched the trend for nine days. The plan, agreed today and not built yet: a small usage guard that runs every 3 hours from a public GitHub repo (free Actions minutes), outside the apps it watches, because the Vercel Hobby allowance is shared by every project on the account.

- **Baseline:** each quota has a planned curve that reaches 90% of the free limit at the end of its window. For Vercel CPU that is 7.2 minutes a day; for Neon transfer, 150 MB a day.
- **Every morning:** one line per quota, used against the baseline for the date and the projected end of the window.
- **20% over the baseline**, in a day or in total: the email adds a root-cause report (which project grew, the last hour of requests grouped by host and path, the uptime monitors, workflow runs) and light measures switch on by themselves: a slower uptime check, no security scan on dev deploys, no dev data fetch.
- **Projected past 100%:** heavier measures (dev behind Vercel's login, a firewall rule for bots) are proposed with the command to apply them, and wait for me. Production is never paused.

Run against this window, the guard would have acted around Nov 13, when Vercel CPU went to 10 to 17 minutes a day against a 7.2-minute baseline, eleven days before I opened the Usage page.

## Sources

- [Vercel: Limits](https://vercel.com/docs/limits) and [Hobby plan](https://vercel.com/docs/plans/hobby)
- [Vercel: Fluid compute](https://vercel.com/docs/fluid-compute)
- [Vercel: Runtime logs](https://vercel.com/docs/logs/runtime)
- [Vercel: Observability Plus](https://vercel.com/docs/observability/observability-plus)
- [Sentry: Uptime monitoring](https://docs.sentry.io/product/monitors-and-alerts/monitors/uptime-monitoring/) and [troubleshooting](https://docs.sentry.io/product/monitors-and-alerts/monitors/uptime-monitoring/troubleshooting/)
- [Next.js: robots.ts](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots)
- [Neon: Plans](https://neon.com/docs/introduction/plans)

*The monitor was one setting I never chose; the guard is so the next one shows up in a morning email instead.*
