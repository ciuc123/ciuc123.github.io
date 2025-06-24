# Let me recreate the complete SCSS file properly
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
}

// Header
.site-header {
  background: rgba($primary-color, 0.95);
  backdrop-filter: blur(10px);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 1rem 0;
  border-bottom: 1px solid $border-color;
  
  .wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .site-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    @media (max-width: $breakpoint-md) {
      flex-direction: column;
      gap: 1rem;
    }
  }
  
  .site-title {
    font-size: 1.5rem;
    font-weight: $font-weight-bold;
    color: $secondary-color;
    text-decoration: none;
    
    @media (max-width: $breakpoint-md) {
      font-size: 1.3rem;
    }
  }
  
  .nav-links {
    display: flex;
    gap: 2rem;
    
    @media (max-width: $breakpoint-md) {
      gap: 1.5rem;
    }
  }
  
  .nav-link {
    color: $text-light;
    text-decoration: none;
    font-weight: $font-weight-medium;
    transition: color 0.3s ease;
    
    &:hover {
      color: $secondary-color;
    }
  }
  
  .nav-social {
    display: flex;
    gap: 1rem;
  }
  
  .social-link {
    color: $text-muted;
    font-size: 1.2rem;
    transition: color 0.3s ease;
    
    &:hover {
      color: $secondary-color;
    }
  }
}

// Main content adjustment for fixed header
.page-content {
  padding-top: 80px;
}

// Hero section
.hero {
  min-height: 90vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, $primary-color 0%, darken($primary-color, 15%) 100%);
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 20% 50%, rgba($secondary-color, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba($accent-color, 0.1) 0%, transparent 50%);
  }
  
  .hero-content {
    position: relative;
    z-index: 1;
  }
  
  h1 {
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, $text-light, $secondary-color);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  h2 {
    font-size: 2rem;
    color: $secondary-color;
    margin: 0 0 1rem 0;
    font-weight: $font-weight-medium;
    
    &::after {
      display: none;
    }
    
    @media (max-width: $breakpoint-md) {
      font-size: 1.5rem;
    }
  }
  
  .hero-subtitle {
    font-size: 1.3rem;
    margin-bottom: 2.5rem;
    color: $text-muted;
  }
  
  .hero-buttons {
    display: flex;
    gap: 1.5rem;
    
    @media (max-width: $breakpoint-sm) {
      flex-direction: column;
      align-items: flex-start;
    }
  }
}

// Services section
.services {
  padding: 5rem 0;
  background: lighten($primary-color, 2%);
  
  .services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2.5rem;
    margin-top: 3rem;
  }
  
  .service-card {
    background: $background-overlay;
    border: 1px solid $border-color;
    border-radius: 10px;
    padding: 2.5rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, $secondary-color, $accent-color);
      transform: scaleX(0);
      transition: transform 0.3s ease;
    }
    
    &:hover {
      transform: translateY(-8px);
      box-shadow: 0 20px 40px rgba($secondary-color, 0.1);
      border-color: rgba($secondary-color, 0.3);
      
      &::before {
        transform: scaleX(1);
      }
    }
    
    .service-icon {
      font-size: 3rem;
      color: $secondary-color;
      margin-bottom: 1.5rem;
    }
    
    h3 {
      margin-bottom: 1.5rem;
    }
    
    ul {
      list-style: none;
      padding: 0;
      
      li {
        margin-bottom: 0.8rem;
        position: relative;
        padding-left: 1.5rem;
        color: $text-muted;
        
        &::before {
          content: "▸";
          color: $secondary-color;
          position: absolute;
          left: 0;
          font-weight: bold;
        }
      }
    }
  }
}'''

print("Complete SCSS file created successfully!"))