---
slug: ai-crawlers-vercel-hobby-cpu
status: drafting
inbox: none (Job Radar, follow-up to vercel-hobby-pause-30-days, 2026-11-28)
---

# Brief: AI crawlers were eating my Vercel Hobby CPU

**Reader:** a developer with a server-rendered Next.js app on Vercel Hobby whose Fluid Active CPU keeps climbing, with no idea which requests cause it.

**Main question:** how do I stop AI and scraper crawlers from using up my Vercel Hobby CPU?

**Related questions:**
- How do you see which bots hit a Vercel Hobby site when the logs keep one hour and have no user agent?
- What is a JA4 fingerprint and why block on it instead of an IP or a user agent?
- Can robots.txt block AI crawlers but keep Google?
- Why does a bot that matches its own robots.txt group ignore the `*` group?

**Intent:** learn (diagnose, then block)

**Service it supports:** none. The default CTA (contact) applies.

**Unique angle / proof:** real counts from one site on November 27 and 28, 2026: about 400 job pages in ten minutes from one AWS IP, a JA4 rule that denied 6,900 requests in a day, the 11 overnight hours of sampled logs with the firewall on (about 340 job-page and 240 home-page renders a day), the agents the Firewall logged (ElevenlabsCrawler 357, a no-ALPN scraper 299, breaknorm-jobs 105), and the robots.ts that shipped.

**Answer in one paragraph:** On Hobby every signed-out render of a dynamic page costs function CPU, and crawlers walk every page. Block the ones that ignore robots.txt in the Vercel Firewall by their JA4 TLS fingerprint, on every path, refused before the function runs; give the polite AI and scraper bots their own `Disallow: /` group in robots.txt, so search engines keep the pages.

**Sources to cite:** Vercel Firewall and custom rules docs, Vercel Hobby plan, JA4 spec (FoxIO), RFC 9309, Next.js robots.ts docs.

## Distribution
- [ ] LinkedIn: hook + 3 takeaways, link in the first comment (Andrei)
- [ ] Add to `_data/llms.yml`? No.
