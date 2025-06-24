# Continue with the complete SCSS file
scss_styles_part2 = '''

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
  transition: background 0.3s ease;
  
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
    font-size: 1.8rem;
    font-weight: $font-weight-bold;
    color: $secondary-color;
    text-decoration: none;
    
    @media (max-width: $breakpoint-md) {
      font-size: 1.5rem;
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
    position: relative;
    
    &:hover {
      color: $secondary-color;
    }
    
    &.active {
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
}

// Skills section
.skills {
  padding: 4rem 0;
  
  .skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }
  
  .skill-category {
    text-align: center;
    
    h4 {
      color: $secondary-color;
      margin-bottom: 1.5rem;
      font-size: 1.2rem;
    }
    
    .skill-tags {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 0.8rem;
    }
    
    .skill-tag {
      background: rgba($secondary-color, 0.1);
      color: $secondary-color;
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: $font-weight-medium;
      border: 1px solid rgba($secondary-color, 0.3);
      transition: all 0.3s ease;
      
      &:hover {
        background: rgba($secondary-color, 0.2);
        transform: translateY(-2px);
      }
    }
  }
}

// Availability section
.availability {
  padding: 4rem 0;
  background: linear-gradient(135deg, darken($primary-color, 5%) 0%, darken($primary-color, 10%) 100%);
  
  .availability-content {
    text-align: center;
    
    h2 {
      color: $secondary-color;
      margin-bottom: 1rem;
      
      &::after {
        margin: 15px auto 0;
      }
    }
    
    > p {
      font-size: 1.2rem;
      margin-bottom: 2.5rem;
      color: $text-light;
    }
  }
  
  .availability-details {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .detail {
    text-align: center;
    padding: 1.5rem;
    background: rgba($secondary-color, 0.05);
    border-radius: 8px;
    border: 1px solid $border-color;
    
    strong {
      display: block;
      color: $secondary-color;
      margin-bottom: 0.5rem;
      font-weight: $font-weight-semibold;
    }
  }
}'''

# Add the second part to the SCSS
project_files['assets/css/main.scss'] += scss_styles_part2

print("Services and main sections styles added. Adding about page and footer styles...")