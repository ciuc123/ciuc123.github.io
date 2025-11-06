# Validate front matter in posts
# This plugin ensures all posts have required front matter fields

Jekyll::Hooks.register :posts, :pre_render do |post|
  # Required fields for all posts
  required_fields = ['title', 'layout', 'date']
  
  missing_fields = required_fields.select { |field| post.data[field].nil? || post.data[field].to_s.strip.empty? }
  
  unless missing_fields.empty?
    error_message = "Post #{post.path} is missing required front matter fields: #{missing_fields.join(', ')}"
    Jekyll.logger.error "Front Matter Validation Error:", error_message
    raise error_message
  end
  
  # Validate that title is not just whitespace
  if post.data['title'] && post.data['title'].strip.empty?
    error_message = "Post #{post.path} has an empty title field"
    Jekyll.logger.error "Front Matter Validation Error:", error_message
    raise error_message
  end
end
