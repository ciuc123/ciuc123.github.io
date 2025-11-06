#!/usr/bin/env ruby
# Validate front matter in Jekyll posts
# This script checks that all posts have required front matter fields

require 'yaml'
require 'date'

# Required fields for all posts
REQUIRED_FIELDS = %w[title layout date]

# Track validation errors
errors = []

# Find all posts
posts_dir = File.join(File.dirname(__FILE__), '_posts')
unless Dir.exist?(posts_dir)
  puts "❌ Error: _posts directory not found"
  exit 1
end

post_files = Dir.glob(File.join(posts_dir, '*.md'))

if post_files.empty?
  puts "⚠️  Warning: No posts found in _posts directory"
  exit 0
end

puts "🔍 Validating #{post_files.length} post(s)..."

post_files.each do |post_path|
  # Read the post file
  content = File.read(post_path)
  
  # Extract front matter
  if content =~ /\A---\s*\n(.*?\n)---\s*\n/m
    front_matter_text = $1
    
    begin
      # Use safe_load with Date class for Jekyll compatibility
      # Date is a standard library class and safe to permit
      front_matter = YAML.safe_load(front_matter_text, permitted_classes: [Date])
      
      # Check for required fields
      missing_fields = REQUIRED_FIELDS.select do |field|
        front_matter[field].nil? || front_matter[field].to_s.strip.empty?
      end
      
      unless missing_fields.empty?
        errors << "#{File.basename(post_path)}: Missing required fields: #{missing_fields.join(', ')}"
      end
      
    rescue Psych::SyntaxError => e
      errors << "#{File.basename(post_path)}: Invalid YAML syntax - #{e.message}"
    rescue => e
      errors << "#{File.basename(post_path)}: Failed to parse front matter - #{e.message}"
    end
  else
    errors << "#{File.basename(post_path)}: No front matter found"
  end
end

# Report results
if errors.empty?
  puts "✅ All posts have valid front matter!"
  exit 0
else
  puts "\n❌ Front matter validation failed:\n\n"
  errors.each { |error| puts "  • #{error}" }
  puts "\n💡 Tip: All posts must have 'title', 'layout', and 'date' fields in their front matter."
  puts "   Example:"
  puts "   ---"
  puts "   layout: post"
  puts "   title: \"Your Post Title\""
  puts "   date: 2025-11-06"
  puts "   ---"
  exit 1
end
