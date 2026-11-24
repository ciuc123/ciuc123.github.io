---
layout: default
title: Projects
description: "Things I built and run: Job Radar, the Orient Optics website, and a JetBrains plugin that brings back Alt+Left/Right terminal tab switching."
permalink: /projects/
---

<section class="about-hero section--full">
  <div class="inner">
    <h1>Projects</h1>
    <p class="lead">Things I've built and still run, for clients and for myself</p>
  </div>
</section>

<section class="projects section--full">
  <div class="inner">
    <div class="projects-grid">

      <article class="project-card">
        <p class="project-kind">Web app · live</p>
        <h2>Job Radar</h2>
        <p>A dashboard that finds remote developer roles and scores each one against your own profile: roles, skills, level, country, salary floor. It never applies for you: "Apply" opens the original listing.</p>
        <ul class="project-points">
          <li>Fetches twice a day, only from sources with an official public API or feed</li>
          <li>Rules-based scoring that needs no AI; optional Claude features for fit analysis and tailored CVs</li>
          <li>Groups near-identical listings of one company into a single role</li>
        </ul>
        <p class="project-stack">Next.js · TypeScript · Postgres (Neon) · Drizzle · Clerk · GitHub Actions · Vercel</p>
        <div class="project-links">
          <a href="https://jobs.ciuculescu.com" class="btn btn-primary" target="_blank" rel="noopener">Open Job Radar</a>
        </div>
      </article>

      <article class="project-card">
        <p class="project-kind">JetBrains plugin · open source</p>
        <h2>Terminal Tab Switch Shortcuts</h2>
        <p>Since 2026.3, PhpStorm and other JetBrains IDEs send <kbd>Alt+Left</kbd> / <kbd>Alt+Right</kbd> to the shell on Windows and Linux, so terminal tabs can't be switched from the keyboard. This plugin lets those two actions through (<a href="{{ '/posts/2026-11-19-phpstorm-terminal-alt-left-right-plugin/' | relative_url }}">how it works</a>).</p>
        <ul class="project-points">
          <li>One Java class on the terminal's allowed-actions extension point</li>
          <li>Built with just a JDK: no Gradle, no IDE</li>
          <li>Custom shortcuts for Select Next / Previous Tab work too</li>
        </ul>
        <p class="project-stack">Java · IntelliJ Platform · GitHub Actions</p>
        <div class="project-links">
          <a href="https://plugins.jetbrains.com/plugin/36314-terminal-tab-switch-shortcuts" class="btn btn-primary" target="_blank" rel="noopener">Marketplace</a>
          <a href="https://github.com/ciuc123/phpstorm-terminal-tabs" class="btn btn-secondary" target="_blank" rel="noopener">GitHub</a>
        </div>
      </article>

      <article class="project-card">
        <p class="project-kind">Client website · live</p>
        <h2>Orient Optics</h2>
        <p>The website of an optical store chain with five locations in Bucharest, in Romanian. One fast page built to turn ad and search traffic into booked eye exams, plus the legal pages.</p>
        <ul class="project-points">
          <li>Online appointment booking through an embedded SimplyBook calendar</li>
          <li>Analytics and ad tracking load only after cookie consent</li>
          <li>Local SEO: LocalBusiness structured data with ratings, a sitemap, titles aimed at local searches</li>
        </ul>
        <p class="project-stack">Next.js (static export) · React · TypeScript · Tailwind CSS · Cloudflare</p>
        <div class="project-links">
          <a href="https://orientoptics.ro" class="btn btn-primary" target="_blank" rel="noopener">Visit orientoptics.ro</a>
        </div>
      </article>

    </div>
  </div>
</section>
