---
layout: post
title: "Deleting a Post, Fixing Another, and URLs I Didn't Create"
description: "Part 8: deleting a one-line post without breaking its URL, rewriting a how-to that never worked, and eleven paths GitHub Pages added to my domain."
date: 2026-11-20
tags: [seo, content, github-pages, client-zero]
series: seo-client-zero
series_part: 8
tldr:
  - "The site's thinnest post, a one-line 'Hello World', is deleted. Its URL redirects to the posts list, so old links still work."
  - "The other thin post, a how-to on removing secrets from git, had commands that would have failed. It's rewritten and every command was tested."
  - "GitHub Pages serves every project site of the account under the main domain: eleven paths on ciuculescu.com that I never created."
  - "One of those paths served a full copy of another website with no canonical tag. Duplicate, off-topic content on the main domain."
faq:
  - q: "Should you delete thin blog posts or improve them?"
    a: "Improve the ones that answer a real question, delete the ones that don't. A placeholder with one sentence has nothing to improve, so it goes. A short how-to on a real problem is worth rewriting properly. Either way, keep the old URL working with a redirect so links and bookmarks don't end in a 404."
  - q: "How do you redirect a deleted post on GitHub Pages?"
    a: "GitHub Pages can't send server-side 301s for single pages, but the jekyll-redirect-from plugin is on its supported list. Add it to the plugins in _config.yml and put a redirect_from line with the old URL in the target page's front matter. Jekyll then writes a small page at the old URL that sends visitors on and tells search engines not to index it."
---

The two thinnest posts on this site are dealt with: one is deleted with its URL redirected, the other is rewritten and tested. While checking which URLs the site really answers on, I found eleven I never created, put there by GitHub Pages, and one of them was serving a copy of another website.

## Which posts were thin, and what happened to them?

The audit from [part 2](/posts/2026-11-20-seo-client-zero-2-audit-tool/) flags posts under 300 words. Two were left after the metadata work in [part 5](/posts/2026-11-20-seo-client-zero-5-metadata/):

| Post | Words | Decision |
|---|---|---|
| Hello World (2024) | 7 | Deleted, URL redirects to /posts/ |
| How to remove git secrets from commits (2025) | about 110, mostly commands | Rewritten and tested, same URL |

The first had nothing to improve: it was the placeholder from the day the blog was set up. The second answers a question people really search for, so it was worth doing properly.

## How do you delete a post without breaking its URL?

Redirect the URL somewhere useful. GitHub Pages doesn't do server-side redirects for single pages, but it supports the `jekyll-redirect-from` plugin. One line in the posts list's front matter:

```yaml
redirect_from:
  - /posts/2024-06-10-hello-world/
```

Jekyll now writes a tiny page at the old URL. It forwards visitors to /posts/, has a canonical link to /posts/, and carries `noindex`, so search engines drop the old URL instead of keeping it as an empty page.

My own audit then failed the build: it checked the redirect page like a real page and found no description, no image and no call to action. A redirect isn't a page, so [seo_audit 0.4.2](https://github.com/ciuc123/homelab/pull/28) skips any page whose meta refresh points elsewhere.

## What was wrong with the git secrets post?

It looked right and wouldn't have worked. I tested every step of a [new version](/posts/2025-08-09-remove-secret-content/) on a throwaway repository and found four problems in the old one:

1. The replacements file was written in one directory and read from another.
2. `git push --force --all` pushes branches but not tags, so a tag on an old commit would have kept the secret.
3. The final check passed every revision on one command line, which breaks on large repositories.
4. It never said to rotate the secret first, which is the step that matters most.

The test also turned up something worth saying out loud: after the rewrite and force-push, the old commit was still on the server and could be read by its SHA. The post now explains what GitHub keeps and who can remove it.

## What URLs did GitHub Pages add to my domain?

Every project site on the account. When a GitHub account's user site has a custom domain, GitHub Pages also serves each project repository's Pages site at `yourdomain.com/<repo-name>/`. I found this by asking why `ciuculescu.com/content/` redirected to another subdomain. The response headers came from GitHub, not Cloudflare.

Eleven repositories on my account have Pages enabled:

| What `ciuculescu.com/<repo>/` does | Paths |
|---|---|
| Redirects (301) to the project's own domain, nine of them over plain `http://` | 10 |
| Serves a full copy of another site, with no canonical tag | 1 |

The redirects are mostly harmless: an extra hop, and a step through plain HTTP where a project doesn't enforce HTTPS. The copy is the real problem. It's an old copy of a small business's website, sitting on a domain about Laravel consulting, with nothing telling search engines which copy is the original. It isn't linked from anywhere, but any link to it would make it crawlable.

None of this shows up in the site's own repository, its sitemap or its build. You only see it by listing the account's repositories with Pages enabled and requesting each path.

## What's left?

The fixes are repository settings, not code, and they're on my list:

- Unpublish the duplicate site's Pages, or give it its own domain.
- Turn off Pages for the repository whose domain is now served by a different host. That also frees the `/content/` path.
- Enforce HTTPS on the remaining project sites, so the redirects skip plain HTTP.

One more post is still waiting for a decision: an off-topic WordPress roundup that doesn't fit a Laravel consulting site. Moving it, keeping it or hiding it from search is an editorial call, not a technical one.

## Check this on your own site

1. **Sort your posts by word count.** Anything under 300 words: improve it, merge it or delete it, but decide.
2. **Redirect what you delete.** Check the old URL afterwards: it should land somewhere useful, not on a 404.
3. **Run the commands in your old how-tos.** If a post tells people what to type, the commands should work today.
4. **On GitHub Pages with a custom domain, list your Pages repositories** (`gh api users/YOU/repos --paginate --jq '.[] | select(.has_pages) | .name'`) and open `yourdomain.com/<repo>/` for each one.
5. **Read the headers of any redirect you didn't set up.** `curl -I` tells you which server answered.

## Sources

- [GitHub Docs: about GitHub Pages (user, organization and project sites)](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages)
- [GitHub Docs: about custom domains and GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)
- [jekyll-redirect-from](https://github.com/jekyll/jekyll-redirect-from)
- [GitHub Pages: dependency versions (supported plugins)](https://pages.github.com/versions/)
- [Google: consolidate duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
