// Smooth scrolling for navigation links
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
