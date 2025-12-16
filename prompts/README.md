# Prompts Directory

This directory contains AI prompt templates for automated content generation.

## Available Prompts

### 1. `new-blog-linkedin-post.md` - Daily Content Generation

The main prompt for generating blog posts and LinkedIn promotional content.

**Purpose**: Automate the creation of high-quality technical blog posts with accompanying LinkedIn posts.

**Target Ratio**: 60% words / 40% code

**Output**: 
- Technical blog post (1,500-2,500 words)
- LinkedIn promotional post (1,200-1,500 characters)

---

## How to Use

### Option 1: Automated Daily Generation (Recommended)

The repository has a GitHub Actions workflow that runs automatically every day at 9:00 AM UTC.

**View workflow status**: https://github.com/ciuc123/ciuc123.github.io/actions

The workflow will:
1. ✅ Generate a new blog post on a trending PHP/Laravel/DevOps topic
2. ✅ Create an accompanying LinkedIn promotional post
3. ✅ Open a Pull Request for review
4. ✅ Include both files ready for publishing

**No manual intervention needed** - the workflow runs automatically!

### Option 2: Manual Trigger with GitHub Actions

1. Go to: https://github.com/ciuc123/ciuc123.github.io/actions
2. Click on "Generate Daily Blog & LinkedIn Post" workflow
3. Click "Run workflow" button
4. Optionally enter a specific topic
5. Wait 2-3 minutes for the PR to be created

### Option 3: Manual Generation with AI Assistant

Point any AI assistant (ChatGPT, Claude, etc.) to the prompt:

```
Please generate a new blog post and LinkedIn post using the prompt file at:
prompts/new-blog-linkedin-post.md

[Optional: Specific topic request]
```

Example with specific topic:
```
Using the prompt at prompts/new-blog-linkedin-post.md, 
create content about "Laravel 11 Service Container patterns"
```

### Option 4: Local Generation with Python Script

If you have the Anthropic API key:

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Generate content
python .github/scripts/generate_content.py

# Or with a specific topic
TOPIC="Laravel Queue Optimization" python .github/scripts/generate_content.py
```

---

## Output Structure

### Blog Post
- **Location**: `_posts/YYYY-MM-DD-topic-slug.md`
- **Format**: Jekyll post with YAML frontmatter
- **Length**: 1,500-2,500 words
- **Code Examples**: Multiple production-ready code blocks
- **Sections**: Hook, Business Value, Implementation, Testing, Conclusion

### LinkedIn Post
- **Location**: `linkedin_posts/YYYY-MM-DD-topic-slug.txt`
- **Format**: Plain text ready to copy-paste
- **Length**: 1,200-1,500 characters
- **Structure**: Hook, Value Points, CTA, Hashtags

---

## Configuration

### GitHub Secrets Required

For automated generation, add this secret to your repository:

1. Go to: https://github.com/ciuc123/ciuc123.github.io/settings/secrets/actions
2. Click "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your Claude API key from https://console.anthropic.com/

### Workflow Schedule

Current schedule: Daily at 9:00 AM UTC

To change the schedule, edit `.github/workflows/generate-daily-content.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Change this line
```

**Cron examples**:
- `0 9 * * *` - Daily at 9:00 AM UTC
- `0 9 * * 1-5` - Monday-Friday at 9:00 AM UTC
- `0 9,15 * * *` - Daily at 9:00 AM and 3:00 PM UTC

---

## Content Quality Guidelines

All generated content follows these standards:

### Blog Posts
✅ SEO-optimized title (under 70 characters)  
✅ Business impact focus  
✅ Production-ready code examples  
✅ Proper syntax highlighting  
✅ Testing section included  
✅ Soft CTA at the end  

### LinkedIn Posts
✅ Compelling hook (visible before "See More")  
✅ 3-5 key value points  
✅ Personal insight/experience  
✅ Clear CTA with full URL  
✅ 3-5 relevant hashtags  

### Content Ratio
✅ 60% explanatory text  
✅ 40% code examples  

---

## Troubleshooting

### Workflow Fails

**Issue**: Workflow fails with "ANTHROPIC_API_KEY not set"  
**Solution**: Add the API key as a GitHub secret (see Configuration above)

**Issue**: Content generation produces errors  
**Solution**: Check the workflow logs and verify the prompt template is valid

### Generated Content Issues

**Issue**: LinkedIn post doesn't include URL  
**Solution**: The URL is auto-generated based on the blog post date and slug

**Issue**: Code examples aren't highlighted  
**Solution**: Ensure code blocks use proper language identifiers (```php, ```bash, etc.)

### Manual Generation Issues

**Issue**: Python script fails with module not found  
**Solution**: Install dependencies: `pip install anthropic python-dotenv`

---

## Customization

### Modify Content Style

Edit `prompts/new-blog-linkedin-post.md` to:
- Change tone or voice
- Adjust word count targets
- Modify section structure
- Update code example requirements
- Change topic focus areas

### Modify Automation

Edit `.github/workflows/generate-daily-content.yml` to:
- Change schedule frequency
- Modify PR labels
- Update commit messages
- Change branch naming

---

## Examples

Check the `_posts/` directory for examples of generated content:
- `_posts/2025-10-09-stripe-security-laravel.md` - Security focus
- `_posts/2025-11-05-laravel-11-slim-architecture.md` - Architecture patterns
- `_posts/2025-09-23-laravel-security-crisis-app-key-rce.md` - Security crisis

LinkedIn posts are stored in `linkedin_posts/` with matching dates.

---

## Support

For issues or questions:
1. Check the workflow logs in GitHub Actions
2. Review this README and the prompt template
3. Test with a manual trigger before troubleshooting automated runs

---

**Last Updated**: December 2024  
**Maintained By**: Automated content generation system
