# Let me create the complete project with all files properly
import os

# Reset and create the complete project
project_files = {}

# Basic Jekyll configuration files
project_files['_config.yml'] = '''title: Andrei Ciuculescu - Laravel & DevOps Specialist
email: contact@ciuculescu.com
description: >-
  Professional Laravel backend developer and DevOps specialist with 13+ years experience 
  building scalable web solutions for small and medium businesses.
baseurl: ""
url: "https://ciuculescu.com"
twitter_username: 
github_username: ciuc123
linkedin_username: andrei-ciuculescu

# Build settings
markdown: kramdown
theme: minima
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag

# Exclude from processing
exclude:
  - .sass-cache/
  - .jekyll-cache/
  - gemfiles/
  - Gemfile
  - Gemfile.lock
  - node_modules/
  - vendor/bundle/
  - vendor/cache/
  - vendor/gems/
  - vendor/ruby/

# Collections
collections:
  pages:
    output: true
    permalink: /:name/

# Defaults
defaults:
  - scope:
      path: ""
      type: "pages"
    values:
      layout: "default"
  - scope:
      path: ""
      type: "posts"
    values:
      layout: "post"

# SEO settings
lang: en
locale: en_US
timezone: Europe/Bucharest
'''

project_files['Gemfile'] = '''source "https://rubygems.org"

gem "jekyll", "~> 4.3.2"
gem "minima", "~> 2.5"
gem "github-pages", "~> 228", group: :jekyll_plugins

group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
end

platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
'''

# JavaScript file
project_files['assets/js/main.js'] = '''// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Contact form handling
document.getElementById('contactForm').addEventListener('submit', function(e) {
  e.preventDefault();
  
  const button = this.querySelector('button[type="submit"]');
  const originalText = button.textContent;
  
  // Add loading state
  button.classList.add('loading');
  button.disabled = true;
  
  // Simulate form submission (replace with actual form handler)
  setTimeout(() => {
    alert('Thank you for your inquiry! I will get back to you within 24 hours.');
    this.reset();
    button.classList.remove('loading');
    button.disabled = false;
  }, 2000);
});

// Add active state to navigation links
const currentLocation = location.pathname;
const menuItems = document.querySelectorAll('.nav-link');
menuItems.forEach(item => {
  if(item.getAttribute('href') === currentLocation){
    item.classList.add('active');
  }
});

// Header background on scroll
window.addEventListener('scroll', function() {
  const header = document.querySelector('.site-header');
  if (window.scrollY > 100) {
    header.style.background = 'rgba(10, 25, 47, 0.98)';
  } else {
    header.style.background = 'rgba(10, 25, 47, 0.95)';
  }
});
'''

print("Core project files created. Now creating page files...")

# Homepage
project_files['index.md'] = '''---
layout: default
title: Home
permalink: /
---

<section class="hero">
  <div class="container">
    <div class="hero-content">
      <h1>Andrei Ciuculescu</h1>
      <h2>Laravel Backend & DevOps Specialist</h2>
      <p class="hero-subtitle">Building robust web solutions for SMBs since 2010</p>
      <div class="hero-buttons">
        <a href="#services" class="btn btn-primary">View Services</a>
        <a href="/about" class="btn btn-secondary">About Me</a>
      </div>
    </div>
  </div>
</section>

<section id="services" class="services">
  <div class="container">
    <h2>Specialized Services</h2>
    <div class="services-grid">
      <div class="service-card">
        <div class="service-icon">
          <i class="fab fa-laravel"></i>
        </div>
        <h3>Laravel Development</h3>
        <ul>
          <li>Custom backend systems</li>
          <li>REST API development</li>
          <li>Legacy app modernization</li>
          <li>Database optimization</li>
        </ul>
      </div>
      <div class="service-card">
        <div class="service-icon">
          <i class="fas fa-server"></i>
        </div>
        <h3>DevOps Solutions</h3>
        <ul>
          <li>CI/CD pipeline setup</li>
          <li>Server optimization</li>
          <li>Cloud infrastructure</li>
          <li>Deployment automation</li>
        </ul>
      </div>
      <div class="service-card">
        <div class="service-icon">
          <i class="fas fa-cogs"></i>
        </div>
        <h3>Technical Consulting</h3>
        <ul>
          <li>Architecture reviews</li>
          <li>Performance audits</li>
          <li>Code quality analysis</li>
          <li>Team mentoring</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="skills">
  <div class="container">
    <h2>Technical Expertise</h2>
    <div class="skills-grid">
      <div class="skill-category">
        <h4>Backend</h4>
        <div class="skill-tags">
          <span class="skill-tag">Laravel</span>
          <span class="skill-tag">PHP</span>
          <span class="skill-tag">MySQL</span>
          <span class="skill-tag">PostgreSQL</span>
        </div>
      </div>
      <div class="skill-category">
        <h4>DevOps</h4>
        <div class="skill-tags">
          <span class="skill-tag">Docker</span>
          <span class="skill-tag">AWS</span>
          <span class="skill-tag">CI/CD</span>
          <span class="skill-tag">Linux</span>
        </div>
      </div>
      <div class="skill-category">
        <h4>Tools</h4>
        <div class="skill-tags">
          <span class="skill-tag">Git</span>
          <span class="skill-tag">Redis</span>
          <span class="skill-tag">Nginx</span>
          <span class="skill-tag">Elasticsearch</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="availability">
  <div class="container">
    <div class="availability-content">
      <h2>Currently Available</h2>
      <p>Accepting select projects with 20+ hour/week commitment</p>
      <div class="availability-details">
        <div class="detail">
          <strong>Response Time:</strong> 24 business hours
        </div>
        <div class="detail">
          <strong>Availability:</strong> 20+ hours/week
        </div>
        <div class="detail">
          <strong>Project Duration:</strong> 1-6 months preferred
        </div>
      </div>
    </div>
  </div>
</section>
'''

print("Homepage created. Creating about page...")

# About page
project_files['about.md'] = '''---
layout: default
title: About
permalink: /about/
---

<section class="about-hero">
  <div class="container">
    <h1>Professional Background</h1>
    <p class="lead">13+ years developing scalable web solutions for businesses across Europe</p>
  </div>
</section>

<section class="experience">
  <div class="container">
    <h2>Core Expertise</h2>
    <div class="expertise-grid">
      <div class="expertise-item">
        <h3>Laravel Specialist</h3>
        <p>Deep expertise in Laravel framework, from rapid prototyping to enterprise-scale applications. Specialized in creating maintainable, testable backends with modern PHP practices.</p>
      </div>
      <div class="expertise-item">
        <h3>DevOps for SMBs</h3>
        <p>Practical DevOps solutions tailored for small and medium businesses. Focus on cost-effective automation, reliable deployments, and scalable infrastructure.</p>
      </div>
      <div class="expertise-item">
        <h3>Database Optimization</h3>
        <p>Performance tuning, query optimization, and database architecture design. Experience with MySQL, PostgreSQL, and NoSQL solutions.</p>
      </div>
    </div>
  </div>
</section>

<section class="philosophy">
  <div class="container">
    <h2>Technical Philosophy</h2>
    <div class="philosophy-content">
      <blockquote>
        "Build simple solutions to complex problems. Focus on maintainability, performance, and clear documentation."
      </blockquote>
      <div class="principles">
        <div class="principle">
          <h4>Code Quality</h4>
          <p>Clean, readable code with comprehensive testing and documentation</p>
        </div>
        <div class="principle">
          <h4>Performance First</h4>
          <p>Optimized solutions that scale with business growth</p>
        </div>
        <div class="principle">
          <h4>Practical Approach</h4>
          <p>Technology choices based on business needs, not trends</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="work-approach">
  <div class="container">
    <h2>Working Together</h2>
    <div class="approach-grid">
      <div class="approach-item">
        <h4>Project Discovery</h4>
        <p>Thorough requirements analysis and technical feasibility assessment</p>
      </div>
      <div class="approach-item">
        <h4>Agile Development</h4>
        <p>Iterative development with regular feedback and transparent progress updates</p>
      </div>
      <div class="approach-item">
        <h4>Knowledge Transfer</h4>
        <p>Complete documentation and team training for long-term maintainability</p>
      </div>
    </div>
  </div>
</section>

<section class="personal">
  <div class="container">
    <h2>Beyond Code</h2>
    <p>Based in Bucharest, Romania. When not coding, I enjoy exploring new technologies, contributing to open source projects, and mentoring junior developers. Passionate about creating technology solutions that make real business impact.</p>
  </div>
</section>
'''

print("About page created. Creating layout files...")