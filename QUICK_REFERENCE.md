# Quick Reference: Content Generation

## 🚀 Easy Call Instructions

### For AI Assistants (ChatGPT, Claude, etc.)

Simply say:

```
Generate a new blog post and LinkedIn post using:
prompts/new-blog-linkedin-post.md
```

**With specific topic:**
```
Using prompts/new-blog-linkedin-post.md, create content about:
[Your specific topic here - e.g., "Laravel 11 Queue Optimization"]
```

**Example:**
```
Using prompts/new-blog-linkedin-post.md, create content about:
PHP 8.4 property hooks and how they improve Laravel code
```

---

## ⚡ Manual Trigger (GitHub)

1. **Go to**: https://github.com/ciuc123/ciuc123.github.io/actions
2. **Click**: "Generate Daily Blog & LinkedIn Post"
3. **Click**: "Run workflow" dropdown
4. **Optional**: Enter topic in the input field
5. **Click**: Green "Run workflow" button
6. **Wait**: 2-3 minutes
7. **Check**: Pull Requests tab for new PR

---

## 📅 Automatic Daily Generation

**Status**: ✅ Runs automatically every day at 9:00 AM UTC

**No action needed!** The system will:
- Generate new content automatically
- Create a PR for review
- Select relevant topics automatically

**View Status**: https://github.com/ciuc123/ciuc123.github.io/actions

---

## 📝 What You Get

Every generation produces:

1. **Blog Post** (`_posts/YYYY-MM-DD-topic.md`)
   - 1,500-2,500 words
   - 60% text, 40% code
   - Production-ready examples
   - Testing section
   - SEO-optimized

2. **LinkedIn Post** (`linkedin_posts/YYYY-MM-DD-topic.txt`)
   - 1,200-1,500 characters
   - Compelling hook
   - 3-5 value points
   - CTA with blog URL
   - Hashtags

---

## ✅ Review Checklist

Before merging the PR:

- [ ] Blog post is accurate and valuable
- [ ] Code examples work correctly
- [ ] No placeholder text remains
- [ ] LinkedIn post has correct blog URL
- [ ] Title is under 70 characters
- [ ] Tags are relevant

---

## 🔑 Setup Required (One Time Only)

If automation isn't working:

1. **Get API Key**: https://console.anthropic.com/
2. **Add to GitHub**:
   - Go to: Settings → Secrets → Actions
   - Add: `ANTHROPIC_API_KEY`
3. **Test**: Run workflow manually

See `SETUP.md` for detailed instructions.

---

## 📚 Full Documentation

- **Setup Guide**: `SETUP.md`
- **Detailed Instructions**: `prompts/README.md`
- **Prompt Template**: `prompts/new-blog-linkedin-post.md`
- **Main README**: `README.md`

---

## 🎯 Topic Ideas

**PHP/Laravel:**
- Laravel 11 new features
- PHP 8.4 updates
- Eloquent performance
- Queue optimization
- Testing strategies

**Security:**
- API security
- Authentication patterns
- OWASP Top 10
- Vulnerability fixes

**DevOps:**
- Docker best practices
- GitHub Actions
- CI/CD pipelines
- Zero-downtime deploys

**Performance:**
- Database optimization
- Caching strategies
- N+1 query prevention
- Redis patterns

---

## ⚙️ Customization

**Change Schedule:**
Edit `.github/workflows/generate-daily-content.yml`

**Modify Content Style:**
Edit `prompts/new-blog-linkedin-post.md`

**Adjust Word Count:**
Edit requirements in prompt template

---

## 🆘 Quick Troubleshooting

**Workflow fails?**
→ Check API key is set in GitHub Secrets

**No PR created?**
→ Check workflow permissions in Settings

**Content quality issues?**
→ Use manual trigger with specific topic

**Want different topics?**
→ Modify topic list in prompt template

---

**That's it!** Point any AI to `prompts/new-blog-linkedin-post.md` and you're done.
