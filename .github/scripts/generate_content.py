#!/usr/bin/env python3
"""
Generate blog and LinkedIn content using Claude API.

This script reads the prompt template, calls Claude API to generate content,
and saves the results as separate files for the blog post and LinkedIn post.
"""

import os
import sys
import re
from datetime import date
from anthropic import Anthropic

def read_prompt_template():
    """Read the prompt template from the prompts directory."""
    prompt_path = "prompts/new-blog-linkedin-post.md"
    
    if not os.path.exists(prompt_path):
        print(f"❌ Error: Prompt template not found at {prompt_path}")
        sys.exit(1)
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_content_with_claude(prompt_template, topic=None):
    """
    Call Claude API to generate blog and LinkedIn content.
    
    Args:
        prompt_template: The full prompt template
        topic: Optional specific topic to write about
        
    Returns:
        tuple: (blog_content, linkedin_content)
    """
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please add your Claude API key as a GitHub secret named ANTHROPIC_API_KEY")
        sys.exit(1)
    
    client = Anthropic(api_key=api_key)
    
    # Build the user message
    if topic:
        user_message = f"{prompt_template}\n\n---\n\n**SPECIFIC TOPIC REQUEST**: Please create content about: {topic}"
    else:
        user_message = f"{prompt_template}\n\n---\n\nPlease generate a blog post on a relevant, trending topic in PHP, Laravel, or DevOps that would provide value to the target audience."
    
    print("🤖 Calling Claude API to generate content...")
    print(f"📅 Date: {date.today().isoformat()}")
    if topic:
        print(f"📌 Topic: {topic}")
    else:
        print("📌 Topic: Auto-selected based on current trends")
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=16000,
            temperature=1,
            messages=[{
                "role": "user",
                "content": user_message
            }]
        )
        
        content = response.content[0].text
        
        print("✅ Content generated successfully")
        print(f"📊 Response length: {len(content)} characters")
        
        return parse_generated_content(content)
        
    except Exception as e:
        print(f"❌ Error calling Claude API: {e}")
        sys.exit(1)

def parse_generated_content(content):
    """
    Parse the generated content to extract blog and LinkedIn posts.
    
    Args:
        content: Raw content from Claude
        
    Returns:
        tuple: (blog_content, linkedin_content)
    """
    # Look for the blog post section
    blog_match = re.search(
        r'## 📝 BLOG POST.*?\n\n(---\nlayout: post.*?)(?=\n---\n\n## 💼 LINKEDIN POST|$)',
        content,
        re.DOTALL
    )
    
    if not blog_match:
        # Try alternative pattern
        blog_match = re.search(
            r'(?:BLOG POST|Blog Post).*?\n\n(---\nlayout: post.*?)(?=\n---?\n\n.*?(?:LINKEDIN POST|LinkedIn Post)|$)',
            content,
            re.DOTALL | re.IGNORECASE
        )
    
    if not blog_match:
        print("⚠️ Warning: Could not find blog post with standard pattern")
        print("Attempting to extract any content with YAML frontmatter...")
        # Last resort: find anything that looks like a Jekyll post
        blog_match = re.search(
            r'(---\nlayout: post.*?)(?=\n---?\n\n|$)',
            content,
            re.DOTALL
        )
    
    # Look for LinkedIn post section
    linkedin_match = re.search(
        r'## 💼 LINKEDIN POST.*?\n\n(.*?)(?:\n\n---|\Z)',
        content,
        re.DOTALL
    )
    
    if not linkedin_match:
        # Try alternative pattern
        linkedin_match = re.search(
            r'(?:LINKEDIN POST|LinkedIn Post).*?\n\n(.*?)(?:\n\n---|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )
    
    if not blog_match:
        print("❌ Error: Could not parse blog post from generated content")
        print("\nFirst 500 characters of content:")
        print(content[:500])
        sys.exit(1)
    
    if not linkedin_match:
        print("❌ Error: Could not parse LinkedIn post from generated content")
        print("\nLast 500 characters of content:")
        print(content[-500:])
        sys.exit(1)
    
    blog_content = blog_match.group(1).strip()
    linkedin_content = linkedin_match.group(1).strip()
    
    # Clean up any metadata lines from LinkedIn post
    linkedin_lines = linkedin_content.split('\n')
    cleaned_linkedin = []
    skip_metadata = False
    
    for line in linkedin_lines:
        if line.startswith('**') and ('Character Count' in line or 'Blog URL' in line or 'Filename' in line):
            skip_metadata = True
            continue
        if skip_metadata and line.strip() == '':
            skip_metadata = False
            continue
        if not skip_metadata:
            cleaned_linkedin.append(line)
    
    linkedin_content = '\n'.join(cleaned_linkedin).strip()
    
    # Validate blog post has required elements
    if not blog_content.startswith('---'):
        print("⚠️ Warning: Blog post doesn't start with YAML frontmatter")
    
    if 'layout: post' not in blog_content:
        print("⚠️ Warning: Blog post missing 'layout: post' in frontmatter")
    
    # Validate LinkedIn post
    if len(linkedin_content) < 100:
        print("⚠️ Warning: LinkedIn post seems too short")
    
    print(f"📝 Blog post: {len(blog_content)} characters")
    print(f"💼 LinkedIn post: {len(linkedin_content)} characters")
    
    return blog_content, linkedin_content

def save_content(blog_content, linkedin_content):
    """Save the generated content to temporary files."""
    
    # Save blog post
    with open('new_blog_post.md', 'w', encoding='utf-8') as f:
        f.write(blog_content)
    
    print("✅ Saved blog post to: new_blog_post.md")
    
    # Save LinkedIn post
    with open('new_linkedin_post.txt', 'w', encoding='utf-8') as f:
        f.write(linkedin_content)
    
    print("✅ Saved LinkedIn post to: new_linkedin_post.txt")
    
    # Show preview
    print("\n" + "="*60)
    print("📝 BLOG POST PREVIEW (first 500 chars)")
    print("="*60)
    print(blog_content[:500])
    print("...\n")
    
    print("="*60)
    print("💼 LINKEDIN POST PREVIEW")
    print("="*60)
    print(linkedin_content[:300])
    if len(linkedin_content) > 300:
        print("...")

def main():
    """Main execution function."""
    print("🚀 Starting content generation...")
    print("="*60)
    
    # Get optional topic from environment
    topic = os.environ.get('TOPIC', '').strip()
    
    # Read prompt template
    prompt_template = read_prompt_template()
    print(f"✅ Loaded prompt template ({len(prompt_template)} characters)")
    
    # Generate content
    blog_content, linkedin_content = generate_content_with_claude(
        prompt_template, 
        topic if topic else None
    )
    
    # Save content
    save_content(blog_content, linkedin_content)
    
    print("\n" + "="*60)
    print("✨ Content generation completed successfully!")
    print("="*60)

if __name__ == "__main__":
    main()
