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
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const button = this.querySelector('button[type="submit"]');
    if (!button) {
      // No submit button found, just submit the form normally
      this.submit();
      return;
    }
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
}

// Add active state to navigation links
const currentLocation = location.pathname;
const menuItems = document.querySelectorAll('.nav-link');
menuItems.forEach(item => {
  if(item.getAttribute('href') === currentLocation){
    item.classList.add('active');
  }
});

// Header background on scroll and hide/show on scroll direction
let lastScrollTop = 0;
const header = document.querySelector('.site-header');
if (header) {
  window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    // Background opacity
    if (scrollTop > 100) {
      header.style.background = 'rgba(10, 25, 47, 0.98)';
    } else {
      header.style.background = 'rgba(10, 25, 47, 0.95)';
    }
    // Hide/show on scroll direction
    if (scrollTop > lastScrollTop && scrollTop > 100) {
      // Scrolling down
      header.classList.add('header-hidden');
    } else {
      // Scrolling up
      header.classList.remove('header-hidden');
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
  });
}
