---
slug: sentry-uptime-vercel-hobby-cpu
status: drafting
inbox: none (found while working on Job Radar, 2026-11-24)
---

# Brief: a Sentry uptime monitor used up my Vercel Hobby CPU

**Reader:** a developer running a side project or small SaaS on Vercel Hobby (often with Neon and Sentry free tiers) who gets an "Upgrade to Pro" banner or a usage email and can't tell what is eating the quota.

**Main question:** what is using my Vercel Fluid Active CPU on the Hobby plan, and how do I find it with one hour of logs?

**Related questions:**
- Does Sentry create uptime monitors by itself?
- How do I see Vercel usage from the CLI or API on Hobby?
- How do I keep crawlers off expensive Next.js routes?
- How do I avoid hitting free-tier limits without checking dashboards?

**Intent:** learn (diagnose and fix)

**Service it supports:** none. The default CTA (contact) applies.

**Unique angle / proof:** a real case with real numbers: 3h 55m of the 4h Hobby CPU used; Vercel keeps one hour of runtime logs; `/` used 20 of about 25 CPU minutes in 12 hours; Vercel Firewall showed `sentry-uptime-monitoring-bot` at 60 requests an hour; Sentry had made the monitor on 2026-11-15 and run 8,959 checks of the dev home page. What the Vercel API gives on Hobby (`/v2/usage` works, `/v1/usage` and the observability query are Pro only), the API call that repointed the monitor, and the guard designed afterwards.

**Answer in one paragraph:** On Vercel Hobby, use Observability → Functions to find the route that uses the CPU, and Firewall → Bot Management to see who calls it. In my case Sentry had auto-created an uptime monitor that loaded a server-rendered dashboard every 60 seconds, about 25 CPU minutes a day of a 4-hour monthly allowance. Point monitors at a cheap health endpoint at a 20-minute interval.

**Sources to cite:** Vercel limits, Hobby plan, Fluid compute, runtime logs, Observability Plus; Sentry uptime monitoring and its troubleshooting page; Next.js robots.ts; Neon plans.

## Distribution
- [ ] LinkedIn: hook + 3 takeaways, link in the first comment (Andrei)
- [ ] One genuine answer where people ask what uses their Vercel Hobby CPU (Andrei, if he wants)
- [ ] Add to `_data/llms.yml`? No.
