#!/usr/bin/env python3
"""
Content Generation Script using GitHub Models API

This script generates blog posts and LinkedIn content using GitHub's AI models.
It reads the prompt from prompts/new-blog-linkedin-post.md and generates content
that matches the ciuculescu.com blog style.
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
import requests


def load_prompt():
    """Load the content creation prompt from file."""
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / "new-blog-linkedin-post.md"
    
    if not prompt_path.exists():
        print(f"Error: Prompt file not found at {prompt_path}", file=sys.stderr)
        sys.exit(1)
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_content_with_github_models(prompt, topic=None):
    """
    Generate content using GitHub Models API.
    
    GitHub Models API provides access to various AI models including GPT-4.
    Docs: https://docs.github.com/en/github-models
    """
    github_token = os.environ.get('GITHUB_TOKEN')
    
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    # Construct the full prompt
    full_prompt = prompt
    if topic:
        full_prompt += f"\n\n### Selected Topic\nCreate content about: {topic}"
    else:
        full_prompt += "\n\n### Selected Topic\nChoose an interesting and timely topic from the suggested areas."
    
    # GitHub Models API endpoint
    # Using GPT-4o which is available through GitHub Models
    api_url = "https://models.inference.ai.azure.com/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {github_token}"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional technical content writer specializing in PHP, Laravel, and DevOps topics."
            },
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
        "top_p": 0.95
    }
    
    print("Calling GitHub Models API...", file=sys.stderr)
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        print("Content generated successfully!", file=sys.stderr)
        return content
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling GitHub Models API: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}", file=sys.stderr)
            print(f"Response body: {e.response.text}", file=sys.stderr)
        sys.exit(1)


def parse_generated_content(content):
    """
    Parse the generated content to extract blog post and LinkedIn post.
    
    Expected format:
    ## BLOG POST
    [blog content]
    ---
    ## LINKEDIN POST
    [linkedin content]
    """
    # Split content by the separator
    parts = re.split(r'\n---+\n', content)
    
    blog_post = ""
    linkedin_post = ""
    
    for part in parts:
        if "## BLOG POST" in part or "## Blog Post" in part:
            # Extract everything after the header
            blog_post = re.sub(r'^.*?## BLOG POST.*?\n', '', part, flags=re.DOTALL | re.IGNORECASE)
            blog_post = blog_post.strip()
        elif "## LINKEDIN POST" in part or "## LinkedIn Post" in part:
            # Extract everything after the header
            linkedin_post = re.sub(r'^.*?## LINKEDIN POST.*?\n', '', part, flags=re.DOTALL | re.IGNORECASE)
            linkedin_post = linkedin_post.strip()
    
    # If the split didn't work, try alternative parsing
    if not blog_post and not linkedin_post:
        # Try to find the sections differently
        blog_match = re.search(r'## BLOG POST\s*\n(.*?)(?=## LINKEDIN POST|$)', content, re.DOTALL | re.IGNORECASE)
        linkedin_match = re.search(r'## LINKEDIN POST\s*\n(.*)', content, re.DOTALL | re.IGNORECASE)
        
        if blog_match:
            blog_post = blog_match.group(1).strip()
        if linkedin_match:
            linkedin_post = linkedin_match.group(1).strip()
    
    return blog_post, linkedin_post


def extract_blog_metadata(blog_post):
    """Extract title and date from blog post YAML front matter."""
    # Extract YAML front matter
    yaml_match = re.search(r'^---\s*\n(.*?)\n---', blog_post, re.DOTALL | re.MULTILINE)
    
    if not yaml_match:
        print("Warning: Could not find YAML front matter in blog post", file=sys.stderr)
        return None, None
    
    yaml_content = yaml_match.group(1)
    
    # Extract title
    title_match = re.search(r'title:\s*["\']?(.*?)["\']?\s*$', yaml_content, re.MULTILINE)
    title = title_match.group(1).strip('"\'') if title_match else None
    
    # Extract date
    date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', yaml_content)
    date = date_match.group(1) if date_match else None
    
    return title, date


def create_slug(title):
    """Create a URL-friendly slug from title."""
    if not title:
        return "untitled"
    
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = slug.strip('-')
    
    return slug


def save_content(blog_post, linkedin_post, output_dir=None):
    """Save the generated content to files."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent
    else:
        output_dir = Path(output_dir)
    
    # Extract metadata from blog post
    title, date = extract_blog_metadata(blog_post)
    
    # Use current date if not found in content
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
        print(f"Warning: Date not found in blog post, using current date: {date}", file=sys.stderr)
    
    # Create slug from title
    if title:
        slug = create_slug(title)
    else:
        slug = "new-post"
        print("Warning: Title not found in blog post, using default slug", file=sys.stderr)
    
    # Save blog post
    posts_dir = output_dir / "_posts"
    posts_dir.mkdir(exist_ok=True)
    
    blog_filename = f"{date}-{slug}.md"
    blog_path = posts_dir / blog_filename
    
    with open(blog_path, 'w', encoding='utf-8') as f:
        f.write(blog_post)
    
    print(f"Blog post saved to: {blog_path}")
    
    # Save LinkedIn post
    linkedin_dir = output_dir / "linkedin_posts"
    linkedin_dir.mkdir(exist_ok=True)
    
    linkedin_filename = f"{date}-{slug}-linkedin.txt"
    linkedin_path = linkedin_dir / linkedin_filename
    
    with open(linkedin_path, 'w', encoding='utf-8') as f:
        f.write(linkedin_post)
    
    print(f"LinkedIn post saved to: {linkedin_path}")
    
    return blog_path, linkedin_path


def main():
    """Main execution function."""
    print("=" * 60)
    print("Content Generation Script - GitHub Models Edition")
    print("=" * 60)
    print()
    
    # Check for topic argument
    topic = None
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        print(f"Topic: {topic}")
    else:
        print("Topic: Auto-selected by AI")
    print()
    
    # Load the prompt
    print("Loading prompt template...")
    prompt = load_prompt()
    print(f"Prompt loaded ({len(prompt)} characters)")
    print()
    
    # Generate content
    print("Generating content...")
    content = generate_content_with_github_models(prompt, topic)
    print()
    
    # Parse the response
    print("Parsing generated content...")
    blog_post, linkedin_post = parse_generated_content(content)
    
    if not blog_post or not linkedin_post:
        print("Error: Could not parse blog post and LinkedIn post from generated content", file=sys.stderr)
        print("\nGenerated content preview:", file=sys.stderr)
        print(content[:500], file=sys.stderr)
        sys.exit(1)
    
    print(f"Blog post: {len(blog_post)} characters")
    print(f"LinkedIn post: {len(linkedin_post)} characters")
    print()
    
    # Save content
    print("Saving content to files...")
    blog_path, linkedin_path = save_content(blog_post, linkedin_post)
    print()
    
    print("=" * 60)
    print("Content generation completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review the generated content")
    print("2. Make any necessary edits")
    print("3. Commit and push to create a PR")
    print()


if __name__ == "__main__":
    main()
