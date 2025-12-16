# Andrei Ciuculescu - Professional Portfolio

A clean, professional Jekyll portfolio website showcasing Laravel backend development and DevOps expertise.

## Features

- Responsive design optimized for all devices
- Professional minimalist theme
- Integrated contact form
- SEO optimized
- Fast loading and accessible
- **Automated daily blog & LinkedIn content generation**

## 🤖 Automated Content Generation

This repository includes an automated system for generating technical blog posts and LinkedIn promotional content.

### Quick Start

**Daily Automation**: Content is automatically generated every day at 9:00 AM UTC via GitHub Actions.

**Manual Trigger**: 
1. Go to [Actions](https://github.com/ciuc123/ciuc123.github.io/actions)
2. Select "Generate Daily Blog & LinkedIn Post"
3. Click "Run workflow"
4. Optionally specify a topic

**Easy AI Reference**: Point any AI assistant to the prompt:
```
Please generate content using prompts/new-blog-linkedin-post.md
```

### What It Does

- ✅ Generates 1,500-2,500 word technical blog posts
- ✅ Creates accompanying LinkedIn promotional posts
- ✅ Maintains 60% words / 40% code ratio
- ✅ Opens Pull Request for review
- ✅ Fully automated - runs daily

### Output Structure

- Blog posts: `_posts/YYYY-MM-DD-topic-slug.md`
- LinkedIn posts: `linkedin_posts/YYYY-MM-DD-topic-slug.txt`

### Documentation

See [`prompts/README.md`](prompts/README.md) for detailed instructions on:
- How to use the automation
- Customizing content generation
- Troubleshooting
- Configuration

### Requirements

To enable automated generation, add your Claude API key as a GitHub secret:
1. Go to Repository Settings → Secrets → Actions
2. Add secret: `ANTHROPIC_API_KEY`

## Deployment

This site is configured for GitHub Pages deployment at ciuculescu.com.

## Local Development

```bash
bundle install
bundle exec jekyll serve --livereload
```

Visit http://localhost:4000 to view the site locally.

## Tags
welcome-email - Include in the welcome email pdf generation

## Generate email from blog posts
All blog posts with the tag welcome-email will be included in the welcome email pdf.
To generate the email, run: ./generate-welcome-pdf.sh

## Contact

For inquiries, please use the contact form on the website or connect via LinkedIn.