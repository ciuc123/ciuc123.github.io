# Content Generation Scripts

This directory contains scripts for automated content generation for ciuculescu.com.

## Files

### `generate_content.py`
Main content generation script that uses GitHub Models API to create blog posts and LinkedIn content.

**Usage**:
```bash
# Auto-select topic
python generate_content.py

# Specify topic
python generate_content.py "Laravel Queue Optimization"
```

**Requirements**:
- Python 3.11+
- `GITHUB_TOKEN` environment variable
- Dependencies from `requirements.txt`

**Configuration**:
- `API_TIMEOUT_SECONDS` - API call timeout (default: 120s)
- `API_ENDPOINT` - GitHub Models API endpoint
- `API_MODEL` - AI model to use (default: gpt-4o)

### `test_generate_content.py`
Unit tests for the content generation script.

**Usage**:
```bash
python test_generate_content.py
```

**Tests**:
- Content parsing (blog + LinkedIn post extraction)
- YAML front matter extraction
- Slug generation
- Alternative format handling

### `requirements.txt`
Python package dependencies.

**Installation**:
```bash
pip install -r requirements.txt
```

## Development

### Adding New Features

1. Edit `generate_content.py`
2. Add corresponding tests to `test_generate_content.py`
3. Run tests: `python test_generate_content.py`
4. Update documentation

### Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set GitHub token
export GITHUB_TOKEN="your_token_here"

# Run script
python generate_content.py

# Run tests
python test_generate_content.py
```

### Debugging

The script logs to stderr for easy debugging:
- API calls and responses
- Content parsing status
- File save locations
- Error messages with stack traces

**View logs in GitHub Actions**:
1. Go to Actions tab
2. Select workflow run
3. Click on "Generate content" step

## Architecture

```
generate_content.py
├── load_prompt()                    # Load prompt template
├── generate_content_with_github_models()  # API call
├── parse_generated_content()       # Extract blog + LinkedIn
├── extract_blog_metadata()         # Get title, date from YAML
├── create_slug()                   # Generate URL slug
└── save_content()                  # Save files to disk
```

## Related Files

- Workflow: `.github/workflows/generate-daily-content.yml`
- Prompt: `prompts/new-blog-linkedin-post.md`
- Setup: `SETUP.md`
- Output: `_posts/` and `linkedin_posts/`

## Troubleshooting

### "GITHUB_TOKEN not set"
Set the environment variable:
```bash
export GITHUB_TOKEN="your_token_here"
```

### "Prompt file not found"
Ensure you're running from repository root or adjust the path in `load_prompt()`.

### "Could not parse content"
Check the API response format. The script expects:
```
## BLOG POST
[content]

## LINKEDIN POST
[content]
```

### API timeout
Increase `API_TIMEOUT_SECONDS` for slower networks or complex content.

## Contributing

1. Write tests for new features
2. Ensure all tests pass
3. Update documentation
4. Follow existing code style

## License

Part of ciuculescu.com repository.
