# Continue creating layout and include files

# Default layout
project_files['_layouts/default.html'] = '''<!DOCTYPE html>
<html lang="{{ page.lang | default: site.lang | default: "en" }}">

{%- include head.html -%}

<body>

  {%- include header.html -%}

  <main class="page-content" aria-label="Content">
    <div class="wrapper">
      {{ content }}
    </div>
  </main>

  {%- include footer.html -%}

  <script src="{{ "/assets/js/main.js" | relative_url }}"></script>
</body>

</html>
'''

# Head include
project_files['_includes/head.html'] = '''<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {%- seo -%}
  <link rel="stylesheet" href="{{ "/assets/css/main.css" | relative_url }}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
  {%- feed_meta -%}
  {%- if jekyll.environment == 'production' and site.google_analytics -%}
    {%- include google-analytics.html -%}
  {%- endif -%}
</head>
'''

# Header include
project_files['_includes/header.html'] = '''<header class="site-header">
  <div class="wrapper">
    <nav class="site-nav">
      <div class="nav-brand">
        <a class="site-title" href="{{ "/" | relative_url }}">AC</a>
      </div>
      
      <div class="nav-links">
        <a href="{{ "/" | relative_url }}" class="nav-link">Home</a>
        <a href="{{ "/about/" | relative_url }}" class="nav-link">About</a>
        <a href="#contact" class="nav-link">Contact</a>
      </div>
      
      <div class="nav-social">
        <a href="https://github.com/ciuc123" target="_blank" class="social-link" aria-label="GitHub">
          <i class="fab fa-github"></i>
        </a>
        <a href="https://www.linkedin.com/in/andrei-ciuculescu/" target="_blank" class="social-link" aria-label="LinkedIn">
          <i class="fab fa-linkedin"></i>
        </a>
      </div>
    </nav>
  </div>
</header>
'''

# Footer include with contact form
project_files['_includes/footer.html'] = '''<footer class="site-footer" id="contact">
  <div class="container">
    <div class="footer-content">
      <div class="contact-section">
        <h3>Get in Touch</h3>
        <p>Ready to discuss your project? Let's connect and explore how I can help achieve your technical goals.</p>
        
        <form id="contactForm" class="contact-form">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" name="name" required>
          </div>
          
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required>
          </div>
          
          <div class="form-group">
            <label for="project">Project Details</label>
            <textarea id="project" name="project" rows="4" placeholder="Brief description of your project requirements, timeline, and budget range" required></textarea>
          </div>
          
          <button type="submit" class="btn btn-primary">Send Inquiry</button>
        </form>
      </div>
      
      <div class="info-section">
        <h4>Professional Info</h4>
        <div class="info-grid">
          <div class="info-item">
            <strong>Location:</strong>
            <span>Bucharest, Romania</span>
          </div>
          <div class="info-item">
            <strong>Availability:</strong>
            <span>20+ hours/week</span>
          </div>
          <div class="info-item">
            <strong>Response Time:</strong>
            <span>24 business hours</span>
          </div>
          <div class="info-item">
            <strong>Preferred Projects:</strong>
            <span>1-6 months</span>
          </div>
        </div>
        
        <div class="social-links">
          <a href="https://github.com/ciuc123" target="_blank" class="social-link">
            <i class="fab fa-github"></i>
            <span>GitHub</span>
          </a>
          <a href="https://www.linkedin.com/in/andrei-ciuculescu/" target="_blank" class="social-link">
            <i class="fab fa-linkedin"></i>
            <span>LinkedIn</span>
          </a>
        </div>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p class="copyright">&copy; {{ "now" | date: "%Y" }} Andrei Ciuculescu. All rights reserved.</p>
    </div>
  </div>
</footer>
'''

print("Layout and include files created. Now creating the complete SCSS file...")

# Complete SCSS file
project_files['assets/css/main.scss'] = '''---
---

// Variables
$primary-color: #0a192f;
$secondary-color: #64ffda;
$accent-color: #f76707;
$text-light: #e6f1ff;
$text-muted: #8892b0;
$border-color: rgba(100, 255, 218, 0.1);
$background-overlay: rgba(100, 255, 218, 0.05);

// Typography
$font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
$font-weight-light: 300;
$font-weight-normal: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;

// Breakpoints
$breakpoint-sm: 576px;
$breakpoint-md: 768px;
$breakpoint-lg: 992px;
$breakpoint-xl: 1200px;

// Reset and base styles
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: $font-family-base;
  font-weight: $font-weight-normal;
  line-height: 1.6;
  color: $text-light;
  background-color: $primary-color;
  overflow-x: hidden;
}

// Container
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  
  @media (min-width: $breakpoint-lg) {
    padding: 0 40px;
  }
}

.wrapper {
  max-width: 100%;
  margin: 0;
  padding: 0;
}

// Typography
h1, h2, h3, h4, h5, h6 {
  font-weight: $font-weight-bold;
  line-height: 1.2;
  margin-bottom: 1rem;
}

h1 {
  font-size: 3.5rem;
  font-weight: $font-weight-bold;
  
  @media (max-width: $breakpoint-md) {
    font-size: 2.5rem;
  }
}

h2 {
  font-size: 2.5rem;
  margin: 3rem 0 2rem;
  position: relative;
  
  &::after {
    content: '';
    display: block;
    width: 60px;
    height: 4px;
    background: linear-gradient(90deg, $secondary-color, $accent-color);
    margin-top: 15px;
    border-radius: 2px;
  }
  
  @media (max-width: $breakpoint-md) {
    font-size: 2rem;
    margin: 2rem 0 1.5rem;
  }
}

h3 {
  font-size: 1.8rem;
  color: $secondary-color;
  margin-bottom: 1rem;
}

h4 {
  font-size: 1.3rem;
  color: $text-light;
  margin-bottom: 0.8rem;
}

p {
  margin-bottom: 1.5rem;
  color: $text-muted;
  font-size: 1.1rem;
}

.lead {
  font-size: 1.3rem;
  font-weight: $font-weight-medium;
  color: $text-light;
  margin-bottom: 2rem;
}

// Buttons
.btn {
  display: inline-block;
  padding: 12px 30px;
  font-size: 1rem;
  font-weight: $font-weight-semibold;
  text-decoration: none;
  border-radius: 5px;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid;
  position: relative;
  
  &.btn-primary {
    background: $secondary-color;
    color: $primary-color;
    border-color: $secondary-color;
    
    &:hover {
      background: transparent;
      color: $secondary-color;
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba($secondary-color, 0.2);
    }
  }
  
  &.btn-secondary {
    background: transparent;
    color: $secondary-color;
    border-color: $secondary-color;
    
    &:hover {
      background: $secondary-color;
      color: $primary-color;
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba($secondary-color, 0.2);
    }
  }
  
  &.loading {
    color: transparent;
    
    &::after {
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 20px;
      height: 20px;
      border: 2px solid transparent;
      border-top: 2px solid currentColor;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
  }
}

@keyframes spin {
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}'''

print("SCSS base styles created. Creating rest of styles...")