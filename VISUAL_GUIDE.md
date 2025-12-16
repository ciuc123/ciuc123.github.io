# Visual Guide: Automated Content Generation

## 🎯 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   AUTOMATED CONTENT SYSTEM                  │
│                                                             │
│  Daily at 9:00 AM UTC or Manual Trigger                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         GitHub Actions Workflow Triggered                   │
│         (.github/workflows/generate-daily-content.yml)      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         Python Script Executes                              │
│         (.github/scripts/generate_content.py)               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         Reads Prompt Template                               │
│         (prompts/new-blog-linkedin-post.md)                 │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         Calls Claude API (Anthropic)                        │
│         - Generates blog post (1,500-2,500 words)          │
│         - Generates LinkedIn post (1,200-1,500 chars)      │
│         - Maintains 60/40 text-to-code ratio               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         Content Parsed and Validated                        │
│         - Blog post extracted                               │
│         - LinkedIn post extracted                           │
│         - Files created temporarily                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         Files Moved to Proper Locations                     │
│         - Blog: _posts/YYYY-MM-DD-slug.md                  │
│         - LinkedIn: linkedin_posts/YYYY-MM-DD-slug.txt     │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         Pull Request Auto-Created                           │
│         - Branch: automated-content-YYYY-MM-DD             │
│         - Labels: automated, blog-post, needs-review       │
│         - Contains review checklist                        │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         YOU: Review and Approve                             │
│         ✓ Check accuracy                                   │
│         ✓ Verify code examples                             │
│         ✓ Edit if needed                                   │
│         ✓ Merge when ready                                 │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         Blog Post Published (Jekyll)                        │
│         LinkedIn Post Ready to Copy                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Directory Structure

```
ciuc123.github.io/
│
├── prompts/
│   ├── README.md                      ← Detailed instructions
│   └── new-blog-linkedin-post.md      ← MAIN PROMPT (point AI here!)
│
├── linkedin_posts/
│   ├── README.md                      ← LinkedIn guide
│   └── YYYY-MM-DD-topic.txt           ← Generated LinkedIn posts
│
├── _posts/
│   └── YYYY-MM-DD-topic.md            ← Generated blog posts
│
├── .github/
│   ├── workflows/
│   │   └── generate-daily-content.yml ← Automation workflow
│   └── scripts/
│       └── generate_content.py        ← Generation logic
│
├── QUICK_REFERENCE.md                 ← START HERE! One-page guide
├── SETUP.md                           ← Setup instructions
├── IMPLEMENTATION_SUMMARY.md          ← Complete overview
└── README.md                          ← Updated with automation info
```

---

## 🚀 Usage Flow Diagram

### Automated Daily (No Action Required)

```
9:00 AM UTC
    │
    ▼
[Workflow Runs] ──► [Content Generated] ──► [PR Created]
                                                 │
                                                 ▼
                                        [You Review & Merge]
                                                 │
                                                 ▼
                                        [Blog Published]
                                        [LinkedIn Ready]
```

### Manual Trigger

```
You Click "Run Workflow"
    │
    ▼
[Optionally Specify Topic]
    │
    ▼
[Same Automated Process]
    │
    ▼
[PR Ready in 2-3 Minutes]
```

### AI Assistant Usage

```
You Tell AI: "Use prompts/new-blog-linkedin-post.md"
    │
    ▼
[AI Reads Prompt]
    │
    ▼
[AI Generates Content Inline]
    │
    ▼
[You Copy & Save Files Manually]
    │
    ▼
[You Commit & Push]
```

---

## 🎨 Content Structure

### Blog Post Format

```yaml
---
layout: post
title: "SEO-Optimized Title (max 70 chars)"
date: YYYY-MM-DD
tags: [laravel, php, devops]
---

[Opening Hook - Business Impact]
2-3 sentences addressing pain point

## Why This Matters
Business value and ROI

## The Solution
Technical implementation with code

```php
<?php
// Production-ready code examples
```

## Testing the Implementation
PHPUnit/Pest test examples

## Conclusion
Summary with soft CTA
```

### LinkedIn Post Format

```
[HOOK - < 200 chars, visible before "See More"]
Compelling statistic or question

Here's what matters:

🔐 Key Point 1
→ Explanation

⚠️ Key Point 2
→ Explanation

✅ Key Point 3
→ Explanation

[Personal insight from 13+ years experience]

Full article: https://ciuculescu.com/posts/YYYY-MM-DD-slug/

Question: [Engagement prompt]?

#Laravel #PHP #DevOps #WebSecurity #BackendDevelopment
```

---

## 🎯 Quick Decision Tree

```
Want to generate content?
    │
    ├─ Let it happen automatically?
    │   └─► Just wait for daily run ✓
    │
    ├─ Want specific topic now?
    │   └─► Manual trigger in GitHub Actions ✓
    │
    ├─ Want to try with AI assistant?
    │   └─► Point AI to prompts/new-blog-linkedin-post.md ✓
    │
    └─ Want to modify the style?
        └─► Edit prompts/new-blog-linkedin-post.md ✓
```

---

## 📊 Content Quality Checklist

```
Blog Post:
┌─────────────────────────────────────┐
│ ✓ YAML frontmatter with date       │
│ ✓ Title under 70 characters        │
│ ✓ Opening hook (business impact)   │
│ ✓ 3+ code examples                 │
│ ✓ Testing section included         │
│ ✓ Conclusion with CTA              │
│ ✓ 1,500-2,500 words total          │
│ ✓ 60% text, 40% code              │
└─────────────────────────────────────┘

LinkedIn Post:
┌─────────────────────────────────────┐
│ ✓ Hook < 200 characters            │
│ ✓ 3-5 key points with emojis       │
│ ✓ Personal insight included        │
│ ✓ Full blog URL present            │
│ ✓ 3-5 hashtags                     │
│ ✓ 1,200-1,500 characters          │
└─────────────────────────────────────┘
```

---

## 🔧 Configuration Overview

```
GitHub Secrets Required:
    ANTHROPIC_API_KEY ← Get from console.anthropic.com

Workflow Schedule:
    cron: '0 9 * * *' ← Daily at 9:00 AM UTC
    (Edit in .github/workflows/generate-daily-content.yml)

Python Dependencies:
    - anthropic
    - python-dotenv
    (Auto-installed by workflow)

Cost:
    ~$0.15-0.30 per post
    ~$5-10 per month for daily generation
```

---

## 🎉 Success Path

```
Day 0: Setup
    │
    ├─► Add ANTHROPIC_API_KEY to GitHub Secrets
    ├─► Configure workflow permissions
    └─► Test with manual trigger
    
Day 1: First Automated Run
    │
    ├─► Review generated PR
    ├─► Make minor edits if needed
    └─► Merge to publish
    
Day 2-∞: Automatic Publishing
    │
    └─► Content generated daily, review weekly or as needed
```

---

## 🆘 Quick Troubleshooting

```
Problem: Workflow fails
    ├─► Check: API key set correctly?
    ├─► Check: Workflow permissions enabled?
    └─► Check: View workflow logs for details

Problem: Content quality issues
    ├─► Solution: Use manual trigger with specific topic
    ├─► Solution: Edit prompt template for style
    └─► Solution: Always review before merging

Problem: Want different schedule
    └─► Edit: cron expression in workflow file

Problem: API costs too high
    └─► Adjust: Schedule to less frequent (weekly, etc.)
```

---

## 📈 Metrics to Track

```
Content Output:
    ├─ Posts per month
    ├─ Average word count
    └─ Code-to-text ratio

Engagement:
    ├─ Blog page views
    ├─ LinkedIn post reach
    └─ Comments and shares

Efficiency:
    ├─ Time saved vs. manual writing
    ├─ Review time per post
    └─ Edit rate needed
```

---

## 🎓 Learning Path

```
Beginner:
    1. Read QUICK_REFERENCE.md
    2. Follow SETUP.md
    3. Test manual trigger

Intermediate:
    4. Review generated content structure
    5. Make minor prompt adjustments
    6. Customize schedule

Advanced:
    7. Modify generation script
    8. Add custom validation
    9. Integrate with other tools
```

---

## ✨ Key Takeaways

```
✅ Fully automated daily content generation
✅ Professional quality with 60/40 ratio
✅ Multiple usage methods
✅ Comprehensive documentation
✅ Easy to customize
✅ Cost-effective
✅ Time-saving
✅ Ready to use!
```

---

**Visual Guide Complete!**
Use `QUICK_REFERENCE.md` for immediate action steps.
