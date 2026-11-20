---
layout: post
title: "github-pages Gem Fails on Ubuntu 26.04: Ruby 3.2 + GCC 15"
description: "bundle install fails on commonmarker 0.23.11 on GitHub's ubuntu-latest. The cause is Ruby 3.2 with GCC 15, and three fixes that I tested on real runners."
date: 2026-11-20
tags: [github-actions, ruby, jekyll, devops]
tldr:
  - "On GitHub's ubuntu-latest runner (Ubuntu 26.04, GCC 15.2), bundle install for the github-pages gem fails while compiling commonmarker 0.23.11 with Ruby 3.2.11."
  - "The errors are in Ruby 3.2's own headers (unknown type name 'bool'). GCC 15 compiles C as C23 by default."
  - "Same runner with Ruby 3.3.14: passes. Ubuntu 24.04 (GCC 13.3) with Ruby 3.2.11: passes."
  - "Best fix: ruby-version 3.3 in ruby/setup-ruby. Ruby 3.2 reached end of life on 2026-04-01 anyway."
faq:
  - q: "Why does commonmarker fail to install on ubuntu-latest?"
    a: "GitHub's ubuntu-latest runner is Ubuntu 26.04 with GCC 15, which compiles C as C23 by default. With Ruby 3.2, the native extension build fails inside Ruby's own headers with unknown type name 'bool'. commonmarker 0.23.11 is a native extension that the github-pages gem pulls in."
  - q: "Do I have to stop using the github-pages gem?"
    a: "No. The github-pages gem installs and builds the site fine on the same Ubuntu 26.04 runner once the workflow uses Ruby 3.3. The failure comes from the Ruby 3.2 and GCC 15 combination, not from the gem itself, so changing the Ruby version is enough."
  - q: "Can I pin my workflow to ubuntu-24.04 instead?"
    a: "Yes, it works today: Ruby 3.2.11 on ubuntu-24.04 uses GCC 13.3 and installs the bundle without errors. It's a temporary fix, because GitHub retires old runner images, so moving to Ruby 3.3 is the change that keeps working."
---

If your GitHub Actions build of a Jekyll / GitHub Pages site suddenly fails at `bundle install` with *"An error occurred while installing commonmarker (0.23.11)"*, it's the combination of **Ruby 3.2** and the **GCC 15** compiler on GitHub's new `ubuntu-latest` (Ubuntu 26.04). Switch `ruby/setup-ruby` to Ruby 3.3 and it installs again.

I hit this in my own site's CI and ran the same bundle on three runner and Ruby combinations to pin it down. Below are the error, the results and three fixes that passed.

## What does the error look like?

`bundle install` stops with the native extension of commonmarker failing to compile:

```text
An error occurred while installing commonmarker (0.23.11), and Bundler cannot continue.

In Gemfile:
  github-pages was resolved to 228, which depends on
    jekyll-commonmark-ghpages was resolved to 0.4.0, which depends on
      jekyll-commonmark was resolved to 1.4.0, which depends on
        commonmarker
```

Higher up in the log, the actual compiler errors are not in commonmarker's code but in Ruby's own headers:

```text
/opt/hostedtoolcache/Ruby/3.2.11/x64/include/ruby-3.2.0/ruby/internal/special_consts.h:137:15:
error: unknown type name 'bool'
note: 'bool' is defined in header '<stdbool.h>'; this is probably fixable by adding '#include <stdbool.h>'
```

In my run that error appeared 60 times, along with `'false' undeclared` (12) and `'true' undeclared` (7).

## Which runners and Ruby versions fail?

Only Ruby 3.2 on Ubuntu 26.04. I ran the same Gemfile and lock file (github-pages 228) on GitHub's hosted runners, with `ruby/setup-ruby`, then `bundle install` and `jekyll build`:

| Runner | Compiler | Ruby | Result |
|---|---|---|---|
| `ubuntu-26.04` (current `ubuntu-latest`) | GCC 15.2.0 | 3.2.11 | fails at commonmarker |
| `ubuntu-26.04` | GCC 15.2.0 | 3.3.14 | passes |
| `ubuntu-24.04` | GCC 13.3.0 | 3.2.11 | passes |

Locally, the official `ruby:3.2` and `ruby:3.3` Docker images (Debian 13, GCC 14.2) both install the bundle too. That's why it "works on my machine".

## Why does Ruby 3.2 break with GCC 15?

GCC 15 changed its default C language standard to C23 (`-std=gnu23`), where `bool`, `true` and `false` are keywords rather than macros from `<stdbool.h>`. GCC's porting notes for version 15 call out `bool` code as the typical breakage. Ruby 3.2's header `ruby/internal/stdbool.h` decides how to provide `bool` based on what its build configuration detected, and with GCC 15 a native extension compiled against those headers ends up without a usable `bool`. Ruby 3.3's headers don't have the problem on the same runner.

I haven't traced the exact path through Ruby 3.2's configuration line by line. The table above is what I can show: same runner, same compiler, Ruby 3.2 fails and Ruby 3.3 passes.

## How do I fix it?

Any of these three passed on GitHub's runners. Pick the first unless something stops you.

**1. Use Ruby 3.3** (recommended). Ruby 3.2 reached end of life on 2026-04-01, so this is overdue anyway:

```yaml
- uses: ruby/setup-ruby@v1
  with:
    ruby-version: '3.3'
    bundler-cache: true
```

**2. Pin the runner to Ubuntu 24.04** if you can't change Ruby yet. It works today, but GitHub retires old runner images, so treat it as temporary:

```yaml
runs-on: ubuntu-24.04
```

**3. Run the job in the official Ruby Docker image.** This is what my site's CI does, because it's the same image I use for local builds, so CI and my machine build identically:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    container: ruby:3.2-trixie
    steps:
      - uses: actions/checkout@v4
      - run: |
          gem install bundler --no-document   # or the version in your Gemfile.lock
          bundle install
          bundle exec jekyll build
```

I didn't test forcing an older C standard through compiler flags. The three options above are the ones I ran.

## Does this affect GitHub Pages' own build?

No, this is only about workflows you run yourself. If GitHub Pages builds your site from a branch ("Deploy from a branch" in the Pages settings), GitHub's own build environment is used, and it isn't affected by what's on `ubuntu-latest`: this site is built that way, and its Pages builds kept passing while my own workflow failed. You hit this when you build the site in your own workflow: for checks, previews, link checking or a custom deploy.

## Sources

- [GCC 15 porting guide: C23 by default](https://gcc.gnu.org/gcc-15/porting_to.html)
- [Ruby maintenance branches (3.2 end of life: 2026-04-01)](https://www.ruby-lang.org/en/downloads/branches/)
- [GitHub Actions runner images](https://github.com/actions/runner-images)
- [ruby/setup-ruby](https://github.com/ruby/setup-ruby)
- [github/pages-gem](https://github.com/github/pages-gem)
- [commonmarker 0.23.11 on RubyGems](https://rubygems.org/gems/commonmarker/versions/0.23.11)
- [GitHub Docs: running jobs in a container](https://docs.github.com/en/actions/using-jobs/running-jobs-in-a-container)
