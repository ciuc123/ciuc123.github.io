---
layout: post
title: "PHP 8.5 vs 8.4 vs 8.3 for Laravel: a Real-App Benchmark"
description: "A Laravel 13 app benchmarked on PHP 8.3, 8.4 and 8.5 on three machines: a full request differs by about 2%, while the CPU made a 2x difference."
date: 2026-11-20
tags: [laravel, php, php-8.4, performance]
tldr:
  - "A full Laravel 13 request (boot, routing, Eloquent, Blade) ran within about 2% on PHP 8.3, 8.4 and 8.5 on two server CPUs."
  - "PHP 8.5 was the fastest of the three on both servers, by 1.4-2.2% per request, and up to 6% on Blade rendering."
  - "The same request took 3.8 ms on one cloud CPU and 7.4 ms on another: the hardware mattered about 50 times more than the PHP version."
  - "Upgrade PHP for support dates and language features. PHP 8.3 gets security fixes only until 31 December 2027."
faq:
  - q: "Is PHP 8.4 faster than PHP 8.3 for Laravel?"
    a: "Not measurably for a typical request. In this benchmark a full Laravel 13 request on PHP 8.4 was between 0.4% faster and 1% slower than on 8.3 on two server CPUs. Eloquent and Blade were up to 4% faster on one of them. Upgrade for the features and the longer support window, not for speed."
  - q: "Should I upgrade straight to PHP 8.5?"
    a: "If your framework and packages support it, yes. Laravel 13 supports PHP 8.3 to 8.5, PHP 8.5 was the fastest version in this benchmark, and it gets security fixes until the end of 2029, a year longer than 8.4. Run your test suite on 8.5 in CI first, since deprecations are where upgrades usually hurt."
  - q: "Does enabling JIT make Laravel faster?"
    a: "This benchmark ran with JIT off, which is the default. JIT mainly helps CPU-heavy code like math and image processing, while a Laravel request spends its time in autoloading, object creation, the database and string handling. Measure your own app with and without JIT before turning it on in production."
---

Upgrading PHP won't make your Laravel app noticeably faster. I measured a Laravel 13 app on PHP 8.3, 8.4 and 8.5 on three machines, and a full request differed by about 2% between versions on the two server CPUs. PHP 8.5 was slightly the fastest. Switching to a different CPU changed the same request by 2x.

Upgrade articles often promise double-digit speedups from a new PHP version. Those numbers usually come from synthetic benchmarks or from upgrades several versions apart. This test compares the three versions Laravel 13 supports, on a small but real app, with everything else held the same.

## What did I measure?

A fresh Laravel 13.43 app with a `posts` table (5,000 posts by 500 users, SQLite), an Eloquent model with casts and an accessor, and a Blade page listing 50 posts with their authors. Four workloads:

| Workload | One iteration |
|---|---|
| Full request | Create and boot the app, route `/posts`, query 50 posts with authors, render Blade: what PHP-FPM does per request |
| Eloquent | Load 1,000 posts with their authors and convert them to arrays |
| Blade | Render the list view for 50 already-loaded posts |
| Collections | A map, filter, groupBy, sum and sort pipeline over 100,000 items |

**Settings, identical on every version:**
- Official `php:8.3-cli`, `8.4-cli` and `8.5-cli` Docker images (8.3.37, 8.4.28, 8.5.13).
- OPcache on, JIT off (the default), assertions off.
- Production mode with config, routes and views cached.
- Sessions and cache in memory, so a request doesn't write to disk.

**Method:**
- Eight rounds. Each round runs every workload on every version, in a shuffled order, so a slow moment on the machine hits all versions equally.
- Each run warms up first, then takes 5 samples, for 40 samples per workload and version.
- The numbers below are medians.

**Machines:**
- Two GitHub Actions runners, with AMD EPYC 9V45 and EPYC 7763 CPUs.
- My laptop, an Intel i7-10750H running Docker under WSL2.

The whole harness and the raw results are [public](https://github.com/ciuc123/homelab/tree/main/benchmarks/laravel-php). You can run it on GitHub with one click, or on your own machine with two commands.

## Is PHP 8.5 faster than 8.3 for Laravel?

Slightly. The change compared with PHP 8.3, median of 40 samples; negative means faster:

| Workload | EPYC 9V45: 8.4 / 8.5 | EPYC 7763: 8.4 / 8.5 | Laptop: 8.4 / 8.5 |
|---|---|---|---|
| **Full request** | −0.4% / **−1.4%** | +1.0% / **−2.2%** | +7.0% / +0.8% |
| Eloquent, 1,000 models | −3.4% / −3.5% | +0.3% / −2.6% | +1.6% / +1.1% |
| Blade, 50 posts | −3.8% / −6.4% | −1.5% / −4.2% | +1.1% / +1.6% |
| Collections, 100k items | +9.3% / +5.6% | −0.2% / −2.7% | +1.2% / +0.6% |

On both servers, PHP 8.5 was the fastest of the three for a full request, Eloquent and Blade, by 1-6%. PHP 8.4 was within 1% of 8.3 for a full request on both servers, a little faster on one and a little slower on the other.

Two results don't fit that pattern, and they're worth reading as noise or hardware, not as a verdict:

- **The laptop's +7% for 8.4** comes with a wide spread. Its middle half of samples ran from 7.1 to 10.0 ms, against 7.4-7.6 ms on the EPYC 7763. A laptop running other programs is a noisy place to measure 2% differences.
- **Collections were 6-9% slower on 8.4 and 8.5 on the EPYC 9V45 only.** On the other two machines the three versions were within 3%. A slowdown that shows up on one CPU model and not on the others isn't a PHP regression you can plan around.

## What mattered more than the PHP version?

The CPU. The same full request on PHP 8.3 took:

| Machine | Full request, PHP 8.3 |
|---|---|
| GitHub runner, AMD EPYC 9V45 | 3.76 ms |
| My laptop, Intel i7-10750H | 7.07 ms |
| GitHub runner, AMD EPYC 7763 | 7.37 ms |

Moving from the EPYC 7763 to the 9V45 cut the time of every workload by 46-57%. Upgrading PHP on either one changed it by about 2%. If a Laravel app needs to be faster, the order of returns is roughly:

1. **Queries and N+1 problems:** usually the biggest win on the pages that have them. See [preventing N+1 queries](/posts/2025-10-02-preventing-n-plus-one/).
2. **Caching and queues:** work you don't do during the request. See [optimizing Laravel queues](/posts/2025-11-03-laravel-queue-performance-optimization/).
3. **Hardware:** a newer CPU generation, here 2x.
4. **The PHP version:** about 2% between 8.3, 8.4 and 8.5.

## So why upgrade PHP at all?

For support and features. Security support on php.net:

| Version | Released | Active support until | Security fixes until |
|---|---|---|---|
| PHP 8.3 | 23 Nov 2023 | ended 31 Dec 2025 | 31 Dec 2027 |
| PHP 8.4 | 21 Nov 2024 | 31 Dec 2026 | 31 Dec 2028 |
| PHP 8.5 | 20 Nov 2025 | 31 Dec 2027 | 31 Dec 2029 |

An app on PHP 8.3 has about a year of security fixes left. Laravel 13 supports PHP 8.3 to 8.5, so a team upgrading now can go straight to 8.5. It was the fastest version here, it has the longest support, and it brings language features like [property hooks](/posts/2025-09-14-php-property-hooks-game-changer/) from 8.4. The real cost of an upgrade is deprecations in your own code and packages, so run the test suite on the new version in CI before switching production.

PHP 8.6 came out on 19 November 2026, the day before these runs. Laravel 13 lists 8.3-8.5 as supported, so it's not in this test.

## What are the limits of this benchmark?

- **One app shape.** It's a small app on SQLite with no network calls, run as a single process. A real app spends more of each request waiting on MySQL, Redis and HTTP calls, which makes the PHP version matter even less.
- **No concurrency.** It runs one request at a time on two pinned cores. It's not a load test.
- **Shared machines.** GitHub's runners have neighbors and the laptop runs other programs. Interleaving the versions and using medians reduces the noise but doesn't remove it. Read any difference under about 5% as "about the same".

## Check this on your own app

1. **Run the harness** from the [repository](https://github.com/ciuc123/homelab/tree/main/benchmarks/laravel-php) on the hardware you deploy to.
2. **Better, benchmark your own heaviest page.** Swap the `/posts` route in `bench.php` for one of yours.
3. **Before an upgrade for speed, profile first.** If most of the request is database time, a new PHP version can't help.
4. **Check your support dates.** If you're on PHP 8.3 or older, plan the upgrade in 2027 at the latest.

## Sources

- [PHP: supported versions](https://www.php.net/supported-versions.php)
- [Laravel 13 release notes and support policy](https://laravel.com/docs/13.x/releases)
- [Benchmark harness, raw results and summaries](https://github.com/ciuc123/homelab/tree/main/benchmarks/laravel-php)
- GitHub Actions runs [44803515937](https://github.com/ciuc123/homelab/actions/runs/44803515937) (EPYC 9V45) and [44804921270](https://github.com/ciuc123/homelab/actions/runs/44804921270) (EPYC 7763)
- [PHP 8.4 release announcement](https://www.php.net/releases/8.4/en.php) and [PHP 8.5 release announcement](https://www.php.net/releases/8.5/en.php)
