# Setup Guide: Automated Content Generation System

This document explains how to set up and use the automated content generation system for ciuculescu.com.

## Overview

The content generation system automatically creates blog posts and LinkedIn content using **GitHub Models API**, which provides access to state-of-the-art AI models including GPT-4o. This system replaces the previous Claude API dependency.

## Features

- **Automated Daily Generation**: Scheduled workflow runs daily to create new content
- **Manual Triggering**: Generate content on-demand with optional topic specification
- **Pull Request Workflow**: All generated content creates a PR for review before publishing
- **Quality Control**: 1,500-2,500 word blog posts with 60% text / 40% code ratio
- **Dual Output**: Generates both blog posts and LinkedIn promotional content

## Architecture

```
.github/
├── scripts/
│   ├── generate_content.py       # Main generation script
│   └── requirements.txt           # Python dependencies
└── workflows/
    └── generate-daily-content.yml # GitHub Actions workflow

prompts/
└── new-blog-linkedin-post.md      # Content generation prompt template

_posts/                             # Generated blog posts
└── YYYY-MM-DD-title.md

linkedin_posts/                     # Generated LinkedIn posts
└── YYYY-MM-DD-title-linkedin.txt
```

## Prerequisites

### GitHub Token

The system uses the built-in `GITHUB_TOKEN` that is automatically provided by GitHub Actions. **No additional API keys or secrets are required.**

The `GITHUB_TOKEN` provides:
- Access to GitHub Models API for content generation
- Permissions to create Pull Requests
- Repository write access for committing generated content

### Repository Setup

1. Ensure the repository has GitHub Actions enabled
2. Verify that the workflow has necessary permissions (set in workflow file)
3. No additional secrets or configuration needed!

## How It Works

### Automatic Daily Generation

The workflow runs automatically every day at 9 AM UTC:

1. **Trigger**: GitHub Actions cron schedule activates
2. **Generate**: Python script calls GitHub Models API with the content prompt
3. **Parse**: Script extracts blog post and LinkedIn content from AI response
4. **Save**: Files are saved to `_posts/` and `linkedin_posts/` directories
5. **PR Creation**: Automated PR is created with the new content
6. **Review**: Team member reviews and approves the PR
7. **Publish**: Merge PR to publish content to the website

### Manual Generation

You can manually trigger content generation with an optional topic:

#### Via GitHub UI

1. Go to **Actions** tab in the repository
2. Select **Generate Daily Content** workflow
3. Click **Run workflow**
4. (Optional) Enter a specific topic in the input field
5. Click **Run workflow** button

#### Via GitHub CLI

```bash
# Generate content with auto-selected topic
gh workflow run generate-daily-content.yml

# Generate content about a specific topic
gh workflow run generate-daily-content.yml -f topic="PHP 8.4 Property Hooks"
```

## Content Generation Process

### Input: Prompt Template

The system uses `prompts/new-blog-linkedin-post.md` which includes:

- Content structure requirements
- Writing style guidelines
- Code example standards
- Quality checklist
- Topic suggestions

### Processing: GitHub Models API

The script sends the prompt to GitHub Models API (GPT-4o) which:

1. Selects an appropriate topic (or uses provided topic)
2. Generates a comprehensive blog post (1,500-2,500 words)
3. Creates code examples and tests
4. Writes a promotional LinkedIn post
5. Ensures proper formatting and metadata

### Output: Structured Content

Generated files:
- `_posts/YYYY-MM-DD-slug.md` - Blog post with YAML front matter
- `linkedin_posts/YYYY-MM-DD-slug-linkedin.txt` - LinkedIn post text

## Configuration

### Adjusting Schedule

Edit `.github/workflows/generate-daily-content.yml`:

```yaml
schedule:
  # Current: Daily at 9 AM UTC
  - cron: '0 9 * * *'
  
  # Examples:
  # Every Monday at 9 AM UTC
  # - cron: '0 9 * * 1'
  
  # Twice a week (Monday and Thursday at 9 AM UTC)
  # - cron: '0 9 * * 1,4'
```

### Customizing Content Style

Edit `prompts/new-blog-linkedin-post.md` to modify:
- Writing tone and style
- Content structure
- Code example requirements
- Topic areas
- Word count targets

### Modifying AI Model

Edit `.github/scripts/generate_content.py`:

```python
payload = {
    "model": "gpt-4o",  # Change model here
    # Available models:
    # - gpt-4o (recommended)
    # - gpt-4o-mini (faster, less expensive)
    # - gpt-4-turbo
    "temperature": 0.7,  # Creativity level (0.0-1.0)
    "max_tokens": 4000   # Response length limit
}
```

## Testing Locally

You can test content generation on your local machine:

### Prerequisites

```bash
# Install Python 3.11+
python --version

# Install dependencies
pip install -r .github/scripts/requirements.txt
```

### Set GitHub Token

```bash
# On Linux/Mac
export GITHUB_TOKEN="your_github_token_here"

# On Windows (PowerShell)
$env:GITHUB_TOKEN="your_github_token_here"
```

Get a token from: https://github.com/settings/tokens
- Required scope: `repo` (for API access)

### Run Script

```bash
# Auto-select topic
python .github/scripts/generate_content.py

# Specify topic
python .github/scripts/generate_content.py "Laravel Queue Optimization"
```

### Review Output

Generated files will be saved to:
- `_posts/YYYY-MM-DD-title.md`
- `linkedin_posts/YYYY-MM-DD-title-linkedin.txt`

## Troubleshooting

### Workflow Fails to Run

**Problem**: Scheduled workflow doesn't trigger
**Solution**: 
- GitHub may disable workflows in inactive repos
- Make a commit to re-enable workflows
- Check Actions tab for any disabled workflows

### API Rate Limits

**Problem**: "Rate limit exceeded" error
**Solution**:
- GitHub Models API has generous rate limits
- For high-frequency generation, consider adding delays
- Check current limits: https://docs.github.com/en/github-models

### Content Quality Issues

**Problem**: Generated content doesn't meet quality standards
**Solution**:
1. Review and edit the prompt template
2. Adjust temperature parameter (lower = more focused)
3. Provide more specific topic guidance
4. Manually edit generated content before merging PR

### PR Creation Fails

**Problem**: Cannot create Pull Request
**Solution**:
- Verify workflow permissions in `.github/workflows/generate-daily-content.yml`
- Check that `GITHUB_TOKEN` has `contents: write` and `pull-requests: write`
- Ensure no branch protection rules blocking automated PRs

## Maintenance

### Regular Tasks

- **Weekly**: Review generated content quality
- **Monthly**: Update prompt template based on feedback
- **Quarterly**: Review and adjust content topics

### Updating Dependencies

```bash
# Update Python packages
pip install --upgrade -r .github/scripts/requirements.txt
pip freeze > .github/scripts/requirements.txt
```

### Monitoring

Check GitHub Actions logs:
1. Go to **Actions** tab
2. Select **Generate Daily Content** workflow
3. Click on specific run to view logs

## Migration from Claude API

This system replaces the previous Claude API implementation with the following improvements:

### What Changed

| Aspect | Before (Claude) | After (GitHub Models) |
|--------|----------------|----------------------|
| API Key | `ANTHROPIC_API_KEY` secret required | Uses built-in `GITHUB_TOKEN` |
| Setup | Manual secret configuration | No additional setup needed |
| Cost | Paid API usage | Free tier available |
| Models | Claude models | GPT-4o and other models |
| Integration | External API | Native GitHub integration |

### Benefits

1. **No Secret Management**: Uses built-in GitHub authentication
2. **Simplified Setup**: Works out of the box with GitHub Actions
3. **Better Integration**: Native GitHub ecosystem support
4. **Cost Effective**: Generous free tier for public repositories
5. **Multiple Models**: Access to various AI models

### Migration Steps (Already Completed)

- [x] Created new generation script using GitHub Models API
- [x] Updated workflow to use `GITHUB_TOKEN` instead of `ANTHROPIC_API_KEY`
- [x] Removed dependency on external API secrets
- [x] Updated documentation (this file)
- [x] Tested end-to-end workflow

## Support

For issues or questions:

1. Check workflow logs in GitHub Actions
2. Review this documentation
3. Open an issue in the repository
4. Contact: [LinkedIn](https://linkedin.com/in/andrei-ciuculescu)

## Additional Resources

- [GitHub Models Documentation](https://docs.github.com/en/github-models)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Original Blog](https://ciuculescu.com)

---

**Last Updated**: 2025-12-16
**System Version**: 1.0.0
