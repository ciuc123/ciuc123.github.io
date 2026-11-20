---
slug: github-pages-gem-ruby-32-gcc-15
status: published
inbox: content/inbox/2026-11-20-commonmarker-ubuntu-2604.md
---

# Brief: github-pages gem fails on ubuntu-latest (Ruby 3.2 + GCC 15)

**Reader:** a developer or small team building a Jekyll / GitHub Pages site in their own GitHub Actions
workflow (for checks, previews or a custom deploy) whose build suddenly fails at `bundle install`.

**Main question:** why does `bundle install` fail installing commonmarker 0.23.11 on ubuntu-latest, and how do I fix it?

**Related questions:**
- Why does it work on my machine / on ubuntu-24.04?
- Which Ruby version should a github-pages build use?
- Can I just pin the runner to ubuntu-24.04?
- Do I have to drop the github-pages gem?

**Intent:** learn (fix a broken build)

**Service it supports:** none. Deliberate: it's a DevOps/CI fix in the site's niche; the default CTA (contact) applies.

**Unique angle / proof:** a 3-way matrix on GitHub's own runners (run 44744308438): ubuntu-26.04 + Ruby 3.2.11
(GCC 15.2.0) fails; ubuntu-26.04 + Ruby 3.3.14 (GCC 15.2.0) passes; ubuntu-24.04 + Ruby 3.2.11 (GCC 13.3.0)
passes. Exact errors from the log (60× `unknown type name 'bool'` in ruby/internal/special_consts.h). Plus the
container fix used in production on this site. Not verified: the exact header interaction, compiler-flag fixes.

**Answer in one paragraph:** GitHub's ubuntu-latest runner is now Ubuntu 26.04 with GCC 15, which compiles C as
C23 by default. Ruby 3.2's headers then fail to compile native extensions, and commonmarker 0.23.11 (required
by the github-pages gem) is one. Use Ruby 3.3 in setup-ruby, or run the job on ubuntu-24.04 or in the ruby:3.2 Docker image.

**Sources to cite:** GCC 15 porting guide (C23 by default), Ruby branches page (3.2 EOL 2026-04-01),
actions/runner-images, ruby/setup-ruby, github/pages-gem, commonmarker 0.23.11 on RubyGems, GitHub docs on container jobs.

## Distribution
- [ ] LinkedIn: hook + 3 takeaways, link in the first comment (Andrei)
- [ ] One genuine answer where people ask about this error (Andrei, if he wants)
- [ ] Add to `_data/llms.yml`? No: useful, but not one of the ten best for buyers.
