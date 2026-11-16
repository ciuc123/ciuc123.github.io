# dev.ciuculescu.com: investigation (2026-11-16)

## What was checked

- **This repository**: no reference to `dev.ciuculescu.com` anywhere (config, layouts, workflow, posts). `CNAME` holds only `ciuculescu.com`.
- **job-radar repository**: no reference either. Its environments are `jobs.ciuculescu.com` (production, Vercel) and Vercel preview URLs for `development` and `preview`; none is mapped to `dev.`.
- **Live DNS / HTTP**: not checked. The cloud session that did this survey could not reach `ciuculescu.com` or `dev.ciuculescu.com` (blocked by the session's network policy). The checks below are for the owner, or for a later session with those hosts allowed.

So `dev.ciuculescu.com` is not served by anything in these two repositories. Either it has no DNS record, or it points somewhere set up by hand.

## Checks to run (5 minutes)

```bash
dig +short dev.ciuculescu.com CNAME
dig +short dev.ciuculescu.com A
curl -sI https://dev.ciuculescu.com/ | head -5
```

| Result | Meaning | Action |
|---|---|---|
| No record | Subdomain unused | Decide whether it should exist (options below) |
| CNAME to `ciuc123.github.io` or a GitHub Pages IP, page says "There isn't a GitHub Pages site here" | **Dangling record: subdomain-takeover risk** (anyone could claim it with a Pages repo) | Delete the record, or attach a repo to it; verify `ciuculescu.com` in GitHub (Settings → Pages → Verified domains), which blocks takeover of every subdomain |
| CNAME to `cname.vercel-dns.com`, Vercel 404 "DEPLOYMENT_NOT_FOUND" | Dangling Vercel record, same risk | Delete it or assign it to a project |
| A working site | Something already lives there | Note what in `PLAN.md`; add `noindex` if it is a copy of the main site |

Whatever the result: verifying the domain in GitHub is worth doing anyway.

## Options if a dev site is wanted

GitHub Pages serves one custom domain per repository, so the blog cannot have both `ciuculescu.com` and `dev.ciuculescu.com` from the same repo.

1. **Recommended: no dev subdomain; local preview + PR previews.** `bundle exec jekyll serve` locally, and if a shareable preview is needed, Cloudflare Pages or Netlify building PRs on their own `*.pages.dev` / `*.netlify.app` URLs (free, nothing to index, no DNS to maintain).
2. **dev.ciuculescu.com as staging of the blog**: a Cloudflare Pages / Netlify / Vercel project on a `develop` branch, mapped to `dev.`, with `robots: noindex` (an `X-Robots-Tag: noindex` header or a `_config.dev.yml` that adds the meta tag) and a canonical pointing at `ciuculescu.com`. Without noindex it competes with the real site as duplicate content.
3. **dev.ciuculescu.com as a developer hub** (projects, open source, tools, a link to Job Radar). Only worth it with content that does not belong on the main site; otherwise a `/projects/` page on `ciuculescu.com` ranks better (one domain gathers all links).
4. **Map it to Job Radar's development environment** (Vercel domain on the `development` branch). Needs Clerk development allowed origins updated and `noindex`; the Vercel preview URL already does this job, so little gain.
