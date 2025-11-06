#!/usr/bin/env ruby
# Validate front matter in Jekyll posts
# This script checks that all posts have required front matter fields
# and warns about duplicate H1 headings

require 'yaml'
require 'date'

# Required fields for all posts
REQUIRED_FIELDS = %w[title layout date]

# Track validation errors and warnings
errors = []
warnings = []

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
  if content =~ /\A---\s*\n(.*?\n)---\s*\n(.*)/m
    front_matter_text = $1
    post_content = $2
    
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
      
      # Check for duplicate H1 heading
      if front_matter['title']
        # Get first # heading from content
        if post_content =~ /^\s*#\s+(.+?)$/
          first_heading = $1.strip
          title = front_matter['title'].to_s.strip
          
          # Compare titles (case insensitive, ignore punctuation differences)
          if first_heading.downcase.gsub(/[^a-z0-9\s]/, '') == title.downcase.gsub(/[^a-z0-9\s]/, '')
            warnings << "#{File.basename(post_path)}: Post starts with # heading that duplicates the title. The layout already displays the title as H1, so remove the duplicate # heading from the content."
          end
        end
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
if errors.empty? && warnings.empty?
  puts "✅ All posts have valid front matter!"
  exit 0
elsif errors.empty?
  puts "\n⚠️  Validation passed with warnings:\n\n"
  warnings.each { |warning| puts "  • #{warning}" }
  puts "\n💡 Tip: Posts should not start with a # heading that duplicates the title."
  puts "   The layout automatically displays the title as H1."
  exit 0
else
  puts "\n❌ Front matter validation failed:\n\n"
  errors.each { |error| puts "  • #{error}" }
  
  unless warnings.empty?
    puts "\n⚠️  Warnings:\n"
    warnings.each { |warning| puts "  • #{warning}" }
  end
  
  puts "\n💡 Tip: All posts must have 'title', 'layout', and 'date' fields in their front matter."
  puts "   Example:"
  puts "   ---"
  puts "   layout: post"
  puts "   title: \"Your Post Title\""
  puts "   date: 2025-11-06"
  puts "   ---"
  puts "   "
  puts "   Do not start content with # heading that duplicates the title."
  exit 1
end
