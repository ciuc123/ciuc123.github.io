# Content pipeline

How an idea becomes a published, search-ready, AI-citable post. Nothing in `content/` is published
(it's excluded from the Jekyll build). Drafts live in `_drafts/` (Jekyll's own drafts folder, also unpublished).

```
content/inbox/  →  content/briefs/  →  _drafts/  →  _posts/  →  distribute
   (raw)            (who/why/query)     (writing)    (CI lint)   (LinkedIn, newsletter)
```

## 1. Inbox: `content/inbox/YYYY-MM-DD-short-name.md`

No rules. Paste anything: a thought, a client question, a problem you solved this week, a voice note
transcript, a link. Optional first line `source: client-work | idea | question-asked | news`.
Best inputs: questions people actually asked, and problems you actually solved (real demand + first-hand proof).

## 2. Brief: `content/briefs/<slug>.md` (copy `templates/brief.md`)

Reader, the main question and 3-5 related ones, intent, the service it supports, the unique angle or proof,
and the answer in one paragraph. **Gate:** no reader, no question or no proof → don't write it yet.

## 3. Draft: `_drafts/<slug>.md` (copy `templates/post.md`)

The post standard, enforced by CI for posts dated 2026-11-20 or later:

- Front matter: `title` ≤ 60, `description` 120-160, `tags`, `tldr` (3-5 takeaways), optional `faq`,
  optional `last_modified_at`, `cluster`, `service`.
- Open with 2-3 sentences that answer the main question directly.
- At least one `##`/`###` heading phrased as a question; the first 40-60 words under it answer it.
- Concrete: versions, numbers with units, code, commands. **Never an invented statistic.**
- End with `## Sources` linking the docs, releases or data behind the claims.

The layout renders `tldr` as Key takeaways, `faq` as a visible FAQ plus FAQPage structured data, the
updated date, the author box and the call to action (to `service` if set).

Preview with drafts: `bundle exec jekyll serve --drafts`.

## 4. Publish

Rename to `_posts/YYYY-MM-DD-<slug>.md` on a branch and open a PR. `seo-checks.yml` lints the posts and
audits the built site; errors block the merge. Delete the brief's inbox note (or keep it, marked done).

## 5. Distribute and refresh

The brief has a distribution checklist (LinkedIn, newsletter, one genuine community answer, llms.txt if it's
one of the best ten). Quarterly: rewrite titles/descriptions of posts with impressions but low CTR, expand
posts ranking 8-20, bump `last_modified_at`.
