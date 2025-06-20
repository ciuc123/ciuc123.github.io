// Language switcher functionality
document.addEventListener('DOMContentLoaded', function() {
    // Store user's language preference
    const languageSwitcher = document.querySelector('.language-switcher');
    
    if (languageSwitcher) {
        const langLinks = languageSwitcher.querySelectorAll('.lang-link');
        
        langLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const targetLang = this.textContent.toLowerCase();
                localStorage.setItem('preferred-language', targetLang);
            });
        });
    }
    
    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
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
    
    // Add fade-in animation to sections on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe sections for animation
    const sections = document.querySelectorAll('.service-card, .skill-item');
    sections.forEach(section => observer.observe(section));
});

// Mobile menu toggle
function toggleMobileMenu() {
    const navTrigger = document.getElementById('nav-trigger');
    const siteNav = document.querySelector('.site-nav');
    
    if (navTrigger && siteNav) {
        navTrigger.addEventListener('change', function() {
            if (this.checked) {
                siteNav.classList.add('nav-open');
            } else {
                siteNav.classList.remove('nav-open');
            }
        });
    }
}

// Initialize mobile menu
document.addEventListener('DOMContentLoaded', toggleMobileMenu);