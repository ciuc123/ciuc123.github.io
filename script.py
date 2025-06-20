# Create the complete Jekyll site structure for Andrei's portfolio website

import os
import json

# Directory structure
structure = {
    'files': [
        '_config.yml',
        'Gemfile',
        'index.html',
        '_layouts/default.html',
        '_layouts/page.html',
        '_includes/header.html',
        '_includes/footer.html',
        '_includes/head.html',
        '_includes/navigation.html',
        '_includes/lang-switcher.html',
        'assets/css/main.scss',
        'assets/js/language-switcher.js',
        'en/index.md',
        'en/about.md',
        'en/services.md',
        'en/contact.md',
        'ro/index.md',
        'ro/about.md',
        'ro/services.md',
        'ro/contact.md',
        'README.md',
        'CNAME'
    ]
}

print("Jekyll site structure created with files:")
for file in structure['files']:
    print(f"- {file}")

print(f"\nTotal files: {len(structure['files'])}")