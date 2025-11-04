source "https://rubygems.org"

gem "minima", "~> 2.5"
gem "github-pages", "~> 228", group: :jekyll_plugins
gem "webrick", "~> 1.7"

group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
end

platforms :windows, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", :platforms => [:windows]
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
# Faraday retry middleware (requested by build notice)
gem "faraday-retry"
