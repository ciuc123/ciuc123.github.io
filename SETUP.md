# Setup Guide: Automated Content Generation

This guide will help you set up the automated daily blog and LinkedIn post generation system.

## Prerequisites

- GitHub repository with Actions enabled
- Anthropic (Claude) API access

## Step-by-Step Setup

### 1. Get Your Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in to your account
3. Navigate to "API Keys" in the settings
4. Click "Create Key"
5. Copy your API key (starts with `sk-ant-...`)
6. **Important**: Save this key securely - you won't see it again!

### 2. Add API Key to GitHub Secrets

1. Go to your repository: https://github.com/ciuc123/ciuc123.github.io
2. Click **Settings** (top right)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Enter the following:
   - **Name**: `ANTHROPIC_API_KEY`
   - **Secret**: Paste your API key from step 1
6. Click **Add secret**

### 3. Verify Workflow Permissions

1. In your repository, go to **Settings** → **Actions** → **General**
2. Scroll to "Workflow permissions"
3. Ensure **Read and write permissions** is selected
4. Check **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

### 4. Test the Workflow

1. Go to **Actions** tab in your repository
2. Click on **Generate Daily Blog & LinkedIn Post** workflow
3. Click **Run workflow** (dropdown button)
4. Optionally enter a test topic (e.g., "Laravel Testing Best Practices")
5. Click the green **Run workflow** button
6. Wait 2-3 minutes for the workflow to complete

### 5. Review the Output

Once the workflow completes:

1. Go to **Pull Requests** tab
2. You should see a new PR titled "📝 New Blog Post: ..."
3. Review the generated content:
   - Blog post in `_posts/`
   - LinkedIn post in `linkedin_posts/`
4. Check the PR description for review checklist
5. Make any necessary edits
6. Merge when ready to publish

## Automated Daily Schedule

The workflow is configured to run automatically **every day at 9:00 AM UTC**.

### Adjust Schedule (Optional)

To change when content is generated daily:

1. Edit `.github/workflows/generate-daily-content.yml`
2. Find the `schedule:` section:
   ```yaml
   schedule:
     - cron: '0 9 * * *'
   ```
3. Modify the cron expression:
   - `'0 9 * * *'` = 9:00 AM UTC daily
   - `'0 13 * * 1-5'` = 1:00 PM UTC, Monday-Friday only
   - `'0 9,15 * * *'` = 9:00 AM and 3:00 PM UTC daily

[Cron expression helper](https://crontab.guru/)

## Usage Methods

### Method 1: Automatic (Daily)
✅ No action required - runs automatically at scheduled time  
✅ Creates PR automatically  
✅ Topic selected automatically based on trends

### Method 2: Manual Trigger via GitHub Actions
1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Optionally specify topic
5. Wait for PR

### Method 3: AI Assistant Reference
Point any AI assistant to the prompt:
```
Please generate content using the prompt at:
prompts/new-blog-linkedin-post.md

Topic: [Your specific topic]
```

### Method 4: Local Python Script
```bash
# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run script
python .github/scripts/generate_content.py

# Or with topic
TOPIC="Your Topic" python .github/scripts/generate_content.py
```

## Troubleshooting

### Issue: Workflow fails with "ANTHROPIC_API_KEY not set"

**Solution**: 
- Verify you added the secret in Step 2
- Secret name must be exactly `ANTHROPIC_API_KEY`
- Try removing and re-adding the secret

### Issue: Workflow runs but no PR is created

**Solution**:
- Check workflow logs for errors
- Verify workflow permissions (Step 3)
- Ensure content was generated (check logs for "content_generated=true")

### Issue: Generated content has issues

**Solution**:
- Content quality varies - review and edit as needed
- For specific topics, use manual trigger with topic input
- Adjust prompt template in `prompts/new-blog-linkedin-post.md`

### Issue: Want to change content style/format

**Solution**:
- Edit `prompts/new-blog-linkedin-post.md`
- Adjust instructions, examples, or requirements
- Changes apply to next generation

## API Usage & Costs

### Anthropic API Pricing

**Note**: Pricing information is subject to change. Check current rates at: https://www.anthropic.com/pricing

**Estimated costs as of December 2024:**
- Claude 3.5 Sonnet: ~$3 per million input tokens, ~$15 per million output tokens
- Typical blog post generation: ~$0.15-0.30 per post
- Daily usage (1 post/day): ~$5-10/month
- Weekly usage (1 post/week): ~$1-2/month

**Cost will vary based on:**
- Post length and complexity
- Number of code examples
- Topic difficulty
- API model version used

### Monitor Usage
1. Go to https://console.anthropic.com/
2. Check "Usage" section
3. Set up billing alerts if needed

## Content Review Workflow

### Before Publishing
1. ✅ Read the entire blog post
2. ✅ Verify code examples are correct and functional
3. ✅ Check that statistics and claims are accurate
4. ✅ Ensure title is compelling and under 70 characters
5. ✅ Review LinkedIn post for tone and clarity
6. ✅ Verify blog URL in LinkedIn post is correct
7. ✅ Test any code examples if possible

### Publishing Process
1. Merge the PR to publish blog post
2. Copy LinkedIn post from `linkedin_posts/` directory
3. Paste to LinkedIn
4. Post immediately or schedule

## Customization Options

### Content Topics
Edit topic suggestions in `prompts/new-blog-linkedin-post.md`:
- Add your preferred topics
- Remove topics you don't want covered
- Adjust topic selection strategy

### Content Length
Adjust in prompt template:
- Blog post: Change from "1,500-2,500 words"
- LinkedIn: Change from "1,200-1,500 characters"
- Code ratio: Adjust from "60% words / 40% code"

### Writing Style
Modify in prompt template:
- Tone and voice instructions
- Key phrases to include
- Audience targeting
- Section structure

### Workflow Behavior
Edit `.github/workflows/generate-daily-content.yml`:
- Schedule frequency
- Branch naming
- PR title/description
- Labels applied

## Security Best Practices

✅ **Never commit API keys** to the repository  
✅ Use GitHub Secrets for sensitive data  
✅ Review generated content before publishing  
✅ Monitor API usage for unexpected charges  
✅ Rotate API keys periodically  
✅ Use read-only keys where possible  

## Support Resources

- **Prompt Documentation**: `prompts/README.md`
- **Workflow Logs**: GitHub Actions tab → Select run
- **API Status**: https://status.anthropic.com/
- **Cron Helper**: https://crontab.guru/

## Next Steps

1. ✅ Complete setup steps above
2. ✅ Run test workflow
3. ✅ Review generated content
4. ✅ Make any adjustments to prompt
5. ✅ Let it run automatically!

---

**Questions?** Review the documentation in `prompts/README.md` or check the workflow logs for detailed error messages.

**Last Updated**: December 2024
