# Andrei Ciuculescu - Professional Portfolio

A clean, professional Jekyll portfolio website showcasing Laravel backend development and DevOps expertise.

## Features

- Responsive design optimized for all devices
- Professional minimalist theme
- Integrated contact form
- SEO optimized
- Fast loading and accessible
- Automated front matter validation

## Deployment

This site is configured for GitHub Pages deployment at ciuculescu.com.

## Local Development

```bash
bundle install
bundle exec jekyll serve --livereload
```

Visit http://localhost:4000 to view the site locally.

## Creating New Posts

All blog posts must have required front matter fields. See [FRONT_MATTER_VALIDATION.md](FRONT_MATTER_VALIDATION.md) for details.

**Required fields:**
```markdown
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD
---
```

Before committing, validate your posts:
```bash
ruby validate_posts.rb
```

## Contact

For inquiries, please use the contact form on the website or connect via LinkedIn.


## Tags
welcome-email - Include in the welcome email pdf generation

## Generate email from blog posts
All blog posts with the tag welcome-email will be included in the welcome email pdf.
To generate the email, run: ./generate-welcome-pdf.sh