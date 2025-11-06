# Post Front Matter Validation

## Why This Is Important

All Jekyll blog posts require specific front matter fields to render correctly. Additionally, posts must not have duplicate H1 headings.

### The Problem with Duplicate H1 Tags

The most common issue is when posts include BOTH a `title` in the front matter AND a redundant `# heading` in the content that repeats the same title.

**Incorrect structure:**
```markdown
---
layout: post
title: "My Post Title"
date: 2025-09-27
---

# My Post Title  <!-- DON'T DO THIS -->

Content starts here...
```

**Why this is wrong:**

1. **Post Layout** displays the title from front matter as an `<h1>` tag
2. **Markdown # heading** gets converted to another `<h1>` tag
3. **Result**: You end up with **duplicate H1 tags**

**Results in HTML:**
```html
<h1>My Post Title</h1>  <!-- From page.title in layout -->
<h1>My Post Title</h1>  <!-- From # markdown heading -->
```

This causes:
- **SEO Issues**: Search engines see duplicate titles and may penalize the page
- **Accessibility Problems**: Screen readers announce the same heading twice
- **Poor User Experience**: Visual redundancy at the top of the page
- **HTML Standards Violation**: Pages should have exactly one H1 tag

### The Correct Structure

**✅ Do this:**
```markdown
---
layout: post
title: "My Post Title"
date: 2025-09-27
---

Content starts here without a # heading.

## First Section

More content...
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
