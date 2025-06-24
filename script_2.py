# Continue with the SCSS file - completing the styles
scss_continuation = '''
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
}

// About page styles
.about-hero {
  padding: 5rem 0 3rem;
  background: linear-gradient(135deg, $primary-color 0%, darken($primary-color, 10%) 100%);
  text-align: center;
}

.experience {
  padding: 4rem 0;
  
  .expertise-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2.5rem;
    margin-top: 2rem;
  }
  
  .expertise-item {
    h3 {
      color: $secondary-color;
      margin-bottom: 1rem;
    }
    
    p {
      color: $text-muted;
      line-height: 1.7;
    }
  }
}

.philosophy {
  padding: 4rem 0;
  background: lighten($primary-color, 2%);
  
  .philosophy-content {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    
    blockquote {
      font-size: 1.4rem;
      font-style: italic;
      color: $text-light;
      margin: 2rem 0 3rem;
      padding: 0 2rem;
      position: relative;
      
      &::before {
        content: '"';
        font-size: 4rem;
        color: $secondary-color;
        position: absolute;
        top: -1rem;
        left: 0;
      }
    }
  }
  
  .principles {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
  }
  
  .principle {
    text-align: center;
    
    h4 {
      color: $secondary-color;
      margin-bottom: 1rem;
    }
    
    p {
      color: $text-muted;
      font-size: 1rem;
    }
  }
}

.work-approach {
  padding: 4rem 0;
  
  .approach-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }
  
  .approach-item {
    padding: 2rem;
    background: rgba($secondary-color, 0.05);
    border-radius: 8px;
    border-left: 4px solid $secondary-color;
    
    h4 {
      color: $secondary-color;
      margin-bottom: 1rem;
    }
    
    p {
      color: $text-muted;
      margin-bottom: 0;
    }
  }
}

.personal {
  padding: 4rem 0;
  background: lighten($primary-color, 2%);
  
  p {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    font-size: 1.2rem;
    line-height: 1.8;
    color: $text-light;
  }
}

// Footer
.site-footer {
  background: darken($primary-color, 8%);
  padding: 4rem 0 2rem;
  border-top: 1px solid $border-color;
  
  .footer-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    margin-bottom: 3rem;
    
    @media (max-width: $breakpoint-md) {
      grid-template-columns: 1fr;
      gap: 3rem;
    }
  }
  
  .contact-section {
    h3 {
      margin-bottom: 1rem;
      color: $secondary-color;
    }
    
    > p {
      margin-bottom: 2rem;
      color: $text-muted;
    }
  }
  
  .contact-form {
    .form-group {
      margin-bottom: 1.5rem;
      
      label {
        display: block;
        margin-bottom: 0.5rem;
        color: $text-light;
        font-weight: $font-weight-medium;
      }
      
      input, textarea {
        width: 100%;
        padding: 0.8rem;
        background: rgba($text-light, 0.05);
        border: 1px solid $border-color;
        border-radius: 5px;
        color: $text-light;
        font-family: $font-family-base;
        transition: border-color 0.3s ease;
        
        &:focus {
          outline: none;
          border-color: $secondary-color;
          box-shadow: 0 0 0 2px rgba($secondary-color, 0.2);
        }
        
        &::placeholder {
          color: rgba($text-muted, 0.7);
        }
      }
      
      textarea {
        resize: vertical;
        min-height: 100px;
      }
    }
  }
  
  .info-section {
    h4 {
      margin-bottom: 1.5rem;
      color: $secondary-color;
    }
    
    .info-grid {
      margin-bottom: 2rem;
    }
    
    .info-item {
      display: flex;
      justify-content: space-between;
      padding: 0.8rem 0;
      border-bottom: 1px solid rgba($border-color, 0.5);
      
      &:last-child {
        border-bottom: none;
      }
      
      strong {
        color: $text-light;
        font-weight: $font-weight-medium;
      }
      
      span {
        color: $text-muted;
      }
    }
    
    .social-links {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    
    .social-link {
      display: flex;
      align-items: center;
      gap: 0.8rem;
      color: $text-muted;
      text-decoration: none;
      transition: color 0.3s ease;
      
      &:hover {
        color: $secondary-color;
      }
      
      i {
        font-size: 1.2rem;
        width: 20px;
      }
    }
  }
  
  .footer-bottom {
    border-top: 1px solid rgba($border-color, 0.5);
    padding-top: 2rem;
    
    .copyright {
      text-align: center;
      color: rgba($text-muted, 0.7);
      font-size: 0.9rem;
      margin: 0;
    }
  }
}

// Responsive utilities
@media (max-width: $breakpoint-md) {
  .container {
    padding: 0 15px;
  }
  
  .hero {
    min-height: 70vh;
    text-align: center;
    
    .hero-buttons {
      justify-content: center;
    }
  }
  
  .services-grid,
  .skills-grid,
  .expertise-grid,
  .approach-grid {
    grid-template-columns: 1fr;
  }
  
  .availability-details {
    grid-template-columns: 1fr;
  }
}

// Smooth scrolling
html {
  scroll-behavior: smooth;
}

// Animation for cards
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.service-card,
.skill-category,
.expertise-item,
.approach-item {
  animation: fadeInUp 0.6s ease forwards;
}

// Loading states
.btn {
  position: relative;
  
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
}
'''

# Add the continuation to the main SCSS
project_files['assets/css/main.scss'] = project_files['assets/css/main.scss'] + scss_continuation

print("SCSS file completed successfully!")