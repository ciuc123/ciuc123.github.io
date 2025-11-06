# Post Front Matter Validation

## Why This Is Important

All Jekyll blog posts require specific front matter fields to render correctly. When these fields are missing, several issues can occur:

### The Problem with Missing Titles

When you remove the `title` field from a post's front matter, Jekyll doesn't fail to build. Instead:

1. **Jekyll SEO Plugin** auto-generates a title from the filename
   - Example: `2025-09-27-linkedin-automation-workflow.md` becomes "Linkedin Automation Workflow"

2. **Post Layout** displays this auto-generated title in an `<h1>` tag

3. **Post Content** typically has its own `<h1>` heading

4. **Result**: You end up with **duplicate H1 tags**, which causes:
   - Poor SEO (search engines see conflicting page titles)
   - Accessibility issues (screen readers get confused)
   - Unpredictable social media sharing (wrong title in previews)
   - Malformed HTML structure

### Example of the Issue

**Front matter without title:**
```markdown
---
layout: post
date: 2025-09-27
---

# My Actual Post Title
```

**Results in HTML:**
```html
<h1>Linkedin Automation Workflow</h1>  <!-- Auto-generated from filename -->
<h1>My Actual Post Title</h1>          <!-- From markdown content -->
```

## Solution: Validation

We've implemented automatic validation to prevent this issue:

### 1. Validation Script (`validate_posts.rb`)

A Ruby script that checks all posts in `_posts/` directory for:
- Required fields: `title`, `layout`, `date`
- Non-empty values
- Valid YAML syntax

**Run locally:**
```bash
ruby validate_posts.rb
```

### 2. GitHub Actions Workflow

The validation runs automatically:
- On every pull request that modifies posts
- On every push to master that modifies posts
- Can be run manually via workflow dispatch

If validation fails, the workflow will fail and prevent deployment of invalid posts.

## Required Front Matter Fields

Every post **must** have these fields:

```markdown
---
layout: post
title: "Your Post Title Here"
date: YYYY-MM-DD
---
```

### Optional but Recommended Fields

```markdown
---
layout: post
title: "Your Post Title Here"
date: YYYY-MM-DD
tags: [tag1, tag2]
description: "Brief description for SEO"
---
```

## How to Fix Validation Errors

If you see a validation error:

1. **Missing required fields**: Add the missing field(s) to your post's front matter
2. **Empty title**: Provide a meaningful title
3. **Invalid YAML**: Check your YAML syntax (quotes, colons, indentation)

## Testing Locally

Before committing changes:

1. Run the validation script:
   ```bash
   ruby validate_posts.rb
   ```

2. Build the site locally:
   ```bash
   bundle exec jekyll serve
   ```

3. Check the rendered post at `http://localhost:4000`

## What Happens Without Validation

Without this validation, posts with missing titles will:
- ✅ Build successfully (no errors)
- ❌ Have duplicate H1 tags
- ❌ Show wrong titles in SEO
- ❌ Create accessibility issues
- ❌ Display incorrectly in social media shares

The validation ensures these issues are caught before deployment.
