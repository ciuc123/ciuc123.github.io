#!/usr/bin/env python3
"""
Unit tests for the content generation script.
Tests core functionality without making actual API calls.

Note: This test file uses sys.path manipulation to import the generate_content module.
This is acceptable for a simple test script in the same directory. For a larger project,
consider using a proper package structure with __init__.py files.
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to the path to import generate_content module
# This works because the test file is in the same directory as the module
sys.path.insert(0, str(Path(__file__).parent))

from generate_content import (
    parse_generated_content,
    extract_blog_metadata,
    create_slug
)


def test_parse_generated_content():
    """Test parsing of generated content into blog and LinkedIn posts."""
    sample_content = """
## BLOG POST

---
layout: post
title: "Test Blog Post"
date: 2025-12-16
tags: [test, example]
---

This is a test blog post content.

---

## LINKEDIN POST

This is a test LinkedIn post content.

#Test #Example
"""
    
    blog_post, linkedin_post = parse_generated_content(sample_content)
    
    assert blog_post, "Blog post should not be empty"
    assert linkedin_post, "LinkedIn post should not be empty"
    assert "Test Blog Post" in blog_post
    assert "LinkedIn post content" in linkedin_post
    print("✓ test_parse_generated_content passed")


def test_extract_blog_metadata():
    """Test extraction of title and date from YAML front matter."""
    sample_blog = """---
layout: post
title: "Laravel Performance Optimization"
date: 2025-12-16
tags: [laravel, performance]
---

Blog content here.
"""
    
    title, date = extract_blog_metadata(sample_blog)
    
    assert title == "Laravel Performance Optimization", f"Expected title to be 'Laravel Performance Optimization', got '{title}'"
    assert date == "2025-12-16", f"Expected date to be '2025-12-16', got '{date}'"
    print("✓ test_extract_blog_metadata passed")


def test_create_slug():
    """Test slug creation from titles."""
    test_cases = [
        ("Laravel Performance Optimization", "laravel-performance-optimization"),
        ("PHP 8.4: New Features", "php-84-new-features"),
        ("Testing with PHPUnit & Pest", "testing-with-phpunit-pest"),
        ("  Extra   Spaces  ", "extra-spaces"),
    ]
    
    for title, expected_slug in test_cases:
        slug = create_slug(title)
        assert slug == expected_slug, f"Expected '{expected_slug}', got '{slug}'"
    
    print("✓ test_create_slug passed")


def test_parse_alternative_format():
    """Test parsing with different content formats."""
    # Test with different casing
    sample_content = """
## Blog Post

Test blog content here.

---

## LinkedIn Post

Test LinkedIn content here.
"""
    
    blog_post, linkedin_post = parse_generated_content(sample_content)
    
    assert blog_post, "Blog post should not be empty (case-insensitive)"
    assert linkedin_post, "LinkedIn post should not be empty (case-insensitive)"
    print("✓ test_parse_alternative_format passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Running Content Generation Script Tests")
    print("=" * 60)
    print()
    
    try:
        test_parse_generated_content()
        test_extract_blog_metadata()
        test_create_slug()
        test_parse_alternative_format()
        
        print()
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
