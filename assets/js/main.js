// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      // allow default if external or no element target
      const href = this.getAttribute('href');
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });

      // If nav menu is open (mobile), close it after clicking an in-page link
      const navMenu = document.getElementById('nav-menu');
      const navToggle = document.querySelector('.nav-toggle');
      if (navMenu && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  });

  // Contact form handling (guarded)
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();

      const button = this.querySelector('button[type="submit"]');
      const originalText = button ? button.textContent : '';

      // Add loading state
      if (button) {
        button.classList.add('loading');
        button.disabled = true;
      }

      // Simulate form submission (replace with actual form handler)
      setTimeout(() => {
        alert('Thank you for your inquiry! I will get back to you within 24 hours.');
        this.reset();
        if (button) {
          button.classList.remove('loading');
          button.disabled = false;
        }
      }, 2000);
    });
  }

  // Add active state to navigation links (more robust normalization)
  const normalize = (p) => (p || '').replace(/\/?$/, ''); // remove trailing slash
  const currentPath = normalize(location.pathname);
  const menuItems = document.querySelectorAll('.nav-link');
  menuItems.forEach(item => {
    const href = item.getAttribute('href');
    if (!href) return;
    // ignore hash-only anchors
    if (href.startsWith('#')) return;
    // Build an anchor to resolve relative URLs
    try {
      const url = new URL(href, location.origin);
      if (normalize(url.pathname) === currentPath) {
        item.classList.add('active');
      }
    } catch (e) {
      // fallback: simple compare
      if (normalize(href) === currentPath) item.classList.add('active');
    }
  });

  // Header background on scroll
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 100) {
        header.style.background = 'rgba(10, 25, 47, 0.98)';
      } else {
        header.style.background = 'rgba(10, 25, 47, 0.95)';
      }
    });
  }

  // Mobile nav toggle behavior
  const navToggle = document.querySelector('.nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function(e) {
      const isOpen = navMenu.classList.toggle('open');
      this.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close menu when any nav link is clicked
    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', function() {
        if (navMenu.classList.contains('open')) {
          navMenu.classList.remove('open');
          navToggle.setAttribute('aria-expanded', 'false');
        }
      });
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.focus();
      }
    });

    // Close when clicking outside
    document.addEventListener('click', function(e) {
      if (!navMenu.classList.contains('open')) return;
      const withinNav = navMenu.contains(e.target) || navToggle.contains(e.target);
      if (!withinNav) {
        navMenu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Header hide/show on scroll (hide on scroll down, show on scroll up)
  let lastScrollY = window.scrollY || 0;
  let ticking = false;
  const headerEl = document.querySelector('.site-header');
  const SCROLL_THRESHOLD = 10; // ignore tiny scrolls

  function onScroll() {
    const currentY = window.scrollY || 0;
    const delta = currentY - lastScrollY;

    // If change is small, ignore but still update lastScrollY and release ticker
    if (Math.abs(delta) < SCROLL_THRESHOLD) {
      lastScrollY = currentY;
      ticking = false;
      return;
    }

    if (delta > 0 && currentY > 80) {
      // scrolling down
      if (headerEl && !headerEl.classList.contains('hidden')) {
        headerEl.classList.add('hidden');
      }
      // close mobile menu if open
      if (navMenu && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
      }
    } else if (delta < 0) {
      // scrolling up
      if (headerEl && headerEl.classList.contains('hidden')) {
        headerEl.classList.remove('hidden');
      }
    }

    lastScrollY = currentY;
    ticking = false;
  }

  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });
});
